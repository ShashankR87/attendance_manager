from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import secrets
from datetime import date
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'shreyas'
app.config['MYSQL_PASSWORD'] = 'Password@123'
app.config['MYSQL_DB'] = 'dbmsmini'
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if 's' in request.form:
            return redirect(url_for('sign_student'))

        elif 't' in request.form:
            return redirect(url_for('sign_teacher'))

        elif 'h' in request.form:
            return redirect(url_for('sign_hod'))

    elif request.method == 'GET':
        return render_template('typeofuser.html')


@app.route('/signstudent', methods=['GET', 'POST'])
def sign_student():
    if request.method == "POST":
        if 'f2' in request.form:
            return redirect(url_for('login'))
        else:
            details = request.form
            name = details['name']
            usn = details['usn']
            sem = details['sem']
            sec = details['sec']
            contact = details['contactno']
            pass1 = details['password']
            password2 = details['cpass']

            session['electivecount'] = details['electivecount']
            if pass1 == password2:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO student VALUES (%s, %s,%s, %b, %s, %b)", (usn, name, pass1, sem, sec, contact))
                mysql.connection.commit()
                session['sec'] = sec
                session['sem'] = sem
                session['usn'] = usn
                cur.close()
                return redirect(url_for('studentelective'))
            else:
                return "Passwords don't match."
    return render_template('sign-student.html')


@app.route('/studentelective', methods=['GET', 'POST'])
def studentelective():
    if request.method == "POST":
        if 'f2' in request.form:
            return redirect(url_for('login'))
        else:
            details = request.form
            usn = session['usn']
            subs = []
            sec = session['sec']
            electivecount = session['electivecount']

            subjs = request.form.getlist("checkbox")

            cur = mysql.connection.cursor()

            for sub in subjs:

                cnt = cur.execute("SELECT subjectcode from subject where subname=%s", (sub,))
                scode = cur.fetchall()
                subc = []
                for i in range(0, cnt):
                    subc.append(''.join(scode[i]))

                cnt = cur.execute("SELECT staffid from taughtby where subjectcode=%s and sec=%s", (subc, sec))
                teachers = cur.fetchall()
                res = []
                for i in range(0, cnt):
                    res.append(''.join(teachers[i]))
                for i in range(0, cnt):
                    cur.execute("INSERT into teaches values(%s,%s,%s)", (res[i], usn, subc))
                    mysql.connection.commit()
            return redirect(url_for('login'))

    sec = session['sec']
    sem = session['sem']
    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "SELECT distinct(S.subname) from taughtby T, subject S where T.sec=%s and T.elective='Y' and S.sem=%s and S.subjectcode=T.subjectcode",
        (sec, sem))

    subs = cur.fetchall()
    res = []
    for i in range(0, cnt):
        res.append(''.join(subs[i]))
    electivecount = session['electivecount']
    return render_template('student-elective.html', subs=res, num=electivecount)


@app.route('/signteacher', methods=['GET', 'POST'])
def sign_teacher():
    if request.method == "POST":
        if 'f2' in request.form:
            return redirect(url_for('login'))
        else:
            details = request.form
            name = details['first']
            staffid = details['staffid']
            contact = details['contactno']
            pass1 = details['password']
            password2 = details['cpass']
            if pass1 == password2:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO teacher VALUES (%s, %s,%s, %b)", (staffid, name, pass1, contact))
                mysql.connection.commit()
                cur.close()
                return 'success'
            else:
                return 'pass no match'
    return render_template('sign-teacher.html')


@app.route('/signhod', methods=['POST', 'GET'])
def sign_hod():
    if request.method == "POST":
        if 'f1' in request.form:
            details = request.form
            name = details['name']
            hid = details['hid']
            dept = details['dept']
            contact = details['contactno']
            pass1 = details['password']
            password2 = details['cpass']
            if pass1 == password2:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO hod VALUES (%s, %s,%s,%s, %b)", (hid, name, pass1, dept, contact))
                mysql.connection.commit()
                cur.close()
                return 'success'
            else:
                return 'pass no match'
        else:
            return redirect(url_for('login'))

    return render_template('hod.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'f2' in request.form:
            return redirect(url_for('signup'))
        else:
            details = request.form
            un = details['usn']
            password = details['pass1']
            session["username"] = un
            session["password"] = password
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM student WHERE usn=%s AND password=%s", (un, password))
            if result <= 0:
                result = cur.execute("SELECT * FROM teacher WHERE staffid=%s AND password=%s", (un, password))

                if result <= 0:
                    result = cur.execute("SELECT * FROM hod WHERE usn=%s AND password=%s", (un, password))

                    if result <= 0:
                        return 'No such user'
                    else:
                        userdetails = cur.fetchone()
                        cur.close()
                        return redirect(url_for('hoddash'))
                else:
                    userdetails = cur.fetchone()
                    cur.close()
                    return redirect(url_for('teacherdash'))

            else:
                userdetails = cur.fetchone()
                cur.close()
                return redirect(url_for('studentdash'))

    return render_template('login.html')


@app.route('/teacherdash', methods=['POST', 'GET'])
def teacherdash():
    if request.method == 'POST':
        if 'summary' in request.form:
            return redirect(url_for('teachsum'))
        elif 'add' in request.form:
            return redirect(url_for('teachadd'))

    cur = mysql.connection.cursor()
    un = session["username"]
    pasw = session["password"]
    res = cur.execute("SELECT tname, staffid FROM teacher WHERE staffid=%s AND password=%s", (un, pasw))
    userdetails = cur.fetchone()
    name = userdetails[1]
    staffid = userdetails[0]
    cnt = cur.execute("SELECT subname FROM subject WHERE subjectcode IN (SELECT DISTINCT(T.subjectcode) FROM teaches T "
                      "where T.staffid=%s) ", (un,))
    subs = cur.fetchall()
    cur.close()
    res = []
    for i in range(0, cnt):
        res.append(''.join(subs[i]))
    session["subs"] = res
    session["countofsubs"] = cnt

    return render_template('teacherhome.html', userdetails=[name, staffid], subjects=res)


@app.route('/teachsum', methods=['POST', 'GET'])
def teachsum():
    if request.method == 'POST':
        # return str(request.form)
        if 'go' in request.form:
            details = request.form

            dt = details["dt"]
            sb = details["sub"]

            session["dt"] = dt
            session["sb"] = sb

            return redirect(url_for('teachdetailsum'))
        elif 'profile' in request.form:
            return redirect(url_for('teacherdash'))

        else:

            return redirect(url_for('teachadd'))
    subs = session["subs"]
    cnt = session["countofsubs"]
    userid = session["username"]
    res = []
    for i in range(0, cnt):
        res.append(''.join(subs[i]))

    cur = mysql.connection.cursor()
    numstud = []
    vnames = []
    averages = []
    subz = []
    for sub in subs:
        cur.execute("SELECT subjectcode from subject where subname=%s", (sub,))
        subcode = cur.fetchone()
        scode = ''.join(subcode)
        subz.append(scode)

        i = cur.execute(
            "SELECT avg(no) from (select A.datetaken, A.hour, A.subjectcode, count(A.usn) as no  from attendance A "
            "where A.status='p' and A.sec= (SELECT T.sec from taughtby T where T.subjectcode=A.subjectcode and "
            "T.staffid=%s) and A.subjectcode=%s group by A.datetaken,A.hour,A.subjectcode order by A.datetaken, "
            "A.hour,A.subjectcode)as T1",
            (userid, scode))
        avg = cur.fetchone()

        averages.append(avg)
        cur.execute("SELECT COUNT(usn) FROM teaches WHERE staffid=%s and subjectcode=%s", (userid, scode))
        numstud.append(cur.fetchone())

    percentages = []

    i = 0
    for n in averages:
        percentages.append(int((n[0] / numstud[i][0]) * 100))
        i = i + 1
    return render_template('teachersummary.html', subs=subs, cnt=cnt, num=percentages)


@app.route('/teachdetailsum', methods=['GET', 'POST'])
def teachdetailsum():
    if request.method == 'POST':
        if 'summary' in request.form:
            return redirect(url_for('teachsum'))
        elif 'add' in request.form:
            return redirect(url_for('teachadd'))
        else:
            return redirect(url_for('teacherdash'))
    dt = session["dt"]
    sb = session["sb"]
    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "SELECT S.usn, S.name, A.status from student S, attendance A where A.datetaken=%s and A.usn=S.usn and A.subjectcode=(SELECT U.subjectcode from subject U where U.subname=%s) and A.sec=S.sec",
        (dt, sb))
    rep = cur.fetchall()

    cur.close()

    return render_template('teachersummarydetailed.html', tab=rep)


@app.route('/teachadd', methods=['POST', 'GET'])
def teachadd():
    if request.method == 'POST':
        if 'profile' in request.form:
            return redirect(url_for('teacherdash'))
        elif 'summary' in request.form:
            return redirect(url_for('teachsum'))
        elif 'add' in request.form:
            return redirect(url_for('teachadd'))
        else:
            details = request.form

            sub = details["choice"]
            hour = details["hour"]
            session["choice"] = sub
            session["hour"] = hour
            return redirect(url_for('teachaddatt'))
    sid = session["username"]
    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "SELECT S.subname from subject S where S.subjectcode in (SELECT T.subjectcode from taughtby T where T.staffid=%s)",
        (sid,))
    sb = cur.fetchall()
    subs = []
    for i in range(0, cnt):
        subs.append(''.join(sb[i]))
    return render_template('teacheradd.html', sb=subs)


@app.route('/teachaddatt', methods=['POST', 'GET'])
def teachaddatt():
    if request.method == 'POST':
        if 'summary' in request.form:
            return redirect(url_for('teachsum'))
        elif 'add' in request.form:
            return redirect(url_for('teachadd'))
        elif 'profile' in request.form:
            return redirect(url_for('teacherdash'))
        else:
            hour = session["hour"]
            sub = session["choice"]
            sid = session["username"]
            cur = mysql.connection.cursor()
            cnt = cur.execute("SELECT U.subjectcode from subject U where U.subname=%s", (sub,))
            subcode = cur.fetchone()
            dte = date.today()
            status = request.form.getlist("checkbox")

            cur.execute("SELECT sec from taughtby where staffid=%s and subjectcode=%s", (sid, subcode))
            sec = cur.fetchone()
            totstud = cur.execute(
                "SELECT T.usn from teaches T, student S where T.subjectcode=(SELECT U.subjectcode from subject U where U.subname=%s) and T.staffid=%s and S.usn=T.usn order by T.usn",
                (sub, sid))
            allstud = cur.fetchall()
            studs = []
            for i in range(0, totstud):
                studs.append(''.join(allstud[i]))
            absentees = (set(studs) - set(status))

            for s in status:
                cou = cur.execute(
                    "INSERT  INTO attendance (datetaken, hour,usn,subjectcode,sec,status) values(%s,%b,%s,%s,%s,%s)",
                    (dte, hour, s, subcode, sec, 'p'))
                cur.connection.commit()
            for s in absentees:
                cou = cur.execute(
                    "INSERT  INTO attendance (datetaken, hour,usn,subjectcode,sec,status) values(%s,%b,%s,%s,%s,%s)",
                    (dte, hour, s, subcode, sec, 'a'))
                cur.connection.commit()
            cur.close()
            return "Attendance entered!"

    sid = session["username"]
    sub = session["choice"]

    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "SELECT T.usn, S.name from teaches T, student S where T.subjectcode=(SELECT U.subjectcode from subject U "
        "where U.subname=%s) and T.staffid=%s and S.usn=T.usn order by T.usn",
        (sub, sid))
    lst = cur.fetchall()

    return render_template('teacheraddatt.html', lst=lst)


@app.route('/studentdash', methods=['POST', 'GET'])
def studentdash():
    if request.method == 'POST':
        if 'profile' in request.form:
            return redirect(url_for('studentdash'))
        elif 'summary' in request.form:
            return redirect(url_for('studsum'))
        elif 'all' in request.form:
            return redirect(url_for('all'))

    cur = mysql.connection.cursor()
    un = session["username"]
    pasw = session["password"]
    res = cur.execute("SELECT name, usn FROM student WHERE usn=%s AND password=%s", (un, pasw))
    userdetails = cur.fetchone()
    name = userdetails[1]
    usn = userdetails[0]
    cnt = cur.execute(
        "SELECT subname FROM subject WHERE subjectcode IN (SELECT DISTINCT(T.subjectcode) FROM teaches T where T.usn=%s) ",
        (un,))
    subs = cur.fetchall()
    cur.close()
    res = []
    for i in range(0, cnt):
        res.append(''.join(subs[i]))
    session["subs"] = res
    session["countofsubs"] = cnt

    return render_template('studhome.html', userdetails=[name, usn], subjects=res)


@app.route('/studsum', methods=['POST', 'GET'])
def studsum():
    if request.method == 'POST':
        if 'profile' in request.form:
            return redirect(url_for('studentdash'))
        elif 'summary' in request.form:
            return redirect(url_for('studsum'))
        elif 'all' in request.form:
            return redirect(url_for('all'))
        elif 'go' in request.form:
            details = request.form

            dt = details["dt"]
            sb = details["sub"]

            userid = session["username"]
            session["username"] = userid

            session["dt"] = dt
            session["sb"] = sb

            return redirect(url_for('studdetsum'))

        # else:

        #   return redirect(url_for('teachadd'))
    subs = session["subs"]
    cnt = session["countofsubs"]
    userid = session["username"]
    session["username"] = userid
    res = []
    for i in range(0, cnt):
        res.append(''.join(subs[i]))

    cur = mysql.connection.cursor()
    # numstud = []
    # vnames = []
    numofpres = []
    numoftot = []
    averages = []
    subz = []
    for sub in subs:
        cur.execute("SELECT subjectcode from subject where subname=%s", (sub,))
        subcode = cur.fetchone()
        scode = ''.join(subcode)
        subz.append(scode)

        noofperpresent = cur.execute(
            "select count(no) from (select A.datetaken, A.hour, A.subjectcode, A.status as no from attendance A where A.usn=%s and A.status='p' and A.subjectcode=%s group by A.datetaken,A.hour,A.subjectcode order by A.datetaken,A.hour,A.subjectcode) as t1",
            (userid, scode))
        nop = cur.fetchone()
        totalnoofperiods = cur.execute(
            "select count(no) from (select A.datetaken, A.hour, A.subjectcode, A.status as no from attendance A where A.usn=%s and A.subjectcode=%s group by A.datetaken,A.hour,A.subjectcode order by A.datetaken,A.hour,A.subjectcode) as t2",
            (userid, scode))
        nop1 = cur.fetchone()

        numofpres.append(nop)
        numoftot.append(nop1)

    # print(numoftot[0][0])
    percentages = []
    i = 0
    flag = 1
    for n in numoftot:
        if n[0] != 0:
            percentages.append(int((numofpres[i][0] * 100 / n[0])))

            if int((numofpres[i][0] * 100 / n[0])) < 75:
                flag = 0;
            i = i + 1


        else:
            percentages.append(100)

    if flag == 1:
        flash("You have no attendance shortage!!")
    elif flag == 0:
        flash("You have attendance shortage. Do not bunk classes")
    return render_template('studsum.html', subs=subs, cnt=cnt, num=percentages)


@app.route('/studdetsum', methods=['GET', 'POST'])
def studdetsum():
    if request.method == 'POST':
        if 'summary' in request.form:
            return redirect(url_for('studsum'))
        elif 'profile' in request.form:
            return redirect(url_for('studentdash'))
        elif 'all' in request.form:
            return redirect(url_for('all'))

    dt = session["dt"]
    userid = session["username"]

    sb = session["sb"]
    print(userid, sb)
    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "select A.datetaken, A.hour, A.status from attendance A where A.usn=%s and A.subjectcode=(SELECT U.subjectcode from subject U where U.subname=%s) group by A.datetaken,A.hour order by A.datetaken, A.hour",
        (userid, sb))
    rep = cur.fetchall()

    cur.close()

    return render_template('studdetsum.html', tab=rep)


@app.route('/all', methods=['GET', 'POST'])
def all():
    if request.method == 'POST':
        if 'summary' in request.form:
            return redirect(url_for('studsum'))
        elif 'profile' in request.form:
            return redirect(url_for('studentdash'))
        elif 'all' in request.form:
            return redirect(url_for('all'))
        elif 'go' in request.form:
            details = request.form

            dt = details["dt"]
            sb = details["sub"]

            userid = session["username"]
            session["username"] = userid

            session["dt"] = dt
            session["sb"] = sb

            return redirect(url_for('all'))

    dt = session["dt"]
    userid = session["username"]

    sb = session["sb"]
    print(userid, sb)
    cur = mysql.connection.cursor()
    cnt = cur.execute(
        "SELECT A.datetaken,A.hour,U.subname,A.status from attendance A,subject U where A.datetaken=%s and A.usn=%s and A.subjectcode=U.subjectcode group by A.datetaken,A.hour order by A.datetaken, A.hour ",
        (dt, userid))
    rep = cur.fetchall()

    cur.close()

    return render_template('all.html', tab=rep)


@app.route('/hoddash', methods=['POST', 'GET'])
def hoddash():
    cur = m
    return render_template('teacherhome.html')


if __name__ == '__main__':
    app.run(debug=True)

# create procedure fillTeaches()
# begin
# declare stid varchar(10);
# declare us varchar(10);
# declare sub varchar(10);
# declare staffcur cursor for select A.staffid from taughtby A, student S, subject U where U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec;
# declare uscur cursor for select S.usn from taughtby A, student S, subject U where U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec;
# declare subcur cursor for select U.subjectcode from taughtby A, student S, subject U where U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec;
# open staffcur;
# open uscur;
# open subcur;
# filltable: loop
# fetch staffcur into stid;
# fetch uscur into us;
# fetch subcur into sub;
# insert into teaches values (stid, us, sub);
# end loop filltable;
# close staffcur;
# close uscur;
# close subcur;
# end
