import FinalTest.RecordCommand as cmd
import FinalTest.InitService as ser
import FinalTest.Reflection as ref


class Opearte():
    """
        # Initialization:
        # Read data from disk,
        # And encapsulated as entity objects
    """

    def __init__(self):
        import FinalTest.CommandParser as cmdper
        self.entrylist = []
        self.cmpder = cmdper.Parser()
        with open(ser.outlinedata_data, 'r')as r:  # 磁盘数据的更新都大于等于服务器，每次启动都会更新磁盘,所以直接从磁盘加载
            list = r.read().split('\n')
            for entry in list:
                if not len(entry) == 0:
                    ent = ref.getInstance()
                    a = entry.split(",")
                    for i in range(0, len(a)):
                        try:
                            setattr(ent, ref.shuxing[i], a[i])
                        except IndexError:
                            print(
                                "\033[7;31m\nThe table field is mismatch.Please check the 'properties/service.xml'\n\033[1;31;40m")
                            exit(0)
                    self.entrylist.append(ent)
        r.close()

    #
    # Get the user command name and parse it
    #
    def get_user_command(self, ucmd):
        if (str(ucmd).strip(" ").startswith("ls-key")):
            key = str(ucmd[6:len(ucmd)]).strip(" ")
            for i in self.entrylist:
                if getattr(i, ref.shuxing[0]) == key:
                    self.showattr()
                    print(i)
                    return
            print("can't find the key is '%s'" % key)
            return
        sql = self.cmpder.get_input_cmd(ucmd)
        if sql == "ls ":
            self.ls_some(str(ucmd[2:len(ucmd)]).strip(' ').split(' '))
        elif sql == 'insert ':
            if ucmd.strip(" ") == "add":
                print("\033[1;33;40m [add key=value key=value ...]\033[0m")
                return
            realsql = self.add_ent(str(ucmd[3:len(ucmd)]).strip(' ').split(' '))
            if not realsql == "":
                self.insert(realsql)
        elif sql == 'delete ':
            if ucmd.strip(" ") == "del":
                print("\033[1;33;40m [del key=value key=value ...]\033[0m")
                return
            realsql = self.del_ent(str(ucmd[3:len(ucmd)]).strip(' ').split(' '))
            if not realsql == "":
                self.deldata(realsql)
        elif sql == 'update ':
            if ucmd.strip(" ") == "update":
                print("\033[1;33;40m ['update PRIMARY KRY'  to enter modify information]\033[0m")
                return
            self.update_mode(str(ucmd[6:len(ucmd)]).strip(' '))
        elif sql == 'sum ':
            if ucmd.strip(" ") == "sum":
                print("\033[1;33;40m ['sum keys' ,the 'keys' must be a computable data type]\033[0m")
                return
            for i in self.get_sum_list(str((ucmd.strip(' '))[4:len(ucmd)]).strip(' ').split(' ')):
                res = self.to_sum(i)
                if (not res==''):
                    print('sum(%s)\t\t%s'%(i,str(res)))


        elif sql.startswith("-Unknown command"):
            print(sql)
            return

    def insert(self, sql):
        self.flush_file()
        cmd.insert(sql)  # 更新服务器

    def deldata(self, sql):
        self.flush_file()
        cmd.delete(sql)

    def update(self, sql):
        self.flush_file()
        cmd.update(sql)  # 更新服务器

    def ls_some(self, attr):
        if attr.__contains__(""): attr.remove("")
        t = ""
        for i in self.entrylist:
            for j in attr:
                try:
                    t = t + str(getattr(i, j)) + "\t\t"
                except BaseException:
                    print("'%s' is unknown attribute" % j)
                    return ""
            print(t)
            t = ''
        print(attr)

    def add_ent(self, attr):
        if len(attr) < 1: return
        if attr.__contains__(""): attr.remove("")
        k = []
        v = []
        for i in attr:
            if not i.__contains__("="):
                print("Command error nearby:%s" % i)
                return ""
            i = i.split("=")
            k.append(i[0])
            v.append(i[1])
            for i in k:
                if i.__contains__("="):
                    print("key error contains '='")
                    return ""
                if not (i in ref.shuxing):
                    print("'%s' is unknown attribute" % i)
                    return ""
            for i in v:
                if i.__contains__("="):
                    print("value error contains '='")
                    return ""
                for c in i:
                    if c in (',', ')', '(', '.', ' ', '='):
                        print("The input contains illegal characters '%s'" % c)
                        return ""
        ent = ref.getInstance()
        for i in range(0, len(k)):  # 封装输入的值为对象
            setattr(ent, k[i], v[i])
        for r in ref.shuxing:  # 如果某些值为空，那就把空值赋值为-
            kong = getattr(ent, r, "")
            if kong == '':
                setattr(ent, r, "-")
        for i in self.entrylist:  # 如果key建已存在:
            if getattr(i, ref.shuxing[0]) == getattr(ent, ref.shuxing[0]):
                print("'%s' already exsist" % getattr(ent, ref.shuxing[0]))
                return ""
        self.entrylist.append(ent)  # 到这里内存更新完成
        values = ''  # 接下来就是返会对于的sql语句
        key = ''
        for oo in ref.shuxing:
            key = key + oo + ","
            values = values + "'" + getattr(ent, oo, "-") + "'" + ","
        values = values[0:len(values) - 1]
        key = key[0:len(key) - 1]
        sql = "insert into %s (%s) values(%s)" % (ref.tablename, key, values)
        print("-OK")
        return sql

    def del_ent(self, attr):
        if len(attr) < 1: return ""
        if attr.__contains__(""): attr.remove("")
        k = []
        v = []
        for i in attr:
            if not i.__contains__("="):
                print("Command error nearby:'%s'" % i)
                return ""
            i = i.split("=")
            k.append(i[0])
            v.append(i[1])
            for i in k:
                if i.__contains__("="):
                    print("key error contains '='")
                    return ""
                if not (i in ref.shuxing):
                    print("'%s' is unknown attribute" % i)
                    return ""
                for i in v:
                    if i.__contains__("="):
                        print("value error contains '='")
                        return ""
                    for c in i:
                        if c in (',', ')', '(', '.', ' ', '='):
                            print("The input contains illegal characters '%s'" % c)
                            return ""
        candel = True
        for i in self.entrylist:
            for n in range(0, len(k)):
                if getattr(i, k[n]) == v[n]:
                    continue
                else:
                    candel = False  # 不满足条件，不删除，就直接跳出循环
                    break
            if candel == True: self.entrylist.remove(i)
            candel = True
        t = ""
        con = []
        for i in range(0, len(k)):
            t = k[i] + "=" + "'%s'" % v[i]
            con.append(t)
        s = ""
        for j in con:
            s = s + (j + " AND ")
        print("-OK")
        return "delete from %s where %s" % (ref.tablename, s[0:len(s) - 4])

    def update_mode(self, pri_key):
        find = False
        for i in self.entrylist:
            if (getattr(i, ref.shuxing[0]) == pri_key):
                find = True
                break
        if not find:
            print("'%s' is not exist" % pri_key)
            return ""
        print('''                 -----------------------------
                |input 'done()' to exit modify|
                 -----------------------------''')
        print("\033[1;33;4m [modify command:'key=value,key=value']\033[0m")
        ent = None
        for i in self.entrylist:
            if getattr(i, ref.shuxing[0]) == pri_key:
                ent = i
                break
        self.showattr()
        print(ent)
        while 1:
            cmd = input("\033[1;33;40m [MODIFY ON: '%s']\033[0m" % pri_key + " >>> ")
            if (cmd == 'done()'): break
            for i in cmd.strip(" ").split(","):
                if not i.__contains__("="):
                    print("command error")
                    break
                l = i.split("=")
                k = l[0].strip(" ")
                v = l[1].strip(" ")
                if not self.pri_key_isExsist(k):
                    print("'%s' is Unkonwn attribute" % k)
                    continue
                if not self.islegal(v):
                    print("'%s' contains illegal character" % v)
                    continue
                if k == ref.shuxing[0]:
                    if self.v_is_exist_key(v):
                        print("'%s' is already exist" % v)
                        continue
                setattr(ent, k, v)
                sql = "update %s SET %s='%s' where %s='%s'" % (ref.tablename, k, v, ref.shuxing[0], pri_key)
                self.update(sql)
            self.showattr()
            print(ent)

    def islegal(self, prikey):
        for i in prikey:
            if i in (',', ')', '(', '=', ' ', ''): return False
        return True

    def pri_key_isExsist(self, prikey):
        if prikey in (ref.shuxing):
            return True
        else:
            return False

    def showattr(self):
        t = ""
        for i in ref.shuxing:
            t = t + i + "        "
        print("[", t, "]")

    def v_is_exist_key(self, v):
        for x in self.entrylist:
            if v == getattr(x, ref.shuxing[0]):
                return True
        return False

    def to_sum(self,attr):
        if not (attr in ref.shuxing):
            print("Unknown '%s' "%attr)
            return ''
        for x in self.entrylist:
            try:
                float(getattr(x,attr))
            except BaseException:
                print("'%s' contains  value which couldn't to sum"%attr)
                return ''
        sum=0
        for x in self.entrylist:
            sum=sum+float(getattr(x,attr))
        return sum

    def get_sum_list(self,attrs):
        a=[]
        for i in attrs:
            if(not i==''):
                a.append(i.strip(' '))
        return a
    def flush_file(self):  # 如果是本地模式就从内存刷写新的信息到磁盘
        with open(ser.outlinedata_data, 'w') as t:
            for i in self.entrylist:
                s = ""
                for x in ref.shuxing:
                    s = s + getattr(i, x) + ","
                s = s[0:len(s) - 1] + "\n"
                t.writelines(s)
                s = ""
        t.close()
