import string
import sqlite3
import os
if(os.name == 'nt'):
    try:
        os.system("IF NOT EXIST C:\AmbSQL MKDIR C:\AmbSQL")
    except:
        pass
    path = 'C:\\AmbSQL\\'
else:
    try:
        os.system("mkdir -p DB")
    except:
        pass
    path = 'DB/'
    # Connect to Tables Database
db = sqlite3.connect(path+"dtables.db")
c = db.cursor()
def createtable(tname="", *cols):
    x = list(cols)
    for s in range(len(cols)):
        x[s] = str(x[s])
    y = tuple(x)
    del x
    c.execute("CREATE TABLE " + tname + " (id INTEGER PRIMARY KEY)")
    for j in y:
        c.execute("ALTER TABLE " + tname + " ADD " + j + " TEXT")
    db.commit()
def insertvalues(tname="", *cols):
    x = list(cols)
    for s in range(len(cols)):
        x[s] = str(x[s])
    y = tuple(x)
    del x
    c.execute("INSERT INTO "+tname +" VALUES(NULL"+",?"*(len(cols))+")", y)
    db.commit()
def showtable(tname=""):
    c.execute("pragma table_info('"+tname+"')")
    abv = c.fetchall()
    print("       cid\t    name\t       pk")
    print("----------\t--------\t---------")
    for p, q, r, s, t, u in abv:
        print(" "*(10-len(str(p)))+str(p)+"\t"+" " *(8-len(str(q)))+str(q)+"\t"+" "*(9-len(str(u)))+str(u))
    print("")
def showvalues(tname=""):
    c.execute("pragma table_info('"+tname+"')")
    abv = c.fetchall()
    for p, q, r, s, t, u in abv:
        print(" "*(9-len(str(q)))+str(q), end="\t")
    print("")

    for p, q, r, s, t, u in abv:
        print("---------", end="\t")
    print("")

    c.execute("SELECT * FROM "+tname)
    tables = c.fetchall()
    for i in tables:
        for j in i:
            print(" "*(9-len(str(j)))+str(j), end="\t")
        print("")
def deletetable(tname=""):
    c.execute("DELETE FROM "+tname)
    db.commit()
    
def updatevalue(tname, colm, nval, conc, conv):
    colm = str(colm)
    conc = str(conc)
    if(colm!='id' and colm!='ID'):
        nval = str(nval)
        if(conc == 'id' or conc == 'ID'):
            conv = int(conv)
            c.execute("UPDATE "+tname+" SET "+colm+"='"+nval+"' WHERE id="+str(conv))
        else:
            conv = str(conv)
            c.execute("UPDATE "+tname+" SET "+colm+"='" +nval+"' WHERE "+conc+"='"+conv+"';")
    else:
        nval = int(nval)
        if(conc == 'id' or conc == 'ID'):
            c.execute("UPDATE "+tname+" SET "+colm+"="+nval+" WHERE id="+str(conv))
        else:
            c.execute("UPDATE "+tname+" SET "+colm+"=" +
                      nval+" WHERE "+conc+"='"+conv+"';")
    db.commit()
'''
def updatevalue(tname, colm, nval):
    colm = str(colm)
    if(colm!='id' and colm!='ID'):
        nval = str(nval)
    else:
        nval = int(nval)
    c.execute("UPDATE "+tname+" SET "+colm+"='"+nval+"';")
    db.commit()
'''
def clear():
    if(os.name=='nt'):
        os.system("cls")
    else:
        os.system("clear")
def altertable(otname="", ntname=""):
    c.execute("ALTER TABLE "+otname +" RENAME TO "+ntname)
    db.commit()
def droptable(tname=""):
    c.execute("DROP TABLE "+tname)
    db.commit()
