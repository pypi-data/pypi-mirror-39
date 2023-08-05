'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const ts_deferred_1 = require("ts-deferred");
const component = require("../common/component");
const datastore_1 = require("../common/datastore");
const errors_1 = require("../common/errors");
const experimentStartupInfo_1 = require("../common/experimentStartupInfo");
const log_1 = require("../common/log");
const utils_1 = require("../common/utils");
class NNIDataStore {
    constructor() {
        this.db = component.get(datastore_1.Database);
        this.log = log_1.getLogger();
    }
    init() {
        if (this.initTask !== undefined) {
            return this.initTask.promise;
        }
        this.initTask = new ts_deferred_1.Deferred();
        const databaseDir = utils_1.getDefaultDatabaseDir();
        if (experimentStartupInfo_1.isNewExperiment()) {
            utils_1.mkDirP(databaseDir).then(() => {
                this.db.init(true, databaseDir).then(() => {
                    this.initTask.resolve();
                }).catch((err) => {
                    this.initTask.reject(err);
                });
            }).catch((err) => {
                this.initTask.reject(err);
            });
        }
        else {
            this.db.init(false, databaseDir).then(() => {
                this.initTask.resolve();
            }).catch((err) => {
                this.initTask.reject(err);
            });
        }
        return this.initTask.promise;
    }
    async close() {
        await this.db.close();
    }
    async storeExperimentProfile(experimentProfile) {
        try {
            await this.db.storeExperimentProfile(experimentProfile);
        }
        catch (err) {
            throw new errors_1.NNIError('Datastore error', `Datastore error: ${err.message}`, err);
        }
    }
    getExperimentProfile(experimentId) {
        return this.db.queryLatestExperimentProfile(experimentId);
    }
    storeTrialJobEvent(event, trialJobId, hyperParameter, jobDetail) {
        this.log.debug(`storeTrialJobEvent: event: ${event}, data: ${hyperParameter}, jobDetail: ${JSON.stringify(jobDetail)}`);
        let timestamp;
        if (event === 'WAITING' && jobDetail) {
            timestamp = jobDetail.submitTime;
        }
        else if (event === 'RUNNING' && jobDetail) {
            timestamp = jobDetail.startTime;
        }
        else if (['EARLY_STOPPED', 'SUCCEEDED', 'FAILED', 'USER_CANCELED', 'SYS_CANCELED'].includes(event) && jobDetail) {
            timestamp = jobDetail.endTime;
        }
        if (timestamp === undefined) {
            timestamp = Date.now();
        }
        return this.db.storeTrialJobEvent(event, trialJobId, timestamp, hyperParameter, jobDetail).catch((err) => {
            throw new errors_1.NNIError('Datastore error', `Datastore error: ${err.message}`, err);
        });
    }
    async getTrialJobStatistics() {
        const result = [];
        const jobs = await this.listTrialJobs();
        const map = new Map();
        jobs.forEach((value) => {
            let n = map.get(value.status);
            if (!n) {
                n = 0;
            }
            map.set(value.status, n + 1);
        });
        map.forEach((value, key) => {
            const statistics = {
                trialJobStatus: key,
                trialJobNumber: value
            };
            result.push(statistics);
        });
        return result;
    }
    listTrialJobs(status) {
        return this.queryTrialJobs(status);
    }
    async getTrialJob(trialJobId) {
        const trialJobs = await this.queryTrialJobs(undefined, trialJobId);
        return trialJobs[0];
    }
    async storeMetricData(trialJobId, data) {
        const metrics = JSON.parse(data);
        if (metrics.type === 'REQUEST_PARAMETER') {
            return;
        }
        assert(trialJobId === metrics.trial_job_id);
        try {
            await this.db.storeMetricData(trialJobId, JSON.stringify({
                trialJobId: metrics.trial_job_id,
                parameterId: metrics.parameter_id,
                type: metrics.type,
                sequence: metrics.sequence,
                data: metrics.value,
                timestamp: Date.now()
            }));
        }
        catch (err) {
            throw new errors_1.NNIError('Datastore error', `Datastore error: ${err.message}`, err);
        }
    }
    getMetricData(trialJobId, metricType) {
        return this.db.queryMetricData(trialJobId, metricType);
    }
    async queryTrialJobs(status, trialJobId) {
        const result = [];
        const trialJobEvents = await this.db.queryTrialJobEvent(trialJobId);
        if (trialJobEvents === undefined) {
            return result;
        }
        const map = this.getTrialJobsByReplayEvents(trialJobEvents);
        const finalMetricsMap = await this.getFinalMetricData(trialJobId);
        for (const key of map.keys()) {
            const jobInfo = map.get(key);
            if (jobInfo === undefined) {
                continue;
            }
            if (!(status !== undefined && jobInfo.status !== status)) {
                if (jobInfo.status === 'SUCCEEDED') {
                    jobInfo.finalMetricData = finalMetricsMap.get(jobInfo.id);
                }
                result.push(jobInfo);
            }
        }
        return result;
    }
    async getFinalMetricData(trialJobId) {
        const map = new Map();
        const metrics = await this.getMetricData(trialJobId, 'FINAL');
        const multiPhase = await this.isMultiPhase();
        for (const metric of metrics) {
            const existMetrics = map.get(metric.trialJobId);
            if (existMetrics !== undefined) {
                if (!multiPhase) {
                    this.log.error(`Found multiple FINAL results for trial job ${trialJobId}, metrics: ${JSON.stringify(metrics)}`);
                }
                else {
                    existMetrics.push(metric);
                }
            }
            else {
                map.set(metric.trialJobId, [metric]);
            }
        }
        return map;
    }
    async isMultiPhase() {
        if (this.multiPhase === undefined) {
            this.multiPhase = (await this.getExperimentProfile(experimentStartupInfo_1.getExperimentId())).params.multiPhase;
        }
        if (this.multiPhase !== undefined) {
            return this.multiPhase;
        }
        else {
            return false;
        }
    }
    getJobStatusByLatestEvent(oldStatus, event) {
        switch (event) {
            case 'USER_TO_CANCEL':
                return 'USER_CANCELED';
            case 'ADD_CUSTOMIZED':
                return 'WAITING';
            case 'ADD_HYPERPARAMETER':
                return oldStatus;
            default:
        }
        return event;
    }
    mergeHyperParameters(hyperParamList, newParamStr) {
        const mergedHyperParams = [];
        const newParam = JSON.parse(newParamStr);
        for (const hyperParamStr of hyperParamList) {
            const hyperParam = JSON.parse(hyperParamStr);
            mergedHyperParams.push(hyperParam);
        }
        if (mergedHyperParams.filter((value) => value.parameter_index === newParam.parameter_index).length <= 0) {
            mergedHyperParams.push(newParam);
        }
        return mergedHyperParams.map((value) => { return JSON.stringify(value); });
    }
    getTrialJobsByReplayEvents(trialJobEvents) {
        const map = new Map();
        for (const record of trialJobEvents) {
            let jobInfo;
            if (record.trialJobId === undefined || record.trialJobId.length < 1) {
                continue;
            }
            if (map.has(record.trialJobId)) {
                jobInfo = map.get(record.trialJobId);
            }
            else {
                jobInfo = {
                    id: record.trialJobId,
                    status: this.getJobStatusByLatestEvent('UNKNOWN', record.event),
                    hyperParameters: []
                };
            }
            if (!jobInfo) {
                throw new Error('Empty JobInfo');
            }
            switch (record.event) {
                case 'RUNNING':
                    if (record.timestamp !== undefined) {
                        jobInfo.startTime = record.timestamp;
                    }
                case 'WAITING':
                    if (record.logPath !== undefined) {
                        jobInfo.logPath = record.logPath;
                    }
                    if (jobInfo.startTime === undefined && record.timestamp !== undefined) {
                        jobInfo.startTime = record.timestamp;
                    }
                    break;
                case 'SUCCEEDED':
                case 'FAILED':
                case 'USER_CANCELED':
                case 'SYS_CANCELED':
                case 'EARLY_STOPPED':
                    if (record.logPath !== undefined) {
                        jobInfo.logPath = record.logPath;
                    }
                    jobInfo.endTime = record.timestamp;
                    if (jobInfo.startTime === undefined && record.timestamp !== undefined) {
                        jobInfo.startTime = record.timestamp;
                    }
                default:
            }
            jobInfo.status = this.getJobStatusByLatestEvent(jobInfo.status, record.event);
            if (record.data !== undefined && record.data.trim().length > 0) {
                if (jobInfo.hyperParameters !== undefined) {
                    jobInfo.hyperParameters = this.mergeHyperParameters(jobInfo.hyperParameters, record.data);
                }
                else {
                    assert(false, 'jobInfo.hyperParameters is undefined');
                }
            }
            if (record.sequenceId !== undefined && jobInfo.sequenceId === undefined) {
                jobInfo.sequenceId = record.sequenceId;
            }
            map.set(record.trialJobId, jobInfo);
        }
        return map;
    }
}
exports.NNIDataStore = NNIDataStore;
