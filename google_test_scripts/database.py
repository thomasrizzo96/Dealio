import sqlite3
import sys

try:
    connection = sqlite3.connect("db.sqlite3")
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM dealioApp_restaurant") 
    print("fetchall:")
    result = cursor.fetchall() 
    for r in result:
        print(r)
    cursor.execute("SELECT * FROM dealioApp_restaurant") 
    #print("\nfetch one:")
    #res = cursor.fetchone() 
    #print(res)


    print("Now trying to write to database")
    cursor.execute("INSERT INTO dealioApp_restaurant VALUES(3,'lololol','yelpfefe.com','Mexcan')")

    connection.commit()

except sqlite3.Error as e:
    
    if connection:
        connection.rollback()
        
    print ("Error %s:" % e.args[0])
    sys.exit(1)
    
finally:
    
    if connection:
        connection.close() 
