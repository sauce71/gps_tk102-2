import pymysql


class DbWrapper:
    def __init__(self, config):
        self.connection = pymysql.connect(host=config['host'],
                                          user=config['user'],
                                          password=config['password'],
                                          db=config['db'])

    def insert_device(self, params):
        self.connection.ping(True)
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `device` (`id`) VALUES (%s)"
            cursor.execute(sql, params)
        self.connection.commit()

    def insert_location(self, params):
        self.connection.ping(True)
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `location` (`device_id`, `lat`, `lng`, `speed`, `date`, `url`, `availability`, `iostate`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, params)

        # connection is not autocommit by default. So you must commit to save your changes.
        self.connection.commit()

    def __del__(self):
        self.connection.close()
