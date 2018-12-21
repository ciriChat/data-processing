from mysql import connector
from config import db_config


def get_connection(db_name):
    config = db_config['mysql'][db_name]
    return connector.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            database=config['database'],
            port=config['port'],
            auth_plugin='mysql_native_password'
        )

