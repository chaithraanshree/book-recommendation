from flask import Flask, render_template, url_for, request, Response, json
import sqlite3
from testing import rcmd , build_chart

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM admin WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('adminlog.html')

    return render_template('index.html')


@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        email = request.form['email']
        password = request.form['password']

        query = "SELECT email, password FROM userdetails WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('userlog.html')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        Fname = request.form['Fname']
        Lname = request.form['Lname']
        password1 = request.form['password1']
        password2 = request.form['password2']
        mobile = request.form['phone']
        email = request.form['email']
        language = request.form['language']
        genre = request.form['genre']
        date = request.form['date']
        
        if password1 == password2:
            print(Fname, Lname, mobile, email, password2, password1, language, genre, date)

            command = """CREATE TABLE IF NOT EXISTS userdetails(Fname TEXT, Lname TEXT, genre TEXT, language TEXT, password TEXT, mobile TEXT, email TEXT, date TEXT)"""
            cursor.execute(command)

            cursor.execute("INSERT INTO userdetails VALUES ('"+Fname+"', '"+Lname+"', '"+language+"', '"+genre+"', '"+password1+"', '"+mobile+"', '"+email+"', '"+date+"')")
            connection.commit()

            return render_template('index.html', msg='Successfully Registered')
        else:
            return render_template('index.html', msg='password mismatched')
    
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')    

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/userhome')
def userhome():
    return render_template('userlog.html')

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    if request.method == 'POST':
        book=request.form['book']
        book= book.title()
        books = rcmd(book)

        bookT = []
        for i in range(len(books)):
            bookT.append(books[i])

        return render_template('recommend.html', n=len(books), names=bookT)
    return render_template('recommend.html')
        

@app.route('/children',methods=['GET','POST'])
def children():
    Titles=[]
    Authors=[]
    Rack=[]
    vc=[]
    if request.method == 'POST':
        category=request.form['category']
        #category= category.title()
        authors, titles, rack,Vc = build_chart(category)
        for i in range(len(titles)):
            Titles.append(titles[i])
            Authors.append(authors[i])
            Rack.append(rack[i])
            vc.append(Vc[i])
    return (render_template('category.html', j=len(Titles),poster=Authors,titles=Titles,rack=Rack,vc=vc))   
      

if __name__ == "__main__":
    app.run(debug=True)
