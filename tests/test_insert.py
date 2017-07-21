#!/usr/bin/python
#-*-coding:utf-8-*-
import click
import MySQLdb
import hashlib
import time

note = """
这段代码主要是来证明：在innodb存储引擎里面，md5值不适合作为主键

这是表结构

```sql
CREATE TABLE `origin`(
  `taskid` char(32) not null,
  `number` int(11) not null,
  `content` TEXT,
  PRIMARY KEY (`taskid`)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;
```

```sql
CREATE TABLE `improved`(
  `number` int(11) not null ,
  `taskid` char(32) not null,
  `content` TEXT,
  PRIMARY KEY (`number`),
  unique key `unique_taskid`(`taskid`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
在普通的磁盘7200转/min的磁盘上实验，实验结果表明，在插入10w条记录的情况下，
zephyr@warrior:~$ ./manage.py insert_origin -s 100000
[origin]insert  100000 record using 174.643198967
zephyr@warrior:~$ ./manage.py insert_improved -s 100000
[improved]insert 100000 record using 143.876350164
zephyr@warrior:~$ ./manage.py insert_origin -s 100000
[origin]insert  100000 record using 177.827208996
zephyr@warrior:~$ ./manage.py insert_improved -s 100000
[improved]insert 100000 record using 143.824852943
可以看到，md5做主键大概要比auto_increment作为主键慢30s！
"""

content = """
nfoseek公司资深工程师。李彦宏所持有的“超链分析”技术专利，是奠定整个现代搜索引擎发展趋势和方向的基础发明之一。
2000年1月，李彦宏创建了百度。经过十多年的发展，百度已经发展成为全球第二大独立搜索引擎和最大的中文搜索引擎。百度的成功，也使中国成为美国、俄罗斯和韩国之外，全球仅有的4个拥有搜索引擎核心技术的国家之一。2005年，百度在美国纳斯达克成功上市，并成为首家进入纳斯达克成分股的中国公司。百度已经成为中国最具价值的品牌之一。
2013年，当选第十二届全国政协委员，兼任第十一届中华全国工商业联合会副主席、第八届北京市科协副主席等职务，并获聘“国家特聘专家”。
2016年3月两会，李彦宏公布了自己的两会提案：一、关于加快制定和完善无人驾驶汽车相关政策法规，抢占产业发展制高点的提案；二是关于支持专网资源投入社会化运营，促进提速降费的提案 ；三是关于完善我国空域资源管理制度，提升民航准点率，推动我国航空事业发展的提案 。
学习生涯
北大骄子
1968年，李彦宏出生在山西阳泉一个普通的家庭。年少时着迷过戏曲，曾被山西阳泉晋剧团录取。但中学时代，李彦宏回归“主业”，全身心投入功课学习中。
在北京颐和园门前留影
在北京颐和园门前留影
1987年，李彦宏以阳泉市第一名的成绩考上了北京大学图书情报专业（即现在的信息管理）。不过，其迈进中国最高学府的激动心情，渐渐被图书情报学的枯燥、乏味消融。 “那时候，中国的氛围较为沉闷，大学毕业进入机关单位，已经是非常好的选择了。在我看来，选择出国是一条自然而然的道路。”
从大三开始，李彦宏心无旁骛，买来托福、GRE等书，过着“教室—图书馆—宿舍”三点一线的生活，目标是留学美国，方向锁定在计算机专业。
留学美国
1991年，李彦宏收到美国布法罗纽约州立大学计算机系的录取通知书。白天上课，晚上补习英语，编写程序，经常忙碌到凌晨两点。 “现在回想起来，觉得当时挺苦的，但年轻就应该吃苦。”李彦宏评价这段经历。
“我出国不是一帆风顺。因为换专业，刚到美国学计算机，很多功课一开始都跟不上。有时和教授面谈时，由于较心急，谈一些自己不是很了解的领域，结果那些教授就觉得我不行。”
在学校呆了一年后，李彦宏顺利进入日本松下实习。“这三个多月的实习，对我后来职业道路的选择起了至关重要的作用。”李彦宏说。
驰骋硅谷
“硅谷给予我最大的感触是，希望通过技术改变世界，改变生活。”
1994年暑假前，李彦宏收到华尔街一家公司——道·琼斯子公司的聘书。“在实习结束
日本著名财经杂志Diamond拍的照片
日本著名财经杂志Diamond拍的照片(4张)
 后，研究成果得到这一领域最权威人物的赏识，相关论文发表在该行业最权威的刊物上，这对以后的博士论文也很有帮助。”李彦宏说：“但那时候，中国留学生中有一股风气，就是读博士的学生一旦找到工作就放弃学业。起先，我认为自己不会这样。但这家公司老板也是个技术专家，他对我的研究非常赏识。两人大有相见恨晚的感觉。士为知己者死，于是我决心离开学校，接受这家公司高级顾问的职位。”
 在华尔街的三年半时间里，李彦宏每天都跟实时更新的金融新闻打交道，先后担任了道·琼斯子公司高级顾问、《华尔街日报》网络版实时金融信息系统设计人员。
 1997年，李彦宏离开了华尔街，前往硅谷著名搜索引擎公司Infoseek(搜信)公司。
 在硅谷的日子，让李彦宏感受最深刻的还是商战气氛。他经常翻看《华尔街日报》：微软如何跳出来公然反叛IBM，又怎样以软件教父的身份对抗SUN、网景等等，这些故事让李彦宏感觉到：“原来技术本身并不是唯一的决定性因素，商战策略才是真正决胜千里的因素。”[3] 
 归国创业
 李彦宏
 李彦宏(5张)
 李彦宏在海外的8年时间里，中国互联网界正发生着翻天覆地的变化。从1995年起，李彦宏每年要回国进行考察。1999年，李彦宏认定环境成熟，于是启程回国，在北大资源宾馆租了两间房，连同1个财会人员5个技术人员，以及合作伙伴徐勇，8人一行，开始了创建百度公司。
 接着，李彦宏顺利融到第一笔风险投资金120万美金。在百度成立的9个月之后，风险投资商德丰杰联合IDG又向百度投入了1000万美元。[2] 
 2001年，李彦宏在百度董事会上提出百度转型做独立搜索引擎网站，开展竞价排名的计划。然而，他的这个提议遭到股东们的一致反对：此时，百度的收入全部来自给门户网站提供搜索技术服务支持。如果百度转做独立的搜索引擎网站，那些门户网站不再与百度合作，百度眼前的收入就没了；而竞价排名模式又不能马上赚钱，百度就只有死路一条。
 李彦宏在讲演
 李彦宏在讲演(6张)
 在充分陈述了自己的计划和观点后，仍旧得不到首肯的李彦宏平生第一次发了大火。尽管李彦宏的一贯自信这次受到了极大的挑战，然而只要他认准了的东西，几乎没有人能改变，尤其是在关乎百度未来发展的大方向、大问题上，他丝毫不会退让。
 最终，投资人同意李彦宏将百度转型为面向终端用户的搜索引擎公司，他们告诉李彦宏："是你的态度而不是你的论据打动了我们。"
 推出竞价排名并实施“闪电计划”对百度实行第二次技术升级后，百度已成为全球第二大的独立搜索引擎，在中文搜索引擎中名列第一。
 2014年10月，在2014中国富豪榜中，李彦宏以147亿美元身家名列第二。
 2005年8月，百度在美国纳斯达克成功上市，成为全球资本市场最受关注的上市公司之一。
"""

@click.group()
@click.pass_context
def public(context):
    """
    public
    :param context:
    :return:
    """
    pass


@public.command()
@click.option('-s','--size',type=int,default="1000",help="insert rows")
@click.pass_context
def insert_origin(context,size):
    """
    :param context:
    :return:
    """
    connection = MySQLdb.connect(host="localhost",port=3306,user="qiulimao",passwd="mimashiroot",db="test")
    cursor = connection.cursor()
    sql = "insert into origin(taskid, number,content) values('%s',%s,'%s')"
    start_time = time.time()
    for i in range(0,size):
        hash_val = hashlib.md5(str(i).encode("utf-8")).hexdigest()
        to_execute_sql = sql % (hash_val, i,content)
        cursor.execute(to_execute_sql)
        connection.commit()

    end_time = time.time()
    click.echo("[origin]insert  %s record using %s" % (size,end_time - start_time))
    cursor.close()


@public.command()
@click.option('-s','--size',type=int,default="1000",help="insert rows")
@click.pass_context
def insert_improved(context,size):
    """

    :param context:
    :return:
    """
    connection = MySQLdb.connect(host="localhost",port=3306,user="qiulimao",passwd="mimashiroot",db="test")
    cursor = connection.cursor()
    sql = "insert into improved(number, taskid,content) values(%s,'%s','%s')"
    start_time = time.time()
    for i in range(0,size):
        hash_val = hashlib.md5(str(i).encode("utf-8")).hexdigest()
        to_execute_sql = sql % (i,hash_val,content)
        cursor.execute(to_execute_sql)
        connection.commit()

    end_time = time.time()
    click.echo("[improved]insert %s record using %s" % (size,end_time - start_time))
    cursor.close()

if __name__ == "__main__":
    public()
