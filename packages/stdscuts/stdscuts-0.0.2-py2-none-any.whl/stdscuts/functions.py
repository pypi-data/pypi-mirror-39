import os.path as op
import hashlib


def hash_file(file_path):
    """Utility for file hashing

    :param file_path: a valid path
    :return:
    """
    assert op.exists(file_path)
    h = hashlib.sha256()
    with open(file_path, 'rb', buffering=0) as f:
        for b in iter(lambda: f.read(128 * 1024), b''):
            h.update(b)
    return h.hexdigest()
