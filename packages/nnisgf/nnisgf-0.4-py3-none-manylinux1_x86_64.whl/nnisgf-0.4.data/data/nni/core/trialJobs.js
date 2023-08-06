'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const events_1 = require("events");
const utils_1 = require("../common/utils");
class TrialJobs {
    constructor(trainingService, pastExecDuration, maxExecDuration) {
        this.eventEmitter = new events_1.EventEmitter();
        this.trialJobs = new Map();
        this.noMoreTrials = false;
        this.stopLoop = false;
        this.trainingService = trainingService;
        this.pastExecDuration = pastExecDuration;
        this.maxExecDuration = maxExecDuration;
    }
    setTrialJob(key, value) {
        this.trialJobs.set(key, value);
    }
    getTrialJob(key) {
        return this.trialJobs.get(key);
    }
    setNoMoreTrials() {
        this.noMoreTrials = true;
    }
    setStopLoop() {
        this.stopLoop = true;
    }
    updateMaxExecDuration(duration) {
        this.maxExecDuration = duration;
    }
    on(listener) {
        this.eventEmitter.addListener('all', listener);
    }
    async requestTrialJobsStatus() {
        for (const trialJobId of Array.from(this.trialJobs.keys())) {
            const trialJobDetail = await this.trainingService.getTrialJob(trialJobId);
            switch (trialJobDetail.status) {
                case 'SUCCEEDED':
                case 'USER_CANCELED':
                    this.eventEmitter.emit('all', trialJobDetail.status, trialJobDetail);
                    this.trialJobs.delete(trialJobId);
                    break;
                case 'FAILED':
                case 'SYS_CANCELED':
                    this.eventEmitter.emit('all', trialJobDetail.status, trialJobDetail);
                    this.trialJobs.delete(trialJobId);
                    break;
                case 'WAITING':
                    break;
                case 'RUNNING':
                    const oldTrialJobDetail = this.trialJobs.get(trialJobId);
                    assert(oldTrialJobDetail);
                    if (oldTrialJobDetail !== undefined && oldTrialJobDetail.status === "WAITING") {
                        this.trialJobs.set(trialJobId, trialJobDetail);
                        this.eventEmitter.emit('all', trialJobDetail.status, trialJobDetail);
                    }
                    break;
                case 'UNKNOWN':
                    break;
                default:
            }
        }
        return Promise.resolve();
    }
    async run() {
        const startTime = Date.now();
        while ((Date.now() - startTime) / 1000 + this.pastExecDuration < this.maxExecDuration) {
            if (this.stopLoop ||
                (this.noMoreTrials && this.trialJobs.size === 0)) {
                break;
            }
            await this.requestTrialJobsStatus();
            await utils_1.delay(5000);
        }
        this.eventEmitter.emit('all', 'EXPERIMENT_DONE');
    }
}
exports.TrialJobs = TrialJobs;
