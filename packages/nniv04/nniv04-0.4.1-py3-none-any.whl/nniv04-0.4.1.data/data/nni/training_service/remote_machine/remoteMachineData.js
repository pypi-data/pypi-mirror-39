'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class RemoteMachineMeta {
    constructor(ip, port, username, passwd, sshKeyPath, passphrase) {
        this.ip = ip;
        this.port = port;
        this.username = username;
        this.passwd = passwd;
        this.sshKeyPath = sshKeyPath;
        this.passphrase = passphrase;
        this.gpuReservation = new Map();
    }
}
exports.RemoteMachineMeta = RemoteMachineMeta;
class RemoteCommandResult {
    constructor(stdout, stderr, exitCode) {
        this.stdout = stdout;
        this.stderr = stderr;
        this.exitCode = exitCode;
    }
}
exports.RemoteCommandResult = RemoteCommandResult;
class RemoteMachineTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form, sequenceId) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.sequenceId = sequenceId;
        this.tags = [];
    }
}
exports.RemoteMachineTrialJobDetail = RemoteMachineTrialJobDetail;
var ScheduleResultType;
(function (ScheduleResultType) {
    ScheduleResultType[ScheduleResultType["SUCCEED"] = 0] = "SUCCEED";
    ScheduleResultType[ScheduleResultType["TMP_NO_AVAILABLE_GPU"] = 1] = "TMP_NO_AVAILABLE_GPU";
    ScheduleResultType[ScheduleResultType["REQUIRE_EXCEED_TOTAL"] = 2] = "REQUIRE_EXCEED_TOTAL";
})(ScheduleResultType = exports.ScheduleResultType || (exports.ScheduleResultType = {}));
exports.REMOTEMACHINE_RUN_SHELL_FORMAT = `#!/bin/bash
export NNI_PLATFORM=remote NNI_SYS_DIR={0} NNI_TRIAL_JOB_ID={1} NNI_OUTPUT_DIR={0}
export MULTI_PHASE={7}
export NNI_TRIAL_SEQ_ID={8}
cd $NNI_SYS_DIR
echo $$ >{2}
eval {3}{4} 2>{5}
echo $? \`date +%s%3N\` >{6}`;
exports.HOST_JOB_SHELL_FORMAT = `#!/bin/bash
cd {0}
echo $$ >{1}
eval {2} >stdout 2>stderr
echo $? \`date +%s%3N\` >{3}`;
