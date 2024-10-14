# CLEFIP2011 XML2MySQL
Although the CLEFIP2011 text collection (http://www.ifs.tuwien.ac.at/~clef-ip/download/2011/index.shtml) is a well-known benchmark in the field of Information Retrieval and Text Classification, there is currently no available coding to transfer it in a MySQL database that can make it easily accessed.

In this repository, someone can find the code to create a database, named clefip2011, and the code to parse the CLEFIP2011 text collection and populate the clefip2011 database's tables with this content. Moreover, the CLEFIP-0.54M-Kamateri dataset is released which has been created using the clefip2011 database.

**Code description**

**_database_creation_part_1.py_**

The code of the _database_creation_part_1.py_ file creates a database, named clefip2011, and three tables, named patents, patents_en_text, and patent_ipc_codes. 

The **_patents_** table keeps all available information for a patent document found in the CLEFIP2011 test collection. We tried to keep this table light providing only indicators regarding the presence (or not) of the EN/DE/FR abstract, description and claims for a patent document, while the actual content of these parts can be found in the patents_en/de/fr_text table.

The **_patents_en_text_** table keeps the lengthy textual content of abstract, description and claims parts of a patent document for the English text. However, there is available code that can be activated to create respective tables and parsing code for the German and French texts of abstract, description and claims.


The **_patent_ipc_codes_** table keeps the IPC codes of a patent document for all levels (1-5) and the source of the code, \<classification-ipc> (which is further specialized into \<main-classification> and \<further-classification>) and \<classification-ipcr>. 

**_database_creation_part_2.py_**
  
The code of the _database_creation_part_2.py_ file populates the three tables of the clefip2011 database with content parsed from the patent documents of the CLEFIP2011 text collection.

**Details regarding the parsing:**

- A patent folder may contain multiple documents/versions of a patent. If a patent document does not have title, abstract, description or claims text, we keep the previous record for this field coming from a previous document/version for the specific patent. 
- The ecla codes are listed and separated by a comma (,).
- When parsing the ipcr codes, we check if we had already encountered and saved them. If yes, we indicate it in the existing code by setting its ipcr field as true.
- The only preprocessing performed in the text of abstract, description and claims were that (1) the characters were converted to lower case, (2) the double eps (") was replaced with single eps (΄) because double eps were causing a problem when entering into the database and (3) words split and rejoined so as to correct cases of consecutive spaces and line changes.  
- If the English text of abstract, description or claims is not available, we check the language of the German/French text for the corresponding field. 
If it is detected to be English, then we store it as English text as well. Moreover, we check the language of the English text. If the language is German or Frence, we empty the variable keeping the English text (assuming that the label EN was given by mistake). If the language is any besides German or Frence, we keep this in the variable storing the English text.

**File requirements**

The following files are required:

- the _database_creation_part_1_public.py_ file
- the _database_creation_part_2_public.py_ file
- the CLEFIP2011 XML patent files unzipped in a folder named clefip2011

**Program requirements**

On the computer where the clefip2011 database will be located, the following programs are required:

- **mysql**. Note: I installed mysql 5.5.62. I followed the "Typical installation" and (mostly) the recommended settings. The only exceptions were that I selected "Non-Transactional Database Only (MyISAM)" that creates separate files for each database table and "Manual Selected Default Character Set/Collation" to have character set utf8.
- **mysql-workbench-community**. Note: I installed 6.3.10 and followed the recommended settings.
- **python**. Note: I installed 3.9.7 and followed the recommended settings. During installation, I also set the path to be put in the environmental variables.
- **Spyder**. Note: I installed 5.2.1 and followed the recommended settings. After installation, I configure it to use python 3.9.7 (Tools->Preferences->Python interpreter-> Use the following Python interpreter: C:/Users/User/AppData/Local/Programs/Python/Python39/python.exe->OK and restart the spyder).

**Python libraries requirements**

The following python libraries are required to be installed in spyder (from the console on the right): 
- !pip install mysql-connector-python
- !pip install bs4
- !pip install lxml
- !pip install langdetect

**Guidelines for running the code**
1.	First, set "steps = [1]" in the database_creation_part_1_public.py and run it - it creates the clefip2011 database
2.	Next, set steps = [2] in the database_creation_part_1_public.py and run it - it creates the tables of the clefip2011 database
3.	Last, write the correct path of the CLEFIP2011 test collection in the database_creation_part_2_public.py and run it - it parses the XML patent files from the CLEFIP2011 test collection and populates the database tables with their data as defined by the various rules created in this python script


**CLEFIP-0.54M dataset (https://github.com/ekamater/CLEFIP-0.54M)**

This dataset has been created querying and extracting data from the created CLEFIP 2011 MySQL database. 

The dataset contains 6 csv files with data coming from 541,131 patents. Each csv file has two columns; the main IPC code at level-4 column and the text from a patent field, i.e., abstract, description, claims, title, applicants and inventors. 

This content comes from the latest documents/versions of these 541,131 patents that have simultaneously an EN abstract, EN description, EN claims, EN title, applicants and inventors. Moreover, the text of EN abstract, EN description, and EN claims has undergone a further preprocessing removing any character that is not alphabetic and removing English stopwords. 

The dataset is available in the following link: https://drive.google.com/drive/folders/1tfBsUkQwIpwwgDyw28EOZctaiiJqZr1Q?usp=sharing
