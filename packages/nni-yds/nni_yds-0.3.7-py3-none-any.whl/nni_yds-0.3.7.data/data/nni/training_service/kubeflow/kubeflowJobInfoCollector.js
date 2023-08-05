'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
class KubeflowJobInfoCollector {
    constructor(jobMap) {
        this.log = log_1.getLogger();
        this.MAX_FAILED_QUERY_JOB_NUMBER = 30;
        this.trialJobsMap = jobMap;
        this.statusesNeedToCheck = ['RUNNING', 'WAITING'];
    }
    async retrieveTrialStatus() {
        const updateKubeflowTrialJobs = [];
        for (let [trialJobId, kubeflowTrialJob] of this.trialJobsMap) {
            if (!kubeflowTrialJob) {
                throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
            }
            if (Date.now() - kubeflowTrialJob.submitTime < 20 * 1000) {
                return Promise.resolve();
            }
            updateKubeflowTrialJobs.push(this.retrieveSingleTrialJobInfo(kubeflowTrialJob));
        }
        await Promise.all(updateKubeflowTrialJobs);
    }
    async retrieveSingleTrialJobInfo(kubeflowTrialJob) {
        if (!this.statusesNeedToCheck.includes(kubeflowTrialJob.status)) {
            return Promise.resolve();
        }
        let result;
        try {
            result = await cpp.exec(`kubectl get ${kubeflowTrialJob.k8sPluralName} ${kubeflowTrialJob.kubeflowJobName} -o json`);
            if (result.stderr) {
                this.log.error(`Get ${kubeflowTrialJob.k8sPluralName} ${kubeflowTrialJob.kubeflowJobName} failed. Error is ${result.stderr}, failed checking number is ${kubeflowTrialJob.queryJobFailedCount}`);
                kubeflowTrialJob.queryJobFailedCount++;
                if (kubeflowTrialJob.queryJobFailedCount >= this.MAX_FAILED_QUERY_JOB_NUMBER) {
                    kubeflowTrialJob.status = 'UNKNOWN';
                }
            }
        }
        catch (error) {
            this.log.error(`kubectl get ${kubeflowTrialJob.k8sPluralName} ${kubeflowTrialJob.kubeflowJobName} failed, error is ${error}`);
            return Promise.resolve();
        }
        const kubeflowJobInfo = JSON.parse(result.stdout);
        if (kubeflowJobInfo.status && kubeflowJobInfo.status.conditions) {
            const latestCondition = kubeflowJobInfo.status.conditions[kubeflowJobInfo.status.conditions.length - 1];
            const tfJobType = latestCondition.type;
            switch (tfJobType) {
                case 'Created':
                    kubeflowTrialJob.status = 'WAITING';
                    kubeflowTrialJob.startTime = Date.parse(latestCondition.lastUpdateTime);
                    break;
                case 'Running':
                    kubeflowTrialJob.status = 'RUNNING';
                    if (!kubeflowTrialJob.startTime) {
                        kubeflowTrialJob.startTime = Date.parse(latestCondition.lastUpdateTime);
                    }
                    break;
                case 'Failed':
                    kubeflowTrialJob.status = 'FAILED';
                    kubeflowTrialJob.endTime = Date.parse(latestCondition.lastUpdateTime);
                    break;
                case 'Succeeded':
                    kubeflowTrialJob.status = 'SUCCEEDED';
                    kubeflowTrialJob.endTime = Date.parse(latestCondition.lastUpdateTime);
                    break;
                default:
                    break;
            }
        }
        return Promise.resolve();
    }
}
exports.KubeflowJobInfoCollector = KubeflowJobInfoCollector;
