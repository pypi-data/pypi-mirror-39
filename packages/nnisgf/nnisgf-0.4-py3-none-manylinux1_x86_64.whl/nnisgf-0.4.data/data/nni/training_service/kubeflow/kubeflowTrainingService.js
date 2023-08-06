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
const assert = require("assert");
const component = require("../../common/component");
const cpp = require("child-process-promise");
const fs = require("fs");
const path = require("path");
const containerJobData_1 = require("../common/containerJobData");
const events_1 = require("events");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const utils_1 = require("../../common/utils");
const kubeflowConfig_1 = require("./kubeflowConfig");
const kubeflowData_1 = require("./kubeflowData");
const kubeflowJobRestServer_1 = require("./kubeflowJobRestServer");
const kubeflowJobInfoCollector_1 = require("./kubeflowJobInfoCollector");
const util_1 = require("../common/util");
const azureStorageClientUtils_1 = require("./azureStorageClientUtils");
const kubernetesApiClient_1 = require("./kubernetesApiClient");
var azure = require('azure-storage');
var base64 = require('js-base64').Base64;
let KubeflowTrainingService = class KubeflowTrainingService {
    constructor() {
        this.NNI_KUBEFLOW_TRIAL_LABEL = 'nni-kubeflow-trial';
        this.stopping = false;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.genericK8sClient = new kubernetesApiClient_1.GeneralK8sClient();
        this.kubeflowJobInfoCollector = new kubeflowJobInfoCollector_1.KubeflowJobInfoCollector(this.trialJobsMap);
        this.trialLocalNFSTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-nfs-tmp');
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.nextTrialSequenceId = -1;
        this.CONTAINER_MOUNT_PATH = '/tmp/mount';
    }
    async run() {
        const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
        await restServer.start();
        this.log.info(`Kubeflow Training service rest server listening on: ${restServer.endPoint}`);
        while (!this.stopping) {
            await utils_1.delay(3000);
            await this.kubeflowJobInfoCollector.retrieveTrialStatus(this.operatorClient);
        }
    }
    async submitTrialJob(form) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        if (!this.operatorClient) {
            throw new Error('Kubeflow job operator client is undefined');
        }
        if (!this.kubeflowRestServerPort) {
            const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
            this.kubeflowRestServerPort = restServer.clusterRestServerPort;
        }
        let kubeflowTrialConfig;
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else {
            throw Error(`operator ${this.kubeflowClusterConfig.operator} is invalid`);
        }
        const trialJobId = utils_1.uniqueString(5);
        const curTrialSequenceId = this.generateSequenceId();
        const trialWorkingFolder = path.join(this.CONTAINER_MOUNT_PATH, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId);
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await cpp.exec(`mkdir -p ${path.dirname(trialLocalTempFolder)}`);
        await cpp.exec(`cp -r ${kubeflowTrialConfig.codeDir} ${trialLocalTempFolder}`);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        await cpp.exec(`mkdir -p ${trialLocalTempFolder}`);
        if (kubeflowTrialConfig.worker) {
            const workerRunScriptContent = this.generateRunScript(trialJobId, trialWorkingFolder, kubeflowTrialConfig.worker.command, curTrialSequenceId.toString(), 'worker', kubeflowTrialConfig.worker.gpuNum);
            await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_worker.sh'), workerRunScriptContent, { encoding: 'utf8' });
        }
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            if (tensorflowTrialConfig.ps) {
                const psRunScriptContent = this.generateRunScript(trialJobId, trialWorkingFolder, tensorflowTrialConfig.ps.command, curTrialSequenceId.toString(), 'ps', tensorflowTrialConfig.ps.gpuNum);
                await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_ps.sh'), psRunScriptContent, { encoding: 'utf8' });
            }
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            let pytorchTrialConfig = this.kubeflowTrialConfig;
            if (pytorchTrialConfig.master) {
                const masterRunScriptContent = this.generateRunScript(trialJobId, trialWorkingFolder, pytorchTrialConfig.master.command, curTrialSequenceId.toString(), 'master', pytorchTrialConfig.master.gpuNum);
                await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_master.sh'), masterRunScriptContent, { encoding: 'utf8' });
            }
        }
        const trialForm = form;
        if (trialForm && trialForm.hyperParameters) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
        const kubeflowJobName = `nni-exp-${this.experimentId}-trial-${trialJobId}`.toLowerCase();
        const workerPodResources = {};
        if (kubeflowTrialConfig.worker) {
            workerPodResources.requests = this.generatePodResource(kubeflowTrialConfig.worker.memoryMB, kubeflowTrialConfig.worker.cpuNum, kubeflowTrialConfig.worker.gpuNum);
        }
        workerPodResources.limits = Object.assign({}, workerPodResources.requests);
        let nonWorkerResources = {};
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            if (tensorflowTrialConfig.ps) {
                nonWorkerResources.requests = this.generatePodResource(tensorflowTrialConfig.ps.memoryMB, tensorflowTrialConfig.ps.cpuNum, tensorflowTrialConfig.ps.gpuNum);
                nonWorkerResources.limits = Object.assign({}, nonWorkerResources.requests);
            }
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            let pyTorchTrialConfig = this.kubeflowTrialConfig;
            nonWorkerResources.requests = this.generatePodResource(pyTorchTrialConfig.master.memoryMB, pyTorchTrialConfig.master.cpuNum, pyTorchTrialConfig.master.gpuNum);
            nonWorkerResources.limits = Object.assign({}, nonWorkerResources.requests);
        }
        let trialJobOutputUrl = '';
        assert(!this.kubeflowClusterConfig.storage
            || this.kubeflowClusterConfig.storage === 'azureStorage'
            || this.kubeflowClusterConfig.storage === 'nfs');
        if (this.kubeflowClusterConfig.storage === 'azureStorage') {
            try {
                await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${trialLocalTempFolder}`);
                trialJobOutputUrl = `https://${this.azureStorageAccountName}.file.core.windows.net/${this.azureStorageShare}/${path.join('nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
            }
            catch (error) {
                this.log.error(error);
                return Promise.reject(error);
            }
        }
        else if (this.kubeflowClusterConfig.storage === 'nfs' || this.kubeflowClusterConfig.storage === undefined) {
            let nfsKubeflowClusterConfig = this.kubeflowClusterConfig;
            await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`);
            await cpp.exec(`cp -r ${trialLocalTempFolder}/* ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}/.`);
            const nfsConfig = nfsKubeflowClusterConfig.nfs;
            trialJobOutputUrl = `nfs://${nfsConfig.server}:${path.join(nfsConfig.path, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
        }
        const trialJobDetail = new kubeflowData_1.KubeflowTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form, kubeflowJobName, curTrialSequenceId, trialJobOutputUrl);
        const kubeflowJobConfig = this.generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, nonWorkerResources);
        await this.operatorClient.createKubeflowJob(kubeflowJobConfig);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        return Promise.resolve(trialJobDetail);
    }
    generatePodResource(memory, cpuNum, gpuNum) {
        return {
            'memory': `${memory}Mi`,
            'cpu': `${cpuNum}`,
            'nvidia.com/gpu': `${gpuNum}`
        };
    }
    updateTrialJob(trialJobId, form) {
        throw new errors_1.MethodNotImplementedError();
    }
    listTrialJobs() {
        const jobs = [];
        this.trialJobsMap.forEach(async (value, key) => {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        });
        return Promise.resolve(jobs);
    }
    getTrialJob(trialJobId) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        const kubeflowTrialJob = this.trialJobsMap.get(trialJobId);
        if (!kubeflowTrialJob) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(kubeflowTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (!trialJobDetail) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} not found`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        if (!this.operatorClient) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} failed because operatorClient is undefined`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        try {
            await this.operatorClient.deleteKubeflowJob(new Map([
                ['app', this.NNI_KUBEFLOW_TRIAL_LABEL],
                ['expId', experimentStartupInfo_1.getExperimentId()],
                ['trialId', trialJobId]
            ]));
        }
        catch (err) {
            const errorMessage = `Delete trial ${trialJobId} failed: ${err}`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        trialJobDetail.endTime = Date.now();
        trialJobDetail.status = utils_1.getJobCancelStatus(isEarlyStopped);
        return Promise.resolve();
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.KUBEFLOW_CLUSTER_CONFIG:
                let kubeflowClusterJsonObject = JSON.parse(value);
                let kubeflowClusterConfigBase = new kubeflowConfig_1.KubeflowClusterConfigBase(kubeflowClusterJsonObject.operator, kubeflowClusterJsonObject.apiVersion, kubeflowClusterJsonObject.storage);
                if (kubeflowClusterConfigBase && kubeflowClusterConfigBase.storage === 'azureStorage') {
                    const azureKubeflowClusterConfig = new kubeflowConfig_1.KubeflowClusterConfigAzure(kubeflowClusterJsonObject.operator, kubeflowClusterJsonObject.apiVersion, kubeflowClusterJsonObject.keyVault, kubeflowClusterJsonObject.azureStorage, kubeflowClusterJsonObject.storage);
                    const vaultName = azureKubeflowClusterConfig.keyVault.vaultName;
                    const valutKeyName = azureKubeflowClusterConfig.keyVault.name;
                    this.azureStorageAccountName = azureKubeflowClusterConfig.azureStorage.accountName;
                    this.azureStorageShare = azureKubeflowClusterConfig.azureStorage.azureShare;
                    try {
                        const result = await cpp.exec(`az keyvault secret show --name ${valutKeyName} --vault-name ${vaultName}`);
                        if (result.stderr) {
                            const errorMessage = result.stderr;
                            this.log.error(errorMessage);
                            return Promise.reject(errorMessage);
                        }
                        const storageAccountKey = JSON.parse(result.stdout).value;
                        this.azureStorageClient = azure.createFileService(this.azureStorageAccountName, storageAccountKey);
                        await azureStorageClientUtils_1.AzureStorageClientUtility.createShare(this.azureStorageClient, this.azureStorageShare);
                        this.azureStorageSecretName = 'nni-secret-' + utils_1.uniqueString(8).toLowerCase();
                        await this.genericK8sClient.createSecret({
                            apiVersion: 'v1',
                            kind: 'Secret',
                            metadata: {
                                name: this.azureStorageSecretName,
                                namespace: 'default',
                                labels: {
                                    app: this.NNI_KUBEFLOW_TRIAL_LABEL,
                                    expId: experimentStartupInfo_1.getExperimentId()
                                }
                            },
                            type: 'Opaque',
                            data: {
                                azurestorageaccountname: base64.encode(this.azureStorageAccountName),
                                azurestorageaccountkey: base64.encode(storageAccountKey)
                            }
                        });
                    }
                    catch (error) {
                        this.log.error(error);
                        throw new Error(error);
                    }
                    this.kubeflowClusterConfig = azureKubeflowClusterConfig;
                }
                else if (kubeflowClusterConfigBase && (kubeflowClusterConfigBase.storage === 'nfs' || kubeflowClusterConfigBase.storage === undefined)) {
                    const nfsKubeflowClusterConfig = new kubeflowConfig_1.KubeflowClusterConfigNFS(kubeflowClusterJsonObject.operator, kubeflowClusterJsonObject.apiVersion, kubeflowClusterJsonObject.nfs, kubeflowClusterJsonObject.storage);
                    await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}`);
                    const nfsServer = nfsKubeflowClusterConfig.nfs.server;
                    const nfsPath = nfsKubeflowClusterConfig.nfs.path;
                    try {
                        await cpp.exec(`sudo mount ${nfsServer}:${nfsPath} ${this.trialLocalNFSTempFolder}`);
                    }
                    catch (error) {
                        const mountError = `Mount NFS ${nfsServer}:${nfsPath} to ${this.trialLocalNFSTempFolder} failed, error is ${error}`;
                        this.log.error(mountError);
                        throw new Error(mountError);
                    }
                    this.kubeflowClusterConfig = nfsKubeflowClusterConfig;
                }
                else {
                    const error = `kubeflowClusterConfig format error!`;
                    this.log.error(error);
                    throw new Error(error);
                }
                this.operatorClient = kubernetesApiClient_1.KubeflowOperatorClient.generateOperatorClient(this.kubeflowClusterConfig.operator, this.kubeflowClusterConfig.apiVersion);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (!this.kubeflowClusterConfig) {
                    this.log.error('kubeflow cluster config is not initialized');
                    return Promise.reject(new Error('kubeflow cluster config is not initialized'));
                }
                assert(this.kubeflowClusterConfig !== undefined);
                let kubeflowTrialJsonObjsect = JSON.parse(value);
                if (this.kubeflowClusterConfig.operator === 'tf-operator') {
                    this.kubeflowTrialConfig = new kubeflowConfig_1.KubeflowTrialConfigTensorflow(kubeflowTrialJsonObjsect.codeDir, kubeflowTrialJsonObjsect.worker, kubeflowTrialJsonObjsect.ps);
                }
                else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
                    this.kubeflowTrialConfig = new kubeflowConfig_1.KubeflowTrialConfigPytorch(kubeflowTrialJsonObjsect.codeDir, kubeflowTrialJsonObjsect.master, kubeflowTrialJsonObjsect.worker);
                }
                if (!this.kubeflowTrialConfig) {
                    this.log.error('kubeflow kubeflow TrialConfig is not initialized');
                    return Promise.reject(new Error('kubeflow kubeflow TrialConfig is not initialized'));
                }
                try {
                    await util_1.validateCodeDir(this.kubeflowTrialConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    return Promise.reject(new Error(error));
                }
                break;
            default:
                break;
        }
        return Promise.resolve();
    }
    getClusterMetadata(key) {
        return Promise.resolve('');
    }
    async cleanUp() {
        this.stopping = true;
        for (let [trialJobId, kubeflowTrialJob] of this.trialJobsMap) {
            if (['RUNNING', 'WAITING', 'UNKNOWN'].includes(kubeflowTrialJob.status)) {
                try {
                    await this.cancelTrialJob(trialJobId);
                }
                catch (error) { }
                kubeflowTrialJob.status = 'SYS_CANCELED';
            }
        }
        try {
            if (this.operatorClient) {
                await this.operatorClient.deleteKubeflowJob(new Map([
                    ['app', this.NNI_KUBEFLOW_TRIAL_LABEL],
                    ['expId', experimentStartupInfo_1.getExperimentId()]
                ]));
            }
        }
        catch (error) {
            this.log.error(`Delete kubeflow job with label: app=${this.NNI_KUBEFLOW_TRIAL_LABEL},expId=${experimentStartupInfo_1.getExperimentId()} failed, error is ${error}`);
        }
        try {
            await cpp.exec(`sudo umount ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            this.log.error(`Unmount ${this.trialLocalNFSTempFolder} failed, error is ${error}`);
        }
        const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
        try {
            await restServer.stop();
            this.log.info('Kubeflow Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`Kubeflow Training service rest server stopped failed, error: ${error.message}`);
            Promise.reject(error);
        }
        return Promise.resolve();
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, nonWorkerPodResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        if (!this.operatorClient) {
            throw new Error('Kubeflow operator client is not initialized');
        }
        const replicaSpecsObj = {};
        let replicaSpecsObjMap = new Map();
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            replicaSpecsObj.Worker = this.generateReplicaConfig(trialWorkingFolder, tensorflowTrialConfig.worker.replicas, tensorflowTrialConfig.worker.image, 'run_worker.sh', workerPodResources);
            if (tensorflowTrialConfig.ps) {
                replicaSpecsObj.Ps = this.generateReplicaConfig(trialWorkingFolder, tensorflowTrialConfig.ps.replicas, tensorflowTrialConfig.ps.image, 'run_ps.sh', nonWorkerPodResources);
            }
            replicaSpecsObjMap.set(this.operatorClient.jobKind, { 'tfReplicaSpecs': replicaSpecsObj });
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            let pytorchTrialConfig = this.kubeflowTrialConfig;
            if (pytorchTrialConfig.worker) {
                replicaSpecsObj.Worker = this.generateReplicaConfig(trialWorkingFolder, pytorchTrialConfig.worker.replicas, pytorchTrialConfig.worker.image, 'run_worker.sh', workerPodResources);
            }
            replicaSpecsObj.Master = this.generateReplicaConfig(trialWorkingFolder, pytorchTrialConfig.master.replicas, pytorchTrialConfig.master.image, 'run_master.sh', nonWorkerPodResources);
            replicaSpecsObjMap.set(this.operatorClient.jobKind, { 'pytorchReplicaSpecs': replicaSpecsObj });
        }
        return {
            apiVersion: `kubeflow.org/${this.operatorClient.apiVersion}`,
            kind: this.operatorClient.jobKind,
            metadata: {
                name: kubeflowJobName,
                namespace: 'default',
                labels: {
                    app: this.NNI_KUBEFLOW_TRIAL_LABEL,
                    expId: experimentStartupInfo_1.getExperimentId(),
                    trialId: trialJobId
                }
            },
            spec: replicaSpecsObjMap.get(this.operatorClient.jobKind)
        };
    }
    generateReplicaConfig(trialWorkingFolder, replicaNumber, replicaImage, runScriptFile, podResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        if (!this.operatorClient) {
            throw new Error('Kubeflow operator client is not initialized');
        }
        let volumeSpecMap = new Map();
        if (this.kubeflowClusterConfig.storage && this.kubeflowClusterConfig.storage === 'azureStorage') {
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    azureFile: {
                        secretName: `${this.azureStorageSecretName}`,
                        shareName: `${this.azureStorageShare}`,
                        readonly: false
                    }
                }
            ]);
        }
        else {
            let nfsKubeflowClusterConfig = this.kubeflowClusterConfig;
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    nfs: {
                        server: `${nfsKubeflowClusterConfig.nfs.server}`,
                        path: `${nfsKubeflowClusterConfig.nfs.path}`
                    }
                }
            ]);
        }
        return {
            replicas: replicaNumber,
            template: {
                metadata: {
                    creationTimestamp: null
                },
                spec: {
                    containers: [
                        {
                            name: this.operatorClient.containerName,
                            image: replicaImage,
                            args: ["sh", `${path.join(trialWorkingFolder, runScriptFile)}`],
                            volumeMounts: [
                                {
                                    name: 'nni-vol',
                                    mountPath: this.CONTAINER_MOUNT_PATH
                                }
                            ],
                            resources: podResources
                        }
                    ],
                    restartPolicy: 'ExitCode',
                    volumes: volumeSpecMap.get('nniVolumes')
                }
            }
        };
    }
    generateRunScript(trialJobId, trialWorkingFolder, command, trialSequenceId, roleType, gpuNum) {
        const runScriptLines = [];
        runScriptLines.push('#!/bin/bash');
        runScriptLines.push('export NNI_PLATFORM=kubeflow');
        runScriptLines.push(`export NNI_SYS_DIR=$PWD/nni/${trialJobId}`);
        runScriptLines.push(`export NNI_OUTPUT_DIR=${path.join(trialWorkingFolder, 'output', `${roleType}_output`)}`);
        runScriptLines.push('export MULTI_PHASE=false');
        runScriptLines.push(`export NNI_TRIAL_JOB_ID=${trialJobId}`);
        runScriptLines.push(`export NNI_EXP_ID=${experimentStartupInfo_1.getExperimentId()}`);
        runScriptLines.push(`export NNI_CODE_DIR=${trialWorkingFolder}`);
        runScriptLines.push(`export NNI_TRIAL_SEQ_ID=${trialSequenceId}`);
        if (gpuNum === 0) {
            runScriptLines.push(`export CUDA_VISIBLE_DEVICES=''`);
        }
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        runScriptLines.push('mkdir -p $NNI_SYS_DIR');
        runScriptLines.push('mkdir -p $NNI_OUTPUT_DIR');
        runScriptLines.push('cp -rT $NNI_CODE_DIR $NNI_SYS_DIR');
        runScriptLines.push('cd $NNI_SYS_DIR');
        runScriptLines.push('sh install_nni.sh # Check and install NNI pkg');
        runScriptLines.push(`python3 -m nni_trial_tool.trial_keeper --trial_command '${command}' `
            + `--nnimanager_ip '${nniManagerIp}' --nnimanager_port '${this.kubeflowRestServerPort}' `
            + `1>$NNI_OUTPUT_DIR/trialkeeper_stdout 2>$NNI_OUTPUT_DIR/trialkeeper_stderr`);
        return runScriptLines.join('\n');
    }
    generateSequenceId() {
        if (this.nextTrialSequenceId === -1) {
            this.nextTrialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.nextTrialSequenceId++;
    }
};
KubeflowTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], KubeflowTrainingService);
exports.KubeflowTrainingService = KubeflowTrainingService;
