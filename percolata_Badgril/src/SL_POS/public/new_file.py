#coding=utf-8
import os

def newfile(result_dir):
    #定义文件目录
    #result_dir = 'D:\\Workspaces\\python\\TestLogin126\\log'
    #获取目录下所有文件
    lists=os.listdir(result_dir)
    #重新按时间对目录下的文件进行排列
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn))
    print ('最新日志： '+lists[-1])
    file = os.path.join(result_dir,lists[-1])
    #print file
    return file
if __name__ == '__main__':
    newfilename = newfile('D:\\Workspaces\\python\\TestLogin126\\log')
    print newfilename
