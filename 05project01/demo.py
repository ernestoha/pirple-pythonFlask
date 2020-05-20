from flask import Flask, render_template, request, session, redirect, url_for, g
from db import user, task #db models to use

app = Flask(__name__)
app.secret_key = '*SecretkeY*'

@app.route('/', methods=['GET'])
def home():
        return render_template('index.html', title="ToDo List", msg = None) #, username = session.get("username")
        # return render_template('index.html', title="ToDo List", msg = {"class":"success", "text":"Bla bla bla bla."})
        # return render_template('index.html', title="ToDo List", msg = {"class":"error", "text":"Bla bla bla bla."})

@app.route('/about', methods=['GET'])
def about():
        return render_template('about.html', title="About Us:", msg = None)

@app.route('/terms-of-use', methods=['GET'])
def termsOfUse():
        return render_template('terms-of-use.html', title="Terms Of Use:", msg = None)

@app.route('/privacy', methods=['GET'])
def privacy():
        return render_template('privacy.html', title="Privacy:", msg = None)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
        if request.method=='GET':
                return render_template('sign-up.html', title="Sign-Up:", user = None, msg = None)
        else:
                fname = request.form['fname']
                lname = request.form['lname']
                email = request.form['email']
                password = request.form['password']
                terms = request.form.getlist('terms')#['terms']
                print(request.form)
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
                        print(res)
                        if res.get('res'):
                                return setSessionUserData(email)
                                # msg = {"class":"success", "text": res.get('txt')}
                                # return render_template('sign-up.html', title="Sign-Up:", user = None, msg = msg)
                        else:
                                msg = {"class":"error", "text": res.get('txt')}
                                return render_template('sign-up.html', title="Sign-Up:", user = userData, msg = msg)
                else:
                        return render_template('sign-up.html', title="Sign-Up:", user = userData, msg = {"class":"error", "text": "Fill all the fields and check terms, please try again."})

@app.route('/log-in', methods=['GET', 'POST'])
def logIn():
        if request.method=='GET':
                return render_template('log-in.html', title="Log In:", msg = None, ehaData = None)
        else:
                email = request.form['email']
                password = request.form['password']
                if len(email)>0:
                        print(user.getPasswordByEmail(email))
                        if password == user.getPasswordByEmail(email):
                                # msg = {"class":"success", "text": "Loggin correct"}
                                return setSessionUserData(email)
                        else:
                                msg = {"class":"error", "text": "Email or Password incorrect, check and try again."}
                                return render_template('log-in.html', title="Log In:", msg = msg, ehaData = None)
                else:
                        return render_template('log-in.html', title="Log In:", msg = None, ehaData = {"email":"test01@test.com", "password":"1234"})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashBoard():
        if isAuth():
                msg = None
                if not request.method=='GET':
                        msg = manageTask("UPD")
                if (msg):
                        msg = msg['msg']
                return render_template('dashboard.html', title="Dashboard:", task = task.getByUserId(session['user']['id']), msg = msg)
        else:
                return redirect(url_for('logIn'))

@app.route('/todo-new', methods=['GET', 'POST'])
def todoNew():
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
                        return render_template('todo-new.html', title="Task New:", task = taskData, msg = msg)
        else:
                return redirect(url_for('logIn'))

def manageTask(action):
        title = request.form['title']
        done = request.form.getlist('done')#['done']
        if done==["on"]:
                done = True
        else:
                done = False
        print(request.form)
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
                        msg = {"res": res['res'], "taskData": taskData, "msg": {"class":"error", "text": res.get('txt')}}
        else:
                msg = {"res": None, "taskData": taskData, "msg": {"class":"error", "text": "Fill the title, and try again."}}
        return msg
                
@app.route('/user-edit', methods=['GET', 'PATCH', 'POST'])
def userEdit():
        if isAuth():
                if request.method=='GET':
                        print(user.getById(session["user"]["id"])) #testing model user_id 1 hardcoded...
                        return render_template('user-edit.html', title="Account Settings:", user = user.getObjByEmail(session["user"]["email"]), msg = None)
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
                                        msg = {"class":"error", "text": res.get('txt')}
                                return render_template('user-edit.html', title="Account Settings:", user = userData, msg = msg)
                        else:
                                return render_template('sign-up.html', title="Sign-Up:", user = userData, msg = {"class":"error", "text": "Fill all the fields and check terms, please try again."})
                        #
                        email = request.form['email']
                        password = request.form['password']
                
        else:
                return redirect(url_for('logIn'))

@app.route('/log-out', methods=['GET'])
def logOut():
        session.pop('user', None)
        # return render_template('index.html', title="ToDo List", msg = {"class" : "success", "text" : "Logged out correctly."})
        return redirect(url_for('home'))
                
def isAuth():
        if 'user' in session:
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

def setSessionUserData(email):
        data = user.getObjByEmail(email)
        session['user'] = {"id": data.get("id"), "email":email}
        return redirect(url_for('dashBoard'))

# @app.route('/getsession')
# def getsession():
#     if 'user' in session:
#         return session['user']
#     return redirect(url_for('logIn'))

if __name__ == '__main__':
        app.run(host = "0.0.0.0", port = 7000, debug = True)
