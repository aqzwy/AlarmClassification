import pymysql.cursors

# 获取数据库连接
from main.models.alarm import Alarm


def get_connect():
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='alarm',
        charset='utf8'
    )
    return connect


# 读取数据
def select_alarm_all():
    arrList = []
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "SELECT id,AlarmFirstType,AlarmSecondType,AlarmContent FROM alarminfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            # print(row[0])
            alarm = Alarm()
            alarm.id = row[0]
            alarm.first_type = row[1]
            alarm.second_type = row[2]
            alarm.content = row[3]
            arrList.append(alarm)
    except Exception as e:
        print(e)
    finally:
        return arrList


def select_alarm():
    arrList = []
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "SELECT id,AlarmFirstType,AlarmSecondType,AlarmContent FROM alarminfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            # print(row[0])
            alarm = Alarm()
            alarm.id = row[0]
            alarm.first_type = row[1]
            alarm.second_type = row[2]
            alarm.content = row[3]
            arrList.append(alarm)
    except Exception as e:
        print(e)
    finally:
        return arrList

def select_alarm(type):
    arrList = []
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "SELECT id,AlarmFirstType,AlarmSecondType,AlarmContent FROM alarminfo where AlarmSecondType= %s"
        cursor.execute(sql, type)
        result = cursor.fetchall()
        for row in result:
            # print(row[0])
            alarm = Alarm()
            alarm.id = row[0]
            alarm.first_type = row[1]
            alarm.second_type = row[2]
            alarm.content = row[3]
            arrList.append(alarm)
    except Exception as e:
        print(e)
    finally:
        return arrList
