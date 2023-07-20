from sqliteconnect import connect_to_database
# lst format
# [starttime,endtime,periodname]
def insertperiod(tablename, day, lst):
    try:
        # getting cursor object
        conn=connect_to_database()
        curse=conn.cursor()
        # removing previous 
        
        #     return None
        quer='SELECT DATA FROM '+tablename+' WHERE DAY=\"'+day+'\";'
        curse.execute(quer)
        res=curse.fetchone()
        lst2=eval(res[0])
        lst2.append(lst)
        lst2.sort()
        # print(lst2)
        quer='UPDATE '+tablename+' SET DATA=\"'+str(lst2)+'\" WHERE DAY=\"'+day+'\";'
        curse.execute(quer)
        

        quer='SELECT DATA FROM '+tablename+' WHERE DAY=\"'+'Periods'+'\";'
        curse.execute(quer)
        res=curse.fetchone()
        # print(res)
        dct=eval(res[0])

        if lst[2] not in dct.keys():
            dct[lst[2]]=[0,0]
            quer='UPDATE '+tablename+' SET DATA=\"'+str(dct)+'\" WHERE DAY=\"'+'Periods'+'\";'
            curse.execute(quer)
        
        
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return None

def deleteperiod(tablename,dct):
    try:
        # getting cursor object
        conn=connect_to_database()
        curse=conn.cursor()
        

        for day in dct.keys():
            quer='SELECT DATA FROM '+tablename+' WHERE DAY=\"'+day+'\";'
            curse.execute(quer)
            res=curse.fetchone()
            # print(res[0][0])
            lst2=eval(res[0])
            for val in dct[day]:
                lst2.remove(val)
            
            quer='UPDATE '+tablename+' SET DATA=\"'+str(lst2)+'\" WHERE DAY=\"'+day+'\";'
            curse.execute(quer)

        
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return None



def updateperiod(tablename, day, lst, lst3):
    try:
        # getting cursor object
        conn=connect_to_database()
        curse=conn.cursor()
        
        #     return None
        quer='SELECT DATA FROM '+tablename+' WHERE DAY=\"'+day+'\";'
        curse.execute(quer)
        res=curse.fetchall()
        lst2=eval(res[0][0])
        # lst2.append(lst)
        # lst2.sort()
        ind=lst2.index(lst)
        lst2[ind]=lst3
        lst2.sort()
        quer='UPDATE '+tablename+' SET DATA=\"'+str(lst2)+'\" WHERE DAY=\"'+day+'\";'
        curse.execute(quer)
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return None



def getallperiod(tablename):
    try:
        # getting cursor object
        conn=connect_to_database()
        curse=conn.cursor()
        # removing previous 
        
        quer='SELECT * FROM '+tablename+';'
        curse.execute(quer)
        res=curse.fetchall()
        dct={}

        for dat in res:
            dct[dat[0]]=eval(dat[1])
        
        
        conn.close()
        return dct
    except Exception:
        return None


# print(updateperiod('IIT','Monday',[50,100,'Maths'],[50,100,'Geo']))
# print(deleteperiod('IIT',{'Tuesday':[[4900,5100,'GK']]}))
# print(getallperiod('IIT'))
# print(insertperiod('IIT', 'Monday', [50, 100, 'Maths']))