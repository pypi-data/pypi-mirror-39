'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class GPUInfo {
    constructor(activeProcessNum, gpuMemUtil, gpuUtil, index) {
        this.activeProcessNum = activeProcessNum;
        this.gpuMemUtil = gpuMemUtil;
        this.gpuUtil = gpuUtil;
        this.index = index;
    }
}
exports.GPUInfo = GPUInfo;
class GPUSummary {
    constructor(gpuCount, timestamp, gpuInfos) {
        this.gpuCount = gpuCount;
        this.timestamp = timestamp;
        this.gpuInfos = gpuInfos;
    }
}
exports.GPUSummary = GPUSummary;
