import yaml
import json

from psycopg2 import pool, sql
from webutils.utils import UIDs

class DBHandler:
    _instance = None

    def __new__(cls):
        # Singleton Pattern: Ensure only one instance of DBHandler is created
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize the singleton instance and load configuration
        self.load_config()
    
    def load_config(self, config_path='config.yaml'):
        # Load configuration from YAML file
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    
        # Assign values from the configuration
        self.host = config['postgres']['host']
        self.port = config['postgres']['port']
        self.name = config['postgres']['database']
        self.user = config['postgres']['username']
        self.password = config['postgres']['password']
        self.minconn = config['postgres']['minconn']
        self.maxconn = config['postgres']['maxconn']

    def get_connection(self):
        # Create a connection pool using psycopg2
        self.pool = pool.SimpleConnectionPool(
            minconn=self.minconn,
            maxconn=self.maxconn,
            host=self.host,
            port=self.port,
            dbname=self.name,
            user=self.user,
            password=self.password
        )

        # Get a connection from the pool
        return self.pool.getconn()

    def execute_query(self, query):
        # Execute a SQL query and commit changes
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()
        except Exception as e:
            # Rollback changes if an exception occurs
            connection.rollback()
            raise e

        finally:
            # Close the cursor and return the connection to the pool
            cursor.close()
            self.close_connection(connection)

    def fetch_results(self, query):
        # Execute a SQL query and fetch results
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            return results

        except Exception as e:
            raise e

        finally:
            # Close the cursor and return the connection to the pool
            cursor.close()
            self.close_connection(connection)
    
    # Other methods with SQL queries

    def close_connection(self, connection):
        # Return the connection to the pool
        self.pool.putconn(connection)
