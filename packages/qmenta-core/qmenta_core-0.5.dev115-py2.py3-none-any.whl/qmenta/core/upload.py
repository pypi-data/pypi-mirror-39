from os import path
import time
import hashlib

from qmenta.core import platform, errors


"""
Handles the uploading of data to QMENTA platform.
"""


class UploadError(errors.Error):
    """
    When a problem occurs while uploading.
    """
    pass


class AlreadyUploadedError(UploadError):
    """
    When calling upload_file() twice on the same SingleUpload instance.
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
    """
    def __init__(self, auth, filename, file_info):
        self.auth = auth
        self.filename = filename
        self.file_info = file_info

        # Size in bytes of each chunk. Should be expressed as
        # a power of 2: 2**x.
        # Default value of x is 9 (chunk_size = 512 kB).
        # It is recommended to use the default value. We expose the variable
        # to speed up unit tests with tiny file sizes.
        kilo = 1024
        self._chunk_size = (2 ** 9) * kilo

        self.upload_id = self._get_upload_id(filename)
        self._upload_finished = False

    def _get_upload_id(self, file_path):
        m = hashlib.md5()
        m.update(str(file_path).encode("utf-8"))
        return str(time.time()).replace(".", "") + "_" + m.hexdigest()

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

    def upload_file(self, progress_callback=None):
        """
        Upload the file to the QMENTA platform.

        Parameters
        ----------
        progress_callback : function
            This function will be called when the upload progress changes.
            It must have three input parameters: 1. the amount of bytes
            uploaded, 2. total amount of bytes to upload, 3. Boolean which must
            be True when the upload is finished, or False otherwise.

        Returns
        -------
        The Response from the platform for the last uploaded chunk.

        Raises
        ------
        AlreadyUploadedError
        CanOnlyUploadZipFileError
        qmenta.core.errors.CannotReadFileError
        CannotUploadEmptyFileError
        """
        if self._upload_finished:
            raise AlreadyUploadedError(self.filename)

        def progress_cb(bytes_done, bytes_total, finished=False):
            if progress_callback:
                progress_callback(bytes_done, bytes_total, finished)

        fname = path.split(self.filename)[1]
        max_retries = 10

        if fname.split('.')[-1] != 'zip':
            raise CanOnlyUploadZipFileError(self.filename)

        try:
            file_size = path.getsize(self.filename)
        except OSError:
            raise errors.CannotReadFileError(self.filename)

        if file_size == 0:
            raise CannotUploadEmptyFileError(self.filename)

        # TODO: The code below was copied from mintapi and needs to be
        #   cleaned up. See IF-1111.
        with open(self.filename, "rb") as file_object:
            uploaded = 0
            chunk_num = 0
            retries_count = 0
            error_message = ""
            uploaded_bytes = 0
            response = None
            last_chunk = False

            while True:
                data = file_object.read(self._chunk_size)
                if not data:
                    break

                start_position = chunk_num * self._chunk_size
                end_position = start_position + self._chunk_size - 1
                bytes_to_send = self._chunk_size

                if end_position >= file_size:
                    last_chunk = True
                    end_position = file_size - 1
                    bytes_to_send = file_size - uploaded_bytes

                bytes_range = "bytes " + str(start_position) + "-" + \
                              str(end_position) + "/" + str(file_size)

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
                    uploaded_bytes += self._chunk_size
                elif int(response.status_code) == 200:
                    progress_cb(file_size, file_size, finished=True)
                    self._upload_finished = True
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

                uploaded += self._chunk_size
                progress_cb(uploaded, file_size)

        return response
