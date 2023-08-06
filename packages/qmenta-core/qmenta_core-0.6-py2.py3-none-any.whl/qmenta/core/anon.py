import os
from zipfile import ZipFile
from tempfile import TemporaryDirectory

from qmenta.anon.auto import anonymise


def anonymise_zip(in_file, out_file):
    """
    Read the files of the input zip file, anonymise them, and write them
    to the output zip file.

    Parameters
    ----------
    in_file : str
        The name of the input zip file.
    out_file : str
        The name of the output zip file that will be created.

    Raises
    ------
    FileExistsError
        When the output zip file already exists
    OSError
        When there are problems with the reading or writing of files.
    zipfile.BadZipFile
        When the input file is not a proper zip file.
    """
    with ZipFile(in_file) as in_zip, ZipFile(out_file, mode='x') as out_zip, \
            TemporaryDirectory() as tmpdir:

        n = len(in_zip.infolist())
        # Do not use os.chdir here because that is not thread-safe. Instead,
        #   use absolute paths everywhere below when referring to files in
        #   the file system. Inside the zip-files we use relative paths.
        for i, zipinfo in enumerate(in_zip.infolist()):
            in_zip.extract(zipinfo, tmpdir)
            f_rel = zipinfo.filename
            f_abs = os.path.join(tmpdir, f_rel)
            if zipinfo.is_dir():
                print('Adding directory {}'.format(f_rel))
                out_zip.write(f_abs, f_rel)
                os.rmdir(f_abs)
            else:
                try:
                    print('Anonymising file {}/{} ({})'.format(i+1, n, f_abs))
                    status = anonymise(f_abs)
                except RuntimeError as e:
                    print('Failed to anonymise {}: {}'.format(f_abs, e))
                else:
                    if not status["OK"]:
                        print("Unknown file format. Skipping {}".format(f_abs))
                out_zip.write(f_abs, f_rel)
                # If the file was in a subdirectory, the directory will still
                #   exist in the temporary directory. They will be removed all
                #   together.
                os.remove(f_abs)
        print('Finished anonymisation')
