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
    try:
        cursor.execute(sql, param)
        if rtnOne:
            data = cursor.fetchone()
            if data:
                data = data[0]
        else:
            data = cursor.fetchall()
    except Exception as inst:
        print('\033[1m' + '\033[91m') #Bold Red Line
        print(inst)
        print("ERROR. sql: "+sql)
        print(param)
        print('\033[0m' + '--------------------') #Normal Line
    cursor.close()
    connection.close()
    return data

def dml(sql, params, msgOk = "Ok", dupl = "Data"):
    msg = {"res": None, "txt": None}
    connection = conex()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
        connection.commit()
        # msg = msgOk
        msg["res"] = True
        msg["txt"] = msgOk
    except sqlite3.IntegrityError: #UNIQUE constraint failed
        msg["res"] = False
        msg["txt"] = dupl+" already existed!!!"
        # msg = dupl+" already existed!!!"
    cursor.close()
    connection.close()
    return msg
