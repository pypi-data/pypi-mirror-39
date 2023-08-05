import sys
import datetime
#lineNumber = sys._getframe().f_back.f_lineno
#sys._getframe().f_code.co_filename
def get_filename():
    name=[]
    a=sys._getframe()
    while a is not None:
       name.append(a.f_code.co_filename)
       a=a.f_back
    #print name
    return name[-1]
def get_tree():
    #filename=sys._getframe().f_code.co_filename
    filename=get_filename()
    name=[]
    a = sys._getframe()
    linenum=a.f_back.f_lineno
    #filename+='(line-'+str(linenum)+')'
    #while a is not None and a.f_back is not None:
    while a is not None:
       #name.append(a.f_code.co_name+'(%s line:'%(filename)+str(a.f_back.f_lineno)+')')
       name.append(a.f_code.co_name+'(line:'+str(a.f_lineno)+')')
       a=a.f_back
    #print(100*'*')
    #print len(name)
    #print name
    funclist='%s main'%(filename)
    spacelist=4*' '
    for i in range(-1,-len(name)+1,-1):
        #print name[i]
        funclist+=' - '+name[i]
    #print name
    return funclist,'%s %s %s'%(filename,(len(name)-2)*' -  ',name[2])
def addinfo(message,flag=1):
    funclist,spacelist=get_tree()
    flist=(funclist,spacelist)[flag]
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info="[%s] %s :: %s"%(nowTime,flist,message)
    return info
def zprintr(message,flag=1):
    info=addinfo(message,flag)
    sys.stdout.write(info+'\r')
    sys.stdout.flush()
    
def zprint(message,flag=1):

    #funclist,spacelist=get_tree()
    #flist=(funclist,spacelist)[flag]
    #nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #info="[%s] %s :: %s"%(nowTime,flist,message)
    info=addinfo(message,flag)
    sys.stdout.write(info+'\n')
    #print info
def eprint(message,flag=1):
    #funclist,spacelist=get_tree()
    #flist=(funclist,spacelist)[flag]
    #nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #info="[%s] %s :: %s"%(nowTime,flist,message)
    info=addinfo(message,flag)
    sys.stderr.write(info+'\n')
def pprint(i,i_all,width,outstr=sys._getframe().f_code.co_name):
    # process print
    nn=i%width
    #sys.stdout.write('\r %s:'+nn*"#"+(30-nn)*' '+'%.2f%%'%(sys._getframe().f_code.co_name,float(i)/float(len(imglist))*100))
    #sys.stdout.write('\r %s: '%(sys._getframe().f_code.co_name)+nn*"#"+(width-nn)*' '+'%.2f%%'%(float(i)/float(i_all)*100))
    sys.stdout.write('\r %s: '%(outstr)+nn*"#"+(width-nn)*' '+'%.2f%%'%(float(i)/float(i_all)*100))
    sys.stdout.flush()


def zhelp():
    sys.stdout.write(" # pip install zprint -i https://pypi.python.org/simple\n")
    sys.stdout.write(" from zprint import *\n")
    sys.stdout.write(" \n")
    sys.stdout.write(" def fun2():\n")
    sys.stdout.write("     zprint(\" I am in fun2\",1)\n")
    sys.stdout.write("     zprint(\" I am in fun2\",0)\n")
    sys.stdout.write(" \n")
    sys.stdout.write(" def fun1():\n")
    sys.stdout.write("     zprint(\" I am in fun1\")\n")
    sys.stdout.write("     fun2()\n")
    sys.stdout.write(" \n")
    sys.stdout.write(" if __name__==\"__main__\":\n")
    sys.stdout.write("    fun1()\n")

def fun2():
    zprint(" I am in fun2",1)
    zprint(" I am in fun2",0)

def fun1():
    zprint(" I am in fun1")
    fun2()



if __name__=="__main__":
   fun1()
   zhelp()
   zprint("main")

