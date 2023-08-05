'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const component = require("../../common/component");
const cpp = require("child-process-promise");
const fs = require("fs");
const path = require("path");
const request = require("request");
const containerJobData_1 = require("../common/containerJobData");
const ts_deferred_1 = require("ts-deferred");
const events_1 = require("events");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const hdfsClientUtility_1 = require("./hdfsClientUtility");
const errors_1 = require("../../common/errors");
const log_1 = require("../../common/log");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const utils_1 = require("../../common/utils");
const paiJobRestServer_1 = require("./paiJobRestServer");
const paiData_1 = require("./paiData");
const paiJobInfoCollector_1 = require("./paiJobInfoCollector");
const typescript_string_operations_1 = require("typescript-string-operations");
const paiConfig_1 = require("./paiConfig");
const util_1 = require("../common/util");
var WebHDFS = require('webhdfs');
let PAITrainingService = class PAITrainingService {
    constructor() {
        this.stopping = false;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.expRootDir = path.join('/nni', 'experiments', experimentStartupInfo_1.getExperimentId());
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.paiJobCollector = new paiJobInfoCollector_1.PAIJobInfoCollector(this.trialJobsMap);
        this.hdfsDirPattern = 'hdfs://(?<host>([0-9]{1,3}.){3}[0-9]{1,3})(:[0-9]{2,5})?(?<baseDir>/.*)?';
        this.nextTrialSequenceId = -1;
    }
    async run() {
        const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
        await restServer.start();
        this.log.info(`PAI Training service rest server listening on: ${restServer.endPoint}`);
        while (!this.stopping) {
            await this.paiJobCollector.retrieveTrialStatus(this.paiToken, this.paiClusterConfig);
            await utils_1.delay(3000);
        }
    }
    async listTrialJobs() {
        const jobs = [];
        this.trialJobsMap.forEach(async (value, key) => {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        });
        return Promise.resolve(jobs);
    }
    getTrialJob(trialJobId) {
        if (!this.paiClusterConfig) {
            throw new Error('PAI Cluster config is not initialized');
        }
        const paiTrialJob = this.trialJobsMap.get(trialJobId);
        if (!paiTrialJob) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(paiTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    async submitTrialJob(form) {
        const deferred = new ts_deferred_1.Deferred();
        if (!this.paiClusterConfig) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (!this.paiTrialConfig) {
            throw new Error('trial config is not initialized');
        }
        if (!this.paiToken) {
            throw new Error('PAI token is not initialized');
        }
        if (!this.hdfsBaseDir) {
            throw new Error('hdfsBaseDir is not initialized');
        }
        if (!this.hdfsOutputHost) {
            throw new Error('hdfsOutputHost is not initialized');
        }
        if (!this.paiRestServerPort) {
            const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
            this.paiRestServerPort = restServer.clusterRestServerPort;
        }
        this.log.info(`submitTrialJob: form: ${JSON.stringify(form)}`);
        const trialJobId = utils_1.uniqueString(5);
        const trialSequenceId = this.generateSequenceId();
        const trialWorkingFolder = path.join(this.expRootDir, 'trials', trialJobId);
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await cpp.exec(`mkdir -p ${path.dirname(trialLocalTempFolder)}`);
        await cpp.exec(`cp -r ${this.paiTrialConfig.codeDir} ${trialLocalTempFolder}`);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        const trialForm = form;
        if (trialForm) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
        const paiJobName = `nni_exp_${this.experimentId}_trial_${trialJobId}`;
        const hdfsCodeDir = path.join(this.expRootDir, trialJobId);
        const hdfsOutputDir = path.join(this.hdfsBaseDir, this.experimentId, trialJobId);
        const hdfsLogPath = typescript_string_operations_1.String.Format(paiData_1.PAI_LOG_PATH_FORMAT, this.hdfsOutputHost, hdfsOutputDir);
        const trialJobDetail = new paiData_1.PAITrialJobDetail(trialJobId, 'WAITING', paiJobName, Date.now(), trialWorkingFolder, form, trialSequenceId, hdfsLogPath);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        const nniPaiTrialCommand = typescript_string_operations_1.String.Format(paiData_1.PAI_TRIAL_COMMAND_FORMAT, `$PWD/${trialJobId}`, `$PWD/${trialJobId}/nnioutput`, trialJobId, this.experimentId, trialSequenceId, this.paiTrialConfig.command, nniManagerIp, this.paiRestServerPort, hdfsOutputDir, this.hdfsOutputHost, this.paiClusterConfig.userName).replace(/\r\n|\n|\r/gm, '');
        console.log(`nniPAItrial command is ${nniPaiTrialCommand.trim()}`);
        const paiTaskRoles = [new paiConfig_1.PAITaskRole('nni_trail_' + trialJobId, 1, this.paiTrialConfig.cpuNum, this.paiTrialConfig.memoryMB, this.paiTrialConfig.gpuNum, nniPaiTrialCommand)];
        const paiJobConfig = new paiConfig_1.PAIJobConfig(paiJobName, this.paiTrialConfig.image, this.paiTrialConfig.dataDir, this.paiTrialConfig.outputDir, `$PAI_DEFAULT_FS_URI${hdfsCodeDir}`, paiTaskRoles, this.paiTrialConfig.virtualCluster === undefined ? 'default' : this.paiTrialConfig.virtualCluster.toString());
        try {
            await hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(trialLocalTempFolder, hdfsCodeDir, this.hdfsClient);
        }
        catch (error) {
            this.log.error(`PAI Training service: copy ${this.paiTrialConfig.codeDir} to HDFS ${hdfsCodeDir} failed, error is ${error}`);
            throw new Error(error.message);
        }
        const submitJobRequest = {
            uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/user/${this.paiClusterConfig.userName}/jobs`,
            method: 'POST',
            json: true,
            body: paiJobConfig,
            headers: {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + this.paiToken
            }
        };
        request(submitJobRequest, (error, response, body) => {
            if (error || response.statusCode >= 400) {
                this.log.error(`PAI Training service: Submit trial ${trialJobId} to PAI Cluster failed!`);
                trialJobDetail.status = 'FAILED';
                deferred.reject(error ? error.message : 'Submit trial failed, http code: ' + response.statusCode);
            }
            else {
                trialJobDetail.submitTime = Date.now();
                deferred.resolve(trialJobDetail);
            }
        });
        return deferred.promise;
    }
    updateTrialJob(trialJobId, form) {
        throw new errors_1.MethodNotImplementedError();
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        const deferred = new ts_deferred_1.Deferred();
        if (!trialJobDetail) {
            this.log.error(`cancelTrialJob: trial job id ${trialJobId} not found`);
            return Promise.reject();
        }
        if (!this.paiClusterConfig) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (!this.paiToken) {
            throw new Error('PAI token is not initialized');
        }
        const stopJobRequest = {
            uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/user/${this.paiClusterConfig.userName}/jobs/${trialJobDetail.paiJobName}/executionType`,
            method: 'PUT',
            json: true,
            body: { 'value': 'STOP' },
            headers: {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + this.paiToken
            }
        };
        request(stopJobRequest, (error, response, body) => {
            if (error || response.statusCode >= 400) {
                this.log.error(`PAI Training service: stop trial ${trialJobId} to PAI Cluster failed!`);
                deferred.reject(error ? error.message : 'Stop trial failed, http code: ' + response.statusCode);
            }
            else {
                if (isEarlyStopped) {
                    trialJobDetail.status = 'EARLY_STOPPED';
                }
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    async setClusterMetadata(key, value) {
        const deferred = new ts_deferred_1.Deferred();
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                deferred.resolve();
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.PAI_CLUSTER_CONFIG:
                this.paiClusterConfig = JSON.parse(value);
                this.hdfsClient = WebHDFS.createClient({
                    user: this.paiClusterConfig.userName,
                    port: 80,
                    path: '/webhdfs/webhdfs/v1',
                    host: this.paiClusterConfig.host
                });
                const authentication_req = {
                    uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/token`,
                    method: 'POST',
                    json: true,
                    body: {
                        username: this.paiClusterConfig.userName,
                        password: this.paiClusterConfig.passWord
                    }
                };
                request(authentication_req, (error, response, body) => {
                    if (error) {
                        this.log.error(`Get PAI token failed: ${error.message}`);
                        deferred.reject(new Error(`Get PAI token failed: ${error.message}`));
                    }
                    else {
                        if (response.statusCode !== 200) {
                            this.log.error(`Get PAI token failed: get PAI Rest return code ${response.statusCode}`);
                            deferred.reject(new Error(`Get PAI token failed, please check paiConfig username or password`));
                        }
                        this.paiToken = body.token;
                        deferred.resolve();
                    }
                });
                let timeoutId;
                const timeoutDelay = new Promise((resolve, reject) => {
                    timeoutId = setTimeout(() => reject(new Error('Get PAI token timeout. Please check your PAI cluster.')), 5000);
                });
                return Promise.race([timeoutDelay, deferred.promise]).finally(() => clearTimeout(timeoutId));
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (!this.paiClusterConfig) {
                    this.log.error('pai cluster config is not initialized');
                    deferred.reject(new Error('pai cluster config is not initialized'));
                    break;
                }
                this.paiTrialConfig = JSON.parse(value);
                if (this.paiTrialConfig.outputDir === undefined || this.paiTrialConfig.outputDir === null) {
                    this.paiTrialConfig.outputDir = typescript_string_operations_1.String.Format(paiData_1.PAI_OUTPUT_DIR_FORMAT, this.paiClusterConfig.host).replace(/\r\n|\n|\r/gm, '');
                }
                try {
                    await util_1.validateCodeDir(this.paiTrialConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    deferred.reject(new Error(error));
                    break;
                }
                const hdfsDirContent = this.paiTrialConfig.outputDir.match(this.hdfsDirPattern);
                if (hdfsDirContent === null) {
                    throw new Error('Trial outputDir format Error');
                }
                const groups = hdfsDirContent.groups;
                if (groups === undefined) {
                    throw new Error('Trial outputDir format Error');
                }
                this.hdfsOutputHost = groups['host'];
                this.hdfsBaseDir = groups['baseDir'];
                if (this.hdfsBaseDir === undefined) {
                    this.hdfsBaseDir = "/";
                }
                let dataOutputHdfsClient;
                if (this.paiClusterConfig.host === this.hdfsOutputHost && this.hdfsClient) {
                    dataOutputHdfsClient = this.hdfsClient;
                }
                else {
                    dataOutputHdfsClient = WebHDFS.createClient({
                        user: this.paiClusterConfig.userName,
                        port: 50070,
                        host: this.hdfsOutputHost
                    });
                }
                try {
                    const exist = await hdfsClientUtility_1.HDFSClientUtility.pathExists("/", dataOutputHdfsClient);
                    if (!exist) {
                        deferred.reject(new Error(`Please check hdfsOutputDir host!`));
                    }
                }
                catch (error) {
                    deferred.reject(new Error(`HDFS encounters problem, error is ${error}. Please check hdfsOutputDir host!`));
                }
                deferred.resolve();
                break;
            default:
                throw new Error(`Uknown key: ${key}`);
        }
        return deferred.promise;
    }
    getClusterMetadata(key) {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve();
        return deferred.promise;
    }
    async cleanUp() {
        this.stopping = true;
        const deferred = new ts_deferred_1.Deferred();
        const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
        try {
            await restServer.stop();
            deferred.resolve();
            this.log.info('PAI Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`PAI Training service rest server stopped failed, error: ${error.message}`);
            deferred.reject(error);
        }
        return deferred.promise;
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    generateSequenceId() {
        if (this.nextTrialSequenceId === -1) {
            this.nextTrialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.nextTrialSequenceId++;
    }
};
PAITrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], PAITrainingService);
exports.PAITrainingService = PAITrainingService;
