from os import path
import threading
import time
import hashlib
from blinker import signal
from enum import Enum

from qmenta.core import platform, errors


"""
Handles the uploading of data to QMENTA platform.
"""


class UploadError(errors.Error):
    """
    When a problem occurs while uploading.
    """
    pass


class UploadAlreadyStartedError(UploadError):
    """
    When calling upload_file() a second time and the upload is already
    in progress.
    """


class UploadAlreadyDoneError(UploadError):
    """
    When calling upload_file() a second time and the upload already finished.
    """
    pass


class CannotUploadEmptyFileError(UploadError):
    """
    When trying to upload a file with a size of 0 bytes.
    """


class CanOnlyUploadZipFileError(UploadError):
    """
    When trying to upload a non-zip file.
    """


class FileInfo:
    """
    Specifies the metadata of a file that will be uploaded to the platform.

    Parameters
    ----------
    project_id : int
        The ID of the project to which the new file will be added
    name : str
        The name of the file in the platform. It is recommended to use the
        filename (optional)
    date_of_scan : str
        The date when the scan was made (optional)
    description : str
        A description of the data that is uploaded (optional)
    subject_name : str
        The anonymised ID of the subject (optional)
    session_id : str
        The ID of the scanning session for the subject (optional).
        If left blank, the next numerical session ID for the subject will
        automatically be assigned to the session by the platform.
    input_data_type : str
        The analysis to be used to process the data (optional).
        When left blank, the input data type will be set automatically.
        It is recommended to leave it blank, except for testing specific tools
        for processing uploaded data.
    is_result : bool
        Default value: False. Set to True if the uploaded data is the output
        of an offline analysis.
    add_to_container_id : int
        ID of the container to which this file should be added (if id > 0).
        Default value: 0. When the value is 0, the data will be added to
        a new container.
    split_data : bool
        If True, the platform will try to split the uploaded file into
        different sessions. It will be ignored when the session_id is given.
        Default value: False.
    """
    def __init__(
        self, project_id, name='', date_of_scan='', description='',
        subject_name='', session_id='', input_data_type='', is_result=False,
        add_to_container_id=0, split_data=False
    ):
        self.project_id = project_id
        self.name = name
        self.date_of_scan = date_of_scan
        self.description = description
        self.subject_name = subject_name
        self.session_id = session_id

        if input_data_type:
            self.input_data_type = input_data_type
        else:
            if is_result:
                self.input_data_type = 'offline_analysis:1.0'
            else:
                self.input_data_type = 'qmenta_mri_brain_data:1.0'

        self.is_result = is_result
        self.add_to_container_id = add_to_container_id

        if session_id:
            self.split_data = False
        else:
            self.split_data = split_data

    def __repr__(self):
        return 'FileInfo({})'.format(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, FileInfo):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, FileInfo):
            return True
        return self.__dict__ != other.__dict__


class UploadStatus(Enum):
    """
    The current stage of a SingleUpload in the uploading process.
    """
    TO_START = 0
    UPLOADING = 1
    DONE = 2
    FAILED = 3


class SingleUpload():
    """
    Class to upload a single ZIP file to the platform

    Parameters
    ----------
    auth : Auth
        The object used to authenticate to the QMENTA platform.
    filename : str
        The file that will be uploaded.
    file_info : FileInfo
        All the metadata for the file to be stored in the platform.

    Attributes
    ----------
    upload_id : str
        The upload session ID. This will be automatically generated and
        depends on the current time and the filename.
    chunk_size : int
        Size in bytes of each chunk. Should be expressed as a power of 2.
        Default value is 512 KB.
        It is recommended to use the default value. We expose the variable
        to speed up unit tests with tiny file sizes.
    upload_index : int
        This vallue will be passed to the 'upload-status' and 'upload-progress'
        signals. It is set by MultipleThreadedUploads and used to quickly
        identify the upload that was updated. Default value: -1.
    file_size : int
        The size in bytes of the file to be uploaded. Automatically determined
        when the SingleUpload object is constructed.

    Raises
    ------
    CanOnlyUploadZipFileError
    CannotReadFileError
    CannotUploadEmptyFileError
    """
    def __init__(self, auth, filename, file_info):
        self.auth = auth
        self.filename = filename
        self.file_info = file_info

        self.chunk_size = (2 ** 9) * 1024

        self._status = UploadStatus.TO_START

        self.file_size = -1  # Will be set in _check_type_and_size
        self._bytes_uploaded = 0
        self.upload_index = -1

        self._status_signal = signal('upload-status')
        self._progress_signal = signal('upload-progress')

        self._check_file_type_and_size()
        self.upload_id = self._get_upload_id(filename)

    def _check_file_type_and_size(self):
        """
        Check that the file is a zip file larger than 0 bytes,
        and sets self.file_size.

        Raises
        ------
        CanOnlyUploadZipFileError
        qmenta.core.errors.CannotReadFileError
        CannotUploadEmptyFileError
        """
        fname = path.split(self.filename)[1]

        if fname.split('.')[-1] != 'zip':
            self.status = UploadStatus.FAILED
            raise CanOnlyUploadZipFileError(self.filename)

        try:
            self.file_size = path.getsize(self.filename)
        except OSError:
            self.status = UploadStatus.FAILED
            raise errors.CannotReadFileError(self.filename)

        if self.file_size == 0:
            self.status = UploadStatus.FAILED
            raise CannotUploadEmptyFileError(self.filename)

    def _get_upload_id(self, file_path):
        m = hashlib.md5()
        m.update(str(file_path).encode("utf-8"))
        return str(time.time()).replace(".", "") + "_" + m.hexdigest()

    @property
    def status(self):
        """
        UploadStatus: The current status of the upload.
        Setting the status will trigger signal('upload-status').
        """
        return self._status

    @status.setter
    def status(self, value):
        if self._status != value:
            self._status = value
            self._status_signal.send(self, upload_index=self.upload_index)

    @property
    def bytes_uploaded(self):
        """
        int: The amount of bytes that has been uploaded so far.
        When the value is updated, signal('upload-progress') is sent.
        """
        return self._bytes_uploaded

    @bytes_uploaded.setter
    def bytes_uploaded(self, value):
        if self._bytes_uploaded != value:
            self._bytes_uploaded = value
            self._progress_signal.send(self, upload_index=self.upload_index)

    def _add_upload_info_to_request_headers(self, upload_info, headers={}):
        headers["X-Mint-Name"] = upload_info.name
        headers["X-Mint-Date"] = upload_info.date_of_scan
        headers["X-Mint-Description"] = upload_info.description
        headers["X-Mint-Patient-Secret"] = upload_info.subject_name
        headers["X-Mint-SSID"] = upload_info.session_id
        headers["X-Mint-Project-Id"] = str(upload_info.project_id)
        headers["X-Mint-Split-Data"] = str(int(upload_info.split_data))

        if upload_info.input_data_type:
            headers["X-Mint-Type"] = upload_info.input_data_type

            if upload_info.is_result:
                headers["X-Mint-In-Out"] = "out"
            else:
                headers["X-Mint-In-Out"] = "in"

        if upload_info.add_to_container_id > 0:
            headers["X-Mint-Add-To"] = str(upload_info.add_to_container_id)
        return headers

    def _upload_chunk(self, data, range_str, length,
                      disposition, last_chunk,
                      file_info):
        request_headers = {}
        request_headers["Content-Type"] = "application/zip"
        request_headers["Content-Range"] = range_str
        request_headers['Session-ID'] = str(self.upload_id)
        request_headers["Content-Length"] = str(length)
        request_headers["Content-Disposition"] = disposition

        if last_chunk:
            self._add_upload_info_to_request_headers(
                file_info, request_headers)
            request_headers["X-Requested-With"] = "XMLHttpRequest"
            request_headers["X-Mint-Filename"] = path.split(self.filename)[1]

        # response_time = 120.0 if last_chunk else 900.0. See IF-1110.
        response = platform.post(
            auth=self.auth,
            endpoint='upload',
            data=data,
            headers=request_headers
        )
        return response

    def upload_file(self):
        """
        Upload the file to the QMENTA platform.
        Triggers signal('upload-progress') when bytes_uploaded is updated.
        Triggers signal('upload-status') when status is updated.

        Returns
        -------
        The Response from the platform for the last uploaded chunk.

        Raises
        ------
        UploadAlreadyDoneError
        UploadAlreadyStartedError
        errors.CannotReadFileError
        """
        if self.status in [UploadStatus.FAILED, UploadStatus.DONE]:
            raise UploadAlreadyDoneError(self.filename)
        elif self.status == UploadStatus.UPLOADING:
            raise UploadAlreadyStartedError(self.filename)

        fname = path.split(self.filename)[1]

        # TODO: The code below was copied from mintapi and needs to be
        #   cleaned up. See IF-1111.
        max_retries = 10
        with open(self.filename, "rb") as file_object:
            chunk_num = 0
            retries_count = 0
            error_message = ""
            self.bytes_uploaded = 0
            response = None
            last_chunk = False

            self.status = UploadStatus.UPLOADING
            while True:
                data = file_object.read(self.chunk_size)
                if not data:
                    self.status = UploadStatus.FAILED
                    raise errors.CannotReadFileError('Unexpeced end of file.')

                start_position = chunk_num * self.chunk_size
                end_position = start_position + self.chunk_size - 1
                bytes_to_send = self.chunk_size

                if end_position >= self.file_size:
                    last_chunk = True
                    end_position = self.file_size - 1
                    bytes_to_send = self.file_size - self.bytes_uploaded

                bytes_range = "bytes " + str(start_position) + "-" + \
                              str(end_position) + "/" + str(self.file_size)

                dispstr = "attachment; filename=%s" % fname

                response = self._upload_chunk(
                    data, bytes_range, bytes_to_send, dispstr,
                    last_chunk, self.file_info
                )

                if response is None:
                    retries_count += 1
                    time.sleep(retries_count * 5)
                    if retries_count > max_retries:
                        error_message = "HTTP Connection Problem"
                        break
                elif int(response.status_code) == 201:
                    chunk_num += 1
                    retries_count = 0
                    self.bytes_uploaded += self.chunk_size
                elif int(response.status_code) == 200:
                    self.bytes_uploaded = self.file_size
                    self.status = UploadStatus.DONE
                    break
                elif int(response.status_code) == 416:
                    retries_count += 1
                    time.sleep(retries_count * 5)
                    if retries_count > self.max_retries:
                        error_message = (
                            "Error Code: 416; "
                            "Requested Range Not Satisfiable (NGINX)")
                        break
                else:
                    retries_count += 1
                    time.sleep(retries_count * 5)
                    if retries_count > max_retries:
                        error_message = ("Number of retries has been reached. "
                                         "Upload process stops here !")
                        print(error_message)
                        break

        return response


class MultipleThreadedUploads():
    """
    Multiple uploads that are running in their own threads.
    signal('upload-progress') is triggered when a SingleUpload progress is
    changed. signal('upload-status') is triggered when a SingleUpload status is
    changed. Both signals are triggered with upload_index as a parameter.

    Parameters
    ----------
    auth : platform.Auth
        The Auth object to communicate with QMENTA platform

    Attributes
    ----------
    upload_list : list[SingleUpload]
        The SingleUpload objects that were added
    uploads_in_progress : int
        The number of uploads that are currently in progress
    """
    def __init__(self, auth):
        self.auth = auth
        self.upload_list = []
        self._last_upload_started_index = -1
        self.uploads_in_progress = 0
        self._max_parallel_uploads = 3

        on_status = signal('upload-status')
        on_status.connect(self._status_changed)

    @property
    def max_parallel_uploads(self):
        """
        int : The maximum number of uploads to be in progress at the same time.
        When files are added and less uploads are in progress than the maximum
        allowed parallel uploads, the new file upload is automatically started.
        If an upload finishes, the next queued file upload will automatically
        be started.
        Decreasing the value of max_parallel_uploads will not terminate
        uploads that are already in progress. Default value: 3.
        """
        return self._max_parallel_uploads

    @max_parallel_uploads.setter
    def max_parallel_uploads(self, value):
        if self._max_parallel_uploads != value:
            self._max_parallel_uploads = value
            can_start_upload = (self._last_upload_started_index <
                                len(self.upload_list) - 1)
            if self.uploads_in_progress < value and can_start_upload:
                self._start_next_upload()

    def add_upload(self, filename, file_info):
        """
        Add a new upload to the upload list.

        Parameters
        ----------
        filename : str
            The full path to the file to be uploaded.
        file_info : FileInfo
            The metadata of the file to be uploaded.
        """
        new_upload = SingleUpload(self.auth, filename, file_info)
        self.upload_list.append(new_upload)
        if self.uploads_in_progress < self.max_parallel_uploads:
            self._start_next_upload()

    def _status_changed(self, single_upload, upload_index):
        if single_upload.status in [
            UploadStatus.DONE, UploadStatus.FAILED
        ]:
            self.uploads_in_progress -= 1
            if self._last_upload_started_index < len(self.upload_list) - 1:
                self._start_next_upload()

    def _start_next_upload(self):
        self.uploads_in_progress += 1
        self._last_upload_started_index += 1
        single_upload = self.upload_list[self._last_upload_started_index]
        single_upload.upload_index = self._last_upload_started_index

        thread = threading.Thread(target=single_upload.upload_file)
        thread.start()
