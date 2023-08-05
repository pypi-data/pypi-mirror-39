import shutil,os
def moveFile(inputpath,inputfilename,outputpath,newfilename):
        '''
        copy inputpath/inputfilename to outputpath/newfilename
        return:
        '''
        shutil.copy(inputpath+"\\"+inputfilename,outputpath+"\\"+newfilename)
def file_name(inputpath):
        '''
        return path a/b/c.txt from path a
        return:a/b/c.txt
        '''  
        dir1=os.listdir(inputpath)
        dir2="".join(dir1)
        dir3=os.listdir(inputpath+"/"+dir2)
        outputpath=inputpath+"/"+dir2+"/"+"".join(dir3)
        return outputpath
def filefullpath(path):
        '''
                               返回目录下单个文件的全路径，包含文件名
        return:c_path
        '''  
        if(len(os.listdir(path))==1):
            for i in os.listdir(path): 
                c_path = os.path.join(path, i)
                c_path=c_path.replace('\\','/')
                return c_path
        else:
            print(path+"下含有多个文件，请及时删除") 
def filename(path):
        '''
        #输入路径返回路径下所有文件名的列表，文件名大写不带后缀
        '''
        list=[]
        for i in os.listdir(path):
            list.append(i.split('.',1)[0].upper())
        return list
def filename1(path):
        '''
        #输入路径返回路径下所有文件名的列表，文件名大写带后缀
        '''
        list=[]
        for i in os.listdir(path):
            list.append(i)
        return list        
def fileqname(filepath):
        '''
        #根据文件路径返回文件内容
        '''
        #不要把open放在try中，以防止打开失败，那么就不用关闭了
        file_object = open(filepath, mode='r',encoding='UTF-8') 
        try:
            #file_context是一个string，读取完后，就失去了对test.txt的文件引用
            file_context = file_object.read()
            #file_context = open(file).read().splitlines() 
            # file_context是一个list，每行文本内容是list中的一个元素
        finally:
            file_object.close()
        return file_context   
def filepath(path):
        '''
        #返回路径下所有文件的全路径的列表，带文件名及后缀
        '''
        list=[]
        for i in os.listdir(path):
            c_path = os.path.join(path, i)
            c_path=c_path.replace('\\','/')
            list.append(c_path)
        return list  
        
        
def filenamefrompath(filepath):
        '''
        #根据文件路径取出文件名,文件名大写
        '''
        fname=filepath.split('.',1)[0]
        fname=fname.split('/')[len(fname.split('/'))-1].upper()
        return fname  
        
def filenb(filepath):
        '''
                            统计目录下文件个数
        '''          
        return len([name for name in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, name))]) 

def writetxt(str,filepath):
    f=open(filepath,'w')
    f.write(str)
    f.close()
   
        
