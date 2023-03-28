from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///dheerajtodolist.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
with app.app_context():
    db = SQLAlchemy(app)
class todo(db.Model):
    SNO=db.Column(db.Integer, primary_key=True) 
    Title=db.Column(db.String(50), nullable=False)
    Description=db.Column(db.String(200),nullable=False)
    Date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.SNO} - {self.Title}"
    
@app.route('/',methods=['GET',"POST"])#methods will describe that we are going to use these two methods in this webapplication page
def hello_world():
    allTodos=todo.query.all() # it will get all the todo values 
    # print(allTodos) # it will print all the return values of __repr__ function for all the todos
    return render_template('index.html',alltodo=allTodos)#here we are passing the allTodos to our template index.html this service is being provided by jinja templating engine in flask
@app.route("/formsubmit",methods=["GET","POST"])
def submitform():
    if request.method == "POST":
        print("post request occured") # means whenever we submit the form of index.html(whose method is POST) then it will execute
        titl=request.form['titlefromform']#titlefromform is the name we give to the input box of title of the form in index.html 
        desc=request.form["descfromform"]#descfromform is the name we give to the input box of description of the form in index.html 
        firsttodo=todo(Title=titl,Description=desc)
        db.session.add(firsttodo)
        db.session.commit()
    return redirect('/')
@app.route('/delete/<int:sno>')
def delete(sno):
    deletingtodo=todo.query.filter_by(SNO=sno).first()
    db.session.delete(deletingtodo)
    db.session.commit()
    return redirect('/')
    

@app.route('/update/<int:sno>',methods=['POST',"GET"])
def update(sno):
    if request.method == "POST":
        titl=request.form['titlefromform']
        desc=request.form['descfromform']
        todoo=todo.query.filter_by(SNO=sno).first()
        todoo.Title=titl
        todoo.Description=desc
        db.session.commit()
        return redirect('/')
    itemforupdate=todo.query.filter_by(SNO=sno).first()
    return render_template("update.html",todo=itemforupdate)
@app.route('/product')
def product_page():
    return "this is product page"
if (__name__)=="__main__":
    app.run(debug=False,host='0.0.0.0')#5000 is default port we can change it by passing parameter(port parameter as. port=8000) 