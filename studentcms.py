import os
import datetime
from flask import Flask, redirect, url_for, request,render_template,jsonify,session,send_file
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
app.config['UPLOAD_FOLDER'] = '/documents'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
mysql.init_app(app)


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/',methods=['POST', 'GET'])   
def login():
	return render_template('login.html',msg="")


@app.route('/logout',methods=['POST', 'GET'])   
def logout():
	session.pop('username', None)
	session.pop('userId', None)
	session.pop('mailId',None)
	return render_template('login.html',msg="Logout Successfully...")	


@app.route('/home',methods=['POST', 'GET'])
def loadApplication():
	if 'username' not in session:
		userId=request.form['user']
		password=request.form['pass']
		if isAuthenticated(userId,password)==1:
			session['userId']=userId
			rows=getTickets(userId)
			return render_template('Home.html',rows=rows,msg="",session=session)
		if isAuthenticated(userId,password)==2:
			session['userId']=userId
			rowsOpen=openTicket()
			rowsClose=closeTicket()
			notAppliedViolation=getNotAppliedViolation();
			appliedbutNotApproved=getAppliedButNotApproved();
			return render_template('Approver.html',rowsOpen=rowsOpen,rowsClose=rowsClose,rowsapplied=appliedbutNotApproved,rowsnotapplied=notAppliedViolation,session=session)

		else:
			return render_template('login.html',msg="Incorrect Details")
	else:	
		if session['role']==1:
			rows=getTickets(session['userId'])
			return render_template('Home.html',rows=rows,msg="",session=session)
		if session['role']==2:
			rowsOpen=openTicket()
			rowsClose=closeTicket()
			return render_template('Approver.html',rowsOpen=rowsOpen,rowsClose=rowsClose,session=session)
	 	#return securityCheck("""http://127.0.0.1:5000/home""")	

def securityCheck(url):
	return render_template('loginSecurity.html',url=url,msg="Login ....")


@app.route('/viewRequest/<ticketId>',methods=['POST', 'GET'])
def viewRequest(ticketId):
	list = getTransaction(ticketId)
	return jsonify(result=list)

############################code for approval and rejection 28/10/2017##################################
@app.route('/approve',methods=['POST', 'GET'])
def approve():
	reason=request.form['reply']
	requestId=request.form['hidden_name_reqId']
	approveRequest(requestId,reason)
	return "approved"

def approveRequest(ticketId,reason):
	cur = mysql.connection.cursor()
	#UPDATE `curfewManagement`.`requestDetail` SET `status`='3' WHERE `requestId`='29';
	cur.execute("UPDATE requestDetail SET status='3' WHERE requestId='"+str(ticketId)+"'")
	cur.execute("insert into curfewManagement.RequestTransaction(RequestId,UserID,Event,EventDate,description)values("+str(ticketId)+",'"+session['userId']+"',3,'"+str(now)+"','"+reason+"')")
	mysql.connection.commit()
	
@app.route('/reject/<ticketId>',methods=['POST', 'GET'])
def reject(ticketId):
	rejectRequest(ticketId)
	return "rejected!!"

def rejectRequest(ticketId):
	cur = mysql.connection.cursor()
	#UPDATE `curfewManagement`.`requestDetail` SET `status`='3' WHERE `requestId`='29';
	cur.execute("UPDATE requestDetail SET status='4' WHERE requestId='"+str(ticketId)+"'")
	cur.execute("insert into curfewManagement.RequestTransaction(RequestId,UserID,Event,EventDate,description)values("+str(ticketId)+",'"+session['userId']+"',4,'"+str(now)+"','"+reason+"')")
	mysql.connection.commit()
	
@app.route('/submitReplyApprover',methods=['POST', 'GET'])	
def submitReplyApprover():
	userId=session['userId']
	reason=request.form['reply']
	#file = request.files['file_upload1']
	requestId=request.form['hidden_name_reqId']
	transId=insertTransaction(requestId,userId,reason,1)
	#list = getTransaction(requestId)
	return "success"
############################ends code for approval and rejection 28/10/2017##################################

@app.route('/submitReply',methods=['POST', 'GET'])	
def submitReply():
	userId=session['userId']
	reason=request.form['reply']
	file = request.files['file_upload1']
	requestId=request.form['hidden_name_reqId']
	transId=insertTransaction(requestId,userId,reason,1)
	url=""
	if file.filename != '':
	 	filename = secure_filename(file.filename)
	 	filename=filename+"_"+str(transId)
	 	url=os.path.join(app.config['UPLOAD_FOLDER'], filename)
	 	print(url)
	 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	 	storeFileAttachment(transId,url)
	#list = getTransaction(requestId)
	return "success"

# @app.route('/call_modal',methods=['POST', 'GET'])
# def call_modal2():
# 	print(uId)
# 	name1='Reshma'
	
# 	rows=getTickets('MT2016054')
# 	#return 
# 	response = Flask.make_response(render_template('Home.html',rows=rows),200)
# 	return redirect(url_for('loadApplication',userId='MT2016054')+'#viewRequestModal',code=302,Response=response)
	
# 	#return redirect('http://127.0.0.1:5000/MT2016054#viewRequestModal')
@app.route('/attachment/<transId>', methods=['GET', 'POST'])
def download(transId):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print("Path")
    print(uploads)
    # return send_from_directory(directory=uploads, filename='2.png',as_attachment=True)
    row=attachedFile(transId)
    try:
    	return send_file(uploads+'/'+row[0], attachment_filename='download.jpg')
    except Exception as e:
    	return str(e)

def attachedFile(transId):
	cur = mysql.connection.cursor()
	#b=cur.execute("insert into  RequestTransaction(RequestId,UserId,Event,EventDate,description)values("+str(requestId)+",'"+userId+"',"+str(event)+",'"+str(now)+"','"+reason+"')")
	cur.execute("SELECT filePath FROM requestAttachment where transId="+str(transId))
	mysql.connection.commit()
	row = cur.fetchone()
	return row
@app.route('/fine',methods=['POST','GET'])
def getNotApprovedViolations():
	print("hello")
	# notAppliedViolation=getNotAppliedViolation();
	# appliedbutNotApproved=getAppliedButNotApproved();


# SELECT r.movementViolations_id,r.studentID,r.violationTime,s.RequestId,s.status,
#  (case violationType when 1 then 'Curfew Violation' when 2 then 'Core Curfew Violation' end), 
#  (case exitOrEntry when 1 then 'Entry' when 0 then 'Exit' end) 
#  FROM studentMovement.movementViolations r ,curfewManagement.requestDetail s
#  where s.studentId=r.studentId and
#  s.outdate<=date(r.violationTime) and s.indate>=date(r.violationTime) and status!=3;

	cur.execute("select ")
def getNotAppliedViolation():
	cur=mysql.connection.cursor()
	cur.execute("SELECT r.studentID,r.violationTime,r.violationType,r.movementViolations_id from studentMovement.movementViolations r where not exists(select * from curfewManagement.requestDetail s where r.studentID=s.studentId and s.outdate<=(r.violationTime) and indate>=(r.violationTime))")
	row=cur.fetchall()
	return row
def getAppliedButNotApproved():
	cur=mysql.connection.cursor()
	cur.execute("SELECT r.studentID,r.violationTime,r.violationType,r.movementViolations_id,s.RequestId,s.status,(case violationType when 1 then 'Curfew Violation' when 2 then 'Core Curfew Violation' end),(case exitOrEntry when 1 then 'Entry' when 0 then 'Exit' end) FROM studentMovement.movementViolations r ,curfewManagement.requestDetail s where s.studentId=r.studentId and s.outdate<=(r.violationTime) and s.indate>=(r.violationTime) and status!=3")
	row=cur.fetchall()
	return row
@app.route('/apply',methods = ['POST', 'GET'])
def raiseTicket():
#date slot name_reason approver name_rollno name_name name_email
	userId=session['userId']
	if request.method == 'POST':
		studentList="";
		studentString="";
		studentgroup=[]
		f = request.form
		for key in f.keys():
			for value in f.getlist(key):
				if "student" in key:
					studentList=studentList+"'"+value+"'"+","
					studentgroup.append(value)
					studentString=studentString+value+","
					print (key,":",value)

		studentList=studentList[:-1]
		studentString=studentString[:-1]
		print(studentList)
		reason=request.form['reason']
		#requestUser=session['user']
		#Do remove type
		requesttype=request.form['requesttype']
		#approver_id=request.form['approver']
		#time=request.form['timeSlot']
		time=1
		reqTypeId=3
		if requesttype=="LateIn":
		 	reqTypeId=1
		elif requesttype=="LateOut":
			reqTypeId=2
		
		outdate=request.form['outdate']
		outimeslot=request.form['hidden_outtime']
		print("reshma")
		print(outimeslot)
		indate=request.form['indate']
		intimeslot=request.form['hidden_intime']
		outdateTime=outdate;
		if outimeslot=="out1":
			outimeslot=1
			outdateTime=outdateTime+" "+"06:00:00"
		elif outimeslot=="out2":
			outimeslot=2
			outdateTime=outdateTime+" "+"22:00:00"
		elif outimeslot=="out3":
			outimeslot=3
			outdateTime=outdateTime+" "+"23:59:59"
		elif outimeslot=="out4":
			outimeslot=4
			outdateTime=outdateTime+" "+"03:00:00"
		print(outdateTime)      
		outdateTime=datetime.datetime.strptime(outdateTime, '%m/%d/%Y %H:%M:%S')

		indateTime=indate;
		if intimeslot=="in1":
			intimeslot=1
			indateTime=indateTime+" "+"22:00:00"
		elif intimeslot=="in2":
			intimeslot=2
			indateTime=indateTime+" "+"23:59:59"
		elif intimeslot=="in3":
			intimeslot=1
			indateTime=indateTime+" "+"03:00:00"
		elif intimeslot=="in4":
			intimeslot=1
			indateTime=indateTime+" "+"06:00:00"	

		indateTime=datetime.datetime.strptime(indateTime, '%m/%d/%Y %H:%M:%S')
		#update get mail id list
		approverMailIdList=fetchMailIdforApprover()
		print (approverMailIdList)
		studentMailIdList=fetchMailIdforStudents(studentList)
		print(studentMailIdList)
		transId,requestId=storeRequest(userId,reqTypeId,outdateTime,outimeslot,indateTime,intimeslot,reason)
		print("reshma")
		print(studentgroup)
		storeAllAppliedIds(requestId,studentgroup)

		file = request.files['file']
		url=""
		if file.filename != '':
		 	filename = secure_filename(file.filename)
		 	filename="_"+str(transId)+filename
		 	#url=os.path.join(app.config['UPLOAD_FOLDER'], filename)
		 	#print(url)uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']+filename)
		 	file.save( os.path.join(app.root_path, app.config['UPLOAD_FOLDER']+filename))
		 	#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		 	storeFileAttachment(transId,filename)
		sendMail(requestId,studentMailIdList,reason,requesttype,approverMailIdList,time,studentString)
		rows=getTickets(userId)
		return render_template('Home.html',session=session,rows=rows,msg="Request is submitted with Ticket Id:"+str(requestId))
	else:
		return redirect(url_for('success',name = "reshma"))	
		
def storeAllAppliedIds(requestId,studentgroup):
	cur = mysql.connection.cursor()
	for id in studentgroup:
		cur.execute("insert into student_request values("+str(requestId)+" ,'"+id+"')")
		mysql.connection.commit()	

def isAuthenticated(userId,password):
	cur = mysql.connection.cursor()
	row= cur.execute("SELECT userName,EmailId,role FROM user where UserId='"+userId+"' and password='"+password+"'")
	if row==1:
		r=cur.fetchone()
		session['mailId']=r[1];
		session['username']=r[0];
		session['role']=r[2]
	return r[2]



def insertTransaction(requestId,userId,reason,event):
	cur = mysql.connection.cursor()
	b=cur.execute("insert into  RequestTransaction(RequestId,UserId,Event,EventDate,description)values("+str(requestId)+",'"+userId+"',"+str(event)+",'"+str(now)+"','"+reason+"')")
	cur.execute("select max(TransId) from RequestTransaction where RequestId="+str(requestId))
	mysql.connection.commit()
	row = cur.fetchone()
	transId=row[0]
	return transId


def storeRequest(studentId,requestType,outdate,outimeslot,indate,intimeslot,reason):
	#storeRequest(studentId,outdate,outimeslot,indate,intimeslot,reason,'null','null',1)
	cur = mysql.connection.cursor()
	a=cur.execute("insert into requestDetail(studentId,outDate,outTime,inDate,inTime,requestDate,status,requestType) values('"+studentId+"','"+str(outdate)+"',"+str(outimeslot)+",'"+str(indate)+"',"+str(intimeslot)+",'"+str(now)+"',1,"+str(requestType)+")")
	cur.execute("select max(requestId) from requestDetail where studentId='"+studentId+"'")
	mysql.connection.commit()
	row = cur.fetchone()
	requestId=row[0]
	b=cur.execute("insert into  RequestTransaction(RequestId,UserId,Event,EventDate,description)values("+str(requestId)+",'"+studentId+"',1,'"+str(now)+"','"+reason+"')")
	cur.execute("select max(TransId) from RequestTransaction where RequestId="+str(requestId))
	mysql.connection.commit()
	row = cur.fetchone()
	transId=row[0]
	return transId,requestId


def getTransaction(ticketId):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM RequestTransaction R left outer join requestAttachment A on R.TransId=A.TransId where R.requestId="+str(ticketId))
	print("tickets:")
	row = cur.fetchall()
	print(row)
	return row


def fetchMailIdforApprover():
	string=''
	cur = mysql.connection.cursor()
	cur.execute("SELECT EmailId FROM user where role=2")
	row = cur.fetchall()
	return row[0]


def fetchMailIdforStudents(studentRollNoList):
	emailList=[]
	cur = mysql.connection.cursor()
	cur.execute("SELECT EmailId FROM user where UserId in ("+studentRollNoList+")")
	rows = cur.fetchall()
	for row in rows:
		emailList.append(row[0])
	return emailList


def sendMail(ticketId,studentMailIdList,reason,requesttype,approverMailId,time,studentRollNoList):
	print(studentRollNoList)
	with app.app_context():
		app.config.update(
			DEBUG=True,
			#EMAIL SETTINGS
			MAIL_SERVER='smtp.office365.com',
			MAIL_PORT=587,
			MAIL_USE_TLS=True,
			MAIL_USERNAME = 'farooqui.mujib@iiitb.org',
			MAIL_PASSWORD = 'RES12@res12'
			)
		mail = Mail(app)
		msgStudent = Message("CHMS",sender="farooqui.mujib@iiitb.org",recipients=studentMailIdList)
		
		ref=url_for('viewRequest',ticketId=ticketId)
		print("REshma")
		print(ref)
		#ref="\"http://localhost:5000/MT2016054\"";
		ref="\"http://localhost:5000/"+session['userId']+"\"";
		print(ref)
		#msgStudent.html="<p>Dear Student,</br>Your request is recorded with Request Id: "+str(ticketId)+"</p><p></br> <a href="+ref+">view/reply the request:</a> </br></p><p></br>Regards,</br>CHM Team</p>"
		msgStudent.html = "<p>Dear Student,</br>Your request is recorded with Request Id: "+str(ticketId)+"</p><p></br> <a href="+ref+">view/reply the request:</a> </br></p><p></br>Regards,</br>CHM Team</p>"
		
		mail.send(msgStudent)
		msgApprover = Message("CHMS",sender="farooqui.mujib@iiitb.org",recipients=["farooqui.mujib@iiitb.org"])
		msgApprover.html="<p>Request is Pending for your approval for <b>"+requesttype+"</b> permission with following details:</br><b>Request Id:</b> "+str(ticketId)+"</br><b>Description:</b> "+reason+"</br><b>Date</b>: "+str(now)+"    <b>time:</b> "+str(time)+"</br><b>Applied Roll No:</b> "+studentRollNoList+"</p><p></br> <a href=""https://www.w3schools.com"">view/reply the request:</a> </br></p>"
		mail.send(msgApprover)


def storeFileAttachment(transId,filename):
	cur = mysql.connection.cursor()
	a=cur.execute("insert into requestAttachment(TransId,filePath)values("+str(transId)+",'"+filename+"')")
	mysql.connection.commit()


# @app.route('/login',methods = ['POST', 'GET'])
# def login():

# 	if request.method == 'POST':
# 		date=request.form['date']
# 		slot=request.form.get('slot')
# 		name_reason=request.form['name_reason']
# 		approver=request.form.get('approver')
# 		name_rollno=request.form['name_rollno']
# 		name_name=request.form['name_name']
# 		name_email=request.form['name_email']
# 		return redirect(url_for('success',name = "rachana"))
# @app.route('/viewTicketList/<userId>')
# def hello_name(userId):
# 	cur = mysql.connection.cursor()
# 	cur.execute("select requestId,requestDate,status from requestDetail where studentIdList like '%"+userId+"%'")
# 	rows = cur.fetchall()
# 	print(rows)
# 	return render_template('viewTickets.html', rows = rows)


def getTickets(userId):
	cur = mysql.connection.cursor()
	cur.execute("select r.requestId,r.requestDate,r.status from requestDetail r,student_request s where  s.requestId=r.requestId and s.studentId='"+userId+"'")
	rows = cur.fetchall()
	return rows


def openTicket():
	cur = mysql.connection.cursor()
	#cur.execute("SELECT RequestId,UserId,EventDate,description FROM RequestTransaction where Event=1 and RequestId not in(select RequestId from RequestTransaction where Event=3 and Event=4)")
	cur.execute("SELECT * FROM requestDetail where status not in(3,4)")
	row=cur.fetchall()
	return row


def closeTicket():
	cur = mysql.connection.cursor()
	#cur.execute("SELECT RequestId,UserId,EventDate,description FROM RequestTransaction where Event=1 and RequestId in(select RequestId from RequestTransaction where Event=3 and Event=4)")
	cur.execute("SELECT * FROM requestDetail where status in (3,4)")
	row=cur.fetchall()
	return row		


if __name__ == '__main__':
   app.run(debug = True)
