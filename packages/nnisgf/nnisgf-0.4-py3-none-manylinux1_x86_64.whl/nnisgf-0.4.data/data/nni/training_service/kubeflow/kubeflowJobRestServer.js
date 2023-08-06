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
const component = require("../../common/component");
const typescript_ioc_1 = require("typescript-ioc");
const kubeflowTrainingService_1 = require("./kubeflowTrainingService");
const clusterJobRestServer_1 = require("../common/clusterJobRestServer");
let KubeflowJobRestServer = class KubeflowJobRestServer extends clusterJobRestServer_1.ClusterJobRestServer {
    constructor() {
        super();
        this.kubeflowTrainingService = component.get(kubeflowTrainingService_1.KubeflowTrainingService);
    }
    handleTrialMetrics(jobId, metrics) {
        for (const singleMetric of metrics) {
            this.kubeflowTrainingService.MetricsEmitter.emit('metric', {
                id: jobId,
                data: singleMetric
            });
        }
    }
};
__decorate([
    typescript_ioc_1.Inject,
    __metadata("design:type", kubeflowTrainingService_1.KubeflowTrainingService)
], KubeflowJobRestServer.prototype, "kubeflowTrainingService", void 0);
KubeflowJobRestServer = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], KubeflowJobRestServer);
exports.KubeflowJobRestServer = KubeflowJobRestServer;
