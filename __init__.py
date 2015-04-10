from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import ldap
import os
import cgi
from functools import wraps
app = Flask(__name__)
app.secret_key = 'key'
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
@app.route('/admin')
@login_required
def welcome():
    return render_template('index.html')  

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
  	ldap_server="ldap://url:389/"
	form = cgi.FieldStorage()
	username =  form.getvalue('username')
	password =  form.getvalue('password')
	username = request.form['username']
	password = request.form['password']
	# ldap settings
	user_dn = "uid="+username+",ou=users,dc=example.com"
	base_dn = "dc=example.com"
	connect = ldap.initialize(ldap_server)
	search_filter = "uid="+username
	try:
		#if authentication successful, get the full user data
		connect.bind_s(user_dn,password)
		result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
		# return all user data results
		connect.unbind_s()
		session['logged_in'] = True
		return redirect(url_for('welcome'))
		
	except ldap.LDAPError:
		connect.unbind_s()
		error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)
@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were logged out.')
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = False
    app.run(debug=True)
