#coding=utf-8
'''
Created on 2015年3月18日

@author: fengping.hu
'''

import types
import re
import os
import copy


class PDxIni:
    """Ini文件解析类库"""
    def __init__(self,filename):
        self.sectionReg = r'^/s*/[/w*/]/s*$'#分段正则
        self.f = file(filename,'r')
        self.sectionValues = []
        self.sections = {}
        self.__paserIni__()
        self.sectionCount = 0
        
    def __del__(self):#释放时触发
        self.updateIniFile()
        self.f.close()
       
    def __paserIni__(self):
        i = 0       
        for line in self.f:
            sectionMatch = re.search(r'^/s*/[/w*/]/s*$',line)         
            line = line.strip()         
            if sectionMatch and (sectionMatch.start()==0):
                tmpSection = line.replace('[',']').replace('','')
                self.sectionValues.append(tmpSection)
                self.sections[tmpSection]={}#本节的数据信息
                self.sections[tmpSection]['index'] = i
                self.sections[tmpSection]['count'] = 0
                self.sectionCount = i
                i += 1
                j = 0
            else:
                line = re.sub(';.*','',line)#去掉注释
                if tmpSection != '':               
                    KeyValue= line.split('=',1)
                    if len(KeyValue) == 2:
                        self.sections[tmpSection][KeyValue[0]] = {} 
                        self.sections[tmpSection][KeyValue[0]]['value']=KeyValue[1]
                        self.sections[tmpSection][KeyValue[0]]['index'] = j                 
                        j += 1
                        self.sections[tmpSection]['count']= j
                     
    def __readValue__(self,sectionName,key,defaultvalue):
        try:         
            ValueList = self.sections[sectionName]
            try:
                return ValueList[key]['value']
            except:
                return defaultvalue
        except:
            return defaultvalue
       
    def readString(self,sectionName,key,defaultvalue):
        """读取字符串,SectionName指定节点,Key指定关键字,DefaultValue指定默认字符串"""
        if type(defaultvalue) == types.StringType:
            return self.__readValue__(sectionName,key,defaultvalue)
        else:
            print 'defaultvalue must String'
          
    def readInteger(self,sectionName,key,defaultvalue):
        """读取整数,SectionName指定节点,Key指定关键字,DefaultValue指定整数"""
        if type(defaultvalue) == types.IntType:
            return self.__readValue__(sectionName,key,defaultvalue)
        else:
            print 'defaultvalue must Integer'
    def readBool(self,sectionName,key,defaultvalue):
        """读取Boolean值,SectionName指定节点,Key指定关键字,DefaultValue指定默认Boolean值"""
        if type(defaultvalue) == types.BooleanType:
            return self.__readValue__(sectionName,key,defaultvalue)
        else:
            'print defaultvalue must Boolean'
   
    def __writeValue__(self,SectionName,Key,Value):
        try:
            ValueList = self.sections[SectionName]
            self.sections[self.tmpSection]['index'] = self.sectionCount
            ValueList[Key]['index'] = self.sections[SectionName]['count']
        except:
            self.sectionValues.append(SectionName)
            self.sections[SectionName] = {}
            self.sections[SectionName]['index'] = self.sectionCount
            ValueList = self.sections[SectionName]
            ValueList['count'] = 1
            ValueList[Key] = {}
            ValueList[Key]['index'] = 0         
            ValueList[Key]['value'] = Value       
    def writeInteger(self,SectionName,Key,Value):
        """写入整数,SectionName指定节点,Key指定关键字,Value指定写入数据"""
        if type(Value) == types.IntType:
            self.__writeValue__(SectionName,Key,Value)
        else:
            print 'error'

    def writeString(self,SectionName,Key,Value):
        """写入字符串,SectionName指定节点,Key指定关键字,Value指定写入数据"""
        if type(Value) ==  types.StringType:
            self.__writeValue__(SectionName,Key,Value)
        else:
            print 'write String Error'

    def writeBool(self,SectionName,Key,Value):
        """写入Boolean,SectionName指定节点,Key指定关键字,Value指定写入数据"""
        if type(Value) ==  types.BooleanType:
            self.__writeValue__(SectionName,Key,Value)
        else:
            print 'write Boolean Error'   

    def getSections(self):
        """获取节点信息"""
        return self.sectionValues

    def getSectionKeys(self,SectionName):
        """获取某个节点下的所有Key信息"""
        SectionDict = copy.deepcopy(self.sections[SectionName])#使用深拷贝生成一个新的数据
        SectionDict.pop('count')
        SectionDict.pop('index')
        return [KeyValue[0] for KeyValue in sorted(SectionDict.items(),key=lambda m: m[1]['index'])]       

    def sectionKeyValues(self,SectionName):
        """获取某个节点下的(Key,Value)信息元祖串"""
        SectionDict = copy.deepcopy(self.sections[SectionName])#使用深拷贝生成一个新的数据
        SectionDict.pop('count')
        SectionDict.pop('index')
        return [(KeyValue[0],KeyValue[1]['value']) for KeyValue in sorted(SectionDict.items(),key=lambda m: m[1]['index'])] 
                   
    def updateIniFile(self):
        filename = self.f.name
        self.f.close()
        os.remove(filename)
        self.f = file(filename,'w+')  
        for SectionDict in sorted(self.sections.items(),key=lambda d: d[1]['index']):
            #获取排列好顺序的Section
            self.f.writelines('[%s]\n'%SectionDict[0])#写入分段           
            SectionDict[1].pop('index')#弹出排序索引           
            SectionDict[1].pop('count')
            if len(SectionDict[1].items()) > 0:
                for KeyValue in sorted(SectionDict[1].items(),key=lambda m: m[1]['index']):
                    self.f.writelines('%s=%s\n'%(KeyValue[0],KeyValue[1]['value']))#写入分段
       
if __name__=='__main__':
    ini = PDxIni(r'Z:\\test\\SL_POS\\testdata\\test.ini')   
    ini.writeInteger('test2','java',788)
    ini.writeInteger('tesSL_Uava',444)
    print ini.readInteger('test2','frlphi',22 )
    del ini