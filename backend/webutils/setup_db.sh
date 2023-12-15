#!/bin/bash

DB_NAME="app_db"
DB_USER="user"
DB_PASSWORD="password"
TABLE_NAME="results"
TABLE_NAME2="reviews"
COLUMN_NAME="url"

sudo -u postgres createuser --interactive --createdb --login --no-superuser --no-createrole --login $DB_USER
sudo -u postgres createdb $DB_NAME --owner=$DB_USER
# sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -d $DB_NAME -c "CREATE TABLE IF NOT EXISTS $TABLE_NAME (id SERIAL PRIMARY KEY, client_id VARCHAR(32), task_id VARCHAR(20), timestamp BIGINT, url VARCHAR(255), score INTEGER, status VARCHAR(16));"
sudo -u postgres psql -d $DB_NAME -c "CREATE INDEX idx_${COLUMN_NAME} ON ${TABLE_NAME}(${COLUMN_NAME});"

sudo -u postgres psql -d $DB_NAME -c "CREATE TABLE IF NOT EXISTS $TABLE_NAME2 (id SERIAL PRIMARY KEY, task_id VARCHAR(32) NOT NULL, status VARCHAR(10) NOT NULL, review_id VARCHAR(32) NOT NULL, content TEXT, score_as99 INTEGER, score_romanov2 INTEGER, score_bui5 INTEGER, score_jlo10 INTEGER, score_vdara2 INTEGER);"
sudo -u postgres psql -d $DB_NAME -c "ALTER TABLE $TABLE_NAME ADD CONSTRAINT fk_results_reviews FOREIGN KEY (task_id) REFERENCES $TABLE_NAME2(task_id);"

echo -n "Database setup complete"