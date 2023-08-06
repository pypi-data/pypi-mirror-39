'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const remoteMachineData_1 = require("./remoteMachineData");
class GPUScheduler {
    constructor(machineSSHClientMap) {
        this.log = log_1.getLogger();
        this.machineSSHClientMap = machineSSHClientMap;
    }
    scheduleMachine(requiredGPUNum, trialJobId) {
        assert(requiredGPUNum >= 0);
        const allRMs = Array.from(this.machineSSHClientMap.keys());
        assert(allRMs.length > 0);
        const eligibleRM = allRMs.filter((rmMeta) => rmMeta.gpuSummary === undefined || requiredGPUNum === 0 || rmMeta.gpuSummary.gpuCount >= requiredGPUNum);
        if (eligibleRM.length === 0) {
            return ({
                resultType: remoteMachineData_1.ScheduleResultType.REQUIRE_EXCEED_TOTAL,
                scheduleInfo: undefined
            });
        }
        if (requiredGPUNum > 0) {
            const result = this.scheduleGPUHost(requiredGPUNum, trialJobId);
            if (result !== undefined) {
                return result;
            }
        }
        else {
            const allocatedRm = this.selectMachine(allRMs);
            return this.allocateHost(requiredGPUNum, allocatedRm, [], trialJobId);
        }
        this.log.warning(`Scheduler: trialJob id ${trialJobId}, no machine can be scheduled, return TMP_NO_AVAILABLE_GPU `);
        return {
            resultType: remoteMachineData_1.ScheduleResultType.TMP_NO_AVAILABLE_GPU,
            scheduleInfo: undefined
        };
    }
    scheduleGPUHost(requiredGPUNum, trialJobId) {
        const totalResourceMap = this.gpuResourceDetection();
        const qualifiedRMs = [];
        totalResourceMap.forEach((gpuInfos, rmMeta) => {
            if (gpuInfos !== undefined && gpuInfos.length >= requiredGPUNum) {
                qualifiedRMs.push(rmMeta);
            }
        });
        if (qualifiedRMs.length > 0) {
            const allocatedRm = this.selectMachine(qualifiedRMs);
            const gpuInfos = totalResourceMap.get(allocatedRm);
            if (gpuInfos !== undefined) {
                return this.allocateHost(requiredGPUNum, allocatedRm, gpuInfos, trialJobId);
            }
            else {
                assert(false, 'gpuInfos is undefined');
            }
        }
    }
    gpuResourceDetection() {
        const totalResourceMap = new Map();
        this.machineSSHClientMap.forEach((client, rmMeta) => {
            if (rmMeta.gpuSummary !== undefined) {
                const availableGPUs = [];
                if (rmMeta.gpuReservation === undefined) {
                    rmMeta.gpuReservation = new Map();
                }
                rmMeta.gpuSummary.gpuInfos.forEach((gpuInfo) => {
                    if (gpuInfo.activeProcessNum === 0 && !rmMeta.gpuReservation.has(gpuInfo.index)) {
                        availableGPUs.push(gpuInfo);
                    }
                });
                totalResourceMap.set(rmMeta, availableGPUs);
            }
        });
        return totalResourceMap;
    }
    selectMachine(rmMetas) {
        assert(rmMetas !== undefined && rmMetas.length > 0);
        return utils_1.randomSelect(rmMetas);
    }
    selectGPUsForTrial(gpuInfos, requiredGPUNum) {
        return gpuInfos.slice(0, requiredGPUNum);
    }
    allocateHost(requiredGPUNum, rmMeta, gpuInfos, trialJobId) {
        assert(gpuInfos.length >= requiredGPUNum);
        const allocatedGPUs = this.selectGPUsForTrial(gpuInfos, requiredGPUNum);
        allocatedGPUs.forEach((gpuInfo) => {
            rmMeta.gpuReservation.set(gpuInfo.index, trialJobId);
        });
        return {
            resultType: remoteMachineData_1.ScheduleResultType.SUCCEED,
            scheduleInfo: {
                rmMeta: rmMeta,
                cuda_visible_device: allocatedGPUs.map((gpuInfo) => { return gpuInfo.index; }).join(',')
            }
        };
    }
}
exports.GPUScheduler = GPUScheduler;
