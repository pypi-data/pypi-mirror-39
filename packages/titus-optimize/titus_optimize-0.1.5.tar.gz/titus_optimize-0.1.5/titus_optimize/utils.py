import time
import ctypes
import io
import os
import platform
import subprocess
import sys
import tempfile
from contextlib import contextmanager


libc = ctypes.CDLL(None)
if platform.system() == 'Linux':
    c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
elif platform.system() == 'Darwin':
    c_stdout = ctypes.c_void_p.in_dll(libc, '__stdoutp')


@contextmanager
def stdout_redirector(stream):
    # The original fd stdout points to. Usually 1 on POSIX systems.
    original_stdout_fd = sys.stdout.fileno()

    def _redirect_stdout(to_fd):
        # Redirect stdout to the given file descriptor.
        # Flush the C-level buffer stdout
        libc.fflush(c_stdout)
        # Flush and close sys.stdout - also closes the file descriptor (fd)
        sys.stdout.close()
        # Make original_stdout_fd point to the same file as to_fd
        os.dup2(to_fd, original_stdout_fd)
        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # Save a copy of the original stdout fd in saved_stdout_fd
    saved_stdout_fd = os.dup(original_stdout_fd)
    try:
        # Create a temporary file and redirect stdout to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stdout(tfile.fileno())
        # Yield to caller, then redirect stdout back to the saved fd
        yield
        _redirect_stdout(saved_stdout_fd)
        # Copy contents of temporary file to the given stream
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read())
    finally:
        tfile.close()
        os.close(saved_stdout_fd)


def s3cp(src_path, dest_path, num_retries=3, quiet=True):
    num_tries = 0
    backoff_time_sec = 0.2
    src_path = src_path.replace("s3n://", "s3://")
    dest_path = dest_path.replace("s3n://", "s3://")
    args = ["aws", "s3", "cp"]
    if quiet:
        args.append("--quiet")
    args.extend([src_path, dest_path])
    while num_tries < 3:
        ret = subprocess.call(args)
        if ret != 0:
            num_tries += 1
            time.sleep(backoff_time_sec)
            backoff_time_sec *= 2
        else:
            break
    if ret != 0:
        raise Exception("Failed to copy %s to %s." % (src_path, dest_path))
