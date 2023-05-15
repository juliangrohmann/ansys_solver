import os
import sys
import socket


def init_scratch():
    home = os.path.expanduser('~')
    scratch_path = os.path.join(home, 'scratch')
    sys.path.append(scratch_path)

    return scratch_path


def init_ansys():
    from ansys.mapdl import core as pymapdl

    ansys_root = os.environ['ANSYS_ROOT']
    ansys_exe = os.path.join(ansys_root, 'v231', 'ansys', 'bin', 'ansys231')
    print(f"Setting ANSYS executable path: {ansys_exe}")
    pymapdl.change_default_ansys_path(ansys_exe)


def init_root():
    root = r'D:\georgia_tech\diverters\src'
    sys.path.append(root)
    return root


def is_local_port_open(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Set a timeout for the connection attempt
        sock.bind(('localhost', port))
        sock.close()
        return True
    except (socket.timeout, OSError):
        return False
