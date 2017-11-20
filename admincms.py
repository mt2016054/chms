import os
import datetime
from flask import Flask, redirect, url_for, request,render_template,jsonify,session
from flask_mysqldb import MySQL
from flask_mail import Mail
from werkzeug import secure_filename
from flask_mail import Message

mysql = MySQL()
app = Flask(__name__)
now = datetime.datetime.now()
app.secret_key = """hmsStudent"""
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'curfewManagement'
app.config['MYSQL_HOST'] = 'localhost'
UPLOAD_FOLDER = '/home/reshma/Desktop/curfewManagement/Documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
mysql.init_app(app)


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name
@app.route('/admin',methods=['POST', 'GET'])   
def login():
	return render_template('loginadmin.html',msg="")
@app.route('/logout',methods=['POST', 'GET'])   
def logout():
	session.pop('username', None)
	session.pop('userId', None)
	session.pop('mailId',None)
	return render_template('loginadmin.html',msg="Logout Successfully...")	

@app.route('/approverhome',methods=['POST', 'GET'])
def loadApplication():
	userId=request.form['user']
	password=request.form['pass']
	print('Reshma')
	print(request.form['login'])
	if isAuthenticated(userId,password)==1:
		session['userId']=userId;
		rowsOpen=openTicket()
		rowsClose=closeTicket()
		return render_template('Approver.html',rowsOpen=rowsOpen,rowsClose=rowsClose,session=session)
	else:
		return render_template('loginadmin.html',msg="Incorrect Details")
	# else:
	# 	return securityCheck("""http://127.0.0.1:5000/home""")		
@app.route('/viewRequest/<ticketId>',methods=['POST', 'GET'])
def viewRequest(ticketId):
	list = getTransaction(ticketId)
	return jsonify(result=list)	
def isAuthenticated(userId,password):
	cur = mysql.connection.cursor()
	row= cur.execute("SELECT userName,EmailId FROM user where UserId='"+userId+"' and password='"+password+"' and role=2")
	if row==1:
		r=cur.fetchone()
		session['mailId']=r[1];
		session['username']=r[0];

	return row	
def getTransaction(ticketId):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM RequestTransaction R left outer join requestAttachment A on R.TransId=A.TransId where R.requestId="+str(ticketId))
	row = cur.fetchall()
	print(row)
	return row	
def openTicket():
	cur = mysql.connection.cursor()
	cur.execute("SELECT RequestId,UserId,EventDate,description FROM RequestTransaction where Event=1 and RequestId not in(select RequestId from RequestTransaction where Event=3)")
	row=cur.fetchall()
	return row
def closeTicket():
	cur = mysql.connection.cursor()
	cur.execute("SELECT RequestId,UserId,EventDate,description FROM RequestTransaction where Event=1 and RequestId in(select RequestId from RequestTransaction where Event=3)")
	row=cur.fetchall()
	return row	
if __name__ == '__main__':
   app.run(debug = True)	