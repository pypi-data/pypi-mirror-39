'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const component = require("../../common/component");
const cpp = require("child-process-promise");
const fs = require("fs");
const path = require("path");
const containerJobData_1 = require("../common/containerJobData");
const events_1 = require("events");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const utils_1 = require("../../common/utils");
const kubeflowConfig_1 = require("./kubeflowConfig");
const kubeflowData_1 = require("./kubeflowData");
const kubeflowJobRestServer_1 = require("./kubeflowJobRestServer");
const kubeflowJobInfoCollector_1 = require("./kubeflowJobInfoCollector");
const util_1 = require("../common/util");
const azureStorageClientUtils_1 = require("./azureStorageClientUtils");
var yaml = require('node-yaml');
var azure = require('azure-storage');
let KubeflowTrainingService = class KubeflowTrainingService {
    constructor() {
        this.NNI_KUBEFLOW_TRIAL_LABEL = 'nni-kubeflow-trial';
        this.stopping = false;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.kubeflowJobInfoCollector = new kubeflowJobInfoCollector_1.KubeflowJobInfoCollector(this.trialJobsMap);
        this.trialLocalNFSTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-nfs-tmp');
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.nextTrialSequenceId = -1;
        this.CONTAINER_MOUNT_PATH = '/tmp/mount';
    }
    async run() {
        const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
        await restServer.start();
        this.log.info(`Kubeflow Training service rest server listening on: ${restServer.endPoint}`);
        while (!this.stopping) {
            await utils_1.delay(3000);
            await this.kubeflowJobInfoCollector.retrieveTrialStatus();
        }
    }
    async submitTrialJob(form) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig || !this.kubeflowTrialConfig.worker) {
            throw new Error('Kubeflow trial config or worker config is not initialized');
        }
        if (!this.kubeflowJobPlural) {
            throw new Error('Kubeflow job plural name is undefined');
        }
        if (!this.kubeflowRestServerPort) {
            const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
            this.kubeflowRestServerPort = restServer.clusterRestServerPort;
        }
        const trialJobId = utils_1.uniqueString(5);
        const curTrialSequenceId = this.generateSequenceId();
        const trialWorkingFolder = path.join(this.CONTAINER_MOUNT_PATH, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId);
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await cpp.exec(`mkdir -p ${path.dirname(trialLocalTempFolder)}`);
        await cpp.exec(`cp -r ${this.kubeflowTrialConfig.codeDir} ${trialLocalTempFolder}`);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        await cpp.exec(`mkdir -p ${trialLocalTempFolder}`);
        if (this.kubeflowTrialConfig.worker) {
            const workerRunScriptContent = this.genereateRunScript(trialJobId, trialWorkingFolder, this.kubeflowTrialConfig.worker.command, curTrialSequenceId.toString(), 'worker');
            await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_worker.sh'), workerRunScriptContent, { encoding: 'utf8' });
        }
        if (this.kubeflowTrialConfig.ps) {
            const psRunScriptContent = this.genereateRunScript(trialJobId, trialWorkingFolder, this.kubeflowTrialConfig.ps.command, curTrialSequenceId.toString(), 'ps');
            await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_ps.sh'), psRunScriptContent, { encoding: 'utf8' });
        }
        const trialForm = form;
        if (trialForm && trialForm.hyperParameters) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
        const kubeflowJobYamlPath = path.join(trialLocalTempFolder, `kubeflow-job-${trialJobId}.yaml`);
        const kubeflowJobName = `nni-exp-${this.experimentId}-trial-${trialJobId}`.toLowerCase();
        const workerPodResources = {};
        workerPodResources.requests = {
            'memory': `${this.kubeflowTrialConfig.worker.memoryMB}Mi`,
            'cpu': `${this.kubeflowTrialConfig.worker.cpuNum}`,
            'nvidia.com/gpu': `${this.kubeflowTrialConfig.worker.gpuNum}`
        };
        workerPodResources.limits = Object.assign({}, workerPodResources.requests);
        let psPodResources = undefined;
        if (this.kubeflowTrialConfig.ps) {
            psPodResources = {};
            psPodResources.requests = {
                'memory': `${this.kubeflowTrialConfig.ps.memoryMB}Mi`,
                'cpu': `${this.kubeflowTrialConfig.ps.cpuNum}`,
                'nvidia.com/gpu': `${this.kubeflowTrialConfig.ps.gpuNum}`
            };
            psPodResources.limits = Object.assign({}, psPodResources.requests);
        }
        yaml.write(kubeflowJobYamlPath, this.generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, psPodResources), 'utf-8');
        let trialJobDetail;
        let trialJobDetailUrl;
        if (this.kubeflowClusterConfig.nfs) {
            await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`);
            await cpp.exec(`cp -r ${trialLocalTempFolder}/* ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}/.`);
            const nfsConfig = this.kubeflowClusterConfig.nfs;
            trialJobDetailUrl = `nfs://${nfsConfig.server}:${path.join(nfsConfig.path, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
        }
        else {
            try {
                await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${trialLocalTempFolder}`);
                trialJobDetailUrl = `https://${this.azureStorageAccountName}.file.core.windows.net/${this.azureStorageShare}/${path.join('nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
            }
            catch (error) {
                this.log.error(error);
                return Promise.reject(error);
            }
        }
        trialJobDetail = new kubeflowData_1.KubeflowTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form, kubeflowJobName, curTrialSequenceId, trialJobDetailUrl, this.kubeflowJobPlural);
        await cpp.exec(`kubectl create -f ${kubeflowJobYamlPath}`);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        return Promise.resolve(trialJobDetail);
    }
    updateTrialJob(trialJobId, form) {
        throw new errors_1.MethodNotImplementedError();
    }
    listTrialJobs() {
        const jobs = [];
        this.trialJobsMap.forEach(async (value, key) => {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        });
        return Promise.resolve(jobs);
    }
    getTrialJob(trialJobId) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        const kubeflowTrialJob = this.trialJobsMap.get(trialJobId);
        if (!kubeflowTrialJob) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(kubeflowTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (!trialJobDetail) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} not found`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        if (!this.kubeflowJobPlural) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} failed because kubeflowJobPlural is undefined`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        const result = await cpp.exec(`kubectl delete ${this.kubeflowJobPlural} -l `
            + `app=${this.NNI_KUBEFLOW_TRIAL_LABEL},expId=${experimentStartupInfo_1.getExperimentId()},trialId=${trialJobId}`);
        if (result.stderr) {
            const errorMessage = `kubectl delete ${this.kubeflowJobPlural} for trial ${trialJobId} failed: ${result.stderr}`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        trialJobDetail.endTime = Date.now();
        trialJobDetail.status = utils_1.getJobCancelStatus(isEarlyStopped);
        return Promise.resolve();
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.KUBEFLOW_CLUSTER_CONFIG:
                this.kubeflowClusterConfig = JSON.parse(value);
                if (this.kubeflowClusterConfig.nfs) {
                    await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}`);
                    const nfsServer = this.kubeflowClusterConfig.nfs.server;
                    const nfsPath = this.kubeflowClusterConfig.nfs.path;
                    try {
                        await cpp.exec(`sudo mount ${nfsServer}:${nfsPath} ${this.trialLocalNFSTempFolder}`);
                    }
                    catch (error) {
                        const mountError = `Mount NFS ${nfsServer}:${nfsPath} to ${this.trialLocalNFSTempFolder} failed, error is ${error}`;
                        this.log.error(mountError);
                        throw new Error(mountError);
                    }
                }
                else if (this.kubeflowClusterConfig.keyVault && this.kubeflowClusterConfig.azureStorage) {
                    const vaultName = this.kubeflowClusterConfig.keyVault.vaultName;
                    const valutKeyName = this.kubeflowClusterConfig.keyVault.name;
                    this.azureStorageAccountName = this.kubeflowClusterConfig.azureStorage.accountName;
                    this.azureStorageShare = this.kubeflowClusterConfig.azureStorage.azureShare;
                    try {
                        const result = await cpp.exec(`az keyvault secret show --name ${valutKeyName} --vault-name ${vaultName}`);
                        if (result.stderr) {
                            const errorMessage = result.stderr;
                            this.log.error(errorMessage);
                            return Promise.reject(errorMessage);
                        }
                        const storageAccountKey = JSON.parse(result.stdout).value;
                        this.azureStorageClient = azure.createFileService(this.azureStorageAccountName, storageAccountKey);
                        await azureStorageClientUtils_1.AzureStorageClientUtility.createShare(this.azureStorageClient, this.azureStorageShare);
                        this.azureStorageSecretName = 'nni-secret-' + utils_1.uniqueString(8).toLowerCase();
                        await cpp.exec(`kubectl create secret generic ${this.azureStorageSecretName} `
                            + `--from-literal=azurestorageaccountname=${this.azureStorageAccountName} `
                            + `--from-literal=azurestorageaccountkey=${storageAccountKey}`);
                    }
                    catch (error) {
                        this.log.error(`command error: ${error}`);
                        throw new Error(error);
                    }
                }
                else {
                    const clusterConfigError = 'kubeflow cluster config format error!';
                    this.log.error(clusterConfigError);
                    throw new Error(clusterConfigError);
                }
                this.kubeflowJobPlural = kubeflowConfig_1.kubeflowOperatorMap.get(this.kubeflowClusterConfig.operator);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (!this.kubeflowClusterConfig) {
                    this.log.error('kubeflow cluster config is not initialized');
                    return Promise.reject(new Error('kubeflow cluster config is not initialized'));
                }
                this.kubeflowTrialConfig = JSON.parse(value);
                assert(this.kubeflowClusterConfig !== undefined && this.kubeflowTrialConfig.worker !== undefined);
                try {
                    await util_1.validateCodeDir(this.kubeflowTrialConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    return Promise.reject(new Error(error));
                }
                break;
            default:
                break;
        }
        return Promise.resolve();
    }
    getClusterMetadata(key) {
        return Promise.resolve('');
    }
    async cleanUp() {
        this.stopping = true;
        for (let [trialJobId, kubeflowTrialJob] of this.trialJobsMap) {
            if (['RUNNING', 'WAITING', 'UNKNOWN'].includes(kubeflowTrialJob.status)) {
                try {
                    await this.cancelTrialJob(trialJobId);
                }
                catch (error) { }
                kubeflowTrialJob.status = 'SYS_CANCELED';
            }
        }
        assert(this.kubeflowJobPlural !== undefined);
        try {
            await cpp.exec(`kubectl delete ${this.kubeflowJobPlural} -l app=${this.NNI_KUBEFLOW_TRIAL_LABEL},expId=${experimentStartupInfo_1.getExperimentId()}`);
        }
        catch (error) {
            this.log.error(`Delete ${this.kubeflowJobPlural} with label: app=${this.NNI_KUBEFLOW_TRIAL_LABEL},expId=${experimentStartupInfo_1.getExperimentId()} failed, error is ${error}`);
        }
        try {
            await cpp.exec(`sudo umount ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            this.log.error(`Unmount ${this.trialLocalNFSTempFolder} failed, error is ${error}`);
        }
        const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
        try {
            await restServer.stop();
            this.log.info('Kubeflow Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`Kubeflow Training service rest server stopped failed, error: ${error.message}`);
            Promise.reject(error);
        }
        return Promise.resolve();
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, psPodResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        const tfReplicaSpecsObj = {};
        tfReplicaSpecsObj.Worker = this.generateReplicaConfig(trialWorkingFolder, this.kubeflowTrialConfig.worker.replicas, this.kubeflowTrialConfig.worker.image, 'run_worker.sh', workerPodResources);
        if (this.kubeflowTrialConfig.ps) {
            tfReplicaSpecsObj.Ps = this.generateReplicaConfig(trialWorkingFolder, this.kubeflowTrialConfig.ps.replicas, this.kubeflowTrialConfig.ps.image, 'run_ps.sh', psPodResources);
        }
        return {
            apiVersion: 'kubeflow.org/v1alpha2',
            kind: 'TFJob',
            metadata: {
                name: kubeflowJobName,
                namespace: 'default',
                labels: {
                    app: this.NNI_KUBEFLOW_TRIAL_LABEL,
                    expId: experimentStartupInfo_1.getExperimentId(),
                    trialId: trialJobId
                }
            },
            spec: {
                tfReplicaSpecs: tfReplicaSpecsObj
            }
        };
    }
    generateReplicaConfig(trialWorkingFolder, replicaNumber, replicaImage, runScriptFile, podResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        let volumeSpecMap = new Map();
        if (this.kubeflowClusterConfig.nfs) {
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    nfs: {
                        server: `${this.kubeflowClusterConfig.nfs.server}`,
                        path: `${this.kubeflowClusterConfig.nfs.path}`
                    }
                }
            ]);
        }
        else if (this.kubeflowClusterConfig.azureStorage && this.kubeflowClusterConfig.keyVault) {
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    azureFile: {
                        secretName: `${this.azureStorageSecretName}`,
                        shareName: `${this.azureStorageShare}`,
                        readonly: false
                    }
                }
            ]);
        }
        else {
            const clusterConfigError = 'kubeflow cluster config format error!';
            this.log.error(clusterConfigError);
            throw new Error(clusterConfigError);
        }
        return {
            replicas: replicaNumber,
            template: {
                metadata: {
                    creationTimestamp: null
                },
                spec: {
                    containers: [
                        {
                            name: 'tensorflow',
                            image: replicaImage,
                            args: ["sh", `${path.join(trialWorkingFolder, runScriptFile)}`],
                            volumeMounts: [
                                {
                                    name: 'nni-vol',
                                    mountPath: this.CONTAINER_MOUNT_PATH
                                }
                            ],
                            resources: podResources
                        }
                    ],
                    restartPolicy: 'ExitCode',
                    volumes: volumeSpecMap.get('nniVolumes')
                }
            }
        };
    }
    genereateRunScript(trialJobId, trialWorkingFolder, command, trialSequenceId, roleType) {
        const runScriptLines = [];
        runScriptLines.push('#!/bin/bash');
        runScriptLines.push('export NNI_PLATFORM=kubeflow');
        runScriptLines.push(`export NNI_SYS_DIR=$PWD/nni/${trialJobId}`);
        runScriptLines.push(`export NNI_OUTPUT_DIR=${path.join(trialWorkingFolder, 'output', `${roleType}_output`)}`);
        runScriptLines.push('export MULTI_PHASE=false');
        runScriptLines.push(`export NNI_TRIAL_JOB_ID=${trialJobId}`);
        runScriptLines.push(`export NNI_EXP_ID=${experimentStartupInfo_1.getExperimentId()}`);
        runScriptLines.push(`export NNI_CODE_DIR=${trialWorkingFolder}`);
        runScriptLines.push(`export NNI_TRIAL_SEQ_ID=${trialSequenceId}`);
        if (this.kubeflowTrialConfig) {
            switch (roleType) {
                case 'ps':
                    if (this.kubeflowTrialConfig.ps && this.kubeflowTrialConfig.ps.gpuNum == 0) {
                        runScriptLines.push(`export CUDA_VISIBLE_DEVICES=''`);
                    }
                    break;
                case 'worker':
                    if (this.kubeflowTrialConfig.worker && this.kubeflowTrialConfig.worker.gpuNum == 0) {
                        runScriptLines.push(`export CUDA_VISIBLE_DEVICES=''`);
                    }
                    break;
                default:
                    break;
            }
        }
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        runScriptLines.push('mkdir -p $NNI_SYS_DIR');
        runScriptLines.push('mkdir -p $NNI_OUTPUT_DIR');
        runScriptLines.push('cp -rT $NNI_CODE_DIR $NNI_SYS_DIR');
        runScriptLines.push('cd $NNI_SYS_DIR');
        runScriptLines.push('sh install_nni.sh # Check and install NNI pkg');
        runScriptLines.push(`python3 -m nni_trial_tool.trial_keeper --trial_command '${command}' `
            + `--nnimanager_ip '${nniManagerIp}' --nnimanager_port '${this.kubeflowRestServerPort}' `
            + `1>$NNI_OUTPUT_DIR/trialkeeper_stdout 2>$NNI_OUTPUT_DIR/trialkeeper_stderr`);
        return runScriptLines.join('\n');
    }
    generateSequenceId() {
        if (this.nextTrialSequenceId === -1) {
            this.nextTrialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.nextTrialSequenceId++;
    }
};
KubeflowTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], KubeflowTrainingService);
exports.KubeflowTrainingService = KubeflowTrainingService;
