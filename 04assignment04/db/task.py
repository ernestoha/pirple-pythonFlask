import db.con as con

table = "tasks"

def getAll():
    return con.dql("SELECT * FROM {}".format(table))

def getById(id):
    return con.dql("SELECT * FROM {} WHERE id=?".format(table), [id])

def getByUserId(user_id):
    return con.dql("SELECT * FROM {} WHERE user_id=?".format(table), [user_id])

def create(user_id, title, done):
    return con.dml("INSERT INTO {} (user_id, title, done) VALUES (?,?,?)".format(table), [user_id, title, done], "You have successfully created a new task!!!")

def update(id, user_id, title, done):
    return con.dml("UPDATE {} SET title=?, done=? WHERE id=? AND user_id=?".format(table), [title, done, id, user_id], "You have successfully updated the task!!!")

def delete(id, user_id):
    return con.dml("DELETE FROM {} WHERE id=? AND user_id=?".format(table), [id, user_id], "You have successfully deleted the task!!!")

def deleteAll(user_id):
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
# # print(deleteAll(2))
# print(getAll())