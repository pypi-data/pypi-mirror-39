# coding:utf-8

def get_host_ip():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def save_host_ip():
    import os
    import tempfile

    ip = get_host_ip()
    data_file = os.path.join(tempfile.gettempdir(), 'xpi_host_ip.txt')

    with open(data_file, 'wt') as f:
        f.write(ip)

    return ip


def read_host_ip():
    import os
    import tempfile

    data_file = os.path.join(tempfile.gettempdir(), 'xpi_host_ip.txt')

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            ip = f.read()
    else:
        ip = save_host_ip()

    return ip

