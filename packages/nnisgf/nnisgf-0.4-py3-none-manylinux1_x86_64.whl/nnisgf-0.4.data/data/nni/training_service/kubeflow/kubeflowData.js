'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class KubeflowTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form, kubeflowJobName, sequenceId, url) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.kubeflowJobName = kubeflowJobName;
        this.sequenceId = sequenceId;
        this.tags = [];
        this.queryJobFailedCount = 0;
        this.url = url;
    }
}
exports.KubeflowTrialJobDetail = KubeflowTrialJobDetail;
