'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
class KubeflowJobInfoCollector {
    constructor(jobMap) {
        this.log = log_1.getLogger();
        this.trialJobsMap = jobMap;
        this.statusesNeedToCheck = ['RUNNING', 'WAITING'];
    }
    async retrieveTrialStatus(operatorClient) {
        assert(operatorClient !== undefined);
        const updateKubeflowTrialJobs = [];
        for (let [trialJobId, kubeflowTrialJob] of this.trialJobsMap) {
            if (!kubeflowTrialJob) {
                throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
            }
            if (Date.now() - kubeflowTrialJob.submitTime < 20 * 1000) {
                return Promise.resolve();
            }
            updateKubeflowTrialJobs.push(this.retrieveSingleTrialJobInfo(operatorClient, kubeflowTrialJob));
        }
        await Promise.all(updateKubeflowTrialJobs);
    }
    async retrieveSingleTrialJobInfo(operatorClient, kubeflowTrialJob) {
        if (!this.statusesNeedToCheck.includes(kubeflowTrialJob.status)) {
            return Promise.resolve();
        }
        if (operatorClient === undefined) {
            return Promise.reject('operatorClient is undefined');
        }
        let kubeflowJobInfo;
        try {
            kubeflowJobInfo = await operatorClient.getKubeflowJob(kubeflowTrialJob.kubeflowJobName);
        }
        catch (error) {
            this.log.error(`Get job ${kubeflowTrialJob.kubeflowJobName} info failed, error is ${error}`);
            return Promise.resolve();
        }
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
