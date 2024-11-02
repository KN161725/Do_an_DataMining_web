from flask import render_template,redirect,request,url_for,session
from urllib.parse import urlparse
import joblib
import numpy as np
import string
import secrets

def set_route(app):
    model=joblib.load('model.joblib')
    @app.route("/")
    def Home_page():
        return render_template("Home_page2.html")
    
    @app.route("/input_data",methods=["GET","POST"])
    def input_data():
        if request.method=="POST":
            rq=request
            if rq!=None:    
                count=0
                try:
                    age=int(rq.form["age"])
                except:
                    age="Invalid"
                    count+=1
                
                try:
                    systolicBP=float(rq.form["systolicBP"])
                except:
                    systolicBP="Invalid"
                    count+=1
                
                try:
                    diastolicBP=float(rq.form["diastolicBP"])
                except:
                    diastolicBP="Invalid"
                    count+=1
                
                try:
                    bs=float(rq.form["bs"])
                except:
                    bs="Invalid"
                    count+=1
                
                try:
                    bodyTemp=float(rq.form["bodyTemp"])
                except:
                    bodyTemp="Invalid"
                    count+=1
                
                try:
                    heartRate=float(rq.form["heartRate"])
                except:
                    heartRate="Invalid"
                    count+=1
                
                if count>0:
                    dict_=dict(age=age, systolicBP=systolicBP, diastolicBP=diastolicBP, bs=bs, bodyTemp=bodyTemp, heartRate=heartRate)
                    return render_template("Error_Input.html",**dict_)
                y_pred=model.predict([[age, systolicBP, diastolicBP, bs, bodyTemp, heartRate]])[0]
                session['Result']=y_pred
                return redirect(url_for('result'))
            return render_template("Input_data2.html")
        return render_template("Input_data2.html")
    
    @app.route("/result")
    def result():
        #Secure 
        rff=request.headers.get("Referer")
        url_cur=urlparse(rff)
        
        if (rff!=None) & (url_cur.path==url_for('input_data')):
            return render_template("Result.html",y_pred=session['Result'])
        else: return redirect(url_for('Home_page'))
        

def secret_key(tmp):
    chars=string.digits+string.ascii_letters+string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(tmp))
    
