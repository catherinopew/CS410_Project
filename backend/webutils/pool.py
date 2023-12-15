import yaml
import json

from psycopg2 import pool, sql
from webutils.utils import UIDs

class DBHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.load_config()
    
    def load_config(self, config_path='config.yaml'):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    
        self.host = config['postgres']['host']
        self.port = config['postgres']['port']
        self.name = config['postgres']['database']
        self.user = config['postgres']['username']
        self.password = config['postgres']['password']
        self.minconn = config['postgres']['minconn']
        self.maxconn = config['postgres']['maxconn']

    def get_connection(self):
        self.pool = pool.SimpleConnectionPool(
            minconn=self.minconn,
            maxconn=self.maxconn,
            host=self.host,
            port=self.port,
            dbname=self.name,
            user=self.user,
            password=self.password
        )

        return self.pool.getconn()

    def execute_query(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            self.close_connection(connection)

    def fetch_results(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)

            results = cursor.fetchall()

            return results

        except Exception as e:
            raise e

        finally:
            cursor.close()
            self.close_connection(connection)
    

    def insert_task(self, body):
        if not isinstance(body, dict):
            json_str = body.decode('utf-8')
            body = json.loads(json_str)

        query = sql.SQL(f"INSERT INTO app_db.public.results (client_id, task_id, timestamp, url, score,  status) VALUES ('{body['client_id']}', '{body['task_id']}', {body['timestamp']}, '{body['url']}', NULL, 'in progress');")

        self.execute_query(query)
    
    def update_task(self, task_id, status):
        query = sql.SQL(f"UPDATE app_db.public.results SET score = NULL, status = '{status}' WHERE task_id = '{task_id}' AND status = 'in progress';")

        self.execute_query(query)
    
    def insert_reviews(self, task_id, reviews):
        for review_id, content in reviews.items():
            content = content.replace("'", "''")
            query = sql.SQL(f"INSERT INTO app_db.public.reviews (task_id, status, review_id, content) VALUES ('{task_id}', 'in progress', '{review_id}', '{content}');")
            
            self.execute_query(query)

    def update_reviews(self, task_id, reviews, scores):
        if not reviews or not scores:
          return

        ind = 0
        
        vlen = len(scores['review_id']) if 'review_id' in scores else 0

        for i in range(len(UIDs)):
            if scores[UIDs[i]] is None:
                scores[UIDs[i]] = ['NULL']*vlen

        for i in range(vlen):
            query = sql.SQL(f"UPDATE app_db.public.reviews SET score_{UIDs[ind]} = {scores[UIDs[ind]][i]}, score_{UIDs[ind+1]} = {scores[UIDs[ind+1]][i]}, score_{UIDs[ind+2]} = {scores[UIDs[ind+2]][i]}, score_{UIDs[ind+3]} = {scores[UIDs[ind+3]][i]}, score_{UIDs[ind+4]} = {scores[UIDs[ind+4]][i]}, status = 'done' WHERE task_id = '{task_id}' AND review_id = '{scores['review_id'][i]}' AND status = 'in progress';")

            self.execute_query(query)

    def check_result(self, data):
        query = f"SELECT task_id, status FROM app_db.public.results WHERE task_id = '{data['task_id']}' AND client_id = '{data['client_id']}';" 

        rt = self.fetch_results(query)

        if len(rt) == 0:
            rc = {"status": "ok", "message": "the task not found"}
        else:
            rt = rt[0]

            if rt[-1] == "in progress":
                rc = {"status": "ok", "message": "the task is in progress"}
            elif rt[-1] == "no reviews":
                rc = {"status": "error", "message": "reviews not retrieved from the scraper"}
            else:
                query = f"SELECT task_id, review_id, content, score_as99, score_romanov2, score_bui5, score_jlo10, score_vdara2 FROM reviews WHERE task_id = '{data['task_id']}'"
                rt = self.fetch_results(query)

                reviews = {}
                for row in rt:
                    reviews[row[1]] = {"content": row[2], "sentiment": {"as99": row[3], "romanov2": row[4], "bui5": row[5], "jlo10": row[6], "vdara2": row[7]}}

                if len(reviews) > 0:
                    rc = {"status": "ok", "message": {"task_id": row[0], "reviews": reviews}}
                else:
                    rc = {"status": "error", "message": "reviews not found"}
        
        return rc

    def close_connection(self, connection):
        self.pool.putconn(connection)
