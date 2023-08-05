'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const cpp = require("child-process-promise");
const child_process_1 = require("child_process");
const ts_deferred_1 = require("ts-deferred");
const component = require("../common/component");
const datastore_1 = require("../common/datastore");
const errors_1 = require("../common/errors");
const experimentStartupInfo_1 = require("../common/experimentStartupInfo");
const log_1 = require("../common/log");
const trainingService_1 = require("../common/trainingService");
const utils_1 = require("../common/utils");
const commands_1 = require("./commands");
const ipcInterface_1 = require("./ipcInterface");
class NNIManager {
    constructor() {
        this.currSubmittedTrialNum = 0;
        this.trialConcurrencyChange = 0;
        this.customizedTrials = [];
        this.trainingService = component.get(trainingService_1.TrainingService);
        assert(this.trainingService);
        this.dispatcherPid = 0;
        this.waitingTrials = [];
        this.trialJobs = new Map();
        this.log = log_1.getLogger();
        this.dataStore = component.get(datastore_1.DataStore);
        this.experimentProfile = this.createEmptyExperimentProfile();
        this.status = {
            status: 'INITIALIZED',
            errors: []
        };
    }
    updateExperimentProfile(experimentProfile, updateType) {
        switch (updateType) {
            case 'TRIAL_CONCURRENCY':
                this.updateTrialConcurrency(experimentProfile.params.trialConcurrency);
                break;
            case 'MAX_EXEC_DURATION':
                this.updateMaxExecDuration(experimentProfile.params.maxExecDuration);
                break;
            case 'SEARCH_SPACE':
                this.updateSearchSpace(experimentProfile.params.searchSpace);
                break;
            case 'MAX_TRIAL_NUM':
                this.updateMaxTrialNum(experimentProfile.params.maxTrialNum);
                break;
            default:
                throw new Error('Error: unrecognized updateType');
        }
        return this.storeExperimentProfile();
    }
    addCustomizedTrialJob(hyperParams) {
        if (this.currSubmittedTrialNum >= this.experimentProfile.params.maxTrialNum) {
            return Promise.reject(new Error('reach maxTrialNum'));
        }
        this.customizedTrials.push(hyperParams);
        return this.dataStore.storeTrialJobEvent('ADD_CUSTOMIZED', '', hyperParams);
    }
    async cancelTrialJobByUser(trialJobId) {
        await this.trainingService.cancelTrialJob(trialJobId);
        await this.dataStore.storeTrialJobEvent('USER_TO_CANCEL', trialJobId, '');
    }
    async startExperiment(expParams) {
        this.log.debug(`Starting experiment: ${this.experimentProfile.id}`);
        this.experimentProfile.params = expParams;
        await this.storeExperimentProfile();
        this.log.debug('Setup tuner...');
        if (expParams.multiPhase && this.trainingService.isMultiPhaseJobSupported) {
            this.trainingService.setClusterMetadata('multiPhase', expParams.multiPhase.toString());
        }
        const dispatcherCommand = utils_1.getMsgDispatcherCommand(expParams.tuner, expParams.assessor, expParams.advisor, expParams.multiPhase, expParams.multiThread);
        this.log.debug(`dispatcher command: ${dispatcherCommand}`);
        const checkpointDir = await this.createCheckpointDir();
        this.setupTuner(dispatcherCommand, undefined, 'start', checkpointDir);
        this.experimentProfile.startTime = Date.now();
        this.status.status = 'EXPERIMENT_RUNNING';
        await this.storeExperimentProfile();
        this.run().catch((err) => {
            this.criticalError(err);
        });
        return this.experimentProfile.id;
    }
    async resumeExperiment() {
        const experimentId = experimentStartupInfo_1.getExperimentId();
        this.experimentProfile = await this.dataStore.getExperimentProfile(experimentId);
        const expParams = this.experimentProfile.params;
        experimentStartupInfo_1.setInitTrialSequenceId(this.experimentProfile.maxSequenceId + 1);
        if (expParams.multiPhase && this.trainingService.isMultiPhaseJobSupported) {
            this.trainingService.setClusterMetadata('multiPhase', expParams.multiPhase.toString());
        }
        const dispatcherCommand = utils_1.getMsgDispatcherCommand(expParams.tuner, expParams.assessor, expParams.advisor, expParams.multiPhase, expParams.multiThread);
        this.log.debug(`dispatcher command: ${dispatcherCommand}`);
        const checkpointDir = await this.createCheckpointDir();
        this.setupTuner(dispatcherCommand, undefined, 'resume', checkpointDir);
        const allTrialJobs = await this.dataStore.listTrialJobs();
        this.currSubmittedTrialNum = allTrialJobs.length;
        await Promise.all(allTrialJobs
            .filter((job) => job.status === 'WAITING' || job.status === 'RUNNING')
            .map((job) => this.dataStore.storeTrialJobEvent('FAILED', job.id)));
        if (this.experimentProfile.execDuration < this.experimentProfile.params.maxExecDuration &&
            this.currSubmittedTrialNum < this.experimentProfile.params.maxTrialNum &&
            this.experimentProfile.endTime) {
            delete this.experimentProfile.endTime;
        }
        this.status.status = 'EXPERIMENT_RUNNING';
        this.run().catch((err) => {
            this.criticalError(err);
        });
    }
    getTrialJob(trialJobId) {
        return Promise.resolve(this.trainingService.getTrialJob(trialJobId));
    }
    async setClusterMetadata(key, value) {
        let timeoutId;
        const delay1 = new Promise((resolve, reject) => {
            timeoutId = setTimeout(() => { reject(new Error('TrainingService setClusterMetadata timeout. Please check your config file.')); }, 10000);
        });
        await Promise.race([delay1, this.trainingService.setClusterMetadata(key, value)]).finally(() => {
            clearTimeout(timeoutId);
        });
    }
    getClusterMetadata(key) {
        return Promise.resolve(this.trainingService.getClusterMetadata(key));
    }
    async getTrialJobStatistics() {
        return this.dataStore.getTrialJobStatistics();
    }
    async stopExperiment() {
        this.status.status = 'STOPPING';
        this.log.info('Experiment done, cleaning up...');
        await this.experimentDoneCleanUp();
        this.log.info('Experiment done.');
    }
    async getMetricData(trialJobId, metricType) {
        return this.dataStore.getMetricData(trialJobId, metricType);
    }
    getExperimentProfile() {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve(this.experimentProfile);
        return deferred.promise;
    }
    getStatus() {
        return this.status;
    }
    async listTrialJobs(status) {
        return this.dataStore.listTrialJobs(status);
    }
    setupTuner(command, cwd, mode, dataDirectory) {
        if (this.dispatcher !== undefined) {
            return;
        }
        const stdio = ['ignore', process.stdout, process.stderr, 'pipe', 'pipe'];
        let newCwd;
        if (cwd === undefined || cwd === '') {
            newCwd = utils_1.getLogDir();
        }
        else {
            newCwd = cwd;
        }
        let nniEnv = {
            NNI_MODE: mode,
            NNI_CHECKPOINT_DIRECTORY: dataDirectory,
            NNI_LOG_DIRECTORY: utils_1.getLogDir()
        };
        let newEnv = Object.assign({}, process.env, nniEnv);
        const tunerProc = child_process_1.spawn(command, [], {
            stdio,
            cwd: newCwd,
            env: newEnv,
            shell: true
        });
        this.dispatcherPid = tunerProc.pid;
        this.dispatcher = ipcInterface_1.createDispatcherInterface(tunerProc);
        return;
    }
    updateTrialConcurrency(trialConcurrency) {
        this.trialConcurrencyChange += (trialConcurrency - this.experimentProfile.params.trialConcurrency);
        this.experimentProfile.params.trialConcurrency = trialConcurrency;
        return;
    }
    updateMaxExecDuration(duration) {
        this.experimentProfile.params.maxExecDuration = duration;
        return;
    }
    updateSearchSpace(searchSpace) {
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner has not been setup');
        }
        this.dispatcher.sendCommand(commands_1.UPDATE_SEARCH_SPACE, searchSpace);
        this.experimentProfile.params.searchSpace = searchSpace;
        return;
    }
    updateMaxTrialNum(maxTrialNum) {
        this.experimentProfile.params.maxTrialNum = maxTrialNum;
        return;
    }
    async experimentDoneCleanUp() {
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner has not been setup');
        }
        this.dispatcher.sendCommand(commands_1.TERMINATE);
        let tunerAlive = true;
        for (let i = 0; i < 30; i++) {
            if (!tunerAlive) {
                break;
            }
            try {
                await cpp.exec(`kill -0 ${this.dispatcherPid}`);
            }
            catch (error) {
                tunerAlive = false;
            }
            await utils_1.delay(1000);
        }
        try {
            await cpp.exec(`kill ${this.dispatcherPid}`);
        }
        catch (error) {
        }
        const trialJobList = await this.trainingService.listTrialJobs();
        for (const trialJob of trialJobList) {
            if (trialJob.status === 'RUNNING' ||
                trialJob.status === 'WAITING') {
                try {
                    await this.trainingService.cancelTrialJob(trialJob.id);
                }
                catch (error) {
                }
            }
        }
        await this.trainingService.cleanUp();
        this.experimentProfile.endTime = Date.now();
        await this.storeExperimentProfile();
        this.status.status = 'STOPPED';
    }
    async periodicallyUpdateExecDuration() {
        let count = 1;
        while (this.status.status !== 'STOPPING' && this.status.status !== 'STOPPED') {
            await utils_1.delay(1000 * 1);
            if (this.status.status === 'EXPERIMENT_RUNNING') {
                this.experimentProfile.execDuration += 1;
                if (count % 10 === 0) {
                    await this.storeExperimentProfile();
                }
            }
            count += 1;
        }
    }
    async requestTrialJobsStatus() {
        let finishedTrialJobNum = 0;
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner has not been setup');
        }
        for (const trialJobId of Array.from(this.trialJobs.keys())) {
            const trialJobDetail = await this.trainingService.getTrialJob(trialJobId);
            const oldTrialJobDetail = this.trialJobs.get(trialJobId);
            if (oldTrialJobDetail !== undefined && oldTrialJobDetail.status !== trialJobDetail.status) {
                this.trialJobs.set(trialJobId, Object.assign({}, trialJobDetail));
                await this.dataStore.storeTrialJobEvent(trialJobDetail.status, trialJobDetail.id, undefined, trialJobDetail);
            }
            let hyperParams = undefined;
            switch (trialJobDetail.status) {
                case 'SUCCEEDED':
                case 'USER_CANCELED':
                case 'EARLY_STOPPED':
                    this.trialJobs.delete(trialJobId);
                    finishedTrialJobNum++;
                    if (trialJobDetail.form.jobType === 'TRIAL') {
                        hyperParams = trialJobDetail.form.hyperParameters.value;
                    }
                    else {
                        throw new Error('Error: jobType error, not TRIAL');
                    }
                    this.dispatcher.sendCommand(commands_1.TRIAL_END, JSON.stringify({
                        trial_job_id: trialJobDetail.id,
                        event: trialJobDetail.status,
                        hyper_params: hyperParams
                    }));
                    break;
                case 'FAILED':
                case 'SYS_CANCELED':
                    this.trialJobs.delete(trialJobId);
                    finishedTrialJobNum++;
                    if (trialJobDetail.form.jobType === 'TRIAL') {
                        hyperParams = trialJobDetail.form.hyperParameters.value;
                    }
                    else {
                        throw new Error('Error: jobType error, not TRIAL');
                    }
                    this.dispatcher.sendCommand(commands_1.TRIAL_END, JSON.stringify({
                        trial_job_id: trialJobDetail.id,
                        event: trialJobDetail.status,
                        hyper_params: hyperParams
                    }));
                    break;
                case 'WAITING':
                case 'RUNNING':
                case 'UNKNOWN':
                    break;
                default:
            }
        }
        return finishedTrialJobNum;
    }
    async manageTrials() {
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner has not been setup');
        }
        let allFinishedTrialJobNum = 0;
        while (this.status.status !== 'STOPPING' && this.status.status !== 'STOPPED') {
            const finishedTrialJobNum = await this.requestTrialJobsStatus();
            allFinishedTrialJobNum += finishedTrialJobNum;
            if (allFinishedTrialJobNum >= this.experimentProfile.params.maxTrialNum) {
                this.log.info('Experiment done.');
            }
            const requestTrialNum = this.trialConcurrencyChange + finishedTrialJobNum;
            if (requestTrialNum >= 0) {
                this.trialConcurrencyChange = 0;
            }
            else {
                this.trialConcurrencyChange = requestTrialNum;
            }
            const requestCustomTrialNum = Math.min(requestTrialNum, this.customizedTrials.length);
            for (let i = 0; i < requestCustomTrialNum; i++) {
                if (this.customizedTrials.length > 0) {
                    const hyperParams = this.customizedTrials.shift();
                    this.dispatcher.sendCommand(commands_1.ADD_CUSTOMIZED_TRIAL_JOB, hyperParams);
                }
            }
            if (requestTrialNum - requestCustomTrialNum > 0) {
                this.requestTrialJobs(requestTrialNum - requestCustomTrialNum);
            }
            assert(this.status.status === 'EXPERIMENT_RUNNING' ||
                this.status.status === 'DONE' ||
                this.status.status === 'NO_MORE_TRIAL');
            if (this.experimentProfile.execDuration > this.experimentProfile.params.maxExecDuration ||
                this.currSubmittedTrialNum >= this.experimentProfile.params.maxTrialNum) {
                if (this.status.status === 'EXPERIMENT_RUNNING' ||
                    this.status.status === 'NO_MORE_TRIAL') {
                    this.experimentProfile.endTime = Date.now();
                    await this.storeExperimentProfile();
                }
                this.status.status = 'DONE';
            }
            else {
                if (this.status.status === 'DONE') {
                    delete this.experimentProfile.endTime;
                    await this.storeExperimentProfile();
                }
                if (this.status.status !== 'NO_MORE_TRIAL') {
                    this.status.status = 'EXPERIMENT_RUNNING';
                }
                for (let i = this.trialJobs.size; i < this.experimentProfile.params.trialConcurrency; i++) {
                    if (this.waitingTrials.length === 0 ||
                        this.currSubmittedTrialNum >= this.experimentProfile.params.maxTrialNum) {
                        break;
                    }
                    const hyperParams = this.waitingTrials.shift();
                    if (hyperParams === undefined) {
                        throw new Error(`Error: invalid hyper-parameters for job submission: ${hyperParams}`);
                    }
                    this.currSubmittedTrialNum++;
                    const trialJobAppForm = {
                        jobType: 'TRIAL',
                        hyperParameters: {
                            value: hyperParams,
                            index: 0
                        }
                    };
                    const trialJobDetail = await this.trainingService.submitTrialJob(trialJobAppForm);
                    await this.storeMaxSequenceId(trialJobDetail.sequenceId);
                    this.trialJobs.set(trialJobDetail.id, Object.assign({}, trialJobDetail));
                    const trialJobDetailSnapshot = this.trialJobs.get(trialJobDetail.id);
                    if (trialJobDetailSnapshot != undefined) {
                        await this.dataStore.storeTrialJobEvent(trialJobDetailSnapshot.status, trialJobDetailSnapshot.id, hyperParams, trialJobDetailSnapshot);
                    }
                    else {
                        assert(false, `undefined trialJobDetail in trialJobs: ${trialJobDetail.id}`);
                    }
                }
            }
            await utils_1.delay(1000 * 5);
        }
    }
    storeExperimentProfile() {
        this.experimentProfile.revision += 1;
        return this.dataStore.storeExperimentProfile(this.experimentProfile);
    }
    async run() {
        assert(this.dispatcher !== undefined);
        this.addEventListeners();
        this.sendInitTunerCommands();
        await Promise.all([
            this.periodicallyUpdateExecDuration(),
            this.trainingService.run().catch((err) => {
                throw new errors_1.NNIError('Training service error', `Training service error: ${err.message}`, err);
            }),
            this.manageTrials().catch((err) => {
                throw new errors_1.NNIError('Job management error', `Job management error: ${err.message}`, err);
            })
        ]);
    }
    addEventListeners() {
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner or job maintainer have not been setup');
        }
        this.trainingService.addTrialJobMetricListener((metric) => {
            this.onTrialJobMetrics(metric).catch((err) => {
                this.criticalError(new errors_1.NNIError('Job metrics error', `Job metrics error: ${err.message}`, err));
            });
        });
        this.dispatcher.onCommand((commandType, content) => {
            this.onTunerCommand(commandType, content).catch((err) => {
                this.criticalError(new errors_1.NNIError('Tuner command event error', `Tuner command event error: ${err.message}`, err));
            });
        });
    }
    sendInitTunerCommands() {
        if (this.dispatcher === undefined) {
            throw new Error('Dispatcher error: tuner has not been setup');
        }
        this.log.debug(`Send tuner command: INITIALIZE: ${this.experimentProfile.params.searchSpace}`);
        this.dispatcher.sendCommand(commands_1.INITIALIZE, this.experimentProfile.params.searchSpace);
    }
    async onTrialJobMetrics(metric) {
        await this.dataStore.storeMetricData(metric.id, metric.data);
        if (this.dispatcher === undefined) {
            throw new Error('Error: tuner has not been setup');
        }
        this.dispatcher.sendCommand(commands_1.REPORT_METRIC_DATA, metric.data);
    }
    requestTrialJobs(jobNum) {
        if (jobNum < 1) {
            return;
        }
        if (this.dispatcher === undefined) {
            throw new Error('Dispatcher error: tuner has not been setup');
        }
        if (this.experimentProfile.params.multiThread) {
            for (let i = 0; i < jobNum; i++) {
                this.dispatcher.sendCommand(commands_1.REQUEST_TRIAL_JOBS, '1');
            }
        }
        else {
            this.dispatcher.sendCommand(commands_1.REQUEST_TRIAL_JOBS, String(jobNum));
        }
    }
    async onTunerCommand(commandType, content) {
        this.log.info(`Command from tuner: ${commandType}, ${content}`);
        switch (commandType) {
            case commands_1.INITIALIZED:
                this.requestTrialJobs(this.experimentProfile.params.trialConcurrency);
                break;
            case commands_1.NEW_TRIAL_JOB:
                if (this.status.status === 'NO_MORE_TRIAL') {
                    this.log.warning('It is not supposed to receive more trials after NO_MORE_TRIAL is set');
                    this.status.status = 'EXPERIMENT_RUNNING';
                }
                this.waitingTrials.push(content);
                break;
            case commands_1.SEND_TRIAL_JOB_PARAMETER:
                const tunerCommand = JSON.parse(content);
                assert(tunerCommand.parameter_index >= 0);
                assert(tunerCommand.trial_job_id !== undefined);
                const trialJobForm = {
                    jobType: 'TRIAL',
                    hyperParameters: {
                        value: content,
                        index: tunerCommand.parameter_index
                    }
                };
                await this.trainingService.updateTrialJob(tunerCommand.trial_job_id, trialJobForm);
                await this.dataStore.storeTrialJobEvent('ADD_HYPERPARAMETER', tunerCommand.trial_job_id, content, undefined);
                break;
            case commands_1.NO_MORE_TRIAL_JOBS:
                this.status.status = 'NO_MORE_TRIAL';
                break;
            case commands_1.KILL_TRIAL_JOB:
                await this.trainingService.cancelTrialJob(JSON.parse(content), true);
                break;
            default:
                throw new Error('Error: unsupported command type from tuner');
        }
    }
    criticalError(err) {
        this.logError(err);
        console.error(err);
    }
    logError(err) {
        if (err.stack !== undefined) {
            this.log.error(err.stack);
        }
        this.status.errors.push(err.message);
        this.status.status = 'ERROR';
    }
    createEmptyExperimentProfile() {
        return {
            id: experimentStartupInfo_1.getExperimentId(),
            revision: 0,
            execDuration: 0,
            logDir: utils_1.getLogDir(),
            maxSequenceId: 0,
            params: {
                authorName: '',
                experimentName: '',
                trialConcurrency: 0,
                maxExecDuration: 0,
                maxTrialNum: 0,
                trainingServicePlatform: '',
                searchSpace: ''
            }
        };
    }
    async createCheckpointDir() {
        const chkpDir = utils_1.getCheckpointDir();
        await utils_1.mkDirP(chkpDir);
        if (this.experimentProfile.params.advisor) {
            this.experimentProfile.params.advisor.checkpointDir = chkpDir;
        }
        if (this.experimentProfile.params.tuner) {
            this.experimentProfile.params.tuner.checkpointDir = chkpDir;
        }
        if (this.experimentProfile.params.assessor) {
            this.experimentProfile.params.assessor.checkpointDir = chkpDir;
        }
        return Promise.resolve(chkpDir);
    }
    async storeMaxSequenceId(sequenceId) {
        if (sequenceId > this.experimentProfile.maxSequenceId) {
            this.experimentProfile.maxSequenceId = sequenceId;
            await this.storeExperimentProfile();
        }
    }
}
exports.NNIManager = NNIManager;
