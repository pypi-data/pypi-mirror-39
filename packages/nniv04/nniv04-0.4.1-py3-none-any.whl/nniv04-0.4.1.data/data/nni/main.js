'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const typescript_ioc_1 = require("typescript-ioc");
const component = require("./common/component");
const datastore_1 = require("./common/datastore");
const experimentStartupInfo_1 = require("./common/experimentStartupInfo");
const log_1 = require("./common/log");
const manager_1 = require("./common/manager");
const trainingService_1 = require("./common/trainingService");
const utils_1 = require("./common/utils");
const nniDataStore_1 = require("./core/nniDataStore");
const nnimanager_1 = require("./core/nnimanager");
const sqlDatabase_1 = require("./core/sqlDatabase");
const nniRestServer_1 = require("./rest_server/nniRestServer");
const localTrainingServiceForGPU_1 = require("./training_service/local/localTrainingServiceForGPU");
const remoteMachineTrainingService_1 = require("./training_service/remote_machine/remoteMachineTrainingService");
const paiTrainingService_1 = require("./training_service/pai/paiTrainingService");
const kubeflowTrainingService_1 = require("./training_service/kubeflow/kubeflowTrainingService");
function initStartupInfo(startExpMode, resumeExperimentId, basePort) {
    const createNew = (startExpMode === 'new');
    const expId = createNew ? utils_1.uniqueString(8) : resumeExperimentId;
    experimentStartupInfo_1.setExperimentStartupInfo(createNew, expId, basePort);
}
async function initContainer(platformMode) {
    if (platformMode === 'local') {
        typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(localTrainingServiceForGPU_1.LocalTrainingServiceForGPU).scope(typescript_ioc_1.Scope.Singleton);
    }
    else if (platformMode === 'remote') {
        typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(remoteMachineTrainingService_1.RemoteMachineTrainingService).scope(typescript_ioc_1.Scope.Singleton);
    }
    else if (platformMode === 'pai') {
        typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(paiTrainingService_1.PAITrainingService).scope(typescript_ioc_1.Scope.Singleton);
    }
    else if (platformMode === 'kubeflow') {
        typescript_ioc_1.Container.bind(trainingService_1.TrainingService).to(kubeflowTrainingService_1.KubeflowTrainingService).scope(typescript_ioc_1.Scope.Singleton);
    }
    else {
        throw new Error(`Error: unsupported mode: ${mode}`);
    }
    typescript_ioc_1.Container.bind(manager_1.Manager).to(nnimanager_1.NNIManager).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.Database).to(sqlDatabase_1.SqlDB).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.DataStore).to(nniDataStore_1.NNIDataStore).scope(typescript_ioc_1.Scope.Singleton);
    const ds = component.get(datastore_1.DataStore);
    await ds.init();
}
function usage() {
    console.info('usage: node main.js --port <port> --mode <local/remote/pai> --start_mode <new/resume> --experiment_id <id>');
}
const strPort = utils_1.parseArg(['--port', '-p']);
if (!strPort || strPort.length === 0) {
    usage();
    process.exit(1);
}
const port = parseInt(strPort, 10);
const mode = utils_1.parseArg(['--mode', '-m']);
if (!['local', 'remote', 'pai', 'kubeflow'].includes(mode)) {
    console.log(`FATAL: unknown mode: ${mode}`);
    usage();
    process.exit(1);
}
const startMode = utils_1.parseArg(['--start_mode', '-s']);
if (!['new', 'resume'].includes(startMode)) {
    console.log(`FATAL: unknown start_mode: ${startMode}`);
    usage();
    process.exit(1);
}
const experimentId = utils_1.parseArg(['--experiment_id', '-id']);
if (startMode === 'resume' && experimentId.trim().length < 1) {
    console.log(`FATAL: cannot resume experiment, invalid experiment_id: ${experimentId}`);
    usage();
    process.exit(1);
}
initStartupInfo(startMode, experimentId, port);
utils_1.mkDirP(utils_1.getLogDir()).then(async () => {
    const log = log_1.getLogger();
    try {
        await initContainer(mode);
        const restServer = component.get(nniRestServer_1.NNIRestServer);
        await restServer.start();
        log.info(`Rest server listening on: ${restServer.endPoint}`);
    }
    catch (err) {
        log.error(`${err.stack}`);
    }
}).catch((err) => {
    console.error(`Failed to create log dir: ${err.stack}`);
});
process.on('SIGTERM', async () => {
    const log = log_1.getLogger();
    let hasError = false;
    try {
        const nniManager = component.get(manager_1.Manager);
        await nniManager.stopExperiment();
        const ds = component.get(datastore_1.DataStore);
        await ds.close();
        const restServer = component.get(nniRestServer_1.NNIRestServer);
        await restServer.stop();
    }
    catch (err) {
        hasError = true;
        log.error(`${err.stack}`);
    }
    finally {
        await log.close();
        process.exit(hasError ? 1 : 0);
    }
});
