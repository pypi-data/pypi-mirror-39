'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const cp = require("child_process");
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const ts = require("tail-stream");
const errors_1 = require("../../common/errors");
const log_1 = require("../../common/log");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const utils_1 = require("../../common/utils");
const tkill = require('tree-kill');
function decodeCommand(data) {
    if (data.length < 8) {
        return [false, '', '', data];
    }
    const commandType = data.slice(0, 2).toString();
    const contentLength = parseInt(data.slice(2, 8).toString(), 10);
    if (data.length < contentLength + 8) {
        return [false, '', '', data];
    }
    const content = data.slice(8, contentLength + 8).toString();
    const remain = data.slice(contentLength + 8);
    return [true, commandType, content, remain];
}
class LocalTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form, sequenceId) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.url = `file://localhost:${workingDirectory}`;
        this.sequenceId = sequenceId;
    }
}
class LocalTrainingService {
    constructor() {
        this.isMultiPhase = false;
        this.eventEmitter = new events_1.EventEmitter();
        this.jobMap = new Map();
        this.jobQueue = [];
        this.initialized = false;
        this.stopping = false;
        this.log = log_1.getLogger();
        this.trialSequenceId = -1;
        this.streams = new Array();
    }
    async run() {
        while (!this.stopping) {
            while (this.jobQueue.length !== 0) {
                const trialJobId = this.jobQueue[0];
                const trialJobDeatil = this.jobMap.get(trialJobId);
                if (trialJobDeatil !== undefined && trialJobDeatil.status === 'WAITING') {
                    const [success, resource] = this.tryGetAvailableResource();
                    if (!success) {
                        break;
                    }
                    this.occupyResource(resource);
                    await this.runTrialJob(trialJobId, resource);
                }
                this.jobQueue.shift();
            }
            await utils_1.delay(5000);
        }
    }
    async listTrialJobs() {
        const jobs = [];
        for (const key of this.jobMap.keys()) {
            const trialJob = await this.getTrialJob(key);
            if (trialJob.form.jobType === 'TRIAL') {
                jobs.push(trialJob);
            }
        }
        return jobs;
    }
    async getTrialJob(trialJobId) {
        const trialJob = this.jobMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, 'Trial job not found');
        }
        if (trialJob.form.jobType === 'HOST') {
            return this.getHostJob(trialJobId);
        }
        if (trialJob.status === 'RUNNING') {
            let alive = false;
            try {
                await cpp.exec(`kill -0 ${trialJob.pid}`);
                alive = true;
            }
            catch (error) {
            }
            if (!alive) {
                trialJob.endTime = Date.now();
                this.setTrialJobStatus(trialJob, 'FAILED');
                try {
                    const state = await fs.promises.readFile(path.join(trialJob.workingDirectory, '.nni', 'state'), 'utf8');
                    const match = state.trim().match(/^(\d+)\s+(\d+)/);
                    if (match !== null) {
                        const { 1: code, 2: timestamp } = match;
                        if (parseInt(code, 10) === 0) {
                            this.setTrialJobStatus(trialJob, 'SUCCEEDED');
                        }
                        trialJob.endTime = parseInt(timestamp, 10);
                    }
                }
                catch (error) {
                }
                this.log.info(`trailJob status update: ${trialJobId}, ${trialJob.status}`);
            }
        }
        return trialJob;
    }
    addTrialJobMetricListener(listener) {
        this.eventEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.eventEmitter.off('metric', listener);
    }
    submitTrialJob(form) {
        this.log.info(`submitTrialJob: form: ${JSON.stringify(form)}`);
        if (form.jobType === 'HOST') {
            return this.runHostJob(form);
        }
        else if (form.jobType === 'TRIAL') {
            const trialJobId = utils_1.uniqueString(5);
            const trialJobDetail = new LocalTrialJobDetail(trialJobId, 'WAITING', Date.now(), path.join(this.rootDir, 'trials', trialJobId), form, this.generateSequenceId());
            this.jobQueue.push(trialJobId);
            this.jobMap.set(trialJobId, trialJobDetail);
            this.log.debug(`submitTrialJob: return: ${JSON.stringify(trialJobDetail)} `);
            return Promise.resolve(trialJobDetail);
        }
        else {
            return Promise.reject(new Error(`Job form not supported: ${JSON.stringify(form)}`));
        }
    }
    async updateTrialJob(trialJobId, form) {
        const trialJobDetail = this.jobMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        if (form.jobType === 'TRIAL') {
            await this.writeParameterFile(trialJobDetail.workingDirectory, form.hyperParameters);
        }
        else {
            throw new Error(`updateTrialJob failed: jobType ${form.jobType} not supported.`);
        }
        return trialJobDetail;
    }
    get isMultiPhaseJobSupported() {
        return true;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        this.log.info(`cancelTrialJob: ${trialJobId}`);
        const trialJob = this.jobMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, 'Trial job not found');
        }
        if (trialJob.pid === undefined) {
            this.setTrialJobStatus(trialJob, 'USER_CANCELED');
            return;
        }
        if (trialJob.form.jobType === 'TRIAL') {
            await tkill(trialJob.pid, 'SIGKILL');
        }
        else if (trialJob.form.jobType === 'HOST') {
            await cpp.exec(`pkill -9 -P ${trialJob.pid}`);
        }
        else {
            throw new Error(`Job type not supported: ${trialJob.form.jobType}`);
        }
        this.setTrialJobStatus(trialJob, utils_1.getJobCancelStatus(isEarlyStopped));
    }
    async setClusterMetadata(key, value) {
        if (!this.initialized) {
            this.rootDir = utils_1.getExperimentRootDir();
            await cpp.exec(`mkdir -p ${this.rootDir}`);
            this.initialized = true;
        }
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                this.localTrailConfig = JSON.parse(value);
                if (!this.localTrailConfig) {
                    throw new Error('trial config parsed failed');
                }
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MULTI_PHASE:
                this.isMultiPhase = (value === 'true' || value === 'True');
                break;
            default:
        }
    }
    getClusterMetadata(key) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                let getResult;
                if (!this.localTrailConfig) {
                    getResult = Promise.reject(new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `${key} is never set yet`));
                }
                else {
                    getResult = Promise.resolve(!this.localTrailConfig ? '' : JSON.stringify(this.localTrailConfig));
                }
                return getResult;
            default:
                return Promise.reject(new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, 'Key not found'));
        }
    }
    cleanUp() {
        this.stopping = true;
        for (const stream of this.streams) {
            stream.destroy();
        }
        return Promise.resolve();
    }
    onTrialJobStatusChanged(trialJob, oldStatus) {
    }
    getEnvironmentVariables(trialJobDetail, _) {
        return [
            { key: 'NNI_PLATFORM', value: 'local' },
            { key: 'NNI_SYS_DIR', value: trialJobDetail.workingDirectory },
            { key: 'NNI_TRIAL_JOB_ID', value: trialJobDetail.id },
            { key: 'NNI_OUTPUT_DIR', value: trialJobDetail.workingDirectory },
            { key: 'NNI_TRIAL_SEQ_ID', value: trialJobDetail.sequenceId.toString() },
            { key: 'MULTI_PHASE', value: this.isMultiPhase.toString() }
        ];
    }
    setExtraProperties(trialJobDetail, resource) {
    }
    tryGetAvailableResource() {
        return [true, {}];
    }
    occupyResource(_) {
    }
    setTrialJobStatus(trialJob, newStatus) {
        if (trialJob.status !== newStatus) {
            const oldStatus = trialJob.status;
            trialJob.status = newStatus;
            this.onTrialJobStatusChanged(trialJob, oldStatus);
        }
    }
    async runTrialJob(trialJobId, resource) {
        const trialJobDetail = this.jobMap.get(trialJobId);
        const variables = this.getEnvironmentVariables(trialJobDetail, resource);
        const runScriptLines = [];
        if (!this.localTrailConfig) {
            throw new Error('trial config is not initialized');
        }
        runScriptLines.push('#!/bin/bash', `cd ${this.localTrailConfig.codeDir}`);
        for (const variable of variables) {
            runScriptLines.push(`export ${variable.key}=${variable.value}`);
        }
        runScriptLines.push(`eval ${this.localTrailConfig.command} 2>${path.join(trialJobDetail.workingDirectory, 'stderr')}`, `echo $? \`date +%s%3N\` >${path.join(trialJobDetail.workingDirectory, '.nni', 'state')}`);
        await cpp.exec(`mkdir -p ${trialJobDetail.workingDirectory}`);
        await cpp.exec(`mkdir -p ${path.join(trialJobDetail.workingDirectory, '.nni')}`);
        await cpp.exec(`touch ${path.join(trialJobDetail.workingDirectory, '.nni', 'metrics')}`);
        await fs.promises.writeFile(path.join(trialJobDetail.workingDirectory, 'run.sh'), runScriptLines.join('\n'), { encoding: 'utf8', mode: 0o777 });
        await this.writeParameterFile(trialJobDetail.workingDirectory, trialJobDetail.form.hyperParameters);
        const process = cp.exec(`bash ${path.join(trialJobDetail.workingDirectory, 'run.sh')}`);
        this.setTrialJobStatus(trialJobDetail, 'RUNNING');
        trialJobDetail.startTime = Date.now();
        trialJobDetail.pid = process.pid;
        this.setExtraProperties(trialJobDetail, resource);
        let buffer = Buffer.alloc(0);
        const stream = ts.createReadStream(path.join(trialJobDetail.workingDirectory, '.nni', 'metrics'));
        stream.on('data', (data) => {
            buffer = Buffer.concat([buffer, data]);
            while (buffer.length > 0) {
                const [success, , content, remain] = decodeCommand(buffer);
                if (!success) {
                    break;
                }
                this.eventEmitter.emit('metric', {
                    id: trialJobDetail.id,
                    data: content
                });
                this.log.debug(`Sending metrics, job id: ${trialJobDetail.id}, metrics: ${content}`);
                buffer = remain;
            }
        });
        this.streams.push(stream);
    }
    async runHostJob(form) {
        const jobId = utils_1.uniqueString(5);
        const workDir = path.join(this.rootDir, 'hostjobs', jobId);
        await cpp.exec(`mkdir -p ${workDir}`);
        const wrappedCmd = `cd ${workDir} && ${form.cmd}>stdout 2>stderr`;
        this.log.debug(`runHostJob: command: ${wrappedCmd}`);
        const process = cp.exec(wrappedCmd);
        const jobDetail = {
            id: jobId,
            status: 'RUNNING',
            submitTime: Date.now(),
            workingDirectory: workDir,
            form: form,
            sequenceId: this.generateSequenceId(),
            pid: process.pid
        };
        this.jobMap.set(jobId, jobDetail);
        this.log.debug(`runHostJob: return: ${JSON.stringify(jobDetail)} `);
        return jobDetail;
    }
    async getHostJob(jobId) {
        const jobDetail = this.jobMap.get(jobId);
        if (jobDetail === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `Host Job not found: ${jobId}`);
        }
        try {
            await cpp.exec(`kill -0 ${jobDetail.pid}`);
            return jobDetail;
        }
        catch (error) {
            if (error instanceof Error) {
                this.log.debug(`getHostJob: error: ${error.message}`);
                this.jobMap.delete(jobId);
                throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `Host Job not found: ${error.message}`);
            }
            else {
                throw error;
            }
        }
    }
    async writeParameterFile(directory, hyperParameters) {
        const filepath = path.join(directory, utils_1.generateParamFileName(hyperParameters));
        await fs.promises.writeFile(filepath, hyperParameters.value, { encoding: 'utf8' });
    }
    generateSequenceId() {
        if (this.trialSequenceId === -1) {
            this.trialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.trialSequenceId++;
    }
}
exports.LocalTrainingService = LocalTrainingService;
