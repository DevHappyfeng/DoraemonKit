#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import commands
import json
import string
import sys
from io import StringIO

curdir = os.path.abspath('.')
configFilePath = os.path.join(curdir,'dpconfig.json')

def dependConfig():
    with open(configFilePath, 'r') as f:
        f = open(configFilePath,'r')
        config = json.loads(f.read())
        if (isinstance(config, list) and len(config) > 0):
           return config
    return None


def getAnalyzeFiles():
    (status,output) = commands.getstatusoutput('git status')
    if status != 0:
        return None

    f = StringIO()
    f.writelines(output.decode('utf-8'))
    f.seek(0)
    
    files = []
    currentFile = os.path.basename(__file__)
    
    for line in f.readlines():
        line = line.rstrip()
        line = line.lstrip()
        line = line.strip()
        if (line.find('modified:') == 0 or line.find('new file:') == 0):
            components = line.split()
            if (len(components) > 0 and currentFile != os.path.basename(components[len(components)-1])):
                files.append(components[len(components)-1])
    f.close()
    return files


def shouldAnalyze(files,configFile):
    for file in files:
         (filepath,fileName) = os.path.split(file)
         print(filepath)
         if fileName == configFile:
            return 1 , file
    return 0 , file


def analyzeFile(aFile,aConfig):
    filePath = os.path.join(curdir,aFile)
    output = commands.getoutput('cat {0}'.format(filePath))
    output = output.decode("utf-8")
    for symbolStr in aConfig['forbiddenSymbol']:
        result = string.find(output,symbolStr)
        if result != -1:
            return 1,symbolStr
    return 0,symbolStr


def doAction():
    fileList = getAnalyzeFiles()
    if (fileList == None or len(fileList)<= 0):
        sys.exit(0)

    config = dependConfig()
    if config == None:
        sys.exit(0)
    for x in config:
        (result,file) = shouldAnalyze(fileList,x['targetFile'])
        if result == 0:
            continue
        (status,des)= analyzeFile(file,x)
        if status == 1:
            print('{0} exist invalid symbole {1}, which is configed in dpconfig.json'.format(file,des))
            sys.exit(1)
    sys.exit(0)

if __name__=='__main__':
    doAction()

