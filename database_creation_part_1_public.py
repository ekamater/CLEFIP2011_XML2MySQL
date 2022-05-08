#!pip install mysql-connector-python 

import mysql.connector

steps=[2] #1: create the database, 2: create the tables and 3: drop the tables

for step in steps:
    
    if step==1:
        mydb = mysql.connector.connect(
            host="localhost",    
            user="root",        
            password="admin"
            )
        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE clefip2011 CHARACTER SET utf8 COLLATE utf8_general_ci")
        
    elif step==2:
        mydb = mysql.connector.connect(
            host="localhost",    
            user="root",        
            password="admin",
            database="clefip2011",
            )
            
        mycursor = mydb.cursor()
        
        mycursor.execute("CREATE TABLE patents (ucid VARCHAR(20), country VARCHAR(3), doc_number INTEGER, \
                         kind VARCHAR(3), lang VARCHAR(3), corrected_lang VARCHAR(3), date INTEGER,\
                         family_id VARCHAR(20), date_produced INTEGER, status VARCHAR(20), \
                        ecla_list TEXT, applicant_name_list TEXT, inventor_name_list TEXT, \
                        title_de_text TEXT, title_fr_text TEXT, title_en_text TEXT,\
                        abstract_de_exist INTEGER, abstract_fr_exist INTEGER, abstract_en_exist INTEGER,\
                        description_de_exist INTEGER, description_fr_exist INTEGER, description_en_exist INTEGER,\
                        claims_de_exist INTEGER, claims_fr_exist INTEGER, claims_en_exist INTEGER, PRIMARY KEY (ucid))")

        mycursor.execute("CREATE TABLE patents_en_text (ucid VARCHAR(20), FOREIGN KEY (ucid) REFERENCES patents(ucid), \
                         abstract_en_text TEXT, description_en_text MEDIUMTEXT, claims_en_text MEDIUMTEXT)")

#       Activate the below code if you need to create a table for keeping the German texts of abstract, description and claims 

#       mycursor.execute("CREATE TABLE patents_de_text (ucid VARCHAR(20), FOREIGN KEY (ucid) REFERENCES patents(ucid), \
#                         abstract_de_text TEXT, description_de_text MEDIUMTEXT, claims_de_text MEDIUMTEXT)")

#       Activate the below code if you need to create a table for keeping the French texts of abstract, description and claims 

#        mycursor.execute("CREATE TABLE patents_fr_text (ucid VARCHAR(20), FOREIGN KEY (ucid) REFERENCES patents(ucid), \
#                         abstract_fr_text TEXT, description_fr_text MEDIUMTEXT, claims_fr_text MEDIUMTEXT)")

                    
        mycursor.execute("CREATE TABLE patent_ipc_codes (ucid VARCHAR(20), FOREIGN KEY (ucid) REFERENCES patents(ucid), \
                         ipcr_code VARCHAR(20), level INTEGER, main boolean, further boolean, ipcr boolean)")