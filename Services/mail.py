from flask import Flask, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_mail import Message

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'curfewManagement'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name
   
@app.route('/applySingle',methods = ['POST', 'GET'])
def raiseTicket():
#date slot name_reason approver name_rollno name_name name_email
	if request.method == 'POST':
		studentList="";
		studentString=""
		f = request.form
		for key in f.keys():
			for value in f.getlist(key):
				if "student" in key:
					studentList=studentList+"'"+value+"'"+","
					studentString=studentString+value+","
					print (key,":",value)

		studentList=studentList[:-1]
		studentString=studentString[:-1]
		print(studentList)
		reason=request.form['reason']
		requesttype=request.form['requesttype']
		approver_id=request.form['approver']
		#time=request.form['timeSlot']
		time=1
		reqTypeId=3
		if requesttype=="In":
			reqTypeId=1
		elif requesttype=="Out":
			reqTypeId=2
		#f = request.files['file']
        #f.save(secure_filename(f.filename))
        print(f.filename)
		rdate=request.form['requestdate']
		print(approver_id)
		approverMailId=fetchMailIdforApprover(approver_id)
		print (approverMailId)
		studentMailIdList=fetchMailIdforStudents(studentList)
		print(studentMailIdList)
		ticketId=storeRequest(studentString,reason,reqTypeId,approver_id,rdate,1)
		sendMail(ticketId,studentMailIdList,reason,requesttype,approverMailId,rdate,time,studentString)
		return redirect(url_for('success',name = "Rachana"))
	else:
		return redirect(url_for('success',name = "reshma"))	

def storeRequest(studentRollNoList,reason,requesttype,approverId,rdate,time):
	cur = mysql.connection.cursor()
	print(requesttype)
	print(time)
	#print("insert into requestDetail(requestType,requestDate,timeslot,studentIdList,approverId,status) values(",requesttype,",'",rdate,"',",time,",'",studentRollNoList,"','",approverId,"',1)")
	a=cur.execute("insert into requestDetail(requestType,requestDate,timeslot,studentIdList,approverId,status) values("+str(requesttype)+",'"+rdate+"',"+str(time)+",'"+studentRollNoList+"','"+approverId+"',1)")
	cur.execute("select max(requestId) from requestDetail where studentIdList='"+studentRollNoList+"'")
	mysql.connection.commit()
	row = cur.fetchone()
	print(row)
	return row[0]

def fetchMailIdforApprover(approver_id):
	string=''
	cur = mysql.connection.cursor()
	cur.execute("SELECT EmailId FROM user where UserId='"+approver_id+"'")
	row = cur.fetchone()
	return row[0]

def fetchMailIdforStudents(studentRollNoList):
	emailList=[]
	cur = mysql.connection.cursor()
	cur.execute("SELECT EmailId FROM user where UserId in ("+studentRollNoList+")")
	rows = cur.fetchall()
	for row in rows:
		emailList.append(row[0])
	return emailList

def sendMail(ticketId,studentMailIdList,reason,requesttype,approverMailId,rdate,time,studentRollNoList):
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
		msgStudent.html = "<p>Dear Student,</br>Your request is recorded with Request Id: "+str(ticketId)+"</p><p></br> <a href=""https://www.w3schools.com"">view/reply the request:</a> </br></p><p></br>Regards,</br>CHM Team</p>"
		mail.send(msgStudent)
		msgApprover = Message("CHMS",sender="farooqui.mujib@iiitb.org",recipients=["farooqui.mujib@iiitb.org"])
		msgApprover.html="<p>Request is Pending for your approval for <b>"+requesttype+"</b> permission with following details:</br><b>Request Id:</b> "+str(ticketId)+"</br><b>Description:</b> "+reason+"</br><b>Date</b>: "+rdate+"    <b>time:</b> "+str(time)+"</br><b>Applied Roll No:</b> "+studentRollNoList+"</p><p></br> <a href=""https://www.w3schools.com"">view/reply the request:</a> </br></p>"
		mail.send(msgApprover)


if __name__ == '__main__':

   app.run(debug = True)
