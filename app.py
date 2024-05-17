from flask import Flask,request,redirect,render_template,url_for,flash,session,send_file,abort
#from flask_mysqldb import MySQL
from flask_session import Session
from key import *
import mysql.connector
from sdmail import sendmail

import flask_excel as excel
import random
from itsdangerous import URLSafeTimedSerializer
from tokenreset import token
from io import BytesIO
from sotp import *

app=Flask(__name__)
app.secret_key='KS@917_PATHIVADA038'
app.config['SESSION_TYPE']='filesystem'
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='admin'
# app.config['MYSQL_DB']='spm'
mydb = mysql.connector.connect(host="localhost",user="root",password="Admin",db="fms")
Session(app)
#mysql=MySQL(app)
excel.init_excel(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        fid=request.form['fid']
        fname=request.form['fname']
        email=request.form['email']
        dept=request.form['dept']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from faculty where fname=%s',[fname])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from faculty  where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('register.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('register.html')
        data={'fid':fid,'fname':fname,'password':password,'email':email,'dept':dept}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm1(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        fname=data['fname']
        cursor.execute('select count(*) from faculty where fname=%s',[fname])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('login'))
        else:
            cursor=mydb.cursor(buffered=True)
            lst=[data['fid'],data['fname'],data['email'],data['dept'],data['password']]
            query='insert into faculty values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('login'))
@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
@app.route('/create',methods=['GET','POST']) 
def create():
    if session.get('user'):
        if request.method=='POST':
            time=int(request.form['time'])
            print(time)
            sid=tokgenotp()
            url = url_for('survey_start', token=token(sid, salt=salt), _external=True)

            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into survey(surveyid,url,fid) values(%s,%s,%s)',[sid,url,session.get('user')])
            mydb.commit()
            return redirect(url_for('dashboard'))
        return render_template('create.html')
    else:
        return redirect(url_for('login')) 
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
        #print(e)
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        username=data['username']
        cursor.execute('select count(*) from users where username=%s',[username])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('login'))
        else:
            cursor.execute('insert into users values(%s,%s,%s)',[data['username'],data['password'],data['email']])
            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('login'))
@app.route('/survey',methods=['GET','POST']) 
def survey():
    if session.get('user'):
        return render_template('survey.html')
    
    

@app.route('/survey/<token>',methods=['GET','POST'])
def survey_start(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        survey_dict=serializer.loads(token,salt=salt)
        sid=survey_dict
        
        if request.method=='POST':
            
            
            name=request.form['name']
            rollno=request.form['rollno']
            email=request.form['email']
            dept=request.form['dept']
            specailization=request.form['specialization']
            one=request.form['one']
            two=request.form['two']
            three=request.form['three']
            four=request.form['four']
            five=request.form['five']
            six=request.form['six']
            seven=request.form['seven']
            eight=request.form['eight']
            nine=request.form['nine']
            ten=request.form['ten']
            eleven=request.form['eleven']
            twelve=request.form['twelve']
            thirteen=request.form['thirteen']
            fourteen=request.form['fourteen']
            fifteen=request.form['fifteen']
            sixteen=request.form['sixteen']
            seventeen=request.form['seventeen']
            eighteen=request.form['eighteen']
            nineteen=request.form['nineteen']        
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into sur_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[sid,name,rollno,email,dept,specailization,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen])
            mydb.commit()
            return 'Survey submitted successfully'
        return render_template("survey.html")
    except Exception as e:
        print(e)
        abort(410,description='SUrvey link expired')

@app.route('/feedbackform/<token>')
def feedbackform(token):
    return 'success'
    

@app.route('/preview')
def preview():
    if session.get('user'):
        return render_template('survey.html')
    else:
        return redirect(url_for('login'))       


        

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')    

@app.route('/contactus',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        print(email)
        message=request.form['message']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into contact(name,email,message) values(%s,%s,%s)',[name,email,message])
        mydb.commit()

        return redirect(url_for('index'))
    return render_template('contactus.html')  

       
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        fid=request.form['fid']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from faculty where fid=%s  and password=%s',[fid,password])
        count=cursor.fetchone()[0]
        if count==0:
           
            flash('Invalid id or password')
            return render_template('login.html')
        else:
            session['user']=fid
            return redirect(url_for('dashboard'))
    return render_template('login.html')
   

@app.route('/forget',methods=['GET','POST'])
def forget():
    if request.method=='POST':
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from faculty where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('SELECT email from faculty where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(email,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('login'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update faculty set password=%s where email=%s',[newpassword,email])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('login'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash('already logged out!')
        return redirect(url_for('login'))  

@app.route('/allsurveys')
def allsurveys():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM survey where fid=%s order by created_at',[session.get('user')])
        data=cursor.fetchall()
        return render_template('allsurveys.html',surveys=data)
    else:
        return redirect(url_for('login'))  
@app.route('/download/<sid>')
def download(sid):
    cursor = mydb.cursor(buffered=True)

    lst = [
        'Name', 'Roll no', 'Email', 'dept',
        '1. Considering your overall experience with our college rate your ratings?',
        '2. The professors are well-trained and deliver the syllabus efficiently?',
        '3. Are you satisfied with the teaching staff and their teaching methods?',
        '4. How satisfied are you with the facilities provided by the college?',
        '5. How satisfied are you with your admission process in college?',
        '6. What are your views on the cafeteria and its hygiene and food quality?',
        '7. How satisfied are you with your admission process in college?',
        '8. Were the faculty and support staff helpful enough when you needed them?',
        '9. What are your views on the extra-curricular activities carried out in this college?',
        '10. What are your views on the cafeteria and its hygiene and food quality?',
        '11. What are the views on the sports area?',
        '12. How Professors are reliable and helpful?',
        '13. Is This college has well-equipped computer access facility?',
        '14. Is it easy to gain access to the resources through the college library?',
        '15. Do you think it is a good idea for your siblings or friends to pursue their career in this college?',
        '16. Do you think college pays enough attention to the racial and ethnic biases?',
        '17. Do you think the college responds accurately to bullying cases?',
        '18. What is your overall experience with the college?',
        '19. Please feel free to give your additional inputs on your experience with this college?'
    ]

    cursor.execute('SELECT * FROM sur_data WHERE sid=%s', (sid,))
    data = cursor.fetchall()

    if not data:
        return "No data found for the given SID.", 404

    user_data = [lst] + [list(row)[1:] for row in data]  # Skip the SID column in the result

    print(user_data)  # Debug print to verify data

    try:
        return excel.make_response_from_array(user_data, "xlsx", file_name="Faculty_data.xlsx")
    except Exception as e:
        return str(e), 500




if __name__=='__main__':
    app.run(debug=True,use_reloader=True)

   

       







           
           
       


