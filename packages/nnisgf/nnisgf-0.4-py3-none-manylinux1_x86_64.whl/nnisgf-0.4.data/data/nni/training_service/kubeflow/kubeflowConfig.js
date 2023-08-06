'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class KubeflowClusterConfigBase {
    constructor(operator, apiVersion, storage) {
        this.operator = operator;
        this.apiVersion = apiVersion;
        this.storage = storage;
    }
}
exports.KubeflowClusterConfigBase = KubeflowClusterConfigBase;
class KubeflowClusterConfigNFS extends KubeflowClusterConfigBase {
    constructor(operator, apiVersion, nfs, storage) {
        super(operator, apiVersion, storage);
        this.nfs = nfs;
    }
}
exports.KubeflowClusterConfigNFS = KubeflowClusterConfigNFS;
class KubeflowClusterConfigAzure extends KubeflowClusterConfigBase {
    constructor(operator, apiVersion, keyVault, azureStorage, storage) {
        super(operator, apiVersion, storage);
        this.keyVault = keyVault;
        this.azureStorage = azureStorage;
    }
}
exports.KubeflowClusterConfigAzure = KubeflowClusterConfigAzure;
class NFSConfig {
    constructor(server, path) {
        this.server = server;
        this.path = path;
    }
}
exports.NFSConfig = NFSConfig;
class keyVaultConfig {
    constructor(vaultName, name) {
        this.vaultName = vaultName;
        this.name = name;
    }
}
exports.keyVaultConfig = keyVaultConfig;
class AzureStorage {
    constructor(azureShare, accountName) {
        this.azureShare = azureShare;
        this.accountName = accountName;
    }
}
exports.AzureStorage = AzureStorage;
class KubeflowTrialConfigTemplate {
    constructor(replicas, command, gpuNum, cpuNum, memoryMB, image) {
        this.replicas = replicas;
        this.command = command;
        this.gpuNum = gpuNum;
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
    }
}
exports.KubeflowTrialConfigTemplate = KubeflowTrialConfigTemplate;
class KubeflowTrialConfigBase {
    constructor(codeDir) {
        this.codeDir = codeDir;
    }
}
exports.KubeflowTrialConfigBase = KubeflowTrialConfigBase;
class KubeflowTrialConfigTensorflow extends KubeflowTrialConfigBase {
    constructor(codeDir, worker, ps) {
        super(codeDir);
        this.ps = ps;
        this.worker = worker;
    }
}
exports.KubeflowTrialConfigTensorflow = KubeflowTrialConfigTensorflow;
class KubeflowTrialConfigPytorch extends KubeflowTrialConfigBase {
    constructor(codeDir, master, worker) {
        super(codeDir);
        this.master = master;
        this.worker = worker;
    }
}
exports.KubeflowTrialConfigPytorch = KubeflowTrialConfigPytorch;
