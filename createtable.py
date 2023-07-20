from sqliteconnect import connect_to_database

def setuptable(naam):
    try:
        # getting cursor object
        conn=connect_to_database()
        curse=conn.cursor()
        # removing previous 
        check=checkduplicate(naam,curse)
        if(check!=0):
            return None

        updatetableoftables='INSERT INTO ALLTABLES VALUES(\"'+naam+'\");'
        curse.execute(updatetableoftables)
        curse.execute("DROP TABLE IF EXISTS "+naam)
        # table description
        table="CREATE TABLE "+naam+"("
        table+="""DAY CHAR(10) PRIMARY KEY UNIQUE NOT NULL,
                DATA TEXT
                );"""
        curse.execute(table)

        daysofweek=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        for day in daysofweek:
            # lst=list()
            quer='INSERT INTO '+naam+' VALUES(\"'+day+'\","[]")'
            # print(quer)
            curse.execute(quer)

        quer='INSERT INTO '+naam+' VALUES(\"'+'Periods'+'\","{}")'
        # print(quer)
        curse.execute(quer)

        # curse.execute("SELECT * FROM IIT")
        # rec=curse.fetchall()
        # for row in rec:
        #     print(row)

        # print("now")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return None

def checkduplicate(naam,curse):
    # conn=connect_to_database()
    # curse=conn.cursor()
    try:
        quer='SELECT * FROM ALLTABLES WHERE ACTIVITY=\"'+naam+'\";'
        curse.execute(quer)
        res=curse.fetchall()
        return (len(res))
    except Exception as e:
        print(e)
        return 1


# print(setuptable('IIT'))
# checkduplicate('IIT2',1)