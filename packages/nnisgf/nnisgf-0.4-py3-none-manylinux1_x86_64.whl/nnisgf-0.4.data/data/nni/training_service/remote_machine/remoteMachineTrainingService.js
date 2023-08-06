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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const cpp = require("child-process-promise");
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const ssh2_1 = require("ssh2");
const ts_deferred_1 = require("ts-deferred");
const typescript_string_operations_1 = require("typescript-string-operations");
const component = require("../../common/component");
const errors_1 = require("../../common/errors");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const observableTimer_1 = require("../../common/observableTimer");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const gpuScheduler_1 = require("./gpuScheduler");
const metricsCollector_1 = require("./metricsCollector");
const remoteMachineData_1 = require("./remoteMachineData");
const sshClientUtility_1 = require("./sshClientUtility");
const util_1 = require("../common/util");
let RemoteMachineTrainingService = class RemoteMachineTrainingService {
    constructor(timer) {
        this.stopping = false;
        this.isMultiPhase = false;
        this.remoteOS = 'linux';
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.machineSSHClientMap = new Map();
        this.gpuScheduler = new gpuScheduler_1.GPUScheduler(this.machineSSHClientMap);
        this.jobQueue = [];
        this.expRootDir = utils_1.getExperimentRootDir();
        this.remoteExpRootDir = this.getRemoteExperimentRootDir();
        this.timer = timer;
        this.log = log_1.getLogger();
        this.trialSequenceId = -1;
    }
    async run() {
        while (!this.stopping) {
            while (this.jobQueue.length > 0) {
                const trialJobId = this.jobQueue[0];
                const prepareResult = await this.prepareTrialJob(trialJobId);
                if (prepareResult) {
                    this.jobQueue.shift();
                }
                else {
                    break;
                }
            }
            const metricsCollector = new metricsCollector_1.MetricsCollector(this.machineSSHClientMap, this.trialJobsMap, this.remoteExpRootDir, this.metricsEmitter);
            await metricsCollector.collectMetrics();
            await utils_1.delay(3000);
        }
    }
    listTrialJobs() {
        const jobs = [];
        const deferred = new ts_deferred_1.Deferred();
        this.trialJobsMap.forEach(async (value, key) => {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        });
        deferred.resolve(jobs);
        return deferred.promise;
    }
    async getTrialJob(trialJobId) {
        const trialJob = this.trialJobsMap.get(trialJobId);
        if (!trialJob) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
        }
        if (trialJob.status === 'RUNNING' || trialJob.status === 'UNKNOWN') {
            if (trialJob.rmMeta === undefined) {
                throw new Error(`rmMeta not set for submitted job ${trialJobId}`);
            }
            const sshClient = this.machineSSHClientMap.get(trialJob.rmMeta);
            if (!sshClient) {
                throw new Error(`Invalid job id: ${trialJobId}, cannot find ssh client`);
            }
            return this.updateTrialJobStatus(trialJob, sshClient);
        }
        else {
            return trialJob;
        }
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    submitTrialJob(form) {
        this.log.info(`submitTrialJob: form: ${JSON.stringify(form)}`);
        if (!this.trialConfig) {
            throw new Error('trial config is not initialized');
        }
        if (form.jobType === 'HOST') {
            return this.runHostJob(form);
        }
        else if (form.jobType === 'TRIAL') {
            const trialJobId = utils_1.uniqueString(5);
            const trialWorkingFolder = path.join(this.remoteExpRootDir, 'trials', trialJobId);
            const trialJobDetail = new remoteMachineData_1.RemoteMachineTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form, this.generateSequenceId());
            this.jobQueue.push(trialJobId);
            this.trialJobsMap.set(trialJobId, trialJobDetail);
            return Promise.resolve(trialJobDetail);
        }
        else {
            return Promise.reject(new Error(`Job form not supported: ${JSON.stringify(form)}, jobType should be HOST or TRIAL.`));
        }
    }
    async updateTrialJob(trialJobId, form) {
        this.log.info(`updateTrialJob: form: ${JSON.stringify(form)}`);
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        if (form.jobType === 'TRIAL') {
            const rmMeta = trialJobDetail.rmMeta;
            if (rmMeta !== undefined) {
                await this.writeParameterFile(trialJobId, form.hyperParameters, rmMeta);
            }
            else {
                throw new Error(`updateTrialJob failed: ${trialJobId} rmMeta not found`);
            }
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
        this.log.info(`cancelTrialJob: jobId: ${trialJobId}`);
        const deferred = new ts_deferred_1.Deferred();
        const trialJob = this.trialJobsMap.get(trialJobId);
        if (!trialJob) {
            deferred.reject();
            throw new Error(`trial job id ${trialJobId} not found`);
        }
        const index = this.jobQueue.indexOf(trialJobId);
        if (index >= 0) {
            this.jobQueue.splice(index, 1);
        }
        if (trialJob.rmMeta !== undefined) {
            const sshClient = this.machineSSHClientMap.get(trialJob.rmMeta);
            if (!sshClient) {
                deferred.reject();
                throw new Error(`Invalid job id ${trialJobId}, cannot find ssh client`);
            }
            const jobpidPath = this.getJobPidPath(trialJob.id);
            try {
                await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`pkill -P \`cat ${jobpidPath}\``, sshClient);
                trialJob.status = utils_1.getJobCancelStatus(isEarlyStopped);
            }
            catch (error) {
                this.log.error(`remoteTrainingService.cancelTrialJob: ${error.message}`);
            }
        }
        else {
            assert(isEarlyStopped === false, 'isEarlyStopped is not supposed to be true here.');
            trialJob.status = utils_1.getJobCancelStatus(isEarlyStopped);
        }
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MACHINE_LIST:
                await this.setupConnections(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                const remoteMachineTrailConfig = JSON.parse(value);
                if (!remoteMachineTrailConfig) {
                    throw new Error('trial config parsed failed');
                }
                if (!fs.lstatSync(remoteMachineTrailConfig.codeDir).isDirectory()) {
                    throw new Error(`codeDir ${remoteMachineTrailConfig.codeDir} is not a directory`);
                }
                try {
                    await util_1.validateCodeDir(remoteMachineTrailConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    return Promise.reject(new Error(error));
                }
                this.trialConfig = remoteMachineTrailConfig;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MULTI_PHASE:
                this.isMultiPhase = (value === 'true' || value === 'True');
                break;
            default:
                throw new Error(`Uknown key: ${key}`);
        }
    }
    getClusterMetadata(key) {
        const deferred = new ts_deferred_1.Deferred();
        return deferred.promise;
    }
    cleanUp() {
        this.stopping = true;
        return Promise.resolve();
    }
    async setupConnections(machineList) {
        const deferred = new ts_deferred_1.Deferred();
        const rmMetaList = JSON.parse(machineList);
        let connectedRMNum = 0;
        rmMetaList.forEach((rmMeta) => {
            const conn = new ssh2_1.Client();
            let connectConfig = {
                host: rmMeta.ip,
                port: rmMeta.port,
                username: rmMeta.username
            };
            if (rmMeta.passwd) {
                connectConfig.password = rmMeta.passwd;
            }
            else if (rmMeta.sshKeyPath) {
                if (!fs.existsSync(rmMeta.sshKeyPath)) {
                    deferred.reject(new Error(`${rmMeta.sshKeyPath} does not exist.`));
                }
                const privateKey = fs.readFileSync(rmMeta.sshKeyPath, 'utf8');
                connectConfig.privateKey = privateKey;
                connectConfig.passphrase = rmMeta.passphrase;
            }
            else {
                deferred.reject(new Error(`No valid passwd or sshKeyPath is configed.`));
            }
            this.machineSSHClientMap.set(rmMeta, conn);
            conn.on('ready', async () => {
                this.machineSSHClientMap.set(rmMeta, conn);
                await this.initRemoteMachineOnConnected(rmMeta, conn);
                if (++connectedRMNum === rmMetaList.length) {
                    deferred.resolve();
                }
            }).on('error', (err) => {
                deferred.reject(new Error(err.message));
            }).connect(connectConfig);
        });
        return deferred.promise;
    }
    async initRemoteMachineOnConnected(rmMeta, conn) {
        const nniRootDir = '/tmp/nni';
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`mkdir -p ${this.remoteExpRootDir}`, conn);
        const remoteScriptsDir = this.getRemoteScriptsPath();
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`mkdir -p ${remoteScriptsDir}`, conn);
        await sshClientUtility_1.SSHClientUtility.copyDirectoryToRemote('./scripts', remoteScriptsDir, conn, this.remoteOS);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`chmod 777 ${nniRootDir} ${nniRootDir}/* ${nniRootDir}/scripts/*`, conn);
        sshClientUtility_1.SSHClientUtility.remoteExeCommand(`cd ${remoteScriptsDir} && python3 gpu_metrics_collector.py`, conn);
        this.timer.subscribe(async (tick) => {
            const cmdresult = await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`tail -n 1 ${path.join(remoteScriptsDir, 'gpu_metrics')}`, conn);
            if (cmdresult && cmdresult.stdout) {
                rmMeta.gpuSummary = JSON.parse(cmdresult.stdout);
            }
        });
    }
    async prepareTrialJob(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        if (!this.trialConfig) {
            throw new Error('trial config is not initialized');
        }
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.INVALID_JOB_DETAIL, `Invalid job detail information for trial job ${trialJobId}`);
        }
        const rmScheduleResult = this.gpuScheduler.scheduleMachine(this.trialConfig.gpuNum, trialJobId);
        if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.REQUIRE_EXCEED_TOTAL) {
            const errorMessage = `Required GPU number ${this.trialConfig.gpuNum} is too large, no machine can meet`;
            this.log.error(errorMessage);
            deferred.reject();
            throw new errors_1.NNIError(errors_1.NNIErrorNames.RESOURCE_NOT_AVAILABLE, errorMessage);
        }
        else if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.SUCCEED
            && rmScheduleResult.scheduleInfo !== undefined) {
            const rmScheduleInfo = rmScheduleResult.scheduleInfo;
            const trialWorkingFolder = path.join(this.remoteExpRootDir, 'trials', trialJobId);
            await this.launchTrialOnScheduledMachine(trialJobId, trialWorkingFolder, trialJobDetail.form, rmScheduleInfo);
            trialJobDetail.status = 'RUNNING';
            trialJobDetail.url = `file://${rmScheduleInfo.rmMeta.ip}:${trialWorkingFolder}`;
            trialJobDetail.startTime = Date.now();
            trialJobDetail.rmMeta = rmScheduleInfo.rmMeta;
            deferred.resolve(true);
        }
        else if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.TMP_NO_AVAILABLE_GPU) {
            this.log.info(`Right now no available GPU can be allocated for trial ${trialJobId}, will try to schedule later`);
            deferred.resolve(false);
        }
        else {
            deferred.reject(`Invalid schedule resutl type: ${rmScheduleResult.resultType}`);
        }
        return deferred.promise;
    }
    async launchTrialOnScheduledMachine(trialJobId, trialWorkingFolder, form, rmScheduleInfo) {
        if (!this.trialConfig) {
            throw new Error('trial config is not initialized');
        }
        const cuda_visible_device = rmScheduleInfo.cuda_visible_device;
        const sshClient = this.machineSSHClientMap.get(rmScheduleInfo.rmMeta);
        if (sshClient === undefined) {
            assert(false, 'sshClient is undefined.');
            return;
        }
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`Can not get trial job detail for job: ${trialJobId}`);
        }
        const trialLocalTempFolder = path.join(this.expRootDir, 'trials-local', trialJobId);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`mkdir -p ${trialWorkingFolder}`, sshClient);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`mkdir -p ${path.join(trialWorkingFolder, '.nni')}`, sshClient);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`touch ${path.join(trialWorkingFolder, '.nni', 'metrics')}`, sshClient);
        const runScriptContent = typescript_string_operations_1.String.Format(remoteMachineData_1.REMOTEMACHINE_RUN_SHELL_FORMAT, trialWorkingFolder, trialJobId, path.join(trialWorkingFolder, '.nni', 'jobpid'), (typeof cuda_visible_device === 'string' && cuda_visible_device.length > 0) ?
            `CUDA_VISIBLE_DEVICES=${cuda_visible_device} ` : `CUDA_VISIBLE_DEVICES=" " `, this.trialConfig.command, path.join(trialWorkingFolder, 'stderr'), path.join(trialWorkingFolder, '.nni', 'code'), this.isMultiPhase, trialJobDetail.sequenceId.toString());
        await cpp.exec(`mkdir -p ${path.join(trialLocalTempFolder, '.nni')}`);
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run.sh'), runScriptContent, { encoding: 'utf8' });
        await sshClientUtility_1.SSHClientUtility.copyFileToRemote(path.join(trialLocalTempFolder, 'run.sh'), path.join(trialWorkingFolder, 'run.sh'), sshClient);
        await this.writeParameterFile(trialJobId, form.hyperParameters, rmScheduleInfo.rmMeta);
        await sshClientUtility_1.SSHClientUtility.copyDirectoryToRemote(this.trialConfig.codeDir, trialWorkingFolder, sshClient, this.remoteOS);
        sshClientUtility_1.SSHClientUtility.remoteExeCommand(`bash ${path.join(trialWorkingFolder, 'run.sh')}`, sshClient);
    }
    async runHostJob(form) {
        const rmMeta = this.getRmMetaByHost(form.host);
        const sshClient = this.machineSSHClientMap.get(rmMeta);
        if (sshClient === undefined) {
            throw new Error('sshClient not found.');
        }
        const jobId = utils_1.uniqueString(5);
        const localDir = path.join(this.expRootDir, 'hostjobs-local', jobId);
        const remoteDir = this.getHostJobRemoteDir(jobId);
        await cpp.exec(`mkdir -p ${localDir}`);
        await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`mkdir -p ${remoteDir}`, sshClient);
        const runScriptContent = typescript_string_operations_1.String.Format(remoteMachineData_1.HOST_JOB_SHELL_FORMAT, remoteDir, path.join(remoteDir, 'jobpid'), form.cmd, path.join(remoteDir, 'code'));
        await fs.promises.writeFile(path.join(localDir, 'run.sh'), runScriptContent, { encoding: 'utf8' });
        await sshClientUtility_1.SSHClientUtility.copyFileToRemote(path.join(localDir, 'run.sh'), path.join(remoteDir, 'run.sh'), sshClient);
        sshClientUtility_1.SSHClientUtility.remoteExeCommand(`bash ${path.join(remoteDir, 'run.sh')}`, sshClient);
        const jobDetail = new remoteMachineData_1.RemoteMachineTrialJobDetail(jobId, 'RUNNING', Date.now(), remoteDir, form, this.generateSequenceId());
        jobDetail.rmMeta = rmMeta;
        jobDetail.startTime = Date.now();
        this.trialJobsMap.set(jobId, jobDetail);
        this.log.debug(`runHostJob: return: ${JSON.stringify(jobDetail)} `);
        return jobDetail;
    }
    getRmMetaByHost(host) {
        for (const [rmMeta, client] of this.machineSSHClientMap.entries()) {
            if (rmMeta.ip === host) {
                return rmMeta;
            }
        }
        throw new Error(`Host not found: ${host}`);
    }
    async updateTrialJobStatus(trialJob, sshClient) {
        const deferred = new ts_deferred_1.Deferred();
        const jobpidPath = this.getJobPidPath(trialJob.id);
        const trialReturnCodeFilePath = path.join(this.remoteExpRootDir, 'trials', trialJob.id, '.nni', 'code');
        try {
            const killResult = (await sshClientUtility_1.SSHClientUtility.remoteExeCommand(`kill -0 \`cat ${jobpidPath}\``, sshClient)).exitCode;
            if (killResult !== 0) {
                const trailReturnCode = await sshClientUtility_1.SSHClientUtility.getRemoteFileContent(trialReturnCodeFilePath, sshClient);
                this.log.debug(`trailjob ${trialJob.id} return code: ${trailReturnCode}`);
                const match = trailReturnCode.trim().match(/^(\d+)\s+(\d+)$/);
                if (match) {
                    const { 1: code, 2: timestamp } = match;
                    if (parseInt(code, 10) === 0) {
                        trialJob.status = 'SUCCEEDED';
                    }
                    else {
                        trialJob.status = 'FAILED';
                    }
                    trialJob.endTime = parseInt(timestamp, 10);
                }
                this.log.info(`trailJob status update: ${trialJob.id}, ${trialJob.status}`);
            }
            deferred.resolve(trialJob);
        }
        catch (error) {
            this.log.error(`Update job status exception, error is ${error.message}`);
            if (error instanceof errors_1.NNIError && error.name === errors_1.NNIErrorNames.NOT_FOUND) {
                deferred.resolve(trialJob);
            }
            else {
                trialJob.status = 'UNKNOWN';
                deferred.resolve(trialJob);
            }
        }
        return deferred.promise;
    }
    getRemoteScriptsPath() {
        return path.join(path.dirname(path.dirname(this.remoteExpRootDir)), 'scripts');
    }
    getHostJobRemoteDir(jobId) {
        return path.join(this.remoteExpRootDir, 'hostjobs', jobId);
    }
    getRemoteExperimentRootDir() {
        return path.join(utils_1.getRemoteTmpDir(this.remoteOS), 'nni', 'experiments', experimentStartupInfo_1.getExperimentId());
    }
    getJobPidPath(jobId) {
        const trialJobDetail = this.trialJobsMap.get(jobId);
        if (trialJobDetail === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.INVALID_JOB_DETAIL, `Invalid job detail information for trial job ${jobId}`);
        }
        let jobpidPath;
        if (trialJobDetail.form.jobType === 'TRIAL') {
            jobpidPath = path.join(trialJobDetail.workingDirectory, '.nni', 'jobpid');
        }
        else if (trialJobDetail.form.jobType === 'HOST') {
            jobpidPath = path.join(this.getHostJobRemoteDir(jobId), 'jobpid');
        }
        else {
            throw new Error(`Job type not supported: ${trialJobDetail.form.jobType}`);
        }
        return jobpidPath;
    }
    async writeParameterFile(trialJobId, hyperParameters, rmMeta) {
        const sshClient = this.machineSSHClientMap.get(rmMeta);
        if (sshClient === undefined) {
            throw new Error('sshClient is undefined.');
        }
        const trialWorkingFolder = path.join(this.remoteExpRootDir, 'trials', trialJobId);
        const trialLocalTempFolder = path.join(this.expRootDir, 'trials-local', trialJobId);
        const fileName = utils_1.generateParamFileName(hyperParameters);
        const localFilepath = path.join(trialLocalTempFolder, fileName);
        await fs.promises.writeFile(localFilepath, hyperParameters.value, { encoding: 'utf8' });
        await sshClientUtility_1.SSHClientUtility.copyFileToRemote(localFilepath, path.join(trialWorkingFolder, fileName), sshClient);
    }
    generateSequenceId() {
        if (this.trialSequenceId === -1) {
            this.trialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.trialSequenceId++;
    }
    async writeRemoteTrialFile(trialJobId, fileContent, rmMeta, fileName) {
        const sshClient = this.machineSSHClientMap.get(rmMeta);
        if (sshClient === undefined) {
            throw new Error('sshClient is undefined.');
        }
        const trialWorkingFolder = path.join(this.remoteExpRootDir, 'trials', trialJobId);
        const trialLocalTempFolder = path.join(this.expRootDir, 'trials-local', trialJobId);
        const localFilepath = path.join(trialLocalTempFolder, fileName);
        await fs.promises.writeFile(localFilepath, fileContent, { encoding: 'utf8' });
        await sshClientUtility_1.SSHClientUtility.copyFileToRemote(localFilepath, path.join(trialWorkingFolder, fileName), sshClient);
    }
};
RemoteMachineTrainingService = __decorate([
    __param(0, component.Inject),
    __metadata("design:paramtypes", [observableTimer_1.ObservableTimer])
], RemoteMachineTrainingService);
exports.RemoteMachineTrainingService = RemoteMachineTrainingService;
