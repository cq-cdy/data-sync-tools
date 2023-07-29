import FinalTest.InitService as service
import FinalTest.Operate as opear
import FinalTest.Reflection as Reflection


def wirte_offline_cmd(sql):
    with open(service.mid_data_data, 'a') as t:
        t.write(sql + "\n")


def update(sql):
    if service.get_cur_mode() == 'local':
        wirte_offline_cmd(sql)
    else:
        service.submit_local_sql()  # 如果在系统突然重新获取连接，在进行增删查改之前需要提交离线时的sql数据
        update_in_mysql(sql)


def insert(sql):
    if service.get_cur_mode() == 'local':
        wirte_offline_cmd(sql)
    else:
        service.submit_local_sql()
        insert_in_mysql(sql)


def delete(sql):
    if service.get_cur_mode() == 'local':
        wirte_offline_cmd(sql)
    else:
        service.submit_local_sql()
        delete_in_mysql(sql)


def insert_in_mysql(sql):
    conn = service.getConnection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    service.sync_service_to_file()  # 同时跟新本地磁盘
    conn.close()


def delete_in_mysql(sql):
    conn = service.getConnection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    service.sync_service_to_file()
    conn.close()


def update_in_mysql(sql):
    conn = service.getConnection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    service.sync_service_to_file()
    conn.close()
