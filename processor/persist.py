
import logging.config
import configparser
import psycopg2
import json


class PersistData:
    logging.config.fileConfig("resources/configs/logging.conf")
    logger = logging.getLogger("Persist")
    config = configparser.ConfigParser()
    config.read("./resources/fileprocessor.ini")

    def __init__(self, db_type: str = "postgres"):
        self.logger.debug("Driver constructor initialized")
        self.db_type = db_type

    def store_data(self, course_json):
        try:
            target_table = self.config.get("DATABASE_CONFIGS", "PG_TABLE")
            self.logger.debug(f"Target table name: {target_table}")
            self.logger.debug(f"Storing data to {self.db_type}")
            # self.write_to_pg(target_table)
            self.write_from_json_to_pg(target_table, course_json)
            self.read_from_pg(target_table)
        except Exception as e:
            self.logger.error(f"Error storing data to {self.db_type}. Error: {str(e)}")

    def read_from_pg(self, target_table):
        # Establish connection to Postgres database
        connection = psycopg2.connect(user="postgres",
                                      password="DaveAdmin",
                                      host="localhost",
                                      database="postgres")

        cursor = connection.cursor()  # Create cursor

        select_query = "SELECT * FROM " + target_table

        cursor.execute(select_query)  # execute the query

        records = cursor.fetchall()  # fetch the results

        for record in records:
            print(record)

        cursor.close()
        connection.commit()
        return records

    def write_to_pg(self, target_table):
        # Establish connection to Postgres database
        connection = psycopg2.connect(user="postgres",
                                      password="DaveAdmin",
                                      host="localhost",
                                      database="postgres")

        cursor = connection.cursor()  # Create cursor

        cursor.execute("SELECT max(course_id) from " + target_table)
        max_course_id = cursor.fetchone()[0]

        insert_query = ("INSERT INTO " + target_table + " " +
                        "(course_id, course_name, author_name, course_section, creation_date)"
                        "VALUES(%s, %s, %s, %s, %s)")

        insert_tuple = (max_course_id + 1, 'Ethical Hacking', "KingCode", '{"section": 1, "title": "Hack3"}', "2020-10-20")  # record to insert

        cursor.execute(insert_query, insert_tuple)  # Execute query

        cursor.close()
        connection.commit()

    def write_from_json_to_pg(self, target_table, course_json):
        self.logger.debug("Writing from json to postgres database")
        # Establish connection to Postgres database
        connection = psycopg2.connect(user="postgres",
                                      password="DaveAdmin",
                                      host="localhost",
                                      database="postgres")

        cursor = connection.cursor()  # Create cursor

        cursor.execute("SELECT max(course_id) from " + target_table)
        max_course_id = cursor.fetchone()[0]

        insert_query = ("INSERT INTO " + target_table + " " +
                        "(course_id, course_name, author_name, course_section, creation_date)"
                        "VALUES(%s, %s, %s, %s, %s)")

        insert_tuple = (max_course_id + 1,
                        course_json["course_name"],
                        course_json["author_name"],
                        json.dumps(course_json["course_section"]),
                        course_json["creation_date"])  # record to insert

        cursor.execute(insert_query, insert_tuple)  # Execute query

        cursor.close()
        connection.commit()
