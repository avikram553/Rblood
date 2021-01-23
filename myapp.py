import sys
sys.setrecursionlimit(10**6) 
from flask import Flask,request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_mail import Mail,Message
from flask import g,session,flash



app=Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='123456789'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='requireblood10@gmail.com',
    MAIL_PASSWORD='hello553@',
    MAIL_DEFAULT_SENDER='requireblood10@gmail.com'

)
mail=Mail(app)
db=SQLAlchemy(app)

#Creting Database column as an instance variable of class Donor

class Donor(db.Model):
    
    Firstname=db.Column(db.String(20),unique=False)
    Lastname=db.Column(db.String(20),unique=False)
    Phone=db.Column(db.String(20),unique=True)
    Email=db.Column(db.String(20),primary_key=True,unique=True)
    Password=db.Column(db.String(20),unique=False)
    Address=db.Column(db.String(120))
    Pincode=db.Column(db.Integer,unique=False)
    State=db.Column(db.String(15),unique=False)
    City=db.Column(db.String(15),unique=False)
    Landmark=db.Column(db.String(15),unique=False)
    Bloodgroup=db.Column(db.String(4),unique=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/Join_as_aDonor/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        #Fetch Forn Data
        
        Firstname=request.form.get('f_name')
        Lastname=request.form.get('l_name')
        Phone=request.form.get('phone')
        Email=request.form.get('email')
        Password=request.form.get('password')
        Address=request.form.get('address')
        Pincode=request.form.get('pincode')
        State=request.form.get('state')
        City=request.form.get('city')
        Landmark=request.form.get('l_mark')
        Bloodgroup=request.form.get('b_group')
        entry=Donor(Firstname=Firstname,Lastname=Lastname,Phone=Phone,Password=Password,Email=Email,Address=Address,Pincode=Pincode,State=State,City=City,Landmark=Landmark,Bloodgroup=Bloodgroup)
        db.session.add(entry)
        db.session.commit()
        
        #Sending ThankYou mails for the newly registered Donors
        
        

        mail.send_message('Aditya from RBlood',
                        sender='requireblood10@gmail.com',
                        recipients=[Email],
                        body='Thank You! For joining our hands in this initiative. Your details has been updated in our database,we will notify you whenever someone require blood in your city'
                         )

        return render_template('Thank_you.html')
    return render_template('Join_as_aDonor.html',title='Donor Form')

#Redirects to the loginpage when clicked on Login Button

@app.route('/login_validation')  
def login_validation():
    return render_template('loginpage.html')

#Checking the user already registered or not if yes then redirect it to Dashboard else Registration page

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['email']
        password=request.form['password']
        valid_user=Donor.query.filter(and_(Donor.Email.like(username),Donor.Password.like(password))).all()
        if len(valid_user):
            session['username']=username
            session['password']=password
            return render_template('dashboard.html')
        else:
            #Register Yourself First
            #Flash some mesaage  first then redirect to the given page
            flash('First register yourself as a donor')
            return render_template('Join_as_aDonor.html')

#Logging out

@app.route('/Logout')
def Logout():
    session.pop('username',None)
    session.pop('password',None)
    return render_template('index.html')



#For Changing his profile details
###############################################PROBLEM######################
@app.route('/profile',methods=['GET','POST'])
def profile():
    profile_data=Donor.query.filter(and_(Donor.Email.like(session['username']),Donor.Password.like(session['password']))).all()

    return render_template('profile.html',data=profile_data)
#############################################################################
#Redirecting to Forgot Password Page
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

#FLASH RESET LINK SENT
@app.route('/reset_link/',methods=['GET','POST'])
def reset_link():
    if request.method=='POST':
        email=request.form.get('email')
        user=Donor.query.filter(Donor.Email.like(email)).all()
        if len(user):
            session['email']=email
            with mail.connect() as conn:
                msg=Message("Password Reset link",recipients=[email])
                msg.html=render_template('/mails/reset_password.html',user=user)
                conn.send(msg)
                flash('Reset link has been sent to your Email id')
            return render_template('loginpage.html')
        else:
            flash('User Not found Please register yourself')
            return render_template('Join_as_aDonor.html')



#Reset Passowrd page 
@app.route('/resetpasspage/')
def resetpasspage():
    return render_template('newpassword.html')

#Change Password update in Database
@app.route('/reset_password/',methods=['GET','POST'])
def reset_password():
    if request.method=='POST':
        setpassword=request.form.get('setpassword')
        confirmpassword=request.form.get('confirmpassword')
        if setpassword==confirmpassword:
            finalpass=Donor.query.filter_by(Email=session['email']).update(dict(Password=setpassword))
            db.session.commit()
            session.pop('email',None)
            return render_template('loginpage.html')
        else:
            return flash('Password did not match','error')


    




@app.route('/Find_a_DONOR/',methods=['GET','POST'])
def find_donor():
    if request.method=='POST':
        l=list()
        form_data=request.form
        name=form_data['full_name']
        email=form_data['email']
        address=form_data['address']
        city=form_data['city']
        bloodgroup=form_data['b_group']
        phone=form_data['phone']
        l.append(name)
        l.append(phone)
        l.append(email)
        l.append(address)
        l.append(bloodgroup)

        record=Donor.query.filter(and_(Donor.City.like(city),Donor.Bloodgroup.like(bloodgroup))).all()
        #return record[0]
        if len(record)==0:
            #No Donor Found Page 
            return 'No Donor Found'
        else:
            
            with mail.connect() as conn:
                for i in record:
                    if i.Email==email:
                        record.remove(i)
                        #flag=True
                    else:
                    
                        msg=Message("Urgent Blood required",recipients=[i.Email])           
                        msg.html=render_template('/mails/urgentbloodreq.html',form_data=l)
                        conn.send(msg)

            if len(record)==0:
                #No Donor Found Page
                return 'No Donor Found'

            else:
                return render_template('out.html',record=record)
    return render_template('Find_a_DONOR.html')


if __name__=='__main__':
    app.run(debug=True)
