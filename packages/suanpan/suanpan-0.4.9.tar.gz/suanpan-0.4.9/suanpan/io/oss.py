# coding=utf-8
from __future__ import division, print_function

import os
import shutil
import zipfile

import math
import time
import oss2
from oss2.models import PartInfo
from oss2.resumable import ResumableDownloadStore, ResumableStore

from suanpan import asyncio, path
from suanpan.log import logger


class FrequenceTimeLimiter(object):
    def __init__(self, seconds):
        self.frequence = seconds
        self.time = time.time()

    def ifEnable(self):
        newTime = time.time()
        enable = self.frequence < newTime - self.time
        self.time = newTime if enable else self.time
        return enable


class OssStorage(object):

    DEFAULT_IGNORE_KEYWORDS = {"__MACOSX", ".DS_Store"}
    CONTENT_MD5 = "Content-MD5"

    LARGE_FILE_SIZE = 1024 * 1024  # 1GB
    PREFERRED_SIZE = 500 * 1024 # 500MB

    def __init__(
        self,
        ossAccessId,
        ossAccessKey,
        ossBucketName="suanpan",
        ossEndpoint="http://oss-cn-beijing.aliyuncs.com",
        ossDelimiter="/",
        ossTempStore="/tmp",
        ossDownloadNumThreads=1,
        ossDownloadStoreName=".py-oss-download",
        ossUploadNumThreads=1,
        ossUploadStoreName=".py-oss-upload",
        **kwargs
    ):
        self.accessId = ossAccessId
        self.accessKey = ossAccessKey
        self.bucketName = ossBucketName
        self.endpoint = ossEndpoint

        self.auth = oss2.Auth(self.accessId, self.accessKey)
        self.bucket = self.getBucket(self.bucketName)

        self.delimiter = ossDelimiter
        self.tempStore = ossTempStore

        self.downloadNumThreads = ossDownloadNumThreads
        self.downloadStoreName = ossDownloadStoreName
        self.downloadStore = ResumableDownloadStore(
            self.tempStore, self.downloadStoreName
        )

        self.uploadNumThreads = ossUploadNumThreads
        self.uploadStoreName = ossUploadStoreName
        self.uploadStore = ResumableStore(self.tempStore, self.uploadStoreName)

        self.removeOssLogger()

    def removeOssLogger(self):
        ossLogger = getattr(oss2, "logger", None)
        if ossLogger:
            self.removeLoggerHandlers(ossLogger)

    def removeLoggerHandlers(self, logger):
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        return logger


    def getBucket(self, bucketOrBucketName):
        return (
            bucketOrBucketName
            if isinstance(bucketOrBucketName, oss2.Bucket)
            else self.getBucketByName(bucketOrBucketName)
        )

    def getBucketByName(self, bucketName=None):
        return (
            oss2.Bucket(self.auth, self.endpoint, bucketName)
            if bucketName
            else self.bucket
        )

    def downloadIntoTempStore(
        self,
        name,
        path=None,
        tempStore=None,
        bucketOrBucketName=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        path = path or self.localPathJoin(bucket.bucket_name, name)
        path = self.getPathInTempStore(path, tempStore=tempStore)
        return self.download(name, path, bucketOrBucketName=bucket, ignore=ignore)

    def download(
        self, name, path, bucketOrBucketName=None, ignore=DEFAULT_IGNORE_KEYWORDS
    ):
        bucket = self.getBucket(bucketOrBucketName)
        downloadFunction = (
            self.downloadFile
            if self.isFile(name, bucketOrBucketName=bucket)
            else self.downloadFolder
        )
        return downloadFunction(name, path, bucketOrBucketName=bucket, ignore=ignore)

    def downloadFile(
        self,
        objectName,
        filepath,
        bucketOrBucketName=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        storagePath = self.storageUrl(bucket, objectName)

        if filepath in ignore:
            logger.info(
                "Ignore downloading file: {} -> {}".format(storagePath, filepath)
            )
            return filepath

        if self.checkMd5(objectName, filepath, bucketOrBucketName=bucket):
            logger.info("Ignore existed file: {} -> {}".format(storagePath, filepath))
            return filepath

        limiter = FrequenceTimeLimiter(seconds=5)

        def _percentage(consumed_bytes, total_bytes):
            if total_bytes and limiter.ifEnable():
                rate = round(consumed_bytes / total_bytes * 100, 2)
                logger.info(
                    "Downloading file: {} -> {} - {}".format(
                        storagePath, filepath, "{}%".format(rate)
                    )
                )

        logger.info("Downloading file: {} -> {}".format(storagePath, filepath))
        path.safeMkdirsForFile((filepath))
        oss2.resumable_download(
            bucket,
            objectName,
            filepath,
            num_threads=self.downloadNumThreads,
            store=self.downloadStore,
            progress_callback=_percentage,
        )
        logger.info("Downloaded file: {} -> {}".format(storagePath, filepath))
        return filepath

    def downloadFolder(
        self,
        folderName,
        folderpath,
        delimiter=None,
        bucketOrBucketName=None,
        workers=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        storagePath = self.storageUrl(bucket, folderName)

        if folderpath in ignore:
            logger.info(
                "Ignore downloading folder: {} -> {}".format(folderpath, storagePath)
            )
            return folderpath

        logger.info("Downloading folder: {} -> {}".format(storagePath, folderpath))
        with asyncio.multiThread(workers) as pool:
            for _, _, files in self.walk(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            ):
                for file in files:
                    filepath = self.localPathJoin(
                        folderpath, self.ossRelativePath(file, folderName)
                    )
                    pool.apply_async(
                        self.downloadFile,
                        args=(file, filepath),
                        kwds={"bucketOrBucketName": bucket, "ignore": ignore},
                    )
        self.removeIgnore(folderpath, ignore=ignore)
        logger.info("Downloaded folder: {} -> {}".format(storagePath, folderpath))
        return folderpath

    def uploadFromTempStore(
        self,
        name,
        path=None,
        tempStore=None,
        bucketOrBucketName=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        path = path or self.localPathJoin(bucket.bucket_name, name)
        path = self.getPathInTempStore(path, tempStore=tempStore)
        return self.upload(name, path, bucketOrBucketName=bucket, ignore=ignore)

    def upload(
        self, name, path, bucketOrBucketName=None, ignore=DEFAULT_IGNORE_KEYWORDS
    ):
        bucket = self.getBucket(bucketOrBucketName)
        uploadFunction = self.uploadFolder if os.path.isdir(path) else self.uploadFile
        return uploadFunction(name, path, bucketOrBucketName=bucket, ignore=ignore)

    def uploadFile(
        self,
        objectName,
        filepath,
        bucketOrBucketName=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        storagePath = self.storageUrl(bucket, objectName)

        if filepath in ignore:
            logger.info("Ignore uploading file: {} -> {}".format(filepath, storagePath))
            return filepath

        fileMd5 = path.md5(filepath)
        if self.getMd5(objectName, bucketOrBucketName=bucket) == fileMd5:
            logger.info("Ignore existed file: {} -> {}".format(filepath, storagePath))
            return filepath

        limiter = FrequenceTimeLimiter(seconds=5)

        def _percentage(consumed_bytes, total_bytes):
            if total_bytes and limiter.ifEnable():
                rate = round(consumed_bytes / total_bytes * 100, 2)
                logger.info(
                    "Uploading file: {} -> {} - {}".format(
                        filepath, storagePath, "{}%".format(rate)
                    )
                )

        logger.info("Uploading file: {} -> {}".format(filepath, storagePath))
        oss2.resumable_upload(
            bucket,
            objectName,
            filepath,
            num_threads=self.uploadNumThreads,
            store=self.uploadStore,
            progress_callback=_percentage,
            headers={self.CONTENT_MD5: fileMd5},
        )
        logger.info("Uploaded file: {} -> {}".format(filepath, storagePath))
        return filepath

    def uploadFolder(
        self,
        folderName,
        folderpath,
        bucketOrBucketName=None,
        workers=None,
        ignore=DEFAULT_IGNORE_KEYWORDS,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        storagePath = self.storageUrl(bucket, folderName)

        if folderName in ignore:
            logger.info(
                "Ignore uploading folder: {} -> {}".format(folderName, storagePath)
            )
            return folderpath

        logger.info("Uploading folder: {} -> {}".format(folderpath, storagePath))
        with asyncio.multiThread(workers) as pool:
            for root, _, files in os.walk(folderpath):
                for file in files:
                    filepath = os.path.join(root, file)
                    objectName = self.ossPathJoin(
                        folderName, self.localRelativePath(filepath, folderpath)
                    )
                    pool.apply_async(
                        self.uploadFile,
                        args=(objectName, filepath),
                        kwds={"bucketOrBucketName": bucket, "ignore": ignore},
                    )
        logger.info("Uploaded folder: {} -> {}".format(folderpath, storagePath))
        return folderpath

    def walk(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        root = folderName if folderName.endswith(delimiter) else folderName + delimiter
        folders = []
        files = []
        for obj in oss2.ObjectIterator(bucket, delimiter=delimiter, prefix=root):
            array = folders if obj.is_prefix() else files
            array.append(obj.key)
        if not folders and not files:
            storagePath = self.storageUrl(bucket, root)
            raise Exception("Oss Error: No such folder: {}".format(storagePath))
        yield root, folders, files
        for folder in folders:
            for item in self.walk(
                folder, delimiter=delimiter, bucketOrBucketName=bucket
            ):
                yield item

    def listAll(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        prefix = (
            folderName if folderName.endswith(delimiter) else folderName + delimiter
        )
        return (
            obj
            for obj in oss2.ObjectIterator(
                delimiter=delimiter, prefix=prefix, bucket=bucket
            )
        )

    def listFolders(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        return (
            obj
            for obj in self.listAll(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            )
            if obj.is_prefix()
        )

    def listFiles(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        return (
            obj
            for obj in self.listAll(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            )
            if not obj.is_prefix()
        )

    def isFile(self, objectName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return bucket.object_exists(objectName)

    def isFolder(self, folderName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return next(self.listAll(folderName, bucketOrBucketName=bucket), None)

    def getPathInTempStore(self, path, tempStore=None):
        tempStore = tempStore or self.tempStore
        return self.localPathJoin(tempStore, path)

    def toLocalPath(self, objectName, delimiter=None):
        delimiter = delimiter or self.delimiter
        return objectName.replace(delimiter, os.sep)

    def toOssPath(self, path, delimiter=None):
        delimiter = delimiter or self.delimiter
        return path.replace(os.sep, delimiter)

    def localPathJoin(self, *paths):
        path = os.path.join(*paths)
        return self.toLocalPath(path)

    def ossPathJoin(self, *paths):
        path = os.path.join(*paths)
        return self.toOssPath(path)

    def pathJoin(self, *paths, **kwargs):
        mode = kwargs.get("mode", "oss")
        return self.ossPathJoin(*paths) if mode == "oss" else self.localPathJoin(*paths)

    def localRelativePath(self, path, base):
        return self.relativePath(path, base, delimiter=os.sep)

    def ossRelativePath(self, path, base, delimiter=None):
        delimiter = delimiter or self.delimiter
        return self.relativePath(path, base, delimiter=delimiter)

    def relativePath(self, path, base, delimiter):
        base = base if base.endswith(delimiter) else base + delimiter
        return path[len(base) :] if path.startswith(base) else path

    def compress(self, zipFilePath, path, ignore=DEFAULT_IGNORE_KEYWORDS):
        compressFunc = self.compressFolder if os.path.isdir(path) else self.compressFile
        return compressFunc(zipFilePath, path)

    def compressFolder(self, zipFilePath, folderpath, ignore=DEFAULT_IGNORE_KEYWORDS):
        if folderpath in ignore:
            logger.info(
                "Ignore compressing folder: {} -> {}".format(folderpath, zipFilePath)
            )
            return zipFilePath

        logger.info("Compressing folder: {} -> {}".format(folderpath, zipFilePath))
        with zipfile.ZipFile(zipFilePath, "w") as zip:
            for root, _, files in os.walk(folderpath):
                for file in files:
                    filepath = os.path.join(root, file)
                    zip.write(
                        filepath, arcname=self.localRelativePath(filepath, folderpath)
                    )
        logger.info("Compressed folder: {} -> {}".format(folderpath, zipFilePath))
        return zipFilePath

    def compressFile(self, zipFilePath, filepath, ignore=DEFAULT_IGNORE_KEYWORDS):
        if filepath in ignore:
            logger.info(
                "Ignore compressing File: {} -> {}".format(filepath, zipFilePath)
            )
            return zipFilePath

        logger.info("Compressing File: {} -> {}".format(filepath, zipFilePath))
        with zipfile.ZipFile(zipFilePath, "w") as zip:
            _, filename = os.path.split(filepath)
            zip.write(filepath, arcname=filename)
        logger.info("Compressed File: {} -> {}".format(filepath, zipFilePath))
        return zipFilePath

    def extract(self, zipFilePath, distPath, ignore=DEFAULT_IGNORE_KEYWORDS):
        logger.info("Extracting zip: {} -> {}".format(zipFilePath, distPath))
        with zipfile.ZipFile(zipFilePath, "r") as zip:
            zip.extractall(distPath)
        self.removeIgnore(distPath, ignore=ignore)
        logger.info("Extracted zip: {} -> {}".format(zipFilePath, distPath))

    def remove(self, objectName, delimiter=None, bucketOrBucketName=None):
        delimiter = delimiter or self.delimiter
        bucket = self.getBucket(bucketOrBucketName)
        removeFunc = (
            self.removeFile
            if self.isFile(objectName, bucketOrBucketName=bucket)
            else self.removeFolder
        )
        removeFunc(objectName, delimiter=delimiter, bucketOrBucketName=bucket)

    def removeFile(self, fileName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        bucket.delete_object(fileName)
        storagePath = self.storageUrl(bucket, fileName)
        logger.info("Removed File: {}".format(storagePath))

    def removeFolder(self, folderName, delimiter=None, bucketOrBucketName=None):
        delimiter = delimiter or self.delimiter
        bucket = self.getBucket(bucketOrBucketName)
        folderName = (
            folderName + delimiter if not folderName.endswith(delimiter) else folderName
        )
        for obj in oss2.ObjectIterator(bucket, delimiter=delimiter, prefix=folderName):
            if not obj.is_prefix():
                self.removeFile(obj.key, delimiter=delimiter, bucketOrBucketName=bucket)
            else:
                self.removeFolder(
                    obj.key, delimiter=delimiter, bucketOrBucketName=bucket
                )
        storagePath = self.storageUrl(bucket, folderName)
        logger.info("Removed Folder: {}".format(storagePath))

    def storageUrl(self, bucket, path):
        return "oss:///" + self.ossPathJoin(bucket.bucket_name, path)

    def removeIgnore(self, path, ignore=DEFAULT_IGNORE_KEYWORDS):
        def _ignore(_root, _path):
            if _path in ignore:
                _path = os.path.join(_root, _path)
                if os.path.isfile(_path):
                    os.remove(_path)
                    logger.info("Removed ignore file: {}".format(_path))
                else:
                    shutil.rmtree(_path)
                    logger.info("Removed ignore folder: {}".format(_path))

        for root, folders, files in os.walk(path):
            for folder in folders:
                _ignore(root, folder)
            for file in files:
                _ignore(root, file)

    def getMd5(self, objectName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        try:
            return bucket.head_object(objectName).headers.get(self.CONTENT_MD5)
        except:
            return None

    def checkMd5(self, objectName, filePath, bucketOrBucketName=None):
        if not os.path.isfile(filePath):
            return False

        bucket = self.getBucket(bucketOrBucketName)
        return self.getMd5(objectName, bucketOrBucketName=bucket) == path.md5(filePath)

    def copy(self, name, dist, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        copyFunction = (
            self.copyFile
            if self.isFile(name, bucketOrBucketName=bucket)
            else self.copyFolder
        )
        return copyFunction(name, dist, bucketOrBucketName=bucket)

    def copyFolder(self, folderName, distName, bucketOrBucketName=None, workers=None, delimiter=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        folderName = folderName if folderName.endswith(delimiter) else folderName + delimiter
        distName = distName if distName.endswith(delimiter) else distName + delimiter
        logger.info("Copying folder: {} -> {}".format(folderName, distName))
        with asyncio.multiThread(workers) as pool:
            for _, _, files in self.walk(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            ):
                for file in files:
                    dist = file.replace(folderName, distName)
                    pool.apply_async(
                        self.copyFile,
                        args=(file, dist),
                        kwds={"bucketOrBucketName": bucket},
                    )
        logger.info("Copied folder: {} -> {}".format(folderName, distName))

    def copyFile(self, objectName, distName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        fileSize = bucket.head_object(objectName).content_length
        copyFunction = self.copyLargeFile if fileSize >= self.LARGE_FILE_SIZE else self.copySmallFile
        return copyFunction(objectName, distName, fileSize, bucketOrBucketName=bucket)

    def copySmallFile(self, objectName, distName, size, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        logger.info("Copying file: {} -> {}".format(objectName, distName))
        bucket.copy_object(bucket.bucket_name, objectName, distName)
        logger.info("Copied file: {} -> {}".format(objectName, distName))

    def copyLargeFile(self, objectName, distName, size, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        logger.info("Copying file: {} -> {}".format(objectName, distName))
        partSize = oss2.determine_part_size(size, preferred_size=self.PREFERRED_SIZE)
        uploadId = bucket.init_multipart_upload(distName).upload_id
        parts = math.ceil(size / partSize)
        parts = ((i+1, i*partSize, min((i+1)*partSize, size)) for i in range(parts))

        def _copy(part):
            partNumber, byteRange = part[0], part[1:2]
            result = bucket.upload_part_copy(bucket.bucket_name, objectName, byteRange, distName, uploadId, partNumber)
            return PartInfo(partNumber, result.etag)

        parts = [_copy(part) for part in parts]
        bucket.complete_multipart_upload(distName, uploadId, parts)
        logger.info("Copied file: {} -> {}".format(objectName, distName))
