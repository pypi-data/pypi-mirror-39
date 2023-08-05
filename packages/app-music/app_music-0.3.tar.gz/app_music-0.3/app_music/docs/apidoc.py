#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： apidoc.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/7/18 13:31
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------

import re
import subprocess
import os
import time
import platform


#   当前系统检索
def system_env_search():
    sysstr = platform.system()
    if sysstr == "Windows":
        system = 'win'
    elif sysstr == "Linux":
        system = 'linux'
    elif sysstr == "Darwin":
        system = 'mac'
    return system


#   nodejs环境检索
def nodeJs_env_search():
    #
    nodeJs_su = subprocess.Popen('node -v', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    nodeJs_sub = str(nodeJs_su.stdout.read())
    node_sub_strip = nodeJs_sub.lstrip("b'").rstrip("\r\n'")
    try:
        re.match('^v[0-9]+.[0-9]+.[0-9]+', node_sub_strip).span()
        print('nodejs环境正常')
        return True
    except:
        print('nodejs环境异常，请检查')
        return False


#   apidoc 命令生成
def apidoc(system):
    project = os.getcwd()
    if system == 'win':
        source_file = "".join([project, "\\app\\"])
        target_directory = "".join([project, "\\apidoc\\"])
    elif system == 'linux':
        source_file = "".join([project, "/app/"])
        target_directory = "".join([project, "/apidoc/"])
    elif system == 'mac':
        source_file = "".join([project, "/app/"])
        target_directory = "".join([project, "/apidoc/"])
    path_list = ['apidoc', ' -i ', source_file, ' -o ', target_directory]
    apidoc_commit = "".join(path_list)
    return apidoc_commit, target_directory


if __name__ == "__main__":
    #    判断当前系统版本
    system = system_env_search()
    Nodejs_State = nodeJs_env_search()
    time.sleep(0.5)
    if Nodejs_State:
        apidoc_commit, target_directory = apidoc(system)
        try:
            print('html文件生成开始,请稍后')
            nodeJs_su = subprocess.Popen(apidoc_commit, shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
            nodeJs_sub = str(nodeJs_su.stdout.read())
            print("接口文档html文件生成成功,保存路径为:" + target_directory)
            state = True
        except:
            print("接口文档html文件生成失败")
            state = False
    else:
        print('生成环境异常，请检查是否按照必要环境')
