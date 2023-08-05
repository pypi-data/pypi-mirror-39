'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const cpp = require("child-process-promise");
const path = require("path");
const os = require("os");
const ts_deferred_1 = require("ts-deferred");
const errors_1 = require("../../common/errors");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
var SSHClientUtility;
(function (SSHClientUtility) {
    async function copyDirectoryToRemote(localDirectory, remoteDirectory, sshClient, remoteOS) {
        const deferred = new ts_deferred_1.Deferred();
        const tmpTarName = `${utils_1.uniqueString(10)}.tar.gz`;
        const localTarPath = path.join(os.tmpdir(), tmpTarName);
        const remoteTarPath = path.join(utils_1.getRemoteTmpDir(remoteOS), tmpTarName);
        await cpp.exec(`tar -czf ${localTarPath} -C ${localDirectory} .`);
        await copyFileToRemote(localTarPath, remoteTarPath, sshClient);
        await cpp.exec(`rm ${localTarPath}`);
        await remoteExeCommand(`tar -oxzf ${remoteTarPath} -C ${remoteDirectory}`, sshClient);
        await remoteExeCommand(`rm ${remoteTarPath}`, sshClient);
        deferred.resolve();
        return deferred.promise;
    }
    SSHClientUtility.copyDirectoryToRemote = copyDirectoryToRemote;
    function copyFileToRemote(localFilePath, remoteFilePath, sshClient) {
        assert(sshClient !== undefined);
        const deferred = new ts_deferred_1.Deferred();
        sshClient.sftp((err, sftp) => {
            if (err) {
                log_1.getLogger().error(`copyFileToRemote: ${err.message}, ${localFilePath}, ${remoteFilePath}`);
                deferred.reject(err);
                return;
            }
            assert(sftp !== undefined);
            sftp.fastPut(localFilePath, remoteFilePath, (fastPutErr) => {
                sftp.end();
                if (fastPutErr) {
                    deferred.reject(fastPutErr);
                }
                else {
                    deferred.resolve(true);
                }
            });
        });
        return deferred.promise;
    }
    SSHClientUtility.copyFileToRemote = copyFileToRemote;
    function remoteExeCommand(command, client) {
        const deferred = new ts_deferred_1.Deferred();
        let stdout = '';
        let stderr = '';
        let exitCode;
        client.exec(command, (err, channel) => {
            if (err) {
                log_1.getLogger().error(`remoteExeCommand: ${err.message}`);
                deferred.reject(err);
                return;
            }
            channel.on('data', (data, dataStderr) => {
                if (dataStderr) {
                    stderr += data.toString();
                }
                else {
                    stdout += data.toString();
                }
            }).on('exit', (code, signal) => {
                exitCode = code;
                deferred.resolve({
                    stdout: stdout,
                    stderr: stderr,
                    exitCode: exitCode
                });
            });
        });
        return deferred.promise;
    }
    SSHClientUtility.remoteExeCommand = remoteExeCommand;
    function getRemoteFileContent(filePath, sshClient) {
        const deferred = new ts_deferred_1.Deferred();
        sshClient.sftp((err, sftp) => {
            if (err) {
                log_1.getLogger().error(`getRemoteFileContent: ${err.message}`);
                deferred.reject(new Error(`SFTP error: ${err.message}`));
                return;
            }
            try {
                const sftpStream = sftp.createReadStream(filePath);
                let dataBuffer = '';
                sftpStream.on('data', (data) => {
                    dataBuffer += data;
                }).on('error', (streamErr) => {
                    sftp.end();
                    deferred.reject(new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, streamErr.message));
                }).on('end', () => {
                    sftp.end();
                    deferred.resolve(dataBuffer);
                });
            }
            catch (error) {
                log_1.getLogger().error(`getRemoteFileContent: ${error.message}`);
                sftp.end();
                deferred.reject(new Error(`SFTP error: ${error.message}`));
            }
        });
        return deferred.promise;
    }
    SSHClientUtility.getRemoteFileContent = getRemoteFileContent;
})(SSHClientUtility = exports.SSHClientUtility || (exports.SSHClientUtility = {}));
