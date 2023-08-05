'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
exports.kubeflowOperatorMap = new Map([
    ['tf-operator', 'tfjobs'],
    ['pytorch-operator', 'pytorchjobs'],
    ['mxnet-operator', 'mxjobs'],
    ['caffe2-operator', 'caffe2jobs'],
    ['chainer-operator', 'chainerjobs'],
    ['mpi-operator', 'mpijobs']
]);
class KubeflowClusterConfig {
    constructor(operator, kubernetesServer, nfs, keyVault, azureStorage) {
        this.operator = operator;
        this.nfs = nfs;
        this.kubernetesServer = kubernetesServer;
        this.keyVault = keyVault;
        this.azureStorage = azureStorage;
    }
}
exports.KubeflowClusterConfig = KubeflowClusterConfig;
class NFSConfig {
    constructor(server, path) {
        this.server = server;
        this.path = path;
    }
}
exports.NFSConfig = NFSConfig;
class keyVaultConfig {
    constructor(vaultName, name) {
        this.vaultName = vaultName;
        this.name = name;
    }
}
exports.keyVaultConfig = keyVaultConfig;
class AzureStorage {
    constructor(azureShare, accountName) {
        this.azureShare = azureShare;
        this.accountName = accountName;
    }
}
exports.AzureStorage = AzureStorage;
class KubeflowTrialConfigTemplate {
    constructor(replicas, command, gpuNum, cpuNum, memoryMB, image) {
        this.replicas = replicas;
        this.command = command;
        this.gpuNum = gpuNum;
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
    }
}
exports.KubeflowTrialConfigTemplate = KubeflowTrialConfigTemplate;
class KubeflowTrialConfig {
    constructor(codeDir, worker, ps) {
        this.codeDir = codeDir;
        this.worker = worker;
        this.ps = ps;
    }
}
exports.KubeflowTrialConfig = KubeflowTrialConfig;
