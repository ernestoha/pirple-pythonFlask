import os
from flask import Flask, render_template, request, session, redirect, url_for, g, send_from_directory
from db import admin, user, task #db models to use
import datetime
import math

app = Flask(__name__)
app.secret_key = '*SecretkeY*'
paginatePerPage = 50

@app.template_filter()
def format_datetime(value, format="%m-%d-%Y"):
    return datetime.datetime.strptime(value, "%Y-%m-%d").strftime(format)
    
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
def home():
        return render_template('index.html', nav=getNav(), title="ToDo List", msg = None) #, username = session.get("username")
        # return render_template('index.html', nav=getNav(), title="ToDo List", msg = {"class":"success", "text":"Bla bla bla bla."})
        # return render_template('index.html', nav=getNav(), title="ToDo List", msg = {"class":"alert", "text":"Bla bla bla bla."})

@app.route('/about', methods=['GET'])
def about():
        return render_template('about.html', nav=getNav(), title="About Us:", msg = None)

@app.route('/terms-of-use', methods=['GET'])
def termsOfUse():
        return render_template('terms-of-use.html', nav=getNav(), title="Terms Of Use:", msg = None)

@app.route('/privacy', methods=['GET'])
def privacy():
        return render_template('privacy.html', nav=getNav(), title="Privacy:", msg = None)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
        title = "Please Sign-Up"
        if request.method=='GET':
                return render_template('sign-up.html', nav=getNav(), title=title, user = None, msg = None)
        else:
                fname = request.form['fname']
                lname = request.form['lname']
                email = request.form['email']
                password = request.form['password']
                terms = request.form.getlist('terms')#['terms']
                # print(request.form)
                userData = {
                                "fname" : fname, 
                                "lname" : lname, 
                                "email" : email, 
                                #"password" : password, 
                                "terms" : terms
                        }
                # print(userData)
                if len(fname)>0 and len(lname)>0 and len(email)>0 and len(password)>0 and terms==["on"]:
                        res = user.create(fname, lname, password, email)
                        # print(res)
                        if res.get('res'):
                                return setSessionUserData(email)
                                # msg = {"class":"success", "text": res.get('txt')}
                                # return render_template('sign-up.html', nav=getNav(), title="Sign-Up:", user = None, msg = msg)
                        else:
                                msg = {"class":"alert", "text": res.get('txt')}
                                return render_template('sign-up.html', nav=getNav(), title=title, user = userData, msg = msg)
                else:
                        return render_template('sign-up.html', nav=getNav(), title=title, user = userData, msg = {"class":"alert", "text": "Fill all the fields and check terms, please try again."})

@app.route('/log-in', methods=['GET', 'POST'])
def logIn():
        title = "Please sign in:"
        if request.method=='GET':
                return render_template('log-in.html', nav=getNav(), title=title, msg = None, ehaData = None)
        else:
                email = request.form['email']
                password = request.form['password']
                if len(email)>0:
                        print(user.getPasswordByEmail(email))
                        if password == user.getPasswordByEmail(email):
                                # msg = {"class":"success", "text": "Loggin correct"}
                                return setSessionUserData(email)
                        else:
                                msg = {"class":"alert", "text": "Email or Password incorrect, check and try again."}
                                return render_template('log-in.html', nav=getNav(), title=title, msg = msg, ehaData = None)
                else:
                        return render_template('log-in.html', nav=getNav(), title=title, msg = None, ehaData = {"email":"test01@test.com", "password":"1234"})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashBoard():
        if isAuth():
                msg = None
                if not request.method=='GET':
                        msg = manageTask("UPD")
                if (msg):
                        msg = msg['msg']
                return render_template('dashboard.html', nav=getNav(), title="Dashboard:", task = task.getByUserId(session['user']['id']), msg = msg)
        else:
                return redirect(url_for('logIn'))

@app.route('/todo-new', methods=['GET', 'POST'])
def todoNew():
        title = "Task New"
        if isAuth():
                taskData = None
                msg = None
                if not request.method=='GET':
                        msg = manageTask("INS")
                if (msg and msg.get('res')):
                        return redirect(url_for('dashBoard'))
                else:
                        if (msg):
                                task = msg['taskData']
                                msg = msg['msg']
                        return render_template('todo-new.html', nav=getNav(), title=title, task = taskData, msg = msg)
        else:
                return redirect(url_for('logIn'))

def manageTask(action):
        title = request.form['title']
        done = request.form.getlist('done')#['done']
        if done==["on"]:
                done = True
        else:
                done = False
        # print(request.form)
        taskData = {
                "title" : title, 
                "done" : done
        }
        # print(taskKData)
        if len(title)>0:
                if action=="INS":
                        res = task.create(session['user']['id'], title, done)
                elif action=="UPD":
                        res = task.update(request.form['id'], session['user']['id'], title, done)
                print(res)
                if res.get('res'):
                        msg = {"res": res['res'], "taskData": taskData, "msg": {"class":"success", "text": res.get('txt')}}
                        # return dashBoard()
                else:
                        msg = {"res": res['res'], "taskData": taskData, "msg": {"class":"alert", "text": res.get('txt')}}
        else:
                msg = {"res": None, "taskData": taskData, "msg": {"class":"alert", "text": "Fill the title, and try again."}}
        return msg
                
@app.route('/user-edit', methods=['GET', 'PATCH', 'POST'])
def userEdit():
        title = "Account Settings:"
        if isAuth():
                if request.method=='GET':
                        print(user.getById(session["user"]["id"])) #testing model user_id 1 hardcoded...
                        return render_template('user-edit.html', nav=getNav(), title=title, user = user.getObjByEmail(session["user"]["email"]), msg = None)
                else:
                        #id = request.form['id']
                        fname = request.form['fname']
                        lname = request.form['lname']
                        email = session['user']['email'] # request.form['email']
                        password = request.form['password']
                        print(request.form)
                        userData = {
                                "fname" : fname, 
                                "lname" : lname, 
                                "email" : email, 
                                "password" : password, 
                                #"id" : id
                        }
                        if len(fname)>0 and len(lname)>0 and len(email)>0 and len(password)>0:# and len(id)>0:
                                res = user.updateByEmail(fname, lname, password, email)
                                print(res)
                                if res.get('res'):
                                        msg = {"class":"success", "text": res.get('txt')}
                                else:
                                        msg = {"class":"alert", "text": res.get('txt')}
                                return render_template('user-edit.html', nav=getNav(), title=title, user = userData, msg = msg)
                        else:
                                return render_template('sign-up.html', nav=getNav(), title="Please Sign Up", user = userData, msg = {"class":"alert", "text": "Fill all the fields and check terms, please try again."})
                        #
                        email = request.form['email']
                        password = request.form['password']
                
        else:
                return redirect(url_for('logIn'))

@app.route('/log-out', methods=['GET'])
def logOut():
        session.pop('user', None)
        # return render_template('index.html', nav=getNav(), title="ToDo List", msg = {"class" : "success", "text" : "Logged out correctly."})
        return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def adminLogIn():
        title = "Admin, Please sign in"
        if request.method=='GET':
                return render_template('/admin/log-in.html', nav=getNav(), title=title, msg = None, ehaData = None)
        else:
                email = request.form['email']
                password = request.form['password']
                if len(email)>0:
                        print(admin.getPasswordByEmail(email))
                        if password == admin.getPasswordByEmail(email):
                                # msg = {"class":"success", "text": "Loggin correct"}
                                return setSessionUserData(email, True)
                        else:
                                msg = {"class":"alert", "text": "Email or Password incorrect, check and try again."}
                                return render_template('/admin/log-in.html', nav=getNav(), title=title, msg = msg, ehaData = None)
                else:
                        return render_template('/admin/log-in.html', nav=getNav(), title=title, msg = None, ehaData = {"email":"test01@test.com", "password":"1234"})

@app.route('/admin/dashboard', methods=['GET'])
def adminDashBoard():
        if isAuthAdmin():
                data = ({
                        "totalUsers" : user.getAllCount(),
                        "totalUsers24H" : user.getDayCount(),
                        "totalTasks" : task.getAllCount(),
                        "totalTasks24H" : task.getDayCount()
                        })
                return render_template('admin/dashboard.html', nav=getNav(), title="Admin - Dashboard:",  data = data, msg = None)
        else:
                return redirect(url_for('adminLogIn'))

@app.route('/admin/users', methods=['GET', 'POST'])
def adminUsers():
        print(request)
        if isAuthAdmin():
                if request.method=='POST':
                        res = user.delete(request.form['id'])
                        print(res)
                page = str2IntJLE0(request.args["page"]) if "page" in request.args else 1
                totalData = user.getAllCount()
                offSet = paginatePerPage*(page-1)
                data = ({
                        "page" : page+1,
                        "totalData" : totalData,
                        "paginatePerPage" : paginatePerPage,
                        "totalPages" : math.ceil(user.getAllCount()/paginatePerPage),
                        # "moreButon" : (paginatePerPage*page-1)+paginatePerPage<totalData,
                        "moreButon" : offSet+paginatePerPage<totalData,
                        # "detail" : user.getAll(None, paginatePerPage, page-1),
                        "detail" : user.getAll(None, paginatePerPage, offSet),
                        # "detail" : user.getAll("id < 100", 50),
                        # "detail" : user.getAll("id < 100"),
                        })
                return render_template('admin/users.html', nav=getNav(), title="Dashboard - Users:",  data = data, msg = None)
        else:
                return redirect(url_for('adminLogIn'))

@app.route('/admin/tasks', methods=['GET'])
def adminTasks():
        print(request)
        if isAuthAdmin():
                page = str2IntJLE0(request.args["page"]) if "page" in request.args else 1
                totalData = task.getAllCount()
                offSet = paginatePerPage*(page-1)
                data = ({
                        "page" : page+1,
                        "totalData" : totalData,
                        "paginatePerPage" : paginatePerPage,
                        "totalPages" : math.ceil(task.getAllCount()/paginatePerPage),
                        "moreButon" : offSet+paginatePerPage<totalData,
                        "detail" : task.getAll(None, paginatePerPage, offSet),
                        })
                return render_template('admin/tasks.html', nav=getNav(), title="Dashboard - Tasks:",  data = data, msg = None)
        else:
                return redirect(url_for('adminLogIn'))

def isAuth():
        if 'user' in session:
                # print('00001')
                #g.user=session['user']
                return True
        else:
                # print('00002')
                return False

def isAuthAdmin():
        if 'user' in session and session['user']['isAdmin'] :
                # print('00001')
                #g.user=session['user']
                return True
        else:
                # print('00002')
                return False

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

def setSessionUserData(email, isAdmin=False):
        data = user.getObjByEmail(email)
        session['user'] = {"id": data.get("id"), "email":email, "isAdmin":isAdmin}
        if (isAdmin):
                return redirect(url_for('adminDashBoard'))
        else:
                return redirect(url_for('dashBoard'))

#String to Int and if page <=0 then page = 1
def str2IntJLE0(page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print('\033[1m' + '\033[91m')
        print("ERROR (str2IntJLE0): "+str(e))
        print(chr(175)*20+'\033[0m')
    finally:
        return page if (not page<1) else 1

def getNav():
        # if (g.user==None):
        if not 'user' in session:
                return (
                        {"title": "Home", "href": "/"},
                        {"title": "Dashboard", "href": "/dashboard"},
                        {"title": "Sign Up", "href": "/sign-up"},
                        {"title": "Login", "href": "/log-in"},
                        {"title": "Admin", "href": "/admin"},
                )
        else:
                if not session['user']['isAdmin']:
                        return (
                                {"title": "Home", "href": "/"},
                                {"title": "Dashboard", "href": "/dashboard"},
                                {"title": "Account Settings", "href": "/user-edit"},
                                {"title": "Log Out", "href": "/log-out"}
                        )
                else:
                        return (
                                {"title": "Dashboard", "href": "/admin/dashboard"},
                                {"title": "Users", "href": "/admin/users"},
                                {"title": "Tasks", "href": "/admin/tasks"},
                                {"title": "Log Out", "href": "/log-out"}
                        )
# @app.route('/getsession')
# def getsession():
#     if 'user' in session:
#         return session['user']
#     return redirect(url_for('logIn'))

if __name__ == '__main__':
        app.run()
        #app.run(host = "0.0.0.0", port = 7000, debug = True)
