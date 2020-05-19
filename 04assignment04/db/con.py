import sqlite3

def conex():
    return sqlite3.connect('./db/Task.db', check_same_thread = False)

def dql(sql, param = [], rtnOne = False):
    # print("sql: "+sql)
    # print(param)
    data = None
    connection = conex()
    cursor = connection.cursor()
    #cursor.execute(""" SELECT favorite_color FROM users WHERE username='{username}' ORDER BY pk DESC;""".format(username = username))
    cursor.execute(sql, param)
    if rtnOne:
        data = cursor.fetchone()[0]
    else:
        data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def dml(sql, params, msgOk = "Ok", dupl = "Data"):
    msg = ""
    connection = conex()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
        connection.commit()
        msg = msgOk
    except sqlite3.IntegrityError: #UNIQUE constraint failed
        msg = dupl+" already existed!!!"
    cursor.close()
    connection.close()
    return msg
