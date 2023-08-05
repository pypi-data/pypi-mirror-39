'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const tmp = require("tmp");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const kubeflowTrainingService_1 = require("../kubeflow/kubeflowTrainingService");
const localCodeDir = tmp.dirSync().name;
const mockedTrialPath = './training_service/test/mockedTrial.py';
fs.copyFileSync(mockedTrialPath, localCodeDir + '/mockedTrial.py');
describe('Unit Test for KubeflowTrainingService', () => {
    let skip = false;
    let testKubeflowConfig;
    let testKubeflowTrialConfig;
    try {
        testKubeflowConfig = JSON.parse(fs.readFileSync('../../.vscode/kubeflowCluster.json', 'utf8'));
        testKubeflowTrialConfig = `{\"command\":\"python3 mnist-keras.py\",\"codeDir\":\"/home/desy/nni/examples/trials/mnist",\"gpuNum\":\"1\",\"cpuNum\":\"2\",\"memoryMB\":\"8196\",\"image\":\"msranni/nni:v0.3.3\"}`;
    }
    catch (err) {
        console.log('Please configure rminfo.json to enable remote machine unit test.');
    }
    let kubeflowTrainingService;
    console.log(tmp.dirSync().name);
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    beforeEach(() => {
        if (skip) {
            return;
        }
        kubeflowTrainingService = component.get(kubeflowTrainingService_1.KubeflowTrainingService);
    });
    afterEach(() => {
        if (skip) {
            return;
        }
        kubeflowTrainingService.cleanUp();
    });
    it('Simple Test', async () => {
        if (skip) {
            return;
        }
        kubeflowTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.KUBEFLOW_CLUSTER_CONFIG, testKubeflowConfig),
            kubeflowTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, testKubeflowTrialConfig);
        try {
            const trialDetail = await kubeflowTrainingService.submitTrialJob({ jobType: 'TRIAL' });
        }
        catch (error) {
            console.log('Submit job failed:' + error);
            chai.assert(error);
        }
    });
});
