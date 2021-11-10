from enum import unique
from os import name
from flask import Flask,request,Markup,Response,session
import flask
from flask.app import Flask
from flask.templating import render_template
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
from operator import itemgetter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError,OperationalError
from socket import gethostname,gethostbyname
import jinja2
import smtplib as sp
from email.message import EmailMessage
from flask_session import Session
from datetime import datetime,timedelta
from sqlalchemy import or_,and_
import matplotlib.pyplot as plt

ipik=str(gethostbyname(gethostname()))

app = Flask(  
    __name__ ,
    template_folder='templates',
    static_folder='static'  
)


app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///initDB.db'


app.secret_key='JKEF1_jkdshfjke5&&{sdf/7'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.permanent_session_lifetime=timedelta(minutes=20)

app.config['MAX_CONTENT_PATH']=5*1000*1000




db=SQLAlchemy(app)


global num_Users




class Fournisseure(db.Model):
    nom=db.Column(db.String(20),nullable=False)
    prenom=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(50),nullable=False,primary_key=True)
    phone=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    admin=db.Column(db.Boolean, default=False, nullable=False)
    art_S=db.relationship('Article',backref='owner')


class Reports(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    n_reporter=db.Column(db.String(30),nullable=False)
    e_reporter=db.Column(db.String(30),nullable=False)
    message=db.Column(db.Text)
    seen=db.Column(db.Boolean, default=False)


class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Reference=db.Column(db.String(30),nullable=False)
    nom=db.Column(db.String(30),nullable=False)
    stockage=db.Column(db.String(10),nullable=False)
    gpu=db.Column(db.String(20),nullable=False)
    prix=db.Column(db.String(10),nullable=False)
    ram=db.Column(db.String(10),nullable=False)
    data=db.Column(db.LargeBinary,nullable=False)
    typePIC=db.Column(db.Text,nullable=False)
    A_time=db.Column(db.String(20),default=datetime.today().strftime('%d-%m-%Y'))
    owner_email=db.Column(db.String(50),db.ForeignKey('fournisseure.email', ondelete='SET NULL'))



def findMail(S):
    for i in range(Fournisseure.query.count()+1):
        if i<Fournisseure.query.count():
            M=Fournisseure.query.all()[i].email
            if S == M:
                return i 
        else:
            return False


def viderFournisseure():
    for i in range(Fournisseure.query.count()):
        Mil=Fournisseure.query.all()[i].email

        Fournisseure.query.filter_by(email=Mil).delete()
        db.session.commit()



def E_sender(recever,MSaG):
    server = sp.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('este.acc@gmail.com','iliasilias')
    email=EmailMessage()
    email['From']='este.acc@gmail.com'
    email['To']=recever
    
    email['Subject']='Your account has been added successfully .You can login to your account by this address using the password bellow:'
    email.set_content(MSaG)
    server.send_message(email)


def read_All():
    for i in Reports.query.all():
        i.seen=True
    db.session.commit()
   


@app.route('/images/<NOME>')
def affich(NOME):
    toAFF=Article().query.filter_by(id=NOME).first()
    return Response(toAFF.data,mimetype=toAFF.typePIC)


@app.route('/')
def home():
    
        
    Article_S=Article.query.all()
    try :
        Admin=Fournisseure.query.filter_by(email=session['user']).first().admin
    except:
        Admin=False

    return render_template('home.html',ARts=Article_S,adrs=ipik,Admin=Admin)


@app.route('/login',methods=['GET','POST'])
def base():
    global msg
    global owner
    msg=''
    if 'user' not in session:
        if request.method=='POST':
            mail=request.form.get('email')
            password=request.form.get('mdp')
            if findMail(mail)!=False:
                if Fournisseure.query.all()[findMail(mail)].password==password and Fournisseure.query.all()[findMail(mail)].email==mail :
                    if Fournisseure.query.all()[findMail(mail)].admin==False:
                        global num_Users
                        num_Users=len(session)
                        msg=''
                        session.permanent=True
                        session['user']=Fournisseure.query.filter_by(email=mail).first().email
                        return redirect('/profile')

                    elif Fournisseure.query.all()[findMail(mail)].admin==True:
                            session['user']=Fournisseure.query.filter_by(email=mail).first().email
                            return redirect('/profile')

            else:
                msg='Aucun compte avec ces cordonnées'
    else:
        return redirect('/profile')

    if 'user' in session:
        statu='Vous êtes connecté'
        disco=Markup("""<div class="el" style="margin-left: 70px;">
          <div class="MGS">
            <a href="/Logout">
          <img src="../static/images/icons8-shutdown-24.png"  style="width: 60px;height: 60px;opacity: 1;margin-left: -30px; " alt=""></a></div>
        </div>""")

    else:
        statu='Connectez-vous'
        disco=''


    return render_template('login.html',msg=msg,disconnect=disco,statu=statu)


@app.route('/articles',methods=['GET','POST'])
def articles():
    global msg,U_del
    global num_Users
    num_Users=len(session)
    if request.method=='POST' and request.form.get('available')==None :
        ref=request.form.get('REF')
        nom=request.form.get('NOM')
        ram=request.form.get('RAM')
        gpu=request.form.get('GPU')
        stock=request.form.get('stockage')
        pric=request.form.get('Prix')
        image=request.files['fichier']
        tyPIC=image.mimetype
        owner=request.form.get('owner')
        
        try:
            dic=Article(Reference=ref,nom=nom,stockage=stock,ram=ram,gpu=gpu,prix=pric,data=image.read(),typePIC=tyPIC,owner_email=owner)
            db.session.add(dic)
            db.session.commit()

        except IntegrityError:
            return '<title>Shop</title><script>alert("OOPS") ;window.location.href = "http://%s:5122/articles"    </script>'%(ipik)

    elif request.method=='POST' and request.form.get('available')!=None:
        toDel=request.form.get('available')
        Article.query.filter_by(id=toDel).delete()
        db.session.commit()


    Article.query.filter(or_(Article.nom=='', Article.prix=='')).delete()
    db.session.commit()
        
     

    if 'user' in  session:
        try:
            if Fournisseure.query.filter_by(email=session['user']).first().admin:
                items=Article.query.all()
                Admin=True



            else :
                items=Article.query.join(Fournisseure).filter(Fournisseure.email==session['user']).all()
                Admin=False
                
            return render_template('Articles.html',items=items,adrs=ipik,User=Fournisseure.query.filter_by(email=session['user']).first(),Admin=Admin,fourns=Fournisseure.query.all()[3:])
        except AttributeError:
            return redirect('/Logout')
    else:
        return redirect('/login')
    

@app.route('/profile',methods=['GET','POST'])
def profile():
    if 'user' in session:
        if request.method=='POST':
            pwd=request.form.get('pwd')
            Fournisseure.query.all()[findMail(session['user'])].password=pwd
            db.session.commit()

        return render_template('profile.html',User=Fournisseure.query.filter_by(email=session['user']).first(),Id=findMail(session['user']))
    else:
        return redirect('/login')



@app.route('/report',methods=['GET','POST'])
def report():
    if request.method=='POST':
        nom=request.form.get('nom')
        adress=request.form.get('email')
        Msg=request.form.get('Message')
        full_rep=Reports(n_reporter=nom,e_reporter=adress,message=Msg)
        db.session.add(full_rep)
        db.session.commit()
        return redirect('/')
    return render_template('report.html')


@app.route('/change',methods=['GET','POST'])
def change():
    if 'user' in session :
        if request.method=='POST' and  request.form.get('available')!='None':
            to_Change=Article.query.filter_by(id=request.form.get('available')).first()
            ref=request.form.get('REF')
            nom=request.form.get('NOM')
            ram=request.form.get('RAM')
            gpu=request.form.get('GPU')
            stock=request.form.get('stockage')
            pric=request.form.get('Prix')
            to_Change.nom=nom;to_Change.Reference=ref;to_Change.ram=ram;to_Change.gpu=gpu;to_Change.stockage=stock;to_Change.prix=pric
            db.session.commit()

        if Fournisseure.query.filter_by(email=session['user']).first().admin:
            items=Article.query.all()
            Admin=True



        else :
            items=Article.query.join(Fournisseure).filter(Fournisseure.email==session['user']).all()
            Admin=False
        return render_template('changer.html',adrs=ipik,items=items,Admin=Admin,User=Fournisseure.query.filter_by(email=session['user']).first(),fourns=Fournisseure.query.all()[3:])
    return redirect('/login')


@app.route('/choix')
def choice():
    if 'user' in session:

        if Fournisseure.query.filter_by(email=session['user']).first().admin:
            items=Article.query.all()
            Admin=True



        else :
            items=Article.query.join(Fournisseure).filter(Fournisseure.email==session['user']).all()
            Admin=False
        return render_template('choix.html',items=items,adrs=ipik,User=Fournisseure.query.filter_by(email=session['user']).first(),Admin=Admin,fourns=Fournisseure.query.all()[3:])

    return redirect('/login')



@app.route('/problems',methods=['GET','POST'])
def probs():
    if 'user' in session:

        if Fournisseure.query.filter_by(email=session['user']).first().admin:
            if request.method=='POST':
                Reports.query.filter_by(id=request.form.get('msgID')).delete()
                db.session.commit()

            return render_template('reports.html',reports=Reports.query.all())



    return redirect('/login')



@app.route('/statistiques',methods=['GET','POST'])
def stats():
    global num_Users
    num_Users=len(session)
    try:
        if Fournisseure.query.filter_by(email=session['user']).first().admin:
            if request.method=='POST':
                day=request.form.get('day')
            return render_template('stats.html',online=num_Users)
        else:
            return redirect('/login')
    except:
        return redirect('/login')



@app.route('/Fournisseures',methods=['GET','POST'])
def fournisseures():
    global U_del


    if request.method=='POST':
        if request.form.get('user'):
            U_del=request.form.get('user')
            a=Fournisseure.query.filter_by(email=U_del).first()
            Article.query.filter_by(owner=a).delete()
            Fournisseure.query.filter_by(email=request.form.get('user')).delete()
            db.session.commit()


        else:
            Fournisseure.query.filter_by(email='',password='').delete()
            nom=request.form.get('nom')
            prenom=request.form.get('prenom')
            email=request.form.get('email')
            tel=request.form.get('tele')
            mdp=request.form.get('mdp')
            infos=Fournisseure(nom=nom,prenom=prenom,email=email,phone=tel,password=mdp)
            try :
                
                db.session.add(infos)
                db.session.commit()

                #E_sender(email,'Visitez http://%s:5122/ pour vous authentifier via le code "%s" .'%(ipik,mdp))
            
            except IntegrityError:
                return '<title>Shop</title><script>alert("Email deja utilisé") ;window.location.href = "http://%s:5122/Fournisseures"  </script>'%(ipik)
      
    if 'user' in session:
        if Fournisseure.query.filter_by(email=session['user']).first().admin:
            fourns=Fournisseure.query.all()[3:]
            return render_template('Fournisseures.html',Fourns=fourns)

        else:
            return redirect('/login')

    return redirect('/login')


@app.route('/Logout')
def Logout():
    session.pop('user',None)
    return redirect('/login')


@app.errorhandler(404)
def erHandler(e):
    return render_template('error.html'),404


if __name__=='__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host='0.0.0.0',port=5122)