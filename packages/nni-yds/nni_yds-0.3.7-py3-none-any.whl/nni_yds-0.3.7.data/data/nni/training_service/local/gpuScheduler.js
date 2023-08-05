'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const nodeNvidiaSmi = require("node-nvidia-smi");
const utils_1 = require("../../common/utils");
const gpuData_1 = require("../common/gpuData");
const log_1 = require("../../common/log");
class GPUScheduler {
    constructor() {
        this.stopping = false;
        this.log = log_1.getLogger();
        this.nvdmNotFoundRegex = /nvidia-smi: not found/gi;
    }
    async run() {
        while (!this.stopping) {
            try {
                this.gpuSummary = await this.readGPUSummary();
            }
            catch (error) {
                this.log.error('Read GPU summary failed with error: ', error);
                if (this.nvdmNotFoundRegex.test(error)) {
                    break;
                }
            }
            await utils_1.delay(5000);
        }
    }
    getAvailableGPUIndices() {
        if (this.gpuSummary !== undefined) {
            return this.gpuSummary.gpuInfos.filter((info) => info.activeProcessNum === 0).map((info) => info.index);
        }
        return [];
    }
    stop() {
        this.stopping = true;
    }
    generateEmbededGPUSummary(data) {
        let gpuInfos = [];
        const gpuNumber = parseInt(data.nvidia_smi_log.attached_gpus, 10);
        assert(gpuNumber > 0);
        if (gpuNumber == 1) {
            const embededGPUSummary = data.nvidia_smi_log.gpu;
            gpuInfos.push(this.convertGPUSummaryToInfo(embededGPUSummary));
        }
        else {
            const embededGPUSummaryArray = data.nvidia_smi_log.gpu;
            gpuInfos = embededGPUSummaryArray.map(embededGPUSummary => this.convertGPUSummaryToInfo(embededGPUSummary));
        }
        return gpuInfos;
    }
    convertGPUSummaryToInfo(embededGPUSummary) {
        return new gpuData_1.GPUInfo(typeof embededGPUSummary.process === 'object' ? 1 : 0, parseFloat(embededGPUSummary.utilization.memory_util), parseFloat(embededGPUSummary.utilization.gpu_util), parseInt(embededGPUSummary.minor_number, 10));
    }
    readGPUSummary() {
        return new Promise((resolve, reject) => {
            nodeNvidiaSmi((error, data) => {
                if (error) {
                    reject(error);
                }
                else {
                    const gpuNumber = parseInt(data.nvidia_smi_log.attached_gpus, 10);
                    const gpuSummary = new gpuData_1.GPUSummary(gpuNumber, Date().toString(), this.generateEmbededGPUSummary(data));
                    resolve(gpuSummary);
                }
            });
        });
    }
}
exports.GPUScheduler = GPUScheduler;
