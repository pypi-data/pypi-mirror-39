'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class PAITrialJobDetail {
    constructor(id, status, paiJobName, submitTime, workingDirectory, form, sequenceId, hdfsLogPath) {
        this.id = id;
        this.status = status;
        this.paiJobName = paiJobName;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.sequenceId = sequenceId;
        this.tags = [];
        this.hdfsLogPath = hdfsLogPath;
    }
}
exports.PAITrialJobDetail = PAITrialJobDetail;
exports.PAI_INSTALL_NNI_SHELL_FORMAT = `#!/bin/bash
if python3 -c 'import nni' > /dev/null 2>&1; then
  # nni module is already installed, skip
  return
else
  # Install nni
  python3 -m pip install --user nni
fi`;
exports.PAI_TRIAL_COMMAND_FORMAT = `export NNI_PLATFORM=pai NNI_SYS_DIR={0} NNI_OUTPUT_DIR={1} NNI_TRIAL_JOB_ID={2} NNI_EXP_ID={3} NNI_TRIAL_SEQ_ID={4}
&& cd $NNI_SYS_DIR && sh install_nni.sh 
&& python3 -m nni_trial_tool.trial_keeper --trial_command '{5}' --nnimanager_ip '{6}' --nnimanager_port '{7}' 
--pai_hdfs_output_dir '{8}' --pai_hdfs_host '{9}' --pai_user_name {10}`;
exports.PAI_OUTPUT_DIR_FORMAT = `hdfs://{0}:9000/`;
exports.PAI_LOG_PATH_FORMAT = `http://{0}/webhdfs/explorer.html#{1}`;
