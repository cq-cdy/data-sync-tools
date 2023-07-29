'''
Initialize service category
'''
import os, datetime, getpass, time
import FinalTest.Reflection as ref
import pymysql, jpype
import xml.dom.minidom as xml

cur_sys_user = getpass.getuser()
sys_path = os.path.expanduser('~') + '\python_subject_work'
outlinedata_data = sys_path + '\outlinedata.data'
mid_data_data = sys_path + '\mid_data.data'


def load_mode():
    # 以系统用户路径为主文件夹
    # 若不存在则自动创建
    if not os.path.exists(sys_path):
        os.mkdir(sys_path)
        print("[%s][%s]:Establish offline service direct:%s" %
              (cur_sys_user, get_cur_Time(), sys_path))

    # 判断离线内容文件
    if not os.path.exists(sys_path + '\outlinedata.data'):
        print("[%s][%s]:Establish offline service file:%s"
              % (cur_sys_user, get_cur_Time(), sys_path + '\outlinedata.data'))
        open(sys_path + '\outlinedata.data', 'w')

    # 判断中间文件
    if not os.path.exists(sys_path + '\mid_data.data'):
        print("[%s][%s]:Establish Intermediary data file:%s"
              % (cur_sys_user, get_cur_Time(), sys_path + '\mid_data.data'))
        open(sys_path + '\mid_data.data', 'w')

    if ToSureService() == "local":
        buildOutLine()
    else:
        buildOnLine()


def sync_data():
    # 提交本地缓存sql
    submit_local_sql()
    # 从服务器刷洗数据到本地磁盘
    sync_service_to_file()
    print("[%s][%s]:Data synchronization complete"
          % (cur_sys_user, get_cur_Time()))


def sync_service_to_file():
    conn = getConnection()
    if not conn == None:
        a = []
        cur = conn.cursor()
        try:
            cur.execute("select * from %s;" % (ref.tablename))
        except pymysql.err.ProgrammingError as e:
            print("\033[7;31m %s \033[1;31;40m"%str(e))
        result = cur.fetchall()
        for i in result:
            a.append(i)
        with open(outlinedata_data, 'w') as t:
            s = ""
            for i in a:
                for j in i:
                    s = s + str(j) + ","
                t.write(s[0:len(s) - 1] + "\n")
                s = ""
    if not conn == None:
        conn.close()


def submit_local_sql():
    if os.path.getsize(mid_data_data) > 0:
        conn = getConnection()
        if not conn == None:
            cur = conn.cursor()
            with open(mid_data_data, 'r+') as t:
                sql = t.read().split("\n")
                for i in sql:
                    if not i == '':
                        try:
                            cur.execute(i)
                            conn.commit()
                        except BaseException:
                            pass
                t.truncate(0)
            conn.close()


def buildOnLine():
    print("[%s][%s]:Start synchronizing local data with server data"
          % (cur_sys_user, get_cur_Time()))
    sync_data()
    time.sleep(1)
    print("[%s][%s]:Data synchronization complete"
          % (cur_sys_user, get_cur_Time()))
    print("[%s][%s]:Local data cache in %s"
          % (cur_sys_user, get_cur_Time(), os.path.expanduser('~') + "\\"))


# 如果是离线状态就从文本加载数据
def buildOutLine():
    time.sleep(1)
    print("[%s][%s]:Use local data files : %s"
          % (cur_sys_user, get_cur_Time(), outlinedata_data))


# 确定服务模式
def ToSureService():
    sql_conn = getConnection()
    if sql_conn is not None:
        print("[%s][%s]:Server connection successful"
              % (cur_sys_user, get_cur_Time()))
        time.sleep(1)
        tomode(mode='online')
        print("[%s][%s]:Service mode:onLine" % (cur_sys_user, get_cur_Time()))
    else:
        print("[%s][%s]:Server connection failed:Please check the 'properties/service.xml'"
              % (cur_sys_user, get_cur_Time()))
        tomode(mode='local')
        print("[%s][%s]:Service mode:local" % (cur_sys_user, get_cur_Time()))
    if not sql_conn == None: sql_conn.close()


# 获取数据库连接
def getConnection():
    ini_information = {}
    if (not os.path.exists("properties/service.xml")):
        print("[%s][%s]:systemfile 'service.xml'is not exists" % (cur_sys_user, get_cur_Time()))
    dom = xml.parse("properties/service.xml")
    root = dom.documentElement
    itemlist = root.getElementsByTagName('entry')
    for db in itemlist:
        ini_information['host'] = db.getElementsByTagName('host')[0].childNodes[0].data
        ini_information['port'] = db.getElementsByTagName('port')[0].childNodes[0].data
        ini_information['user'] = db.getElementsByTagName('user')[0].childNodes[0].data
        ini_information['password'] = db.getElementsByTagName('password')[0].childNodes[0].data
        ini_information['db'] = db.getElementsByTagName('db')[0].childNodes[0].data
    try:
        conn = pymysql.connect(host=ini_information.get('host'),
                               port=int(ini_information.get('port')),
                               user=ini_information.get('user'),
                               password=ini_information.get("password"),
                               db=ini_information.get("db"))
    except BaseException:
        conn = None

    return conn


def _start_service_moniter(fp, host, port, user, pwd, db):
    jarpath = os.path.join(os.path.abspath("."),
                           "java/check_service-1.0-SNAPSHOT-jar-with-dependencies.jar")
    try:
        jvmPath = jpype.getDefaultJVMPath()
        print("\nstart jvm | jvmPath:", jvmPath)
    except BaseException:

        print("Monitoring failed to start. "
              "The system environment could not find the Java virtual machine 'jvm.dll'")
        return
    try:
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jarpath))
    except BaseException:
        pass
    javaClass = jpype.JClass("com.cdy.service.CheckService")
    javaClass._start_(fp, host,
                      port,
                      user,
                      pwd,
                      db)


def tomode(mode='local'):
    if not os.path.exists('properties/service_mode.data'):
        open('properties/service_mode.data', 'w')
    with open("properties/service_mode.data", 'w') as t: t.write(mode)


def get_cur_mode():
    with open("properties/service_mode.data", 'r') as t:
        return t.read()


def get_cur_Time():
    return datetime.datetime.now().strftime('%F %T')
