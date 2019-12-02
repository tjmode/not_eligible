from flask import Flask, render_template, request, redirect, url_for,session
import os
from flask_mysqldb import MySQL
import MySQLdb
app=Flask(__name__)
app.secret_key=os.urandom(24)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='flask'
mysql=MySQL(app)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="POST":
		getlogin=request.form
		username=getlogin['username']
		password=getlogin['password']
		conn = MySQLdb.connect(host="localhost", user = "root", passwd = "123456", db = "flask")
		cur = conn.cursor()
		cur.execute("select * from student_details")
		conn.commit()
		r=cur.fetchall()
		k=list(r)
		c=0
		for i in k:
			if i[0]==username:
				if i[2]==password:
					c=c+1
		if c==1:
			session['username']=username
			return render_template("welcomepage.html")
		else:
			return "something is wrong"	
	return render_template("login.html")

@app.route('/welcomepage', methods=['GET','POST'])
def welcomepage():
	return render_template("welcomepage.html")


@app.route('/adminpage', methods=['GET','POST'])
def adminpage():
	return render_template("adminpage.html")


@app.route('/fortestcreating',methods=['GET','POST'])
def fortestcreating():
	try:
		if request.method=="POST":
			gettablename=request.form
			tablename=gettablename['testname']
			conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
			cur=conn.cursor()
			cur.execute("select *from topics")
			conn.commit()
			alltopics=cur.fetchall()
			if tablename in alltopics:
				return "sorry try with other name this name is already taken"
			else:
				report="create table " +tablename+"_report (username varchar(100), mark varchar(10))"
				tablesql="create table "+tablename+ "(question varchar(1000),option_a varchar(100), option_b varchar(100), option_c varchar(100), option_d varchar (100))"
				conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
				cur=conn.cursor()
				session['t_name']=tablename
				cur.execute(tablesql)
				cur.execute(report)
				cur.execute("insert into topics(topics) values(%s)",[tablename])
				conn.commit()
				conn.commit()
				return redirect("/enteringpage")
		return render_template("fortestcreating.html")
	except:
		return "sorry tablename is already taken"

@app.route('/enteringpage',methods=['GET','POST'])
def enteringpage():
	if request.method=="POST":
		getquestions=request.form
		questions=getquestions['question']
		optiona=getquestions['a']
		optionb=getquestions['b']
		optionc=getquestions['c']
		optiond=getquestions['d']
		end=getquestions['end']
		if end=="end":
			return redirect('/answerkey')
		else:
			if 't_name' in session:
				conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
				cur=conn.cursor()
				cur.execute("insert into "+session["t_name"]+" (question,option_a,option_b,option_c,option_d) values(%s,%s,%s,%s,%s)",[questions,optiona,optionb,optionc,optiond])
				conn.commit()
				print("DONE")
				return render_template("enteringpage.html")
	return render_template("enteringpage.html")

@app.route('/practicecreating',methods=['GET','POST'])
def practicecreating():
	if request.method=="POST":
		gettablename=request.form
		tablename=gettablename['testname']
		tablesql="create table "+tablename+ "(question varchar(1000),option_a varchar(100), option_b varchar(100), option_c varchar(100), option_d varchar (100))"
		conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
		cur=conn.cursor()
		session['t_name']=tablename
		cur.execute(tablesql)
		cur.execute("insert into p_topics(topics) values(%s)",[tablename])
		conn.commit()
		conn.commit()
		return redirect("/enteringpage")
	return render_template("practicecreating.html")
	
@app.route('/answerkey', methods=['GET','POST'])
def anserkey():
	if request.method=='POST':
		getans=request.form
		ans=getans['ans'] 
		print("hello")
		if 't_name' in session:
			conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
			cur=conn.cursor()
			cur.execute("insert into answer_key(answer,tablename) values(%s,%s)",(ans,session['t_name']))
			conn.commit()
			print('yes')
			return redirect('/welcomepage')
	return render_template("answerkey.html")

@app.route('/testselection',methods=['GET','POST'])
def testselection():
	conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
	cur=conn.cursor()
	cur.execute("select * from topics")
	conn.commit()
	val=cur.fetchall()
	val1=list(val)
	dispaly = [item for t in val1 for item in t]
	print(dispaly)
	if request.method=='POST':
		gettopic=request.form 
		value=gettopic['starttest']
		session['selected']=value
		return redirect('/workingarea')
	return render_template("testselection.html",dispaly=dispaly)	

@app.route('/workingarea' ,methods=['GET','POST'])
def workingarea():
	if 'selected' in session:
		q=session['selected']
	conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
	cur=conn.cursor()
	m="select * from "+q
	cur.execute(m)
	conn.commit()
	vals=cur.fetchall()
	questions1=list(vals)
	questions2=[item for t1 in questions1 for item in t1]
	lsq=questions2[0::5]
	lsa=questions2[1::5]
	lsb=questions2[2::5]
	lsc=questions2[3::5]
	lsd=questions2[4::5]
	lenval=len(questions2)//5
	validation=[]
	co=0

	if request.method=='POST':
		getans=request.form
		print("frist") 
		for j in range(lenval):
			print("end")
			k="options"+str(j)
			ans=getans[k]
			validation.append(ans)
			co=co+1
	print(validation)
	session['valss']=validation
	if co>=1:
		return redirect('/answervalidation')
	return render_template("work.html", lsq=lsq,lsa=lsa,lsb=lsb,lsc=lsc,lsd=lsd,lenval=lenval)

@app.route('/answervalidation')
def mark():
	if 'valss' in session:
		val1=session['valss']
	if 'username' in session:
		username=session['username']
	if 'selected' in session:
		selected=session['selected']
	conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
	cur=conn.cursor()
	cur.execute("select * from answer_key")
	conn.commit()
	v=cur.fetchall()
	for i1 in v:
		if i1[1]==selected:
			v3=i1[0]
	v2=list(v3)
	mark=0
	print(val1)
	print(v2)
	for i in range(len(v2)):
		if val1[i]==v2[i]:
			mark=mark+1
	conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
	cur=conn.cursor()
	cur.execute("insert into "+selected+"_report (username,mark) values(%s,%s)",[username,mark])
	conn.commit()
	print("DONE")
	return ""
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method=="POST":
		getreg=request.form
		username=getreg['username']
		email=getreg['email']
		password=getreg['password']
		mark='0'
		conn=MySQLdb.connect(host="localhost",user="root",passwd="123456",db="flask")
		cur=conn.cursor()
		cur.execute("insert into student_details(username,email,password,mark) values(%s,%s,%s,%s)",(username,email,password,mark))
		conn.commit()
	return render_template("register.html")
if __name__ == '__main__':
	app.run(debug=True)