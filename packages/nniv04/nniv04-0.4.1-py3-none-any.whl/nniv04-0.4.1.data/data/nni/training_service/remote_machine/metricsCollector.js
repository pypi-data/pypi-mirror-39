'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const path = require("path");
const log_1 = require("../../common/log");
const sshClientUtility_1 = require("./sshClientUtility");
class MetricsCollector {
    constructor(clientMap, jobMap, expDir, eventEmitter) {
        this.log = log_1.getLogger();
        this.machineSSHClientMap = clientMap;
        this.trialJobsMap = jobMap;
        this.expRootDir = expDir;
        this.metricsEmitter = eventEmitter;
    }
    async collectMetrics() {
        const aliveJobStatus = ['RUNNING', 'SUCCEEDED'];
        const runningJobsMap = this.getTrialJobIdsGroupByRmMeta(aliveJobStatus);
        const readMetricsTasks = [];
        ;
        runningJobsMap.forEach((jobIds, rmMeta) => {
            readMetricsTasks.push(this.readRmMetrics(rmMeta, jobIds));
        });
        const allMetrics = await Promise.all(readMetricsTasks.map(task => { return task.catch(err => { this.log.error(err.message); }); }));
        allMetrics.forEach((rmMetrics) => {
            if (rmMetrics !== undefined && rmMetrics.length > 0) {
                rmMetrics.forEach((jobMetrics) => {
                    const trialJobId = jobMetrics.jobId;
                    const trialJobDetail = this.trialJobsMap.get(trialJobId);
                    assert(trialJobDetail);
                    if (!['RUNNING'].includes(jobMetrics.jobStatus)) {
                        if (trialJobDetail.status !== 'EARLY_STOPPED') {
                            trialJobDetail.status = jobMetrics.jobStatus;
                        }
                        this.log.info(`Set trialjob ${trialJobDetail.id} status to ${trialJobDetail.status}`);
                        runningJobsMap.forEach((jobIds, rmMeta) => {
                            if (rmMeta.gpuReservation !== undefined) {
                                rmMeta.gpuReservation.forEach((reserveTrialJobId, gpuIndex) => {
                                    if (reserveTrialJobId == trialJobId) {
                                        rmMeta.gpuReservation.delete(gpuIndex);
                                    }
                                });
                            }
                        });
                    }
                    this.sendMetricsToListeners(jobMetrics);
                });
            }
        });
    }
    getTrialJobIdsGroupByRmMeta(status) {
        const map = new Map();
        this.trialJobsMap.forEach((trialJob, id) => {
            let reservedTrialJobIds = [];
            if (trialJob.rmMeta !== undefined
                && trialJob.rmMeta.gpuReservation !== undefined) {
                reservedTrialJobIds = Array.from(trialJob.rmMeta.gpuReservation.values());
            }
            if (reservedTrialJobIds.includes(id) || status.includes(trialJob.status)) {
                if (map.has(trialJob.rmMeta)) {
                    const ids = map.get(trialJob.rmMeta);
                    if (ids !== undefined && !ids.includes(id)) {
                        ids.push(id);
                    }
                }
                else {
                    let initJobIds = [id];
                    if (trialJob.rmMeta.gpuReservation !== undefined) {
                        const concatJobIds = initJobIds.concat(reservedTrialJobIds);
                        initJobIds = concatJobIds.filter((item, pos) => concatJobIds.indexOf(item) === pos);
                    }
                    map.set(trialJob.rmMeta, initJobIds);
                }
            }
        });
        return map;
    }
    sendMetricsToListeners(jobMetrics) {
        if (jobMetrics === undefined) {
            return;
        }
        const jobId = jobMetrics.jobId;
        jobMetrics.metrics.forEach((metric) => {
            if (metric.length > 0) {
                this.metricsEmitter.emit('metric', {
                    id: jobId,
                    data: metric
                });
            }
        });
    }
    async readRmMetrics(rmMeta, trialJobIds) {
        if (trialJobIds === undefined || trialJobIds.length < 1) {
            return [];
        }
        const scriptFile = path.join(path.dirname(path.dirname(this.expRootDir)), 'scripts', 'metrics_reader.py');
        const cmdStr = `python3 ${scriptFile} --experiment_dir ${this.expRootDir} --trial_job_ids ${trialJobIds.join(',')}`;
        trialJobIds.forEach((id) => {
            const trialJob = this.trialJobsMap.get(id);
            assert(trialJob.rmMeta === rmMeta);
        });
        const sshClient = this.machineSSHClientMap.get(rmMeta);
        if (sshClient === undefined) {
            throw new Error('SSHClient not found!');
        }
        const result = await sshClientUtility_1.SSHClientUtility.remoteExeCommand(cmdStr, sshClient);
        if (result.exitCode !== 0) {
            throw new Error(`Failed to read metrics data: ${result.stderr}`);
        }
        else {
            if (result.stdout !== undefined && result.stdout.length > 0) {
                return JSON.parse(result.stdout);
            }
            else {
                return [];
            }
        }
    }
}
exports.MetricsCollector = MetricsCollector;
