import sys
import os
#import glob
#import re
import numpy as np
# Flask utils
from flask import Flask, redirect, url_for, request, render_template,session
import sqlalchemy
from tensorflow.python.ops.template import _EagerTemplateVariableStore
from werkzeug.utils import secure_filename

# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


# database
import sqlite3 as sql


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'


#Model saved with Keras model.save()
MODEL_PATH ='model_resnet50.h5'                                                             

# Load your trained model
model = load_model(MODEL_PATH)


# Model saved with Keras model.save()
MODEL_PATH1 ='model_inception.h5'

# Load your trained model
model1 = load_model(MODEL_PATH1)

def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="The leaf is diseased cotton leaf"
    elif preds==1:
        preds="The leaf is diseased cotton plant"
    elif preds==2:
        preds="The leaf is fresh cotton leaf"
    else:
        preds="The leaf is fresh cotton plant"
        
    
    
    return preds

def model_predict1(img_path, model1):
    print(img_path)
    img1 = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img1)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
   # x = preprocess_input(x)

    preds = model1.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="Bacterial_spot"
    elif preds==1:
        preds="Early_blight"
    elif preds==2:
        preds="Late_blight"
    elif preds==3:
        preds="Leaf_Mold"
    elif preds==4:
        preds="Septoria_leaf_spot"
    elif preds==5:
        preds="Spider_mites Two-spotted_spider_mite"
    elif preds==6:
        preds="Target_Spot"
    elif preds==7:
        preds="Tomato_Yellow_Leaf_Curl_Virus"
    elif preds==8:
        preds="Tomato_mosaic_virus"
    else:
        preds="Healthy"
        
    
    
    return preds

@app.route('/predict1', methods=['GET', 'POST'])
def upload1():
    if request.method == 'POST':
        print("1 predict")
        # Get the file from post request
        f1 = request.files['file']
        print("2 pedict")

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads1', secure_filename(f1.filename))
        f1.save(file_path)

        # Make prediction
        preds = model_predict1(file_path, model)
        print("3 predict")
        result=preds
        return result
    else:
        return render_template('tomatopredict.html')
    return None



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('home.html')    

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    else:
        return render_template('userpredict.html')
    return None


    
@app.route('/feedback', methods=['GET','POST'])

def feedback():
    if request.method == 'POST':
        try:
            name = request.form['name']
            number = request.form['number']
            title = request.form['title']
            description = request.form['description']
            with sql.connect("leaf.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO feedback(farmername,mobilenumber,title,description) VALUES(?,?,?,?)",(name,number,title,description))
                con.commit
                msg="Record successfully added"
        
        except:
           # con.rollback()
            msg="error in insert operation"
        
        finally:
            return render_template("useraddfeedback.html",msg=msg)
            con.close()
    else:
        return render_template("useraddfeedback.html")



    #return render_template('blog.html')
    #return render_template('blog.html',data1=data1[1:])


#base code



@app.route('/about')
def about():
    return render_template("aboutus.html")



@app.route('/user')
def user():
    return render_template("userlogin.html")

@app.route("/signup", methods = ["GET","POST"])
def signup():
    msg=None
    if(request.method=="POST"):
        if (request.form["uname"]!="" and request.form["uname"]!="" and request.form["username"]!="" and request.form["upassword"]!=""):
            username=request.form["username"]
            password=request.form["upassword"]
            uname=request.form["uname"]
            uphone=request.form["uphone"]


            with sql.connect("leaf.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  signup VALUES('"+uname+"','"+uphone+"','"+username+"','"+password+"')")
                msg = "Your account is created"

                con.commit()
        else:
            msg="Something went wrong"


    return render_template("signup.html", msg=msg)



@app.route('/userloginNext',methods=['GET','POST'])
def userloginNext():
    msg=None
    if (request.method == "POST"):
        username = request.form['username']
      
        upassword = request.form['upassword']
        
        with sql.connect("leaf.db") as con:
            c=con.cursor()
            c.execute("SELECT username,upassword  FROM signup WHERE username = '"+username+"' and upassword ='"+upassword+"'")
            r=c.fetchall()
            for i in r:
                if(username==i[0] and upassword==i[1]):
                    session["logedin"]=True
                    session["username"]=username
                    return redirect(url_for("userhome"))
                else:
                    msg= "please enter valid username and password"
    
    return render_template("userlogin.html",msg=msg)



@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/adminloginNext',methods=['GET','POST'])
def adminloginNext():
    msg=None
    if (request.method == "POST"):
        ausername = request.form['username']
      
        apassword = request.form['apassword']
        
        with sql.connect("leaf.db") as con:
            c=con.cursor()
            c.execute("SELECT amail,apassword  FROM adminlogin WHERE amail = '"+ausername+"' and apassword ='"+apassword+"'")
            r=c.fetchall()
            for i in r:
                if(ausername==i[0] and apassword==i[1]):
                    session["logedin"]=True
                    session["fusername"]=ausername
                    return redirect(url_for("adminhome"))
                else:
                    msg= "please enter valid username and password"
    
    return render_template("admin.html",msg=msg)

#usercode
@app.route('/userhome')
def userhome():
    return render_template("userhome.html")

@app.route('/usergallery')
def usergallery():
    return render_template("usergallery.html")

@app.route('/viewfeedback', methods=['GET','POST'])
def viewfeedback():
    con=sql.connect("leaf.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from feedback")
    rows=cur.fetchall()
    
    return render_template("userviewfeedback.html",rows=rows)

@app.route('/userlogout')
def userlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('index'))

#admincode
@app.route('/adminhome')
def adminhome():
    return render_template("adminhome.html")

@app.route('/viewusers')
def viewusers():
    con=sql.connect("leaf.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select uname,uphone,username from signup")
    rows=cur.fetchall()
    print(rows)
    return render_template("adminviewusers.html",rows=rows)

@app.route('/adminviewfeedback', methods=['GET','POST'])
def adminviewfeedback():
    con=sql.connect("leaf.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from feedback")
    rows=cur.fetchall()
    
    return render_template("adminviewfeedback.html",rows=rows)


@app.route('/adminlogout')
def adminlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('index'))

@app.route('/viewdataset')
def viewdataset():
    return render_template("adminviewdataset.html")

if __name__ == '__main__':
    app.run(debug=True)
