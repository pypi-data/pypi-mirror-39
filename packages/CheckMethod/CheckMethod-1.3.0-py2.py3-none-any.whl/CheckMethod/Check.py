# coding:utf-8
"""
传入DataFrame某列
"""
import re
import tarfile

import pandas as pd
import paramiko
from .ReadXml import *
import os

def function_transfer(data_frame, column_name, function_name, value):
    return eval(function_name)(data_frame[column_name], value)


def equal(data_frame_one_column, value):
    count = 0
    for i in data_frame_one_column:
        count += 1
        if i != value:
            return i, count
    return None, "Pass"


def oneof(data_frame_one_column, value):
    count = 0
    right_set = value.split(',')
    # print(right_set)
    for i in data_frame_one_column:
        count += 1
        if i not in right_set:
            return i, count
    print("execute oneof check succeed")
    return None, "Pass"


def less_than_max_length(data_frame_one_column, value):
    count = 0
    for i in data_frame_one_column:
        count += 1
        if len(str(i)) > int(value):
            return i, count
    print("execute less_than_max_length check succeed")
    return None, "Pass"


def null_check(data_frame_one_column, value):
    count = 0
    for i in data_frame_one_column:
        count += 1
        if str(i) is "":
            return i, count
    print("execute less_than_max_length check succeed")
    return None, "Pass"


def contains_format(data_frame_one_column, value):
    count = 0
    pattern = re.compile(value)
    for i in data_frame_one_column:
        count += 1
        if re.match(pattern=pattern, string=i) is None:
            return i, count
    print("execute contains_format check successed")
    return None, "Pass"


def sign_check(data_frame_one_column, value):
    count = 0
    pattern = re.compile(value)
    for i in data_frame_one_column:
        count += 1
        if str(i).startswith("-"):
            return i, count
    print("execute contains_format check successed")
    return None, "Pass"


def not_check(data_frame_one_column, value):
    return None, "Pass"


def zero_check(data_frame_one_column, value):
    count = 0
    pattern = re.compile(value)
    for i in data_frame_one_column:
        count += 1
        if i != '0' and i != 0 and i != "0":
            return i, count
    print("execute contains_format check successed")
    return None, "Pass"

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def main():
    log = []
    # 上场文件路径
    ip, username, password, port, path, local_path = get_files_path()
    #清目录
    del_file(local_path)
    # ssh 过去打压缩包
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command('cd {0} ; tar -zcvf files.tar.gz *.csv;'.format(path))

    # 拽文件
    conn = paramiko.Transport((ip, int(port)))
    conn.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(conn)
    sftp.get(path+'/files.tar.gz','../Files/files.tar.gz')

    # 解压缩
    tar = tarfile.open('../Files/files.tar.gz', 'r')
    tar.extractall("../Files/")  # 可设置解压地址
    tar.close()

    # 上场文件检验规则
    rules = get_process_flow_path()
    for i in rules.keys():
        try:
            files_to_pd = pd.read_csv(local_path + i + ".csv", encoding="utf-8", sep=",", dtype=str)
        except:
            files_to_pd = pd.read_csv(local_path + i + ".csv", encoding="gbk", sep=",", dtype=str)
        finally:
            for j in rules[i]:
                temp, line_number = function_transfer(files_to_pd, j["column_name"], j["type"], j["value"])
                if temp is not None:
                    log.append(j["type"] + " check error " + "Files " + i + " value is error on lines: " + str(
                        line_number) + " column : " + j["column_name"] + " values " + temp)

    with open('log', 'w') as f:
        f.write("--------------check info----------------\n")
        for i in log:
            f.write(i)
            f.write('\n')


if __name__ == "__main__":
    main()
