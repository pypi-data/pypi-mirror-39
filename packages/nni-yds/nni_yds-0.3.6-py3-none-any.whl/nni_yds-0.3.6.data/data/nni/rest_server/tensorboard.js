'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const component = require("../common/component");
const datastore_1 = require("../common/datastore");
const errors_1 = require("../common/errors");
const log_1 = require("../common/log");
const trainingService_1 = require("../common/trainingService");
class TensorBoard {
    constructor() {
        this.DEFAULT_PORT = 6006;
        this.TENSORBOARD_COMMAND = 'PATH=$PATH:~/.local/bin:/usr/local/bin tensorboard';
        this.log = log_1.getLogger();
        this.tbJobMap = new Map();
        this.trainingService = component.get(trainingService_1.TrainingService);
        this.dataStore = component.get(datastore_1.DataStore);
    }
    async startTensorBoard(trialJobIds, tbCmd, port) {
        let tensorBoardPort = this.DEFAULT_PORT;
        if (port !== undefined) {
            tensorBoardPort = port;
        }
        const host = await this.getJobHost(trialJobIds);
        const tbEndpoint = `http://${host}:${tensorBoardPort}`;
        try {
            if (await this.isTensorBoardRunningOnHost(host)) {
                await this.stopHostTensorBoard(host);
            }
        }
        catch (error) {
            if (error.name !== errors_1.NNIErrorNames.NOT_FOUND) {
                throw error;
            }
            else {
                this.tbJobMap.delete(host);
            }
        }
        const logDirs = [];
        for (const id of trialJobIds) {
            logDirs.push(await this.getLogDir(id));
        }
        let tensorBoardCmd = this.TENSORBOARD_COMMAND;
        if (tbCmd !== undefined && tbCmd.trim().length > 0) {
            tensorBoardCmd = tbCmd;
        }
        const cmd = `${tensorBoardCmd} --logdir ${logDirs.join(':')} --port ${tensorBoardPort}`;
        const form = {
            jobType: 'HOST',
            host: host,
            cmd: cmd
        };
        const jobId = (await this.trainingService.submitTrialJob(form)).id;
        this.tbJobMap.set(host, jobId);
        return tbEndpoint;
    }
    async cleanUp() {
        const stopTensorBoardTasks = [];
        this.tbJobMap.forEach((jobId, host) => {
            stopTensorBoardTasks.push(this.stopHostTensorBoard(host).catch((err) => {
                this.log.error(`Error occurred stopping tensorboard service: ${err.message}`);
            }));
        });
        await Promise.all(stopTensorBoardTasks);
    }
    stopTensorBoard(endPoint) {
        const host = this.getEndPointHost(endPoint);
        return this.stopHostTensorBoard(host);
    }
    stopHostTensorBoard(host) {
        const jobId = this.tbJobMap.get(host);
        if (jobId === undefined) {
            return Promise.resolve();
        }
        return this.trainingService.cancelTrialJob(jobId);
    }
    async isTensorBoardRunningOnHost(host) {
        const jobId = this.tbJobMap.get(host);
        if (jobId === undefined) {
            return false;
        }
        const status = (await this.trainingService.getTrialJob(jobId)).status;
        return ['RUNNING', 'WAITING'].includes(status);
    }
    async getJobHost(trialJobIds) {
        if (trialJobIds === undefined || trialJobIds.length < 1) {
            throw new Error('No trail job specified.');
        }
        const jobInfo = await this.dataStore.getTrialJob(trialJobIds[0]);
        const logPath = jobInfo.logPath;
        if (logPath === undefined) {
            throw new Error(`Failed to find job logPath: ${jobInfo.id}`);
        }
        return logPath.split('://')[1].split(':')[0];
    }
    async getLogDir(trialJobId) {
        const jobInfo = await this.dataStore.getTrialJob(trialJobId);
        const logPath = jobInfo.logPath;
        if (logPath === undefined) {
            throw new Error(`Failed to find job logPath: ${jobInfo.id}`);
        }
        return logPath.split('://')[1].split(':')[1];
    }
    getEndPointHost(endPoint) {
        const parts = endPoint.match(/.*:\/\/(.*):(.*)/);
        if (parts !== null) {
            return parts[1];
        }
        else {
            throw new Error(`Invalid endPoint: ${endPoint}`);
        }
    }
}
exports.TensorBoard = TensorBoard;
