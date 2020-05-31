import db.con as con

table = "tasks"
table_join = "tasks t INNER JOIN users u on t.user_id = u.id"

def getAll(where = None, limit = None, offset = None):
    fields = "t.id, u.email, t.title, t.done, t.created"
    # print("SELECT {4} FROM {0} {1} {2} {3}".format(table_join, "WHERE " + where if where else "", "LIMIT " + str(limit) if limit else "", "OFFSET " + str(offset) if offset else "", fields))
    return con.dql("SELECT {4} FROM {0} {1} ORDER BY t.id {2} {3}".format(table_join, "WHERE " + where if where else "", "LIMIT " + str(limit) if limit else "", "OFFSET " + str(offset) if offset else "", fields))

def getAllCount(where = None):
    return con.dql("SELECT count(id) FROM {0} {1}".format(table, "WHERE " + where if where else ""))[0][0]

def getDayCount(day = 0):
    return con.dql("SELECT count(id) FROM {0} WHERE created=DATE('now','-{1} day')".format(table, day))[0][0]

def getById(id):
    return con.dql("SELECT * FROM {} WHERE id=?".format(table), [id])

def getByUserId(user_id):
    return con.dql("SELECT * FROM {} WHERE user_id=?".format(table), [user_id])

def create(user_id, title, done):
    return con.dml("INSERT INTO {} (user_id, title, done) VALUES (?,?,?)".format(table), [user_id, title, done], "You have successfully created a new task!!!", "Task")

def update(id, user_id, title, done):
    return con.dml("UPDATE {} SET title=?, done=? WHERE id=? AND user_id=?".format(table), [title, done, id, user_id], "You have successfully updated the task!!!", "Task")

def delete(id, user_id):
    return con.dml("DELETE FROM {} WHERE id=? AND user_id=?".format(table), [id, user_id], "You have successfully deleted the task!!!")

def deleteByUserId(user_id):
    return con.dml("DELETE FROM {} WHERE user_id=?".format(table), [user_id], "You have successfully deleted all tasks!!!")

# print(getAll())
# print(getByUserId(2))
# print(create(11,"2assfsdf",True))
# print(create(11,"2assfsdf2",False))
# print(update(3, 1, "1",False))
# # print(update(10, "1","2","3","test01@test.com"))

# # print(updatePassword(10, "11"))
# print(getByUserId(2))
# # print(delete(10, 2))
# print(getByUserId(2))
# # print(deleteByUserId(2))
# print(getAll())