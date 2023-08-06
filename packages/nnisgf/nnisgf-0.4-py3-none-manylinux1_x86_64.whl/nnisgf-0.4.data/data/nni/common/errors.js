'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
var NNIErrorNames;
(function (NNIErrorNames) {
    NNIErrorNames.NOT_FOUND = 'NOT_FOUND';
    NNIErrorNames.INVALID_JOB_DETAIL = 'NO_VALID_JOB_DETAIL_FOUND';
    NNIErrorNames.RESOURCE_NOT_AVAILABLE = 'RESOURCE_NOT_AVAILABLE';
})(NNIErrorNames = exports.NNIErrorNames || (exports.NNIErrorNames = {}));
class NNIError extends Error {
    constructor(name, message, err) {
        super(message);
        this.name = name;
        if (err !== undefined) {
            this.stack = err.stack;
        }
    }
}
exports.NNIError = NNIError;
class MethodNotImplementedError extends Error {
    constructor() {
        super('Method not implemented.');
    }
}
exports.MethodNotImplementedError = MethodNotImplementedError;
