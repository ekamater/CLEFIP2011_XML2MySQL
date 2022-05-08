#!pip install bs4
#!pip install lxml
#!pip install langdetect

import os
from bs4 import BeautifulSoup
import mysql.connector
from langdetect import detect
import re

# Insert the path to the extracted CLEFIP2011 
original_clefip2011_path="C:/Users/User/Desktop/clefip2011"

for folder_level_1 in os.listdir(original_clefip2011_path): #CC
    for folder_level_2 in os.listdir(original_clefip2011_path+"/"+folder_level_1): #nnnnnn
        for folder_level_3 in os.listdir(original_clefip2011_path+"/"+folder_level_1+"/"+folder_level_2): #nn
            for folder_level_4 in os.listdir(original_clefip2011_path+"/"+folder_level_1+"/"+folder_level_2+"/"+folder_level_3): #nn
                for folder_level_5 in os.listdir(original_clefip2011_path+"/"+folder_level_1+"/"+folder_level_2+"/"+folder_level_3+"/"+folder_level_4): #nn
                    
                    # A folder_level_5 contains all the different versions of a paten.
                    # We delete title, abstract, description and claims variables, 
                    # (only) when accessing for first time a folder_level_5.   
                    # By this condition, we keep the previous values in these variables 
                    # in cases that the current value of one of these variable is empty
                    # and there was a previous value coming from a previous patent version (accessed before) 
                    
                    title_de_text = ''
                    title_fr_text = ''
                    title_en_text  = ''     
                    abstract_de_text = ''
                    abstract_fr_text = ''
                    abstract_en_text   = ''                                        
                    description_de_text = ''
                    description_fr_text = ''
                    description_en_text = ''                                                   
                    claims_de_text = ''
                    claims_fr_text = ''
                    claims_en_text = ''

                    for files in os.listdir(original_clefip2011_path+"/"+folder_level_1+"/"+folder_level_2+"/"+folder_level_3+"/"+folder_level_4+"/"+folder_level_5):
                        #print(files)        
                                                                       
                        # Extract all content 

                        content = open(original_clefip2011_path+"/"+folder_level_1+"/"+folder_level_2+"/"+folder_level_3+"/"+folder_level_4+"/"+folder_level_5+"/"+files,'r',encoding='utf-8').read()
                        soup = BeautifulSoup(content, 'lxml')
                        
                        # Get doc info
                          
                        ucid = ''
                        country = ''
                        doc_number = 0                  
                        kind = ''
                        lang = ''
                        corrected_lang=''
                        date = 0
                        family_id = ''
                        date_produced = 0
                        status = '' 
                        
                        document_info = soup.find_all("patent-document")
                        ucid=document_info[0]['ucid']
                        country=document_info[0]['country']
                        doc_number=int(document_info[0]['doc-number'])                            
                        kind=document_info[0]['kind']
                        lang=document_info[0]['lang'] 
                        date=int(document_info[0]['date'])
                        date_produced=int(document_info[0]['date-produced'])
                        status=document_info[0]['status']
                        
                        #Modification for addressing problem no.1 -> make the below code line as comment line
                        #family_id=document_info[0]['family-id']
                                                                       
                        # Get main classification
                            
                        main_section_list = []
                        main_class_list = []
                        main_subclass_list=[]
                        main_group_list=[]
                        main_subgroup_list=[]
                        
                        for main_classification in soup.find_all('main-classification'):
                            code_main=main_classification.getText()
                                                                
                            main_section=code_main.split()[0][0]
                            main_section_list.append(main_section) if main_section not in main_section_list else main_section_list
                               
                            main_class=code_main.split()[0][:3]
                            main_class_list.append(main_class) if main_class not in main_class_list else main_class_list
                            
                            main_subclass=code_main.split()[0]
                            main_subclass_list.append(main_subclass) if main_subclass not in main_subclass_list else main_subclass_list
                            
                            main_group_subgroup=code_main.split()[1]
                            main_group=main_subclass+main_group_subgroup.rsplit('/')[0]
                            main_group_list.append(main_group) if main_group not in main_group_list else main_group_list
                            
                            main_subgroup=main_subclass+main_group_subgroup
                            main_subgroup_list.append(main_subgroup) if main_subgroup not in main_subgroup_list else main_subgroup_list                           
                                                
                        # Get further classification   
                            
                        further_section_list = []
                        further_class_list = []
                        further_subclass_list=[]
                        further_group_list=[]
                        further_subgroup_list=[]
                            
                        for further_classification in soup.find_all('further-classification'):
                            code_further=further_classification.getText()
                            
                            further_section=code_further.split()[0][0]
                            further_section_list.append(further_section) if further_section not in further_section_list else further_section_list
                            
                            further_class=code_further.split()[0][:3]
                            further_class_list.append(further_class) if further_class not in further_class_list else further_class_list
                            
                            further_subclass=code_further.split()[0]
                            further_subclass_list.append(further_subclass) if further_subclass not in further_subclass_list else further_subclass_list
                            
                            further_group_subgroup=code_further.split()[1]
                            further_group=further_subclass+further_group_subgroup.rsplit('/')[0]
                            further_group_list.append(further_group) if further_group not in further_group_list else further_group_list
                            
                            further_subgroup=further_subclass+further_group_subgroup
                            further_subgroup_list.append(further_subgroup) if further_subgroup not in further_subgroup_list else further_subgroup_list
                                                                 
                        # Get ecla classification   
                        
                        ecla_list = []
                        
                        for ecla_classification in soup.find_all('classification-symbol'):
                            code_ecla=ecla_classification.getText()
                            ecla_list.append(code_ecla) if code_ecla not in ecla_list else ecla_list
                        ecla_list = ", ".join(ecla_list)
                        
                        # Get applicants
                        
                        applicant_name_list = []
                                    
                        for applicant_all_info in soup.find_all('applicant'):
                            applicant_last_name=applicant_all_info.find('last-name')
                            applicant_single_name=applicant_all_info.find('name')
                            if applicant_last_name != None:
                                applicant_name = applicant_last_name
                            elif applicant_single_name != None: 
                                applicant_name = applicant_single_name
                            applicant_name_text=applicant_name.getText().lower().replace('"', ' ')
                            #applicant_name_text=applicant_name_text.replace('&', 'and').replace('corporation','corp').replace(',', '').replace('.', '').replace('-', ' ')
                            applicant_name_list.append(applicant_name_text) if applicant_name_text not in applicant_name_list else applicant_name_list
                        applicant_name_list = "; ".join(applicant_name_list)

                        # Get inventors
                        
                        inventor_name_list = []
                                    
                        for inventor_all_info in soup.find_all('inventor'):
                            inventor_last_name=inventor_all_info.find('last-name')
                            inventor_single_name=inventor_all_info.find('name')
                            if inventor_last_name != None:
                                inventor_name = inventor_last_name
                            elif inventor_single_name != None: 
                                inventor_name = inventor_single_name
                            inventor_name_text=inventor_name.getText().lower().replace('"', ' ')
                            #inventor_name_text=inventor_name_text.replace('&', 'and').replace('corporation','corp').replace(',', '').replace('.', '').replace('-', ' ')
                            inventor_name_list.append(inventor_name_text) if inventor_name_text not in inventor_name_list else inventor_name_list
                        inventor_name_list = "; ".join(inventor_name_list)
                       
                        # Get citations
                        
                        ## under development ##
                                    
                       # Get title
                                          
                        title_de=soup.find('invention-title', attrs={'lang':'DE'})
                        if title_de != None:
                            title_de=title_de.getText().lower().replace('"', ' ')
                            title_de=" ".join(title_de.split())
                            title_de_text=title_de

                        title_fr=soup.find('invention-title', attrs={'lang':'FR'})
                        if title_fr != None:
                            title_fr=title_fr.getText().lower().replace('"', ' ')
                            title_fr=" ".join(title_fr.split())
                            title_fr_text=title_fr  
                        
                        title_en=soup.find('invention-title', attrs={'lang':'EN'})
                        if title_en != None:
                            title_en=title_en.getText().lower().replace('"', ' ')
                            title_en=" ".join(title_en.split())
                            title_en_text=title_en  
                                
                        # Get abstract
                        
                        abstract_de_exist=0
                        abstract_de_en_exist=0
                        abstract_fr_exist=0
                        abstract_fr_en_exist=0
                        abstract_en_exist=0        
                        abstract_en_de_exist=0
                        abstract_en_fr_exist=0
                        
                        abstract_de=soup.find('abstract', attrs={'lang':'DE'})
                        if abstract_de != None:
                            abstract_de=abstract_de.getText().lower().replace('"', ' ')
                            abstract_de=" ".join(abstract_de.split())
                            abstract_de_text=abstract_de 
                            abstract_de_exist=1
                            if detect(abstract_de_text)=="en":
                                abstract_de_en_exist=1
                        
                        abstract_fr=soup.find('abstract', attrs={'lang':'FR'})
                        if abstract_fr != None:
                            abstract_fr=abstract_fr.getText().lower().replace('"', ' ')
                            abstract_fr=" ".join(abstract_fr.split())
                            abstract_fr_text=abstract_fr
                            abstract_fr_exist=1
                            if detect(abstract_fr_text)=="en":
                                abstract_fr_en_exist=1
                        
                        abstract_en=soup.find('abstract', attrs={'lang':'EN'})
                        if abstract_en != None:
                            abstract_en=abstract_en.getText().lower().replace('"', ' ')
                            abstract_en=" ".join(abstract_en.split())
                            abstract_en_exist=1
                            
                            if len(abstract_en) > 0:
                                lang_abstract=detect(abstract_en)
                                
                                # whatever language the detector returns 
                                # besides de or fr we consider it as en 
                                
                                if lang_abstract=="de" or lang_abstract=="fr":
                                    abstract_en_text=''
                                    if lang_abstract=="de": abstract_en_de_exist=1
                                    if lang_abstract=="fr": abstract_en_fr_exist=1
                                else:
                                    abstract_en_text=abstract_en
                            #else:
                                #print(ucid,"error - no features in abstract") 
                        else: 
                            if abstract_de_en_exist==1:
                                abstract_en_text= abstract_de_text 
                            if abstract_fr_en_exist==1:
                                abstract_en_text= abstract_fr_text

                        # Get description
                                
                        description_de_exist=0
                        description_de_en_exist=0
                        description_fr_exist=0
                        description_fr_en_exist=0
                        description_en_exist=0
                        description_en_de_exist=0
                        description_en_fr_exist=0
                                    
                        description_de=soup.find('description', attrs={'lang':'DE'})
                        if description_de != None:                            
                            description_de=description_de.getText().lower().replace('"', ' ')
                            description_de=" ".join(description_de.split())
                            description_de_text=description_de
                            description_de_exist=1
                            if detect(description_de_text)=="en":
                                description_de_en_exist=1
                            
                        description_fr = soup.find('description', attrs={'lang':'FR'})
                        if description_fr != None:
                            description_fr=description_fr.getText().lower().replace('"', ' ')
                            description_fr=" ".join(description_fr.split())
                            description_fr_text=description_fr
                            description_fr_exist=1
                            if detect(description_fr_text)=="en":
                                description_fr_en_exist=1
                            
                        description_en = soup.find('description', attrs={'lang':'EN'})
                        if description_en != None:
                            description_en=description_en.getText().lower().replace('"', ' ')
                            description_en=" ".join(description_en.split())
                            description_en_exist=1
                            
                            if len(description_en) > 0:
                                lang_description=detect(description_en)
                                
                                # whatever language the detector returns 
                                # besides de or fr we consider it as en
                                
                                if lang_description=="de" or lang_description=="fr":
                                    description_en_text='' 
                                    if lang_description=="de": description_en_de_exist=1
                                    if lang_description=="fr": description_en_fr_exist=1
                                else:
                                    description_en_text=description_en 
                                    if (len(description_en_text)>200000): description_en_text=description_en_text[0:5000]                                                              

                            #else:
                                #print(ucid,"error - no features in description")  
                        
                        else:
                            if description_de_en_exist==1:
                                description_en_text= description_de_text
                                if (len(description_en_text)>200000): description_en_text=description_en_text[0:5000]                                                              
                            if description_fr_en_exist==1:
                                description_en_text= description_fr_text
                                if (len(description_en_text)>200000): description_en_text=description_en_text[0:5000]                                                              
                                    
                        # Get all claims
                                
                        claims_de_exist=0
                        claims_de_en_exist=0
                        claims_fr_exist=0
                        claims_fr_en_exist=0
                        claims_en_exist=0
                        claims_en_de_exist=0
                        claims_en_fr_exist=0
                        
                        claims_de = soup.find('claims', attrs={'lang':'DE'})
                        if claims_de != None:                            
                            claims_de=claims_de.getText().lower().replace('"', ' ')
                            claims_de=" ".join(claims_de.split())                        
                            claims_de_text=claims_de
                            claims_de_exist=1
                            if detect(claims_de_text)=="en":
                                claims_de_en_exist=1
                            
                        claims_fr = soup.find('claims', attrs={'lang':'FR'})
                        if claims_fr != None:
                            claims_fr=claims_fr.getText().lower().replace('"', ' ')
                            claims_fr=" ".join(claims_fr.split())                            
                            claims_fr_text=claims_fr
                            claims_fr_exist=1
                            if detect(claims_fr_text)=="en":
                                claims_fr_en_exist=1
                            
                        claims_en = soup.find('claims', attrs={'lang':'EN'})
                        if claims_en != None:
                            claims_en=claims_en.getText().lower().replace('"', ' ')
                            claims_en=" ".join(claims_en.split())                          
                            claims_en_exist=1
                            
                            if len(claims_en) > 0:
                                lang_claims=detect(claims_en)
                                
                                # whatever language the detector returns 
                                # besides de or fr we consider it as en
                                
                                if lang_claims=="de" or lang_claims=="fr":
                                    claims_en_text='' 
                                    if lang_claims=="de": claims_en_de_exist=1
                                    if lang_claims=="fr": claims_en_fr_exist=1
                                else:
                                    claims_en_text=claims_en
                            #else:
                                #print(ucid,"error - no features in claims") 
                                 
                        else:
                            if claims_de_en_exist==1:
                                claims_en_text= claims_de_text    
                                if (len(claims_en_text)>200000): claims_en_text=claims_en_text[0:5000]                                                                                      
                            if claims_fr_en_exist==1:
                                claims_en_text= claims_fr_text
                                if (len(claims_en_text)>200000): claims_en_text=claims_en_text[0:5000]                                                                                      
                        
                        if lang!= "EN" :
                            if abstract_de_en_exist==1 or abstract_fr_en_exist==1 or description_de_en_exist==1 or description_fr_en_exist==1 or claims_de_en_exist==1 or claims_fr_en_exist==1 :
                                corrected_lang="EN" 
                            if abstract_en_de_exist==1 or description_en_de_exist==1 or claims_en_de_exist==1 :
                                corrected_lang="DE" 
                            if abstract_en_fr_exist==1 or description_en_fr_exist==1 or claims_en_fr_exist==1 :
                                corrected_lang="FR" 
                                
                                    
######################## Connect to the datbase - fill in the patents and patents_text tables ########################
                            
                        mydb = mysql.connector.connect(
                            host="localhost",    
                            user="root",        
                            password="admin",
                            database="clefip2011"
                            )
                        
                        mycursor = mydb.cursor()
                                
                        # Pass the patent info
                        
                        sql = "INSERT INTO patents (ucid, country, doc_number, kind, \
                        lang, corrected_lang, date, family_id, date_produced, status, \
                        ecla_list, applicant_name_list, inventor_name_list, \
                        title_de_text, title_fr_text, title_en_text, \
                        abstract_de_exist, abstract_fr_exist, abstract_en_exist,\
                        description_de_exist, description_fr_exist, description_en_exist,\
                        claims_de_exist, claims_fr_exist, claims_en_exist) VALUES (%s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s,\
                        %s, %s, %s, \
                        %s, %s, %s, \
                        %s, %s, %s, \
                        %s, %s, %s)"
                                                              
                        
                        val = (ucid, country, doc_number, kind, \
                        lang, corrected_lang, date, family_id, date_produced, status, \
                        ecla_list, applicant_name_list, inventor_name_list, \
                        title_de_text, title_fr_text, title_en_text, \
                        abstract_de_exist, abstract_fr_exist, abstract_en_exist,\
                        description_de_exist, description_fr_exist, description_en_exist,\
                        claims_de_exist, claims_fr_exist, claims_en_exist)                 
                       
                        
                        mycursor.execute(sql, val)
                        mydb.commit()
                        

                        sql0 = "INSERT INTO patents_en_text (ucid, \
                        abstract_en_text, description_en_text, claims_en_text) VALUES (%s, \
                        %s, %s, %s)"
                            
               
                        val0 = (ucid,\
                        abstract_en_text, description_en_text, claims_en_text)  
                                                                                
                        mycursor.execute(sql0, val0)
                        mydb.commit()
                                
#       Activate the below code if you need to create a table for keeping the German texts of abstract, description and claims 
#                        sql00 = "INSERT INTO patents_de_text (ucid, \
#                        abstract_de_text, description_de_text, claims_de_text) VALUES (%s, \
#                        %s, %s, %s)"
#
#                        val00 = (ucid,\
#                        abstract_de_text, description_de_text, claims_de_text)                                                                                 
#                        mycursor.execute(sql00, val00)
#                        mydb.commit()
                        
#       Activate the below code if you need to create a table for keeping the French texts of abstract, description and claims 
#                        sql000 = "INSERT INTO patents_fr_text (ucid, \
#                        abstract_fr_text, description_fr_text, claims_fr_text) VALUES (%s, \
#                        %s, %s, %s)"
#                        val000 = (ucid,\
#                        abstract_fr_text, description_fr_text, claims_fr_text)                                                                               
#                        mycursor.execute(sql000, val000)
#                        mydb.commit()
            
######################## Connect to the datbase - fill in the patent_ipc_codes table ########################
                        
                        
                        # Get classification_ipcr
                            
                        ipcr_section_list = []
                        ipcr_class_list = []
                        ipcr_subclass_list=[]
                        ipcr_group_list=[]
                        ipcr_subgroup_list=[]
                                            
                        for classification_ipcr in soup.find_all('classification-ipcr'):
                            code_ipcr=classification_ipcr.getText()
                                
                            ipcr_section=code_ipcr.split()[0][0]
                                                         
                            # Pass the section info
                            if ipcr_section not in ipcr_section_list:
                                
                                main_section= False if ipcr_section not in main_section_list else True
                                further_section= False if ipcr_section not in further_section_list else True
    
                                sql1 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val1 = (ucid, ipcr_section, 1, main_section, further_section, True) 
                                
                                mycursor.execute(sql1, val1)
                                mydb.commit()
                                
                                ipcr_section_list.append(ipcr_section) 
                            
                            ipcr_class=code_ipcr.split()[0][:3]

                            # Pass the class info
                            if ipcr_class not in ipcr_class_list:
                            
                                main_class=False if ipcr_class not in main_class_list else True
                                further_class=False if ipcr_class not in further_class_list else True
    
                                sql2 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val2 = (ucid, ipcr_class, 2, main_class, further_class, True) 
                                
                                mycursor.execute(sql2, val2)
                                mydb.commit()
                                
                                ipcr_class_list.append(ipcr_class)  

                            ipcr_subclass=code_ipcr.split()[0]
                            
                            # Pass the subclass info
                            if ipcr_subclass not in ipcr_subclass_list:
                                
                                main_subclass=False if ipcr_subclass not in main_subclass_list else True
                                further_subclass=False if ipcr_subclass not in further_subclass_list else True
    
                                sql3 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val3 = (ucid, ipcr_subclass, 3, main_subclass, further_subclass, True) 
                                
                                mycursor.execute(sql3, val3)
                                mydb.commit()
                                
                                ipcr_subclass_list.append(ipcr_subclass)  
                            
                            ipcr_group_subgroup=code_ipcr.split()[1]
                            ipcr_group=ipcr_subclass+ipcr_group_subgroup.rsplit('/')[0]
                            
                            # Pass the group info

                            if ipcr_group not in ipcr_group_list: 

                                main_group=False if ipcr_group not in main_group_list else True
                                further_group=False if ipcr_group not in further_group_list else True
    
                                sql4 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val4 = (ucid, ipcr_group, 4, main_group, further_group, True) 
                                
                                mycursor.execute(sql4, val4)
                                mydb.commit()
                                
                                ipcr_group_list.append(ipcr_group)
                                
                            ipcr_subgroup=ipcr_subclass+ipcr_group_subgroup
                            
                            # Pass the subgroup info
                            
                            if ipcr_subgroup not in ipcr_subgroup_list:

                                main_subgroup=False if ipcr_subgroup not in main_subgroup_list else True
                                further_subgroup=False if ipcr_subgroup not in further_subgroup_list else True
    
                                sql5 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val5 = (ucid, ipcr_subgroup, 5, main_subgroup, further_subgroup, True) 
                                
                                mycursor.execute(sql5, val5)
                                mydb.commit()
                                
                                ipcr_subgroup_list.append(ipcr_subgroup) 
                        
                        # When main code is not listed in the ipcr codes    
                                
                        for main_section in main_section_list:
                            if main_section not in ipcr_section_list:
                                
                                further_section=False if main_section not in further_section_list else True
                                
                                sql6 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val6 = (ucid, main_section, 1, True, further_section, False) 
                                mycursor.execute(sql6, val6)
                                mydb.commit()
                                
                        for main_class in main_class_list:
                            if main_class not in ipcr_class_list:

                                further_class=False if main_class not in further_class_list else True
                                
                                sql7 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val7 = (ucid, main_class, 2, True, further_class, False) 
                                mycursor.execute(sql7, val7)
                                mydb.commit()
                                
                        for main_subclass in main_subclass_list:
                            if main_subclass not in ipcr_subclass_list:
                                further_subclass=False if main_subclass not in further_subclass_list else True
                                
                                sql8 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val8 = (ucid, main_subclass, 3, True, further_subclass, False) 
                                mycursor.execute(sql8, val8)
                                mydb.commit()
                                
                        for main_group in main_group_list:
                            if main_group not in ipcr_group_list:
                                further_group=False if main_group not in further_group_list else True
                                
                                sql9 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val9 = (ucid, main_group, 4, True, further_group, False) 
                                mycursor.execute(sql9, val9)
                                mydb.commit()
                                
                        for main_subgroup in main_subgroup_list:
                            if main_subgroup not in ipcr_subgroup_list:
                                further_subgroup=False if main_subgroup not in further_subgroup_list else True
                                
                                sql10 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val10 = (ucid, main_subgroup, 5, True, further_subgroup, False) 
                                mycursor.execute(sql10, val10)
                                mydb.commit()
                                
                        # When further code is not listed in the ipcr codes and main code(s)

                        for further_section in further_section_list:
                            if further_section not in ipcr_section_list and further_section not in main_section_list:
                                
                                sql11 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val11 = (ucid, further_section, 1, False, True, False) 
                                mycursor.execute(sql11, val11)
                                mydb.commit()
                                
                                
                        for further_class in further_class_list:
                            if further_class not in ipcr_class_list and further_class not in main_class_list:
                                
                                sql12 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val12 = (ucid, further_class, 2, False, True, False) 
                                mycursor.execute(sql12, val12)
                                mydb.commit()
                                
                        for further_subclass in further_subclass_list:
                            if further_subclass not in ipcr_subclass_list and further_subclass not in main_subclass_list:
                                
                                sql13 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val13 = (ucid, further_subclass, 3, False, True, False) 
                                mycursor.execute(sql13, val13)
                                mydb.commit()
                                
                        for further_group in further_group_list:
                            if further_group not in ipcr_group_list and further_group not in main_group_list:
                                
                                sql14 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val14 = (ucid, further_group, 4, False, True, False) 
                                mycursor.execute(sql14, val14)
                                mydb.commit()
                                
                        for further_subgroup in further_subgroup_list:
                            if further_subgroup not in ipcr_subgroup_list and further_subgroup not in main_subgroup_list:
                                
                                sql15 = "INSERT INTO patent_ipc_codes (ucid, \
                                ipcr_code, level, main, further, ipcr)\
                                VALUES (%s, %s, \
                                %s, %s, %s, %s)"
                                    
                                val15 = (ucid, further_subgroup, 5, False, True, False) 
                                mycursor.execute(sql15, val15)
                                mydb.commit()
                                
                        mycursor.close()
                        mydb.close()