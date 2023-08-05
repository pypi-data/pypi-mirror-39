'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const crypto_1 = require("crypto");
const cpp = require("child-process-promise");
const fs = require("fs");
const os = require("os");
const path = require("path");
const ts_deferred_1 = require("ts-deferred");
const typescript_ioc_1 = require("typescript-ioc");
const util = require("util");
const datastore_1 = require("./datastore");
const experimentStartupInfo_1 = require("./experimentStartupInfo");
const manager_1 = require("./manager");
const trainingService_1 = require("./trainingService");
function getExperimentRootDir() {
    return path.join(os.homedir(), 'nni', 'experiments', experimentStartupInfo_1.getExperimentId());
}
exports.getExperimentRootDir = getExperimentRootDir;
function getLogDir() {
    return path.join(getExperimentRootDir(), 'log');
}
exports.getLogDir = getLogDir;
function getDefaultDatabaseDir() {
    return path.join(getExperimentRootDir(), 'db');
}
exports.getDefaultDatabaseDir = getDefaultDatabaseDir;
function getCheckpointDir() {
    return path.join(getExperimentRootDir(), 'checkpoint');
}
exports.getCheckpointDir = getCheckpointDir;
function mkDirP(dirPath) {
    const deferred = new ts_deferred_1.Deferred();
    fs.exists(dirPath, (exists) => {
        if (exists) {
            deferred.resolve();
        }
        else {
            const parent = path.dirname(dirPath);
            mkDirP(parent).then(() => {
                fs.mkdir(dirPath, (err) => {
                    if (err) {
                        deferred.reject(err);
                    }
                    else {
                        deferred.resolve();
                    }
                });
            }).catch((err) => {
                deferred.reject(err);
            });
        }
    });
    return deferred.promise;
}
exports.mkDirP = mkDirP;
function mkDirPSync(dirPath) {
    if (fs.existsSync(dirPath)) {
        return;
    }
    mkDirPSync(path.dirname(dirPath));
    fs.mkdirSync(dirPath);
}
const delay = util.promisify(setTimeout);
exports.delay = delay;
function charMap(index) {
    if (index < 26) {
        return index + 97;
    }
    else if (index < 52) {
        return index - 26 + 65;
    }
    else {
        return index - 52 + 48;
    }
}
function uniqueString(len) {
    if (len === 0) {
        return '';
    }
    const byteLength = Math.ceil((Math.log2(52) + Math.log2(62) * (len - 1)) / 8);
    let num = crypto_1.randomBytes(byteLength).reduce((a, b) => a * 256 + b, 0);
    const codes = [];
    codes.push(charMap(num % 52));
    num = Math.floor(num / 52);
    for (let i = 1; i < len; i++) {
        codes.push(charMap(num % 62));
        num = Math.floor(num / 62);
    }
    return String.fromCharCode(...codes);
}
exports.uniqueString = uniqueString;
function randomSelect(a) {
    assert(a !== undefined);
    return a[Math.floor(Math.random() * a.length)];
}
exports.randomSelect = randomSelect;
function parseArg(names) {
    if (process.argv.length >= 4) {
        for (let i = 2; i < process.argv.length - 1; i++) {
            if (names.includes(process.argv[i])) {
                return process.argv[i + 1];
            }
        }
    }
    return '';
}
exports.parseArg = parseArg;
function getMsgDispatcherCommand(tuner, assessor, advisor, multiPhase = false, multiThread = false) {
    if ((tuner || assessor) && advisor) {
        throw new Error('Error: specify both tuner/assessor and advisor is not allowed');
    }
    if (!tuner && !advisor) {
        throw new Error('Error: specify neither tuner nor advisor is not allowed');
    }
    let command = `python3 -m nni`;
    if (multiPhase) {
        command += ' --multi_phase';
    }
    if (multiThread) {
        command += ' --multi_thread';
    }
    if (advisor) {
        command += ` --advisor_class_name ${advisor.className}`;
        if (advisor.classArgs !== undefined) {
            command += ` --advisor_args ${JSON.stringify(JSON.stringify(advisor.classArgs))}`;
        }
        if (advisor.codeDir !== undefined && advisor.codeDir.length > 1) {
            command += ` --advisor_directory ${advisor.codeDir}`;
        }
        if (advisor.classFileName !== undefined && advisor.classFileName.length > 1) {
            command += ` --advisor_class_filename ${advisor.classFileName}`;
        }
    }
    else {
        command += ` --tuner_class_name ${tuner.className}`;
        if (tuner.classArgs !== undefined) {
            command += ` --tuner_args ${JSON.stringify(JSON.stringify(tuner.classArgs))}`;
        }
        if (tuner.codeDir !== undefined && tuner.codeDir.length > 1) {
            command += ` --tuner_directory ${tuner.codeDir}`;
        }
        if (tuner.classFileName !== undefined && tuner.classFileName.length > 1) {
            command += ` --tuner_class_filename ${tuner.classFileName}`;
        }
        if (assessor !== undefined && assessor.className !== undefined) {
            command += ` --assessor_class_name ${assessor.className}`;
            if (assessor.classArgs !== undefined) {
                command += ` --assessor_args ${JSON.stringify(JSON.stringify(assessor.classArgs))}`;
            }
            if (assessor.codeDir !== undefined && assessor.codeDir.length > 1) {
                command += ` --assessor_directory ${assessor.codeDir}`;
            }
            if (assessor.classFileName !== undefined && assessor.classFileName.length > 1) {
                command += ` --assessor_class_filename ${assessor.classFileName}`;
            }
        }
    }
    return command;
}
exports.getMsgDispatcherCommand = getMsgDispatcherCommand;
function generateParamFileName(hyperParameters) {
    assert(hyperParameters !== undefined);
    assert(hyperParameters.index >= 0);
    let paramFileName;
    if (hyperParameters.index == 0) {
        paramFileName = 'parameter.cfg';
    }
    else {
        paramFileName = `parameter_${hyperParameters.index}.cfg`;
    }
    return paramFileName;
}
exports.generateParamFileName = generateParamFileName;
function prepareUnitTest() {
    typescript_ioc_1.Container.snapshot(experimentStartupInfo_1.ExperimentStartupInfo);
    typescript_ioc_1.Container.snapshot(datastore_1.Database);
    typescript_ioc_1.Container.snapshot(datastore_1.DataStore);
    typescript_ioc_1.Container.snapshot(trainingService_1.TrainingService);
    typescript_ioc_1.Container.snapshot(manager_1.Manager);
    experimentStartupInfo_1.setExperimentStartupInfo(true, 'unittest', 8080);
    mkDirPSync(getLogDir());
    const sqliteFile = path.join(getDefaultDatabaseDir(), 'nni.sqlite');
    try {
        fs.unlinkSync(sqliteFile);
    }
    catch (err) {
    }
}
exports.prepareUnitTest = prepareUnitTest;
function cleanupUnitTest() {
    typescript_ioc_1.Container.restore(manager_1.Manager);
    typescript_ioc_1.Container.restore(trainingService_1.TrainingService);
    typescript_ioc_1.Container.restore(datastore_1.DataStore);
    typescript_ioc_1.Container.restore(datastore_1.Database);
    typescript_ioc_1.Container.restore(experimentStartupInfo_1.ExperimentStartupInfo);
}
exports.cleanupUnitTest = cleanupUnitTest;
let cachedipv4Address = '';
function getIPV4Address() {
    if (cachedipv4Address && cachedipv4Address.length > 0) {
        return cachedipv4Address;
    }
    if (os.networkInterfaces().eth0) {
        for (const item of os.networkInterfaces().eth0) {
            if (item.family === 'IPv4') {
                cachedipv4Address = item.address;
                return cachedipv4Address;
            }
        }
    }
    else {
        throw Error('getIPV4Address() failed because os.networkInterfaces().eth0 is undefined.');
    }
    throw Error('getIPV4Address() failed because no valid IPv4 address found.');
}
exports.getIPV4Address = getIPV4Address;
function getRemoteTmpDir(osType) {
    if (osType == 'linux') {
        return '/tmp';
    }
    else {
        throw Error(`remote OS ${osType} not supported`);
    }
}
exports.getRemoteTmpDir = getRemoteTmpDir;
function getJobCancelStatus(isEarlyStopped) {
    return isEarlyStopped ? 'EARLY_STOPPED' : 'USER_CANCELED';
}
exports.getJobCancelStatus = getJobCancelStatus;
function countFilesRecursively(directory, timeoutMilliSeconds) {
    if (!fs.existsSync(directory)) {
        throw Error(`Direcotory ${directory} doesn't exist`);
    }
    const deferred = new ts_deferred_1.Deferred();
    let timeoutId;
    const delayTimeout = new Promise((resolve, reject) => {
        timeoutId = setTimeout(() => {
            reject(new Error(`Timeout: path ${directory} has too many files`));
        }, 5000);
    });
    let fileCount = -1;
    cpp.exec(`find ${directory} -type f | wc -l`).then((result) => {
        if (result.stdout && parseInt(result.stdout)) {
            fileCount = parseInt(result.stdout);
        }
        deferred.resolve(fileCount);
    });
    return Promise.race([deferred.promise, delayTimeout]).finally(() => {
        clearTimeout(timeoutId);
    });
}
exports.countFilesRecursively = countFilesRecursively;
