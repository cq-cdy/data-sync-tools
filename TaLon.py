import FinalTest.InitService as ser
import FinalTest.Operate as Oper
import time as time
import sys, os, FinalTest.About


def initSystem():
    ser.load_mode()  # 建立连接，确立模式
    ser.sync_data()  # 启动时检查数据同步问题
    import FinalTest.CheckService_Thread as ser_t  # 独立模块开启服务连接监听
    import FinalTest.BGM_t as bgm
    ser_t.Service_Thread().start()
    bgm.BGM().start()

if __name__ == '__main__':
    import FinalTest.About as ab
    import FinalTest.Reflection as ref

    ref.load_reflect()
    initSystem()
    opera = Oper.Opearte()
    time.sleep(1.5)

   # print(ab.logo)
    print(ab.about)
    #ab.print_fozu()


    while (1):
        import FinalTest.Reflection as ref

        cmd = input("[TaLon@%s]>>> " % ser.cur_sys_user)
        if cmd.strip() == "":
            continue
        elif cmd == "ls":
            for i in opera.entrylist:
                print("[Entity]: ", i)
            print("\t\t", ref.shuxing)
            continue
        elif cmd == 'TaLon':
            print(FinalTest.About.about)
            continue
        elif cmd == 'version':
            print(FinalTest.About.version)
            continue
        elif cmd.strip(' ') == 'help':
            print(FinalTest.About.help)
            continue
        elif cmd == "exit":
            print("\nbye\n")
            os._exit(0)
        opera.get_user_command(cmd)
