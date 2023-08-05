'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
const ts_deferred_1 = require("ts-deferred");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
var AzureStorageClientUtility;
(function (AzureStorageClientUtility) {
    async function createShare(fileServerClient, azureShare) {
        const deferred = new ts_deferred_1.Deferred();
        fileServerClient.createShareIfNotExists(azureShare, function (error, result, response) {
            if (error) {
                log_1.getLogger().error(`Create share failed:, ${error}`);
                deferred.reject(error);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    AzureStorageClientUtility.createShare = createShare;
    async function createDirectory(fileServerClient, azureFoler, azureShare) {
        const deferred = new ts_deferred_1.Deferred();
        fileServerClient.createDirectoryIfNotExists(azureShare, azureFoler, function (error, result, response) {
            if (error) {
                log_1.getLogger().error(`Create directory failed:, ${error}`);
                deferred.reject(error);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    AzureStorageClientUtility.createDirectory = createDirectory;
    async function createDirectoryRecursive(fileServerClient, azureDirectory, azureShare) {
        const deferred = new ts_deferred_1.Deferred();
        let directories = azureDirectory.split("/");
        let rootDirectory = "";
        for (let directory of directories) {
            rootDirectory += directory;
            await createDirectory(fileServerClient, rootDirectory, azureShare);
            rootDirectory += '/';
        }
        deferred.resolve();
        return deferred.promise;
    }
    AzureStorageClientUtility.createDirectoryRecursive = createDirectoryRecursive;
    async function uploadFileToAzure(fileServerClient, azureDirectory, azureFileName, azureShare, localFilePath) {
        const deferred = new ts_deferred_1.Deferred();
        await fileServerClient.createFileFromLocalFile(azureShare, azureDirectory, azureFileName, localFilePath, function (error, result, response) {
            if (error) {
                log_1.getLogger().error(`Upload file failed:, ${error}`);
                deferred.reject(error);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    async function downloadFile(fileServerClient, azureDirectory, azureFileName, azureShare, localFilePath) {
        const deferred = new ts_deferred_1.Deferred();
        await fileServerClient.getFileToStream(azureShare, azureDirectory, azureFileName, fs.createWriteStream(localFilePath), function (error, result, response) {
            if (error) {
                log_1.getLogger().error(`Download file failed:, ${error}`);
                deferred.reject(error);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    async function uploadDirectory(fileServerClient, azureDirectory, azureShare, localDirectory) {
        const deferred = new ts_deferred_1.Deferred();
        const fileNameArray = fs.readdirSync(localDirectory);
        await createDirectoryRecursive(fileServerClient, azureDirectory, azureShare);
        for (let fileName of fileNameArray) {
            const fullFilePath = path.join(localDirectory, fileName);
            try {
                if (fs.lstatSync(fullFilePath).isFile()) {
                    await uploadFileToAzure(fileServerClient, azureDirectory, fileName, azureShare, fullFilePath);
                }
                else {
                    await uploadDirectory(fileServerClient, azureDirectory + '/' + fileName, azureShare, fullFilePath);
                }
            }
            catch (error) {
                deferred.reject(error);
                return deferred.promise;
            }
        }
        deferred.resolve();
        return deferred.promise;
    }
    AzureStorageClientUtility.uploadDirectory = uploadDirectory;
    async function downloadDirectory(fileServerClient, azureDirectory, azureShare, localDirectory) {
        const deferred = new ts_deferred_1.Deferred();
        utils_1.mkDirP(localDirectory);
        fileServerClient.listFilesAndDirectoriesSegmented(azureShare, azureDirectory, 'null', function (error, result, response) {
            if (('entries' in result) === false) {
                log_1.getLogger().error(`list files failed, can't get entries in result`);
                throw new Error(`list files failed, can't get entries in result`);
            }
            if (('files' in result['entries']) === false) {
                log_1.getLogger().error(`list files failed, can't get files in result['entries']`);
                throw new Error(`list files failed, can't get files in result['entries']`);
            }
            if (('directories' in result['directories']) === false) {
                log_1.getLogger().error(`list files failed, can't get directories in result['entries']`);
                throw new Error(`list files failed, can't get directories in result['entries']`);
            }
            for (var fileName of result['entries']['files']) {
                const fullFilePath = path.join(localDirectory, fileName.name);
                downloadFile(fileServerClient, azureDirectory, fileName.name, azureShare, fullFilePath);
            }
            for (var directoryName of result['entries']['directories']) {
                const fullDirectoryPath = path.join(localDirectory, directoryName.name);
                const fullAzureDirectory = path.join(azureDirectory, directoryName.name);
                downloadDirectory(fileServerClient, fullAzureDirectory, azureShare, fullDirectoryPath);
            }
            deferred.resolve();
        });
        return deferred.promise;
    }
    AzureStorageClientUtility.downloadDirectory = downloadDirectory;
})(AzureStorageClientUtility = exports.AzureStorageClientUtility || (exports.AzureStorageClientUtility = {}));
