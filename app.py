from flask import Flask,request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class Donor(db.Model):
    
    Firstname=db.Column(db.String(20))
    Lastname=db.Column(db.String(20))
    Email=db.Column(db.String(20))
    Address=db.Column(db.String(120))
    Pincode=db.Column(db.Integer, primary_key=True)
    State=db.Column(db.String(15))
    City=db.Column(db.String(15))
    Landmark=db.Column(db.String(15))
    Bloodgroup=db.Column(db.String(4))
@app.route("/")
def home():
    return render_template('index.html')
@app.route('/Join_as_aDonor/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        #Fetch Forn Data
        
        Firstname=request.form.get('f_name')
        Lastname=request.form.get('l_name')
        Email=request.form.get('email')
        Address=request.form.get('address')
        Pincode=request.form.get('pincode')
        State=request.form.get('state')
        City=request.form.get('city')
        Landmark=request.form.get('l_mark')
        Bloodgroup=request.form.get('b_group')
        entry=Donor(Firstname=Firstname,Lastname=Lastname,Email=Email,Address=Address,Pincode=Pincode,State=State,City=City,Landmark=Landmark,Bloodgroup=Bloodgroup)
        db.session.add(entry)
        db.session.commit()
        return render_template('Thank_you.html')
    return render_template('Join_as_aDonor.html')

app.run(debug=True)
