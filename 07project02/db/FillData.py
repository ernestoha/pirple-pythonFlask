import random

# DDL and DML actions, to reset DB and fill with fresh data.
class FillData:
 
 def __init__(self, cursor):
    self.cursor = cursor

 def dropTables(self):
    self.cursor.execute("DROP TABLE IF EXISTS admin;")
    self.cursor.execute("DROP TABLE IF EXISTS tasks;")
    self.cursor.execute("DROP TABLE IF EXISTS users;")
    # cursor.execute("DROP TABLE admin; DROP TABLE tasks; DROP TABLE users;")

 def fillUsersTable(self):
    total = 1000
    init = "INSERT INTO users (first_name, last_name, password, email, created) VALUES "
    print("--Users-Begin--")
    # users = (("f1","f2",""),("3"),("4"))
    # for n in users:
    #     print(n)
    # cursor.execute(init + "('test{0}', 'test01', '123', 'test01@test.com');".format(s))
    for x in range(1, total+1):
        self.cursor.execute(init + "('test{0}', 'test{0}', '1234', 'test{0}@test.com', DATE('now','-{1} day'));".format(x if x>9 else "0"+str(x), self.get50XRange(x)))
    print("    Total: {0}\n--Users-End----\n".format(total))

 def fillTasksTable(self):
    total = 777
    init = "INSERT INTO tasks (user_id, title, done, created) VALUES "
    for x in range(1, total+1):
        val = self.get50XRange2(x)
        self.cursor.execute(init + "({1}, 'Title {0}', {3}, DATE('now','-{2} day'));".format(x if x>9 else "0"+str(x), val, val-1, random.getrandbits(1)))
    print("--Tasks-Being--")
    print("    Total: {0}\n--Tasks-End----\n".format(total))

 def fillAdminTable(self):
    total = 5
    init = "INSERT INTO admin (first_name, last_name, password, email, created) VALUES "
    # init = "INSERT INTO admin (first_name, last_name, password, email) VALUES "
    print("--Admin-Being--")
    for x in range(1, total+1):
        self.cursor.execute(init + "('test{0}', 'test{0}', '1234', 'test{0}@test.com', DATE('now','-{1} day'));".format(x if x>9 else "0"+str(x), self.get50XRange(x)))
        # cursor.execute(init + "('test{0}', 'test{0}', '1234', 'test{0}@test.com');".format(x if x>9 else "0"+str(x)))
    print("    Total: {0}\n--Admin-End----".format(total))
 
 def get50XRange(self, x):
     return self.get50_1000Range(x)-1

 def get50XRange2(self, x):
     return self.get50_1000Range2(x)

 def get50_1000Range(self, x):
    if (x<=53):  #50
        return 1
    if (x<=108): #100
        return 2
    if (x<=159): #150
        return 3
    if (x<=220): #200
        return 4
    if (x<=249): #250
        return 5
    if (x<=303): #300
        return 6
    if (x<=330): #350
        return 7
    if (x<=400): #400
        return 9
    if (x<=489): #450
        return 10
    if (x<=498): #500
        return 11
    if (x<=572): #550
        return 12
    if (x<=610): #600
        return 13
    if (x<=661): #650
        return 14
    if (x<=723): #700
        return 15
    if (x<=750): #750
        return 16
    if (x<=800): #800
        return 17
    if (x<=876): #850
        return 18
    if (x<=888): #900
        return 19
    if (x<=960): #950
        return 20
    if (x<=1001): #100
        return 21

 def get50_1000Range2(self, x):
    if (x<=167):
        return 1
    if (x<=210):
        return 2
    if (x<=402):
        return 3
    if (x<=689): 
        return 4
    if (x<=1001): 
        return 5
