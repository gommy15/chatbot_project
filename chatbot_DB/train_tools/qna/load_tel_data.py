import pymysql
import openpyxl

from config.DatabaseConfig import *

def all_clear_train_data(db):
    #기존 학습데이터 삭제
    sql = '''
        delete from chatbot_tel_data
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)

    #auto increment 초기화
    sql = '''
        ALTER TABLE chatbot_tel_data AUTO_INCREMENT=1
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)

def insert_data(db, xls_row):
    dept, tel_num, _ = xls_row

    sql = '''
        INSERT chatbot_tel_data(dept, tel_num)
        values('%s', '%s')
    '''% (dept.value, tel_num.value)

    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        print('{} 저장'.format(tel_num.value))
        db.commit()

train_file = './tel_data.xlsx'
db = None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    #기존 학습 데이터 초기화
    all_clear_train_data(db)

    #학습 엑셀 파일 불러오기
    wb = openpyxl.load_workbook(train_file)
    sheet = wb['Sheet1']
    for row in sheet.iter_rows(min_row=2):
        #데이터 저장
        insert_data(db, row)

    wb.close()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print("DB 연결 닫기 성공")