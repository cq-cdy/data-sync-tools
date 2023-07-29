'''
Commands for parsing user input
'''


class Parser:

    def __init__(self):

        self.fin_operator = ''
        self.cmd_category = ['ls ', 'update ', 'del ', 'add ','sum ']

    def get_input_cmd(self, cmd):
        categary = self.toSureCategory(cmd)
        return categary

    def toSureCategory(self, cmd):
        return self.mystartwith(cmd.strip(' ') + ' ')

    def mystartwith(self, cmd):
        for i in self.cmd_category:
            if cmd.startswith(i):
                self.fin_operator = i.strip(' ')
                if self.fin_operator == 'add':
                    return "insert "
                elif self.fin_operator == 'ls':
                    return "ls "
                elif self.fin_operator == 'del':
                    return "delete "
                elif self.fin_operator == 'update':
                    return "update "
                elif self.fin_operator == 'sum':
                    return "sum "
        return "-Unknown command: '%s' " % (self.errstr(cmd))

    # 返回错误的命令指令
    def errstr(self, errcmd):
        t = ''
        for i in errcmd:
            if i == ' ':
                break
            t = t + i
        return t
