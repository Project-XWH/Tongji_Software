import sqlite3
import pickle,os

path = os.path.dirname(__file__)
def CREATE_TABLE():
    conn = sqlite3.connect(path+'/../data/Pathlab.db')
    c = conn.cursor()
    c.execute('''DROP TABLE ENZYME''')
    c.execute('''DROP TABLE PARTS''')
    c.execute('''CREATE  TABLE ENZYME
            (ECNumber    TEXT PRIMARY KEY NOT NULL,
             KKM         VARCHAR(255),
             KM          VARCHAR(255),
             pH          VARCHAR(255),
             T           VARCHAR(255),
             PHR         VARCHAR(255),
             TR          VARCHAR(255)
             );''')
    c.execute('''CREATE  TABLE PARTS
            (PID         TEXT PRIMARY KEY NOT NULL,
             Sequence    VARCHAR(255),
             Parameter   VARCHAR(255),
             Categories  VARCHAR(255),
             Uses        VARCHAR(255)
             );''')

    print("Table created successfully")
    conn.commit()
    conn.close()

# 记录新的中药信息
def InsertEnzyme(ECNumber, KKM, KM, pH, T, PHR, TR):
    conn = sqlite3.connect(path+'/../data/Pathlab.db')
    c = conn.cursor()
    c.execute('''INSERT INTO ENZYME (ECNumber, KKM, KM, pH, T, PHR, TR) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' %(ECNumber, KKM, KM, pH, T, PHR, TR))
    conn.commit()
    conn.close()
    
def InsertParts(PID, Sequence, Parameter, Categories, Uses):
    conn = sqlite3.connect(path+'/../data/Pathlab.db')
    c = conn.cursor()
    c.execute('''INSERT INTO PARTS (PID, Sequence, Parameter, Categories, Uses) \
           VALUES ('%s', '%s', '%s', '%s', '%s')''' %(PID, Sequence, Parameter, Categories, Uses))
    conn.commit()
    conn.close()

def selectPartsByPID(ID):
    conn = sqlite3.connect(path+'/../data/Pathlab.db')
    c = conn.cursor()
    cursor =  c.execute('''SELECT  * from PARTS \
           where PID=="%s" '''%(ID))
    res = []
    for row in cursor:
        res.append(row)
    conn.close()
    return sorted(res)

def update():
    CREATE_TABLE()
    #conn = sqlite3.connect('/home/xubo/sites/Pathlab/data/Pathlab.db')
    IDS = []
    for line in open(path+'/../parts_design/promoter_data.txt'):
        line = line.split('\t')
        print(line)
        PID = line[0]
        if PID in IDS:
            continue
        IDS.append(PID)
        Sequence = line[1]
        Parameter = line[2]
        Categories = line[3]
        Uses = line[4]
        InsertParts(PID, Sequence, Parameter, Categories, Uses)

#update()
        
        
        
        
        
        
        
        
        
        
        
        
        