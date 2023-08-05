'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const joi = require('joi');
var ValidationSchemas;
(function (ValidationSchemas) {
    ValidationSchemas.SETCLUSTERMETADATA = {
        body: {
            machine_list: joi.array().items(joi.object({
                username: joi.string().required(),
                ip: joi.string().ip().required(),
                port: joi.number().min(1).max(65535).required(),
                passwd: joi.string().required(),
                sshKeyPath: joi.string(),
                passphrase: joi.string()
            })),
            trial_config: joi.object({
                image: joi.string().min(1),
                codeDir: joi.string().min(1).required(),
                dataDir: joi.string(),
                outputDir: joi.string(),
                cpuNum: joi.number().min(1),
                memoryMB: joi.number().min(100),
                gpuNum: joi.number().min(0),
                command: joi.string().min(1),
                virtualCluster: joi.string(),
                worker: joi.object({
                    replicas: joi.number().min(1).required(),
                    image: joi.string().min(1),
                    outputDir: joi.string(),
                    cpuNum: joi.number().min(1),
                    memoryMB: joi.number().min(100),
                    gpuNum: joi.number().min(0).required(),
                    command: joi.string().min(1).required()
                }),
                ps: joi.object({
                    replicas: joi.number().min(1).required(),
                    image: joi.string().min(1),
                    outputDir: joi.string(),
                    cpuNum: joi.number().min(1),
                    memoryMB: joi.number().min(100),
                    gpuNum: joi.number().min(0).required(),
                    command: joi.string().min(1).required()
                })
            }),
            pai_config: joi.object({
                userName: joi.string().min(1).required(),
                passWord: joi.string().min(1).required(),
                host: joi.string().min(1).required()
            }),
            kubeflow_config: joi.object({
                operator: joi.string().min(1).required(),
                nfs: joi.object({
                    server: joi.string().min(1).required(),
                    path: joi.string().min(1).required()
                }),
                kubernetesServer: joi.string().min(1),
                keyVault: joi.object({
                    vaultName: joi.string().regex(/^([0-9]|[a-z]|[A-Z]|-){1,127}$/),
                    name: joi.string().regex(/^([0-9]|[a-z]|[A-Z]|-){1,127}$/)
                }),
                azureStorage: joi.object({
                    accountName: joi.string().regex(/^([0-9]|[a-z]|[A-Z]|-){3,31}$/),
                    azureShare: joi.string().regex(/^([0-9]|[a-z]|[A-Z]|-){3,63}$/)
                })
            }),
            nni_manager_ip: joi.object({
                nniManagerIp: joi.string().min(1)
            })
        }
    };
    ValidationSchemas.STARTEXPERIMENT = {
        body: {
            experimentName: joi.string().required(),
            description: joi.string(),
            authorName: joi.string(),
            maxTrialNum: joi.number().min(0).required(),
            trialConcurrency: joi.number().min(0).required(),
            trainingServicePlatform: joi.string(),
            searchSpace: joi.string().required(),
            maxExecDuration: joi.number().min(0).required(),
            multiPhase: joi.boolean(),
            multiThread: joi.boolean(),
            advisor: joi.object({
                builtinAdvisorName: joi.string().valid('Hyperband'),
                codeDir: joi.string(),
                classFileName: joi.string(),
                className: joi.string(),
                classArgs: joi.any(),
                gpuNum: joi.number().min(0),
                checkpointDir: joi.string()
            }),
            tuner: joi.object({
                builtinTunerName: joi.string().valid('TPE', 'Random', 'Anneal', 'Evolution', 'SMAC', 'BatchTuner', 'GridSearch'),
                codeDir: joi.string(),
                classFileName: joi.string(),
                className: joi.string(),
                classArgs: joi.any(),
                gpuNum: joi.number().min(0),
                checkpointDir: joi.string()
            }),
            assessor: joi.object({
                builtinAssessorName: joi.string().valid('Medianstop'),
                codeDir: joi.string(),
                classFileName: joi.string(),
                className: joi.string(),
                classArgs: joi.any(),
                gpuNum: joi.number().min(0),
                checkpointDir: joi.string()
            }),
            clusterMetaData: joi.array().items(joi.object({
                key: joi.string(),
                value: joi.any()
            }))
        }
    };
    ValidationSchemas.UPDATEEXPERIMENT = {
        query: {
            update_type: joi.string().required().valid('TRIAL_CONCURRENCY', 'MAX_EXEC_DURATION', 'SEARCH_SPACE', 'MAX_TRIAL_NUM')
        },
        body: {
            id: joi.string().required(),
            revision: joi.number().min(0).required(),
            params: joi.object(ValidationSchemas.STARTEXPERIMENT.body).required(),
            execDuration: joi.number().required(),
            startTime: joi.number(),
            endTime: joi.number(),
            logDir: joi.string(),
            maxSequenceId: joi.number()
        }
    };
    ValidationSchemas.STARTTENSORBOARD = {
        query: {
            job_ids: joi.string().min(5).max(5).required()
        }
    };
    ValidationSchemas.STOPTENSORBOARD = {
        query: {
            endpoint: joi.string().uri().required()
        }
    };
})(ValidationSchemas = exports.ValidationSchemas || (exports.ValidationSchemas = {}));
