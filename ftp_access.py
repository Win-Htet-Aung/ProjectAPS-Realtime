import ftplib
import zipfile
import os
import csv

def download_file(host, user, pwd, filename):
    server = ftplib.FTP(host = host, user = user, passwd = pwd)
    pdir = os.path.dirname(os.path.abspath(__file__))
    file = open(f"{filename}", 'wb')
    server.retrbinary(f"RETR {filename}", file.write)
    file.close()

def extract_and_process(filename):
    pdir = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(pdir, filename[:-4])
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(pdir)

    files = os.listdir(path = dest)
    for f in files:
        if 'ReportPoints' in f and f.endswith('.csv'):
            with open(os.path.join(dest, f), 'rt') as file:
                data = file.readlines()
                for i in range(0, len(data), 10):
                    if i + 2 < len(data):
                        line1 = data[i].replace('\x00', '').strip()
                        line2 = data[i + 2].replace('\x00', '').strip()
                        print(line1)
                        print(line2)
            print('---')

extract_and_process('ftp_output.zip')
