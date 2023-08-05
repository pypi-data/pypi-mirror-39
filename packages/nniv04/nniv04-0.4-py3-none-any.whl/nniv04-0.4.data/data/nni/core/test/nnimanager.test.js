'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai_1 = require("chai");
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const datastore_1 = require("../../common/datastore");
const manager_1 = require("../../common/manager");
const trainingService_1 = require("../../common/trainingService");
const utils_1 = require("../../common/utils");
const nniDataStore_1 = require("../nniDataStore");
const nnimanager_1 = require("../nnimanager");
const sqlDatabase_1 = require("../sqlDatabase");
const mockedTrainingService_1 = require("./mockedTrainingService");
async function initContainer() {
    utils_1.prepareUnitTest();
    typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(mockedTrainingService_1.MockedTrainingService).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(manager_1.Manager).to(nnimanager_1.NNIManager).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.Database).to(sqlDatabase_1.SqlDB).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.DataStore).to(nniDataStore_1.NNIDataStore).scope(typescript_ioc_1.Scope.Singleton);
    await component.get(datastore_1.DataStore).init();
}
describe('Unit test for nnimanager', function () {
    this.timeout(10000);
    let nniManager;
    let ClusterMetadataKey = 'mockedMetadataKey';
    let experimentParams = {
        authorName: 'zql',
        experimentName: 'naive_experiment',
        trialConcurrency: 2,
        maxExecDuration: 5,
        maxTrialNum: 2,
        trainingServicePlatform: 'local',
        searchSpace: '{"x":1}',
        tuner: {
            className: 'EvolutionTuner',
            classArgs: {
                optimize_mode: 'maximize'
            },
            checkpointDir: '',
            gpuNum: 1
        },
        assessor: {
            className: 'MedianstopAssessor',
            checkpointDir: '',
            gpuNum: 1
        }
    };
    before(async () => {
        await initContainer();
        nniManager = component.get(manager_1.Manager);
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('test resumeExperiment', () => {
    });
    it('test startExperiment', () => {
        return nniManager.startExperiment(experimentParams).then(function (experimentId) {
            chai_1.expect(experimentId.length).to.be.equal(8);
        }).catch(function (error) {
            chai_1.assert.fail(error);
        });
    });
    it('test listTrialJobs', () => {
    });
    it('test getTrialJob valid', () => {
        return nniManager.getTrialJob('1234').then(function (trialJobDetail) {
            chai_1.expect(trialJobDetail.id).to.be.equal('1234');
        }).catch(function (error) {
            chai_1.assert.fail(error);
        });
    });
    it('test getTrialJob with invalid id', () => {
        return nniManager.getTrialJob('4567').then((jobid) => {
            chai_1.assert.fail();
        }).catch((error) => {
            chai_1.assert.isTrue(true);
        });
    });
    it('test getClusterMetadata', () => {
        return nniManager.getClusterMetadata(ClusterMetadataKey).then(function (value) {
            chai_1.expect(value).to.equal("default");
        });
    });
    it('test setClusterMetadata and getClusterMetadata', () => {
        return nniManager.setClusterMetadata(ClusterMetadataKey, "newdata").then(() => {
            return nniManager.getClusterMetadata(ClusterMetadataKey).then(function (value) {
                chai_1.expect(value).to.equal("newdata");
            });
        }).catch((error) => {
            console.log(error);
        });
    });
    it('test cancelTrialJobByUser', () => {
        return nniManager.cancelTrialJobByUser('1234').then(() => {
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test addCustomizedTrialJob', () => {
        return nniManager.addCustomizedTrialJob('hyperParams').then(() => {
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
});
