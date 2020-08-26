from flask import Flask,request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
app=Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class Donor(db.Model):
    
    Firstname=db.Column(db.String(20),unique=False)
    Lastname=db.Column(db.String(20),unique=False)
    Phone=db.Column(db.String(20),unique=True)
    Email=db.Column(db.String(20),primary_key=True,unique=True)
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
        Address=request.form.get('address')
        Pincode=request.form.get('pincode')
        State=request.form.get('state')
        City=request.form.get('city')
        Landmark=request.form.get('l_mark')
        Bloodgroup=request.form.get('b_group')
        entry=Donor(Firstname=Firstname,Lastname=Lastname,Phone=Phone,Email=Email,Address=Address,Pincode=Pincode,State=State,City=City,Landmark=Landmark,Bloodgroup=Bloodgroup)
        db.session.add(entry)
        db.session.commit()
        return render_template('Thank_you.html')
    return render_template('Join_as_aDonor.html',title='Donor Form')

@app.route('/Find_a_DONOR/',methods=['GET','POST'])
def find_donor():
    if request.method=='POST':
        form_data=request.form
        email=form_data['email']
        city=form_data['city']
        bloodgroup=form_data['b_group']
        record=Donor.query.filter(and_(Donor.City.like(city),Donor.Bloodgroup.like(bloodgroup))).all()
        #return record[0]
        if len(record)==0:
            #No Donor Found Page 
            return 'No Donor Found'
        else:
            for i in record:
                if i.Email==email:
                    record.remove(i)
                    break
            if len(record)==0:
                #No Donor Found Page
                return 'No Donor Found'

            else:
                return render_template('out.html',record=record)
    return render_template('Find_a_DONOR.html')


if __name__=='__main__':
    app.run(debug=True)
