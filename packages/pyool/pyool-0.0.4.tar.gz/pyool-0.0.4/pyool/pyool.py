import csv 
from datetime import datetime
from odps import ODPS 
import time 
import uuid 
import os 
import psycopg2 
import requests 
import mysql.connector 
import pandas as pd 


# Defining ODPS specific class to work with 

class OdpsConnector: 

    def connect(self, accessId, accessKey, project, endPoint, tunnelEndPoint):
        self.connection = ODPS(
            access_id = accessId
            , secret_access_key = accessKey
            , project = project
            , endpoint = endPoint 
            ,tunnel_endpoint = tunnelEndPoint
        ) 


    def read_sql(self, file_path):
        with open(file_path, "r", encoding = "utf-8") as file:
            query  = file.read()

        return query 
    

    def extract_header(self, csv_file_path): 
        with open(csv_file_path, "r", newline = "") as file:
            reader = csv.reader(file)
            header = ",".join(next(reader))

        return header 


    def run_query(self, query):
        
        attempt = 0

        while attempt <= 2:
            try:
                print("Querying.....")

                with self.connection.execute_sql(query, None, 1, hints = {"odps.sql.submit.mode" : "script"}).open_reader() as reader:
                    print("Query is finished")
                    return reader 
            except Exception as e:
                attempt += 1
                error = "Attempt {}, error {}. Retrying ....."
                error = error.format(attempt, e) 
                print(error) 
                time.sleep(10) 
                continue  
        
        raise RuntimeError("Cannot query to ODPS due to: %s" % error) 


    def query_from_file(self, file_path):
        with open(file_path, "r") as query_file:
            query = query_file.read()
        return query 


    def dump_to_csv(self, query, storage_path, filename = None): 
        if not filename:
            filename = str(uuid.uuid4())

        filename = filename + ".csv"

        filepath = os.path.join(storage_path, filename)

        attemps = 0 

        while attemps < 3 :
            try: 
                reader = self.run_query(query)
                print("... Done dumping to csv file %s" % filename)
                with open(filepath, "w", encoding ="utf-8") as file:
                    writer = csv.writer(file, delimiter = ",", quoting = csv.QUOTE_NONNUMERIC
                                        , lineterminator = "\n")
                    
                    writer.writerow(reader._schema.names)

                    for record in reader: 
                        writer.writerow(record[0:])
                
                return filepath

            except Exception as e:
                attemps += 1
                print("Retrying... %s. Why: %s" % (attemps, e))
                time.sleep(5)
            else:
                break 



# Defining PostgreSQL Database specific Class to work with

class PostgreSQLConnector: 
    def connect(self, db_name, host, port, user, password):
        self.connection  = psycopg2.connect(dbname = db_name
                                            , host = host
                                            , port = port
                                            , user = user
                                            , password = password) 


    def disconnect(self):
        self.connection.close() 


    def read_sql(self, file_path):
        with open(file_path, "r", encoding = "utf-8") as file:
            query  = file.read()

        return query 
    

    def extract_header(self, csv_file_path): 
        with open(csv_file_path, "r", newline = "") as file:
            reader = csv.reader(file)
            header = ",".join(next(reader))

        return header 


    def run_query(self, query, return_data = False): 
        cur = self.connection.cursor()
        cur.execute(query) 

        if return_data == True: 
            data = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns = column_names) 
            print("Data is returned")
            return df 

        else: 
            self.connection.commit()
            print("Query is executed")  
            return True 

        cur.close() 
        

    def truncate(self, table):
        cur = self.connection.cursor()
        cur.execute("TRUNCATE TABLE %s" % (table)) 


    def uploadCsv(self, filepath, table, fields, truncate = False, remove_file = False):
        if truncate == True: 
            self.truncate(table)
            print("Table truncated. Start uploading...")

        cur = self.connection.cursor()

        attemps = 0

        while attemps < 3:
            try: 
                with open(filepath, 'r', encoding='utf-8') as f:
                    sql = "COPY %s(%s) FROM STDIN WITH ( DELIMITER ',', FORMAT CSV, HEADER, ENCODING 'UTF8', FORCE_NULL(%s))" % (table, fields, fields) 
                    cur.copy_expert(sql, f) 
                    self.connection.commit()

            except Exception as e:
                attemps += 1
                print("Retrying... %s. Why: %s" % (attemps, e))
                time.sleep(5)
            else:
                break  

        if remove_file == True:
            os.remove(filepath) 
        
        return True 



# Defining MySQL specific class to work with 

class MySQLConnector: 

    def connect(self, db_name, host, port, user, password): 
        self.connection = mysql.connector.connect(
                                                    db_name = db_name,
                                                    host = host,
                                                    port = port,
                                                    user = user,
                                                    passwd = password
                                                    )

    
    def read_sql(self, file_path):
        with open(file_path, "r", encoding = "utf-8") as file:
            query  = file.read()

        return query 
    

    def extract_header(self, csv_file_path): 
        with open(csv_file_path, "r", newline = "") as file:
            reader = csv.reader(file)
            header = ",".join(next(reader))

        return header 


    def run_query(self, query, return_data = False):
        cur = self.connection.cursor()
        print("Start querying .....")
        cur.execute(query)

        if return_data == True:
            column_names = cur.column_names
            data = cur.fetchall()

            df = pd.DataFrame(data, columns = column_names) 
            print("Data is returned")
            return df 

        else: 
            print("Query is executed") 
            return True 

        cur.close() 

    def disconnect(self):
        self.connection.close() 




# Defining ChatBot specific Class to send messages to Dingtalk 

class ChatBot: 

    def send_markdown(self, payload, access_token): 
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + str(access_token)  
        headers = {"Content-Type": "application/json;charset=utf-8"}

        attemps = 0 

        while attemps < 3: 
            print("Sending to Dingtalk .....")

            r = requests.post(url, headers = headers, json = payload) 

            if (r.text == """{"errcode":0,"errmsg":"ok"}""" or r.text == """{"errmsg":"ok","errcode":0}"""): 
                print("Message is sent.")
                break 

            else: 
                attemps += 1
                error = "Attemps {}, error {}. Retrying ....."
                error = error.format(attemps, r.text) 
                print(error) 
                time.sleep(10)
                continue 
            
            raise RuntimeError("Cannnot send message due to %s" % r.text) 


    def send2ding(self, title, message, access_token):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": message 
            }, 
            "at": {}
        }

        self.send_markdown(payload = payload, access_token = access_token)
