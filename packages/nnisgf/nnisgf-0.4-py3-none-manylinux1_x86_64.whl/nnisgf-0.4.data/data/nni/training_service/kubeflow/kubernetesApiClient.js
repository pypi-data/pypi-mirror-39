'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const os = require("os");
const path = require("path");
const log_1 = require("../../common/log");
var K8SClient = require('kubernetes-client').Client;
var K8SConfig = require('kubernetes-client').config;
class GeneralK8sClient {
    constructor() {
        this.log = log_1.getLogger();
        this.client = new K8SClient({ config: K8SConfig.fromKubeconfig(path.join(os.homedir(), '.kube', 'config')), version: '1.9' });
        this.client.loadSpec();
    }
    async createSecret(secretManifest) {
        let result;
        const response = await this.client.api.v1.namespaces('default').secrets.post({ body: secretManifest });
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(true);
        }
        else {
            result = Promise.reject(`Create secrets failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
}
exports.GeneralK8sClient = GeneralK8sClient;
class KubeflowOperatorClient {
    constructor() {
        this.log = log_1.getLogger();
        this.client = new K8SClient({ config: K8SConfig.fromKubeconfig(path.join(os.homedir(), '.kube', 'config')) });
        this.client.loadSpec();
    }
    static generateOperatorClient(kubeflowOperator, operatorApiVersion) {
        if (kubeflowOperator === 'tf-operator') {
            if (operatorApiVersion == 'v1alpha2') {
                return new TFOperatorClientV1Alpha2();
            }
            else if (operatorApiVersion == 'v1beta1') {
                return new TFOperatorClientV1Beta1();
            }
        }
        else if (kubeflowOperator === 'pytorch-operator') {
            if (operatorApiVersion == 'v1alpha2') {
                return new PytorchOperatorClientV1Alpha2();
            }
            else if (operatorApiVersion == 'v1beta1') {
                return new PytorchOperatorClientV1Beta1();
            }
        }
        throw new Error(`Invalid operator ${kubeflowOperator} or apiVersion ${operatorApiVersion}`);
    }
    get jobKind() {
        if (this.crdSchema
            && this.crdSchema.spec
            && this.crdSchema.spec.names
            && this.crdSchema.spec.names.kind) {
            return this.crdSchema.spec.names.kind;
        }
        else {
            throw new Error('KubeflowOperatorClient: getJobKind failed, kind is undefined in crd schema!');
        }
    }
    get apiVersion() {
        if (this.crdSchema
            && this.crdSchema.spec
            && this.crdSchema.spec.version) {
            return this.crdSchema.spec.version;
        }
        else {
            throw new Error('KubeflowOperatorClient: get apiVersion failed, version is undefined in crd schema!');
        }
    }
    async createKubeflowJob(jobManifest) {
        let result;
        const response = await this.operator.post({ body: jobManifest });
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(true);
        }
        else {
            result = Promise.reject(`KubeflowOperatorClient create tfjobs failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
    async getKubeflowJob(kubeflowJobName) {
        let result;
        const response = await this.operator(kubeflowJobName).get();
        if (response.statusCode && (response.statusCode >= 200 && response.statusCode <= 299)) {
            result = Promise.resolve(response.body);
        }
        else {
            result = Promise.reject(`KubeflowOperatorClient get tfjobs failed, statusCode is ${response.statusCode}`);
        }
        return result;
    }
    async deleteKubeflowJob(labels) {
        let result;
        const matchQuery = Array.from(labels.keys()).map(labelKey => `${labelKey}=${labels.get(labelKey)}`).join(',');
        try {
            const deleteResult = await this.operator().delete({ qs: { labelSelector: matchQuery } });
            if (deleteResult.statusCode && deleteResult.statusCode >= 200 && deleteResult.statusCode <= 299) {
                result = Promise.resolve(true);
            }
            else {
                result = Promise.reject(`KubeflowOperatorClient, delete labels ${matchQuery} get wrong statusCode ${deleteResult.statusCode}`);
            }
        }
        catch (err) {
            result = Promise.reject(err);
        }
        return result;
    }
}
exports.KubeflowOperatorClient = KubeflowOperatorClient;
class TFOperatorClientV1Alpha2 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/tfjob-crd-v1alpha2.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1alpha2.namespaces('default').tfjobs;
    }
    get containerName() {
        return 'tensorflow';
    }
}
class TFOperatorClientV1Beta1 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/tfjob-crd-v1beta1.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1beta1.namespaces('default').tfjobs;
    }
    get containerName() {
        return 'tensorflow';
    }
}
class PytorchOperatorClientV1Alpha2 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/pytorchjob-crd-v1alpha2.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1alpha2.namespaces('default').pytorchjobs;
    }
    get containerName() {
        return 'pytorch';
    }
}
class PytorchOperatorClientV1Beta1 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/pytorchjob-crd-v1beta1.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1beta1.namespaces('default').pytorchjobs;
    }
    get containerName() {
        return 'pytorch';
    }
}
