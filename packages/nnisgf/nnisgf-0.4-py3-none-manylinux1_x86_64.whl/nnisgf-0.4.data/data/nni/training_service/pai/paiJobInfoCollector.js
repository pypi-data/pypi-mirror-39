'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const request = require("request");
const ts_deferred_1 = require("ts-deferred");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
class PAIJobInfoCollector {
    constructor(jobMap) {
        this.log = log_1.getLogger();
        this.trialJobsMap = jobMap;
        this.statusesNeedToCheck = ['RUNNING', 'UNKNOWN', 'WAITING'];
        this.finalStatuses = ['SUCCEEDED', 'FAILED', 'USER_CANCELED', 'SYS_CANCELED', 'EARLY_STOPPED'];
    }
    async retrieveTrialStatus(paiToken, paiClusterConfig) {
        if (!paiClusterConfig || !paiToken) {
            return Promise.resolve();
        }
        const updatePaiTrialJobs = [];
        for (let [trialJobId, paiTrialJob] of this.trialJobsMap) {
            if (!paiTrialJob) {
                throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
            }
            updatePaiTrialJobs.push(this.getSinglePAITrialJobInfo(paiTrialJob, paiToken, paiClusterConfig));
        }
        await Promise.all(updatePaiTrialJobs);
    }
    getSinglePAITrialJobInfo(paiTrialJob, paiToken, paiClusterConfig) {
        const deferred = new ts_deferred_1.Deferred();
        if (!this.statusesNeedToCheck.includes(paiTrialJob.status)) {
            deferred.resolve();
            return deferred.promise;
        }
        const getJobInfoRequest = {
            uri: `http://${paiClusterConfig.host}/rest-server/api/v1/user/${paiClusterConfig.userName}/jobs/${paiTrialJob.paiJobName}`,
            method: 'GET',
            json: true,
            headers: {
                "Content-Type": "application/json",
                "Authorization": 'Bearer ' + paiToken
            }
        };
        request(getJobInfoRequest, (error, response, body) => {
            if (error || response.statusCode >= 500) {
                this.log.error(`PAI Training service: get job info for trial ${paiTrialJob.id} from PAI Cluster failed!`);
                if (paiTrialJob.status === 'WAITING' || paiTrialJob.status === 'RUNNING') {
                    paiTrialJob.status = 'UNKNOWN';
                }
            }
            else {
                if (response.body.jobStatus && response.body.jobStatus.state) {
                    switch (response.body.jobStatus.state) {
                        case 'WAITING':
                            paiTrialJob.status = 'WAITING';
                            break;
                        case 'RUNNING':
                            paiTrialJob.status = 'RUNNING';
                            if (!paiTrialJob.startTime) {
                                paiTrialJob.startTime = response.body.jobStatus.appLaunchedTime;
                            }
                            if (!paiTrialJob.url) {
                                paiTrialJob.url = response.body.jobStatus.appTrackingUrl;
                            }
                            break;
                        case 'SUCCEEDED':
                            paiTrialJob.status = 'SUCCEEDED';
                            break;
                        case 'STOPPED':
                            if (paiTrialJob.status !== 'EARLY_STOPPED') {
                                paiTrialJob.status = 'USER_CANCELED';
                            }
                            break;
                        case 'FAILED':
                            paiTrialJob.status = 'FAILED';
                            break;
                        default:
                            paiTrialJob.status = 'UNKNOWN';
                            break;
                    }
                    if (this.finalStatuses.includes(paiTrialJob.status)) {
                        if (!paiTrialJob.startTime) {
                            paiTrialJob.startTime = response.body.jobStatus.appLaunchedTime;
                        }
                        if (!paiTrialJob.endTime) {
                            paiTrialJob.endTime = response.body.jobStatus.completedTime;
                        }
                        if (paiTrialJob.hdfsLogPath) {
                            paiTrialJob.url += `,${paiTrialJob.hdfsLogPath}`;
                        }
                    }
                }
            }
            deferred.resolve();
        });
        return deferred.promise;
    }
}
exports.PAIJobInfoCollector = PAIJobInfoCollector;
