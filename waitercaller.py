import datetime
import config
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
#if congif.test:
#    from mockdbhelper import MockDBHelper as DBHelper
#else:
from dbhelper import DBHelper
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from user import User
from forms import RegistrationForm, LoginForm, CreateTableForm

app = Flask(__name__)
login_manager = LoginManager(app)
# cat /dev/urandom | base64 | head -c 100; echo
app.secret_key = 'zkRnTGmcD2cGV0jTDEB5ycsjD7XQ+z'
# Globals
DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

@app.route("/")
def home():
    registrationform = RegistrationForm()
    loginform = LoginForm()
    return render_template("home.html", registrationform=registrationform, loginform=loginform)

# for users with cookie already assigned
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
    return render_template('home.html', loginform=form, registrationform=RegistrationForm())

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged Out")
    return redirect(url_for('home')) 

@app.route("/register", methods=['POST'])    
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', registrationform=form, loginform=LoginForm())
        
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template('home.html', registrationform=form, 
                                            onloadmessage="Registration Successful. Please log in.",
                                            loginform=LoginForm())
    return render_template('home.html', registrationform=form, loginform=LoginForm())


@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds % 60).zfill(2))    
    return render_template("dashboard.html", requests=requests)

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables, createtableform=CreateTableForm())

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    form = CreateTableForm(request.form)
    if form.validate():
        tableid = DB.add_table(form.tablenumber.data, current_user.get_id())
        new_url = BH.shorten_url(config.base_url + "newrequest/" + str(tableid))
        DB.update_table(tableid, new_url)
        return redirect(url_for('account'))
    return render_template("account.html", createtableform=form, tables=DB.get_tables(current_user.get_id()))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly."

@app.route("/dashboard/resolve")
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)


