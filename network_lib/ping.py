import socket
import time

import requests


def tcp(host, port=80, count=1, timeout=1):
    result = []
    for _ in range(count):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start_time = time.time()
        try:
            s.connect((host, port))
            s.shutdown(socket.SHUT_RD)
            stop_time = time.time()
            result.append(round(1000 * (stop_time - start_time), 2))
        except socket.timeout:
            result.append(-1)
        except OSError as e:
            print("OS Error:", e)
            result.append(-1)
        finally:
            s.close()
    return result


def scan(host, ports=(22, 80, 443), timeout=5):
    scan_result = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            scan_result.append(True)
        else:
            scan_result.append(False)
    return scan_result


def speed_test(url, method='HEAD', proxy=None, count=1, timeout=5):
    result = []
    for _ in range(count):
        start_time = time.time()
        try:
            if method in ('HEAD', 'head'):
                requests.head(url, proxies=proxy, timeout=timeout)
            elif method in ('GET', 'get'):
                requests.get(url, proxies=proxy, timeout=timeout)
            stop_time = time.time()
            result.append(round(1000 * (stop_time - start_time), 2))
        except requests.exceptions.Timeout:
            result.append('-1')
    return result
