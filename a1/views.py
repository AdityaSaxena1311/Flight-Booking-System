from django.shortcuts import render, redirect
import mysql.connector as msc
# Create your views here.
l=[]
f=""
t=""
d=""
fno=""
record=""
def home(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    c.execute("create table if not exists transaction(tid int primary key,fno varchar(20),seats int,name varchar(20),date varchar(20),_to_ varchar(20),_from_ varchar(20),fare int)")
    conn.commit()
    c.execute("create table if not exists bank(id varchar(20) primary key,amount int,password varchar(20))")
    conn.commit()
    c.execute("create table if not exists flight(fno varchar(20) primary key,company varchar(20),time varchar(20),start varchar(20),end varchar(20),category varchar(20),fare int,seats varchar(20))")
    conn.commit()
    return render(request,"home.html")
def adminhome(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    p=request.POST.get("password")
    if p=="password":
        c.execute("select fno from flight")
        f=c.fetchall()
        if f!=[]:
            fno="FNO"+str(int(f[len(f)-1][0][3:])+1)
        else:
            fno="FNO1"
        return render(request,"flight.html",{"addf":"1","fno":fno})
    else:
        return render(request,"home.html",{"err":"Incorrect Password"})
def addf(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    c.execute("select fno from flight")
    f=c.fetchall()
    if f!=[]:
        fno="FNO"+str(int(f[len(f)-1][0][3:])+1)
    else:
        fno="FNO1"
    return render(request,"flight.html",{"addf":"1","fno":fno})
def save(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    fno=request.GET.get("fno")
    comp=request.GET.get("comp")
    cat=request.GET.get("category")
    fare=request.GET.get("fare")
    time=request.GET.get("time")
    t=request.GET.get("t")
    frm=request.GET.get("frm")
    seats=request.GET.get("seats")
    c=conn.cursor()
    c.execute("insert into flight values('{}','{}','{}','{}','{}','{}','{}','{}')".format(fno,comp,time,frm,t,cat,fare,seats))
    conn.commit()
    conn.close()
    return redirect("/addf")
def delf(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    c.execute("select * from flight")
    r=c.fetchall()
    conn.commit()
    if r!=[]:
        return render(request,"flight.html",{"delf":"1","rec":r})
    else:
        return render(request,"flight.html",{"delf":"1","nf":"No Flights"})
def delete(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    fno=request.GET.get("fno")
    c.execute("delete from flight where fno='{}'".format(fno))
    conn.commit()
    return redirect("/delf")
def ef(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    c.execute("select * from flight")
    r=c.fetchall()
    conn.commit()
    if r!=[]:
        return render(request,"flight.html",{"ef":"1","record":r})
    else:
        return render(request,"flight.html",{"ef":"1","nf":"No Flights"})
def edit(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    fno=request.GET.get("fno")
    c.execute("select * from flight where fno='{}'".format(fno))
    record=c.fetchone()
    return render(request,"flight.html",{"ef":"1","rec":record})
def editf(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    fno=request.GET.get("fno")
    comp=request.GET.get("comp")
    cat=request.GET.get("category")
    fare=request.GET.get("fare")
    time=request.GET.get("time")
    t=request.GET.get("t")
    frm=request.GET.get("frm")
    c.execute("update flight set company='{}',time='{}',end='{}',start='{}',category='{}',fare='{}' where fno='{}'".format(comp,time,t,frm,cat,fare,fno))
    conn.commit()
    return redirect("/ef")
def book(request):
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    c.execute("select * from flight")
    record=c.fetchall()
    conn.commit()
    conn.close()
    return render(request,"book.html")
def search(request):
    global f,t,d
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    f=request.GET.get("from")
    t=request.GET.get("to")
    d=request.GET.get("date")
    c.execute("select * from flight where start='{}' and end='{}'".format(f,t))
    r=c.fetchall()
    conn.commit()
    if r!=[]:
        return render(request,"book.html",{"rec":r,"f":f,"t":t,"d":d})
    else:
        return render(request,"book.html",{"nf":"No Filghts Available","f":f,"t":t,"d":d})
def user(request):
    global f,t,d,fno
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    fno=request.GET.get("fno")
    c.execute("select * from flight where fno='{}'".format(fno))
    rec=c.fetchall()
    conn.commit()
    return render(request,"book.html",{"seats":"!","rec":rec,"f":f,"t":t,"d":d})
def booking(request):
    global f,t,d,fno
    conn=msc.connect(host="localhost",user="root",password="aditya", database="ams")
    c=conn.cursor()
    seat=int(request.GET.get("seats"))
    c.execute("select * from flight where fno='{}'".format(fno))
    r=c.fetchall()
    rec=r[0]
    conn.commit()
    fare=rec[6]
    fare=fare*seat
    os=int(rec[7])
    c.execute("select sum(seats) from transaction where fno='{}' and date='{}'".format(fno,d))
    fa=c.fetchone()[0]
    sl=os
    if fa!=None:
        sl=os-fa
    if seat<=sl:
        return render(request,"details.html",{"rec":rec,"fare":fare,"seat":seat})
    else:
        return render(request,"book.html",{"seats":"!","rec":r,"f":f,"t":t,"d":d,"msg":"No Vacant Seats"})
def bnow(request):
    global l,d
    fno=request.GET.get("fno")
    seats=int(request.GET.get("seats"))
    name=request.GET.get("name")
    t=request.GET.get("t")
    frm=request.GET.get("frm")
    fare=request.GET.get("fare")
    l=[fno,seats,name,d,t,frm,fare]
    return render(request,"bank.html")
def acc(request):
    global l,d
    conn=msc.connect(host="localhost",user="root",password="aditya",database="ams")
    c=conn.cursor()
    fno=l[0]
    seats=l[1]
    name=l[2]
    date=d
    t=l[4]
    frm=l[5]
    fare=l[6]
    i=request.GET.get("id")
    p=request.GET.get("pw")
    c.execute("select * from bank where id='{}'".format(i))
    a=c.fetchall()[0]
    ps=a[2]
    amt=a[1]
    if p==ps and amt>=int(fare):
        al=amt-int(fare)
        tid=AID("transaction")
        l.append(tid)
        c.execute("insert into transaction values('{}','{}','{}','{}','{}','{}','{}','{}')".format(tid,fno,seats,name,date,t,frm,fare))
        conn.commit()
        c.execute("update bank set amount={} where id='{}'".format(al,i))
        conn.commit()
        return render(request,"ticket.html",{"l":l})
    elif p!=ps:
        return render(request,"bnow.html",{"msg":"Invalid Details"})
    else:
        return render(request,"bnow.html",{"msg":"Insufficient balance to book flight"})
def bth(request):
    return redirect("/ams")
def AID(table):
    conn=msc.connect(host="localhost",user="root",password="aditya",database="ams")
    c=conn.cursor()
    c.execute("select * from {}".format(table))
    a=c.fetchall()
    conn.commit()
    if a==[]:
        return 101
    else:
        return a[len(a)-1][0]+1
