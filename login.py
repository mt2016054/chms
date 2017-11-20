from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name
@app.route('/',methods=['POST', 'GET']):

@app.route('/login',methods = ['POST', 'GET'])
def login():

	if request.method == 'POST':
		date=request.form['date']
		slot=request.form.get('slot')
		name_reason=request.form['name_reason']
		approver=request.form.get('approver')
		name_rollno=request.form['name_rollno']
		name_name=request.form['name_name']
		name_email=request.form['name_email']
		return redirect(url_for('success',name = "rachana"))
   
    

if __name__ == '__main__':
	app.run(debug = True)

