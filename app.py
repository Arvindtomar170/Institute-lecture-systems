from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'arvind'
app.config['MYSQL_DB'] = 'info'

mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'POST' and'password' in request.form:
            password=request.form['password']
            if password=="abcd":
                return render_template('admin.html')
            else:
                return ('query1.html')
    return render_template('home.html')

@app.route('/query1', methods =['GET', 'POST'])
def query1():
	msg =''
	if request.method == 'POST' and 'faculty_id' in request.form :
            faculty_id = request.form['faculty_id']
            s_year=request.form['start_year']
            e_year=request.form['end_year']
            cursor = mysql.connection.cursor()
            cursor.execute('select distinct course_id from records where faculty_id = %s and (year<=%s and year>=%s)' , (faculty_id,e_year,s_year, ))
            account = cursor.fetchall()
            cursor.close()
            return render_template('query1.html', msg = account)
	return render_template('query1.html')

@app.route('/query2', methods =['GET', 'POST'])
def query2():
	msg =''
	if request.method == 'POST' and 'faculty_id' in request.form :
            faculty_id = request.form['faculty_id']
            cursor = mysql.connection.cursor()
            cursor.execute('select distinct course_id from records where faculty_id = %s', (faculty_id, ))
            account = cursor.fetchall()
            cursor.close()
            return render_template('query2.html', msg = account)
	return render_template('query2.html')

@app.route('/query3', methods =['GET', 'POST'])
def query3():
	msg =''
	if request.method == 'POST' and 'Dept_id' in request.form :
            Dept_id = request.form['Dept_id']
            s_year=request.form['start_year']
            e_year=request.form['end_year']
            cursor = mysql.connection.cursor()
            cursor.execute('select distinct course_id from records where faculty_id in (select faculty_id from faculty where Dept_id=%s) and (year<=%s and year>=%s)' , (Dept_id,e_year,s_year, ))
            account = cursor.fetchall()
            cursor.close()
            return render_template('query3.html', msg = account)
	return render_template('query3.html')

@app.route('/query4', methods =['GET', 'POST'])
def query4():
	msg =''
	if request.method == 'POST' and 'Dept_id' in request.form  and 'course_id' in request.form:
            Dept_id = request.form['Dept_id']
            course_id=request.form['course_id']
            cursor = mysql.connection.cursor()
            cursor.execute('select distinct faculty_id from records where course_id=%s and (faculty_id in (select faculty_id from faculty where Dept_id=%s))',(course_id,Dept_id,))
            account = cursor.fetchall()
            cursor.close()
            return render_template('query4.html', msg = account)
	return render_template('query4.html')

@app.route('/query5', methods =['GET', 'POST'])
def query5():
	msg =''
	if request.method == 'POST' and 'semester' in request.form  and 'year' in request.form:
            semester = request.form['semester']
            year=request.form['year']
            cursor = mysql.connection.cursor()
            cursor.execute('select * from records where semester=%s and year=%s',(semester,year,))
            account = cursor.fetchall()
            cursor.close()
            return render_template('query5.html', msg = account)
	return render_template('query5.html')

@app.route('/add_faculty',methods=['POST','GET'])
def add_faculty():
    msg=""
    if request.method=='POST':
        faculty_id=request.form['faculty_id']
        faculty_name=request.form['faculty_name']
        phone=request.form['Phone_no']
        Dept_id=request.form["Dept_id"]
       	cursor=mysql.connection.cursor() 
        cursor.execute('insert into faculty values(%s,%s,%s,%s)',(faculty_id,faculty_name,phone,Dept_id,))
        mysql.connection.commit()
        cursor.close()
        msg="faculty added successfully"
        return render_template('add_faculty.html',msg=msg)
    return render_template('add_faculty.html')

@app.route('/add_course',methods=['POST','GET'])
def add_course():
    if request.method=='POST':
        course_id=request.form['course_id']
        course_name=request.form['course_name']
        Dept_id=request.form['Dept_id']
        cursor=mysql.connection.cursor() 
        cursor.execute('insert into courses values(%s,%s,%s)',(course_id,course_name,Dept_id,))
        mysql.connection.commit()
        cursor.close()
        msg="course added successfully"
        return render_template('add_course.html',msg=msg)
    return render_template('add_course.html')

@app.route('/add_department',methods=['POST','GET'])
def add_department():
    if request.method=='POST':
        Dept_id=request.form['Dept_id']
        Dept_name=request.form['Dept_name']
        cursor=mysql.connection.cursor() 
        cursor.execute('insert into department values(%s,%s)',(Dept_id,Dept_name))
        mysql.connection.commit()
        cursor.close()
        msg="department added successfully"
        return render_template('add_department.html',msg=msg)
    return render_template('add_department.html')

@app.route('/add_schedule',methods=['POST','GET'])
def add_schedule():
    if request.method=='POST':
        year=request.form['year']
        semester=request.form['semester']
        course_id=request.form['course_id']
        faculty_id=request.form['faculty_id']
        student_no=request.form['no_of_student']
        mon_t=request.form['mon_t']
        mon_l=request.form['mon_l']
        tue_t=request.form['tue_t']
        tue_l=request.form['tue_l']
        wed_t=request.form['wed_t']
        wed_l=request.form['wed_l']
        thu_t=request.form['thu_t']
        thu_l=request.form['thu_l']
        fri_t=request.form['fri_t']
        fri_l=request.form['fri_l']
        sat_t=request.form['sat_t']
        sat_l=request.form['sat_l']
        cursor=mysql.connection.cursor() 
        cursor.execute('insert into records values(default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(year,semester,student_no,course_id,faculty_id,mon_t if mon_t else None,mon_l if mon_l else None,tue_t if tue_t else None,tue_l if tue_l else None,wed_t if wed_t else None,wed_l if wed_l else None,thu_t if thu_t else None, thu_l if thu_l else None,fri_t if fri_t else None, fri_l if fri_l else None, sat_t if sat_t else None,sat_l if sat_l else None,))
        mysql.connection.commit()
        cursor.close()
        msg="schedule added successfully"
        return render_template('add_schedule.html',msg=msg)
    return render_template('add_schedule.html')

if __name__=='__main__':
    app.run(debug=True)














































# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_faculty_name'] = 'arvind'
# app.config['MYSQL_DB'] = 'info'
# mysql = MySQL(app)


# @app.route('/', methods=['GET', 'POST'])

# def home():
#     msg = ''
#     if request.method == 'POST':
#         if 'password' in request.form:
#             password=request.form['password']
#             if password=="arvind":
#                 return "i am too happy"
#             else:
#                 return "i am happy"
#     return render_template('home.html')

# @app.route('/query1', methods=['GET', 'POST'])
# def query1():
#         msg = ''
#         msg2 = ''
#         if request.method == 'POST' and 'faculty_id' in request.form and 'faculty_name' in request.form:
#             faculty_id = request.form['faculty_id']
#             faculty_name = request.form['faculty_name']
#             # cursor = mysql.connection.cursor()
#             # cursor.execute('SELECT * FROM student_data WHERE faculty_id = % s AND faculty_name = % s',("1", "CSE", ))
#             # data = cursor.fetchall()
#             data =['ajfdhl','adfjla','jdsakj']
#             return render_template('query1.html',msg=data)
#         return render_template('query1.html')

# # @app.route('/output1')
# # def output1():
# #     return render_template('output1.html')

# # @app.route('/query1')
# # def query1():
# #     return render_template('query1.html')

# # @app.route('/output2')
# # def output2():
# #     return render_template('output2.html')

# # @app.route('/query3')
# # def query3():
# #     return render_template('query3.html')

# # @app.route('/output3')
# # def output3():
# #     return render_template('output3.html')

# # @app.route('/query4', methods=['GET', 'POST'])
# # def query4():
# #     return render_template('query4.html')

# # @app.route('/output4')
# # def output4():
# #     return render_template('output4.html')

# # @app.route('/query5')
# # def query5():
# #     return render_template('query5.html')

# # @app.route('/output5')
# # def output5():
# #     return render_template('output5.html')

# # @app.route('/editing')
# # def editing():
# #   return render_template('editing.html')

# if __name__=='__main__':
#         app.run(debug=True)




