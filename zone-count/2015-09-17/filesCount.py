#/usr/bin/env python
#coding=utf=8
import os,sys

def IsSubString(SubStrList,Str): 
  flag=True
  for substr in SubStrList:
    if not(substr in Str): 
      flag=False
  return flag 

def GetFileList(FindPath,FlagStr=[]): 
 FileList=[] 
 FileNames=os.listdir(FindPath) 
 if (len(FileNames)>0): 
  for fn in FileNames: 
   if (len(FlagStr)>0): 
    if (IsSubString(FlagStr,fn)): 
     fullfilename=os.path.join(FindPath,fn) 
     FileList.append(fullfilename) 
   else: 
    fullfilename=os.path.join(FindPath,fn) 
    FileList.append(fullfilename) 
 if (len(FileList)>0): 
  FileList.sort() 
 return FileList

if __name__ == '__main__':

  filelist = GetFileList(os.getcwd(),"jpg")
  for files in filelist:
    delimiter = ''
    filenames = delimiter.join(files[-28:-18])+" "+delimiter.join(files[-17:-15])+":"+delimiter.join(files[-14:-12])+":"+delimiter.join(files[-11:-9])
    print filenames


