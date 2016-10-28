#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com

#  Created on 2016-10-26 20:36:38
# Modified on 2016-10-26 20:46:20
""" 
 help contributors add info to the files 
""" 
#---------- code begins below -------
import subprocess
import click 
from subprocess import list2cmdline
import datetime 

@click.group()
@click.pass_context
def public(context):
    """
        some tools to easy your developing job.
    """
    return context 


@public.command()
@click.option("--name",prompt="your name",help="your name")
@click.option("--email",prompt="your email",help="your email")
@click.option("--website",prompt="your website",help="your website",default="http://www.getqiu.com")
@click.option("--daysago",prompt="modified time before now",help="modified time before now",default=1,type=int)
@click.pass_context
def newcontributor(context,name,email,website,daysago):
    """ 
        new contributer to weblocust project
    """

    """
    下面的cmd 就是要合成如下这条linux命令:

    find ./ \( -name '*.py' \) -a 
    -mtime -1 
    -exec sed -i "/http:\/\/binux.me/a\#\n# Contributor: qiulimao<qiulimao@getqiu.com>\n#         http://www.getqiu.com\n#" {}\;
    而这条Linux命令就是要在py文件上面添加一下自己的名字,邮箱,网址
    """
    cmd = ["find",'./',"\\(",'-name',"\'*.py\'","\\)","-a","-mtime",str(0-daysago),"-exec","sed","-i",
            '/http:\\/\\/binux.me/a\\#\\n# Contributor: '+name+'<'+email+'>\\n#         '+website+'\\n#',
            '{}','\;']

    subprocess.call(list2cmdline(cmd),shell=True)
    #click.echo(list2cmdline(cmd))

@public.command()
@click.option("--daysago",prompt="modified time before now",help="modified time before now",default=1,type=int)
@click.pass_context
def newmodifydate(context,daysago):
    """
        create modified date on py files
    """
    import datetime 
    
    date=datetime.datetime.now()
    dateString=date.strftime("%Y-%m-%d %H:%M:%S")

    cmd = ['find','./','\\(','-name',"\'*.py\'",'\\)','-mtime',str(0-daysago),
            '-a','-exec','sed','-i',"/Created on 20[0-1][0-9]/a\# Modified on "+dateString,'{}','\;']
    subprocess.call(list2cmdline(cmd),shell=True)
    #click.echo(list2cmdline(cmd))

@public.command()
@click.option("--daysago",prompt="modified time before now",help = "modified time before now",default=1,type=int)
@click.pass_context
def modifydate(context,daysago):
    """
        change the modified date on all the file which you have modified by in the past daysago to NOW()
    """
    import datetime 
    
    date=datetime.datetime.now()
    dateString=date.strftime("%Y-%m-%d %H:%M:%S")

    cmd = ['find','./','\\(','-name',"\'*.py\'",'\\)',
            '-a','-mtime',str(0-daysago),
            '-exec','sed','-i',"1,12s/Modified on 201[0-9]-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9]/Modified on "+dateString+"/g",
            '{}','\;']

    #click.echo(list2cmdline(cmd))
    subprocess.call(list2cmdline(cmd),shell=True)

@public.command()
@click.option("--path",prompt="put the documents to the path in relative",
    default="./weblocust/webui/static/",
    help="place the docs to somewhere in relative path")
@click.pass_context
def mkdocs(context,path):
    """
        make documents
    """
    from os.path import join 
    mkdocs_cmd = ['mkdocs','build','-c']  
    replace_googlefonts_cmd = ['find','./site','-name',"\'*.html\'",'-exec',
                            'sed','-i',"\'1,$s/fonts.googleapis.com/fonts.gmirror.org/g\'",'{}','\;']
    mv_to_path_cmd = ['mv','site',path]

    #click.echo(list2cmdline(replace_googlefonts_cmd))
    #click.echo(list2cmdline(mv_to_path_cmd))
    #click.echo(list2cmdline(mkdocs_cmd))

    subprocess.call(list2cmdline(mkdocs_cmd),shell=True)
    subprocess.call(list2cmdline(replace_googlefonts_cmd),shell=True)
    subprocess.call(list2cmdline(mv_to_path_cmd),shell=True)

@public.command()
@click.option("--path",prompt="the document path in relative",default="./weblocust/webui/static/")
@click.pass_context
def rmdocs(context,path):
    """
        remove the documents
    """
    import os
    cmd = ['rm','-rf',os.path.join(path,"site")]
    #click.echo(list2cmdline(cmd),shell=True)
    subprocess.call(list2cmdline(cmd),shell=True)



if __name__ == "__main__":
    public()
