'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const gpuScheduler_1 = require("./gpuScheduler");
const localTrainingService_1 = require("./localTrainingService");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
class LocalTrainingServiceForGPU extends localTrainingService_1.LocalTrainingService {
    constructor() {
        super();
        this.availableGPUIndices = Array(16).fill(false);
    }
    async run() {
        if (this.gpuScheduler !== undefined) {
            await Promise.all([
                this.gpuScheduler.run(),
                super.run()
            ]);
        }
        else {
            await super.run();
        }
    }
    async setClusterMetadata(key, value) {
        await super.setClusterMetadata(key, value);
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (this.localTrailConfig !== undefined) {
                    this.requiredGPUNum = this.localTrailConfig.gpuNum;
                }
                else {
                    this.requiredGPUNum = 0;
                }
                this.log.info('required GPU number is ' + this.requiredGPUNum);
                if (this.gpuScheduler === undefined && this.requiredGPUNum > 0) {
                    this.gpuScheduler = new gpuScheduler_1.GPUScheduler();
                }
                break;
            default:
        }
    }
    cleanUp() {
        if (this.gpuScheduler !== undefined) {
            this.gpuScheduler.stop();
        }
        return super.cleanUp();
    }
    onTrialJobStatusChanged(trialJob, oldStatus) {
        if (trialJob.gpuIndices !== undefined && trialJob.gpuIndices.length !== 0 && this.gpuScheduler !== undefined) {
            if (oldStatus === 'RUNNING' && trialJob.status !== 'RUNNING') {
                for (const index of trialJob.gpuIndices) {
                    this.availableGPUIndices[index] = false;
                }
            }
        }
    }
    getEnvironmentVariables(trialJobDetail, resource) {
        const variables = super.getEnvironmentVariables(trialJobDetail, resource);
        variables.push({
            key: 'CUDA_VISIBLE_DEVICES',
            value: this.gpuScheduler === undefined ? '' : resource.gpuIndices.join(',')
        });
        return variables;
    }
    setExtraProperties(trialJobDetail, resource) {
        super.setExtraProperties(trialJobDetail, resource);
        trialJobDetail.gpuIndices = resource.gpuIndices;
    }
    tryGetAvailableResource() {
        const [success, resource] = super.tryGetAvailableResource();
        if (!success || this.gpuScheduler === undefined) {
            return [success, resource];
        }
        const availableGPUIndices = this.gpuScheduler.getAvailableGPUIndices();
        const selectedGPUIndices = availableGPUIndices.filter((index) => this.availableGPUIndices[index] === false);
        if (selectedGPUIndices.length < this.requiredGPUNum) {
            return [false, resource];
        }
        selectedGPUIndices.splice(this.requiredGPUNum);
        Object.assign(resource, { gpuIndices: selectedGPUIndices });
        return [true, resource];
    }
    occupyResource(resource) {
        super.occupyResource(resource);
        if (this.gpuScheduler !== undefined) {
            for (const index of resource.gpuIndices) {
                this.availableGPUIndices[index] = true;
            }
        }
    }
}
exports.LocalTrainingServiceForGPU = LocalTrainingServiceForGPU;
