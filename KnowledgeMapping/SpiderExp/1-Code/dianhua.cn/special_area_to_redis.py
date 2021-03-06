"""
指定号码段存入redis
采集这些号码段的号码标记
"""
import pymysql
import redis

if __name__ == '__main__':
    # 连接MySQL
    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    # 连接redis
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    province_list = ['广东', '上海', '北京', '河南', '山东', '江苏', '浙江']
    # province_list = ['广东']

    for province in province_list:
        sql = "SELECT id FROM number_prefix WHERE province='{}'".format(province)
        mysql_cursor.execute(sql)
        results = mysql_cursor.fetchall()
        if results:
            print(province)
            for r in results:
                r_conn.sadd("telephone_task", r[0])
        else:
            print(province, "empty")

    # 关闭mysql连接
    mysql_cursor.close()
    mysql_conn.close()
    print("Close MySQL Connection...")
    print("end")
