import os
from datetime import datetime
from utils import get_time
from utils import id_generator

ids = id_generator(2000)

class FileManager:
    """
    Manager to handle log files
    """
    def __init__(self, filename, mode, enc):
        self.filename = filename
        self.mode = mode
        self.enc = enc
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding=self.enc)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close



def log_create(url, status, response):
    """

    :param url: url
    :param status: status of url from fetch_status
    :param response: HTTP response code
    :return:
    """
    with FileManager('response.txt', 'a', 'utf-8') as f:
        if status:
            f.write(f"Date: {get_time()}: {url} is up! [ID: {ids.__next__()} | Response Code: {response}]\n")
        else:
            f.write(f"Date: {get_time()}: {url} is DOWN [ID: {ids.__next__()} | Response Code: {response}]\n")
    f.close()