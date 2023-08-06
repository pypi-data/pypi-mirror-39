import boto3
import base64
import json
import snowflake.connector


class SnowFlakeConnection:
    def __init__(self, snowflake_db_connection):
        self.snowflakeCredentials = json.loads(snowflake_db_connection)

    def snowflake_db_connection(self):
        kmsClient = boto3.Session(region_name='us-east-1').client('kms')
        response = kmsClient.decrypt(CiphertextBlob=base64.b64decode(self.snowflakeCredentials['ciphertext']))
        self.snowflakeCredentials['password'] = response['Plaintext'].decode("utf-8")
        del self.snowflakeCredentials['ciphertext']
        snowflake_con = snowflake.connector.connect(**self.snowflakeCredentials)
        return snowflake_con

class TableArchival:
    def __init__(self,table_filter_dict,snowflake_db_connection):
        self.table_filter_dict = table_filter_dict
        self.snowflake_db_connection = snowflake_db_connection

    def stream_table_archival(self):

        for table in self.table_filter_dict:
            try:

                joinPredicates = ['{} {} {}'.format(c[0], c[1], c[2]) for c in self.table_filter_dict[table]]

                insert_query = "INSERT INTO {table}_archival SELECT * FROM {table} WHERE {cols};".format(table=table,cols= " AND ".join(joinPredicates))
                delete_query = "DELETE FROM {table} WHERE {cols};".format(table=table,cols= " AND ".join(joinPredicates))

                jdbc_sql_conn = SnowFlakeConnection(self.snowflake_db_connection)
                jdbc_sql_conn_str = jdbc_sql_conn.snowflake_db_connection()
                print("Status Running Query:",insert_query)
                jdbc_sql_conn_str.execute_string(insert_query)
                print("Status Success",'\n')
                print("Status Running Query:",delete_query)
                jdbc_sql_conn_str.execute_string(delete_query)
                print("Status Success")

            except Exception as e:
                print("Job Failed Error: {}".format(e))
                raise