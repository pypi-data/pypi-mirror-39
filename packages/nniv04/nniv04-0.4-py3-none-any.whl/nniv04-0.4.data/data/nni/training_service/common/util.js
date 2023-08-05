'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("../../common/utils");
async function validateCodeDir(codeDir) {
    let fileCount;
    try {
        fileCount = await utils_1.countFilesRecursively(codeDir);
    }
    catch (error) {
        throw new Error(`Call count file error: ${error}`);
    }
    if (fileCount && fileCount > 1000) {
        const errMessage = `Too many files(${fileCount} found}) in ${codeDir},`
            + ` please check if it's a valid code dir`;
        throw new Error(errMessage);
    }
    return fileCount;
}
exports.validateCodeDir = validateCodeDir;
