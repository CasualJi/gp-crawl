import datetime
import hashlib
import logging
import pymysql

def get_db():
    db = pymysql.Connect(
        host='x',
        port=3306,
        user='x',
        passwd='x',
        db='x',
        charset='utf8'
    )
    return db

def save_project_info(p_name,p_type,p_property,s_name,s_num,s_major,s_academy,s_gender,t_name):
    db = get_db()
    cursor = db.cursor()
    sql = "insert into project(project_name,project_type,project_property,student_name,student_num,student_major,student_academy,student_gender,teacher_name) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (p_name.replace('\'','-'), p_type,p_property,s_name,s_num,s_major,s_academy,s_gender,t_name)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        logging.exception(e)
    db.close()

def get_data(field, value):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from project WHERE " + field + " = %s " % value
    print(sql)
    cursor.execute(sql)
    return cursor.fetchall()

def execute(sql):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


