'''
Initialize the XML file,
Through configuration information, the entity object is encapsulated by reflection and method
So as to adapt to various data tables
'''

import importlib
import xml.dom.minidom as xml

shuxing = []
tablename = '-'
ini_information = {}
dom = xml.parse("properties/service.xml")
root = dom.documentElement
itemlist = root.getElementsByTagName('entry')

for db in itemlist:
    ini_information['tab_name'] = db.getElementsByTagName('tab_name')[0].childNodes[0].data
    ini_information['attr'] = db.getElementsByTagName('attr')[0].childNodes[0].data
tablename = ini_information['tab_name']


def load_reflect():
    for i in str(ini_information['attr']).split(","):  # 先从配置文件读取字段
        shuxing.append(i)
    import FinalTest.InitService as service

    try:
        conn = service.getConnection()
        cur = conn.cursor()
        cur.execute("desc %s" % tablename)
        s = cur.fetchall()
        conn.commit()
        conn.close()
        check = []  # 如果是在线模式，就覆盖配置文件配置的字段，直接从表中加载
        for j in s:  # 如果发现加载的字段内容和顺序与配置文件的所配置的不一致就作出警告
            check.append(j[0])
        for i in range(0, len(check)):
            if not (shuxing[i] == check[i]):
                print("\n\033[1;33;4m警告:配置字段与数据表顺序或内容不匹配,系统本次将以数据表字段为主自动纠正，"
                      "请正确配置properties/service.xml\033[0m")
                break
        shuxing.clear()
        for i in s:
            shuxing.append(i[0])
    except BaseException:
        pass
    import FinalTest.InitService as ser


    # 自动完成bean对象的python文件的创建
    w = open("EntityClass.py", 'w')
    w.write("class EntityClass:\n")
    for i in shuxing:
        w.write("\t%s='""'\n" % i)
    w.close()
    w = open("EntityClass.py", "a")
    w.write("\tdef __str__(self):\n")
    t = ""
    for i in shuxing:
        t = t + "%s        "
    t = " '%s' " % (t) + '%('
    for i in shuxing:
        t = t + "self.%s" % i + ","
    t = "return " + t[0:len(t) - 1] + ")"
    w.write("\t\t%s" % t)
    w.close()


def getInstance():
    return importlib.import_module("FinalTest.EntityClass").EntityClass()
