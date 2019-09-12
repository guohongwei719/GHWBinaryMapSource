#!/usr/bin/env python
# -*- coding: utf-8 -*-
#0.1.0


import lldb
import re
import os

# command 是用户输入的符号地址
def gMapSource(debugger, command, result, internal_dict):
    print('command: ' + command)
    savedFilePath = '/Users/guohongwei719/Desktop/GHWBinaryMapSource/script/path.txt'
    localSourceFilePath = '/Users/guohongwei719/Desktop/GHWBinaryMapSource/localPods/BinaryToSource'
    if command == '':
        print('没参数')
        current_path = os.getcwd()
        print('当前所在路径：' + current_path)
        interpreter = lldb.debugger.GetCommandInterpreter()
        returnObject = lldb.SBCommandReturnObject()
        file_handler = open(savedFilePath, 'r')
        content = file_handler.readlines()
        if len(content) == 2:
            filePath = content[0].replace('\n', '')
            sourcePath = content[1].replace('\n', '')
            # filePath = '/Users/guohongwei719/Desktop/test/MapSourceTest/MapSourceTest/GHWMapSourceTest.m'
            # sourcePath = '/Users/guohongwei719/Desktop/GHWBinaryMapSource/localPods/BinaryToSource/MapSourceTest/MapSourceTest/GHWMapSourceTest.m'
            print('filePath = ' + filePath)
            print('sourcePath = ' + sourcePath)
            interpreter.HandleCommand('settings set target.source-map ' + filePath + ' ' + sourcePath, returnObject)
            output = returnObject.GetOutput();
            print('output: ' + output)
            file_handler.close()
        else:
            print('缺失路径信息')


    else:
        print('有参数')

        # 获取 lldb 的命令交互环境，可以动态执行一些命令，比如 po obj
        interpreter = lldb.debugger.GetCommandInterpreter()
        # 创建一个对象，命令执行结果会通过该对象保存
        returnObject = lldb.SBCommandReturnObject()
        # 通过 image loopup 命令查找输入符号地址所在的编译模块信息
        interpreter.HandleCommand('image lookup -v --address ' + command, returnObject)
        # 获取返回结果
        output = returnObject.GetOutput();
        print('output: ' + output)

        # 下面的代码设计思想是：
        # 1、根据{地址}查找该地址所属的{源码编译路径}+{编译文件名}
        # 2、通过{编译文件名}动态在{指定路径}查找相应的{源码路径}
        # 3、将{源码编译路径}与{源码路径}映射

        # 实际使用时，可以参考下面的方案。
        # 1、根据{地址}查找该地址所属的{编译模块}。比如，SDWebImage
        # 2、通过脚本动态下载{编译模块}的{源码仓库}
        # 3、将{编译模块}与{源码仓库}映射



        # 通过正则获取二进制编译时，源码的真正路径
        filePath = re.match(r'(.|\n)*file = "(.*?)".*', output,re.M).group(2)
        print('filePath = ' + filePath)

        # 通过真正路径获取编译源文件的文件名
        fileName = re.match(r'/.*/(.*)', filePath).group(1)
        print('fileName = ' + fileName)
        # 通过文件名在 ~/MMAViewabilitySDK_iOS 目录（可以是任意的地址或者通过 git clone 动态下载）下查找源文件
        sourcePath = os.popen('mdfind -onlyin ' + localSourceFilePath + ' ' + fileName).read().replace('\n','')
        print('sourcePath = ' + sourcePath)

        current_path = os.getcwd()
        print('current_path = ' + current_path)

        txtFilePath = os.path.join(current_path, 'path.txt')
        print('txtFilePath = ' + txtFilePath)

        content = []

        content.append(filePath)
        content.append('\n')
        content.append(sourcePath)

        out = open(savedFilePath, 'w')
        out.writelines(content)
        out.close()


        # 通过 settings set target.source-map 命令执行编译源码位置与当前源码位置的映射
        interpreter.HandleCommand('settings set target.source-map ' + filePath + ' ' + sourcePath, returnObject)

# 添加一个 扩展命令 gMapSource
# 在 lldb 输入 mapSource 0x10803839 时，会执行 GHWBinaryMapSource.py 文件的 gMapSource 方法
def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add gMapSource -f GHWBinaryMapSource.gMapSource')
