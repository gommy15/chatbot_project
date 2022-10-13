import pymysql
from config.DatabaseConfig import *

db = None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )

    sql = '''
      CREATE TABLE IF NOT EXISTS `chatbot_question_data` (
      `ques_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
      `question` text NULL,
      `dept` text NULL,
      PRIMARY KEY (`ques_id`))
    ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''

    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print("DB 연결 닫기 성공")