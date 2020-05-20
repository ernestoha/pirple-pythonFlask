import db.con as con

table = "users"

def getAll():
    return con.dql("SELECT * FROM {}".format(table))

def getById(id):
    return con.dql("SELECT * FROM {} WHERE id=?".format(table), [id])

def getObjByEmail(email): #return user model (1, 'eh1', 'eh2', '1234', 'test01@test.com')
    # return con.dql("SELECT * FROM {} WHERE email=?".format(table), [email])
    data = con.dql("SELECT * FROM {} WHERE email=?".format(table), [email])[0]
    return {
            "id" : data[0],
            "fname" : data[1],
            "lname" : data[2],
            "password" : data[3],
            "email" : data[4]
            }

def getPasswordByEmail(email):
    return con.dql("SELECT password FROM {} WHERE email=?".format(table), [email], True)

def create(first_name, last_name, password, email):
    return con.dml("INSERT INTO {} (first_name, last_name, password, email) VALUES (?,?,?,?)".format(table), [first_name, last_name, password, email], "You have successfully signed up!!!", "User")

def update(id, first_name, last_name, password, email):
    return con.dml("UPDATE {} SET first_name=?, last_name=?, password=?, email=? WHERE id=?".format(table), [first_name, last_name, password, email, id], "You have successfully updated the user information!!!", "User's Email")

def updateByEmail(first_name, last_name, password, email):
    return con.dml("UPDATE {} SET first_name=?, last_name=?, password=? WHERE email=?".format(table), [first_name, last_name, password, email], "You have successfully updated the user information!!!")

def updatePassword(id, password):
    return con.dml("UPDATE {} SET password=? WHERE id=?".format(table), [password, id], "You have successfully updated the user's password!!!")

def delete(id):
    import db.task as task
    task.deleteByUserId(id) #Delete all user's tasks (On Cascade Manually)
    return con.dml("DELETE FROM {} WHERE id=?".format(table), [id], "You have successfully deleted the user and all tasks!!!")


# print(getAll())
# print(getPasswordByEmail("test01@test.com"))
# print(create("15","25","35","45"))
# print(update(10, "1","2","3","5"))
# print(update(10, "1","2","3","test01@test.com"))

# print(updatePassword(10, "11"))

# # print(delete(11))
# print(getAll())