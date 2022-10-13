class FindAnswer:
    def __init__(self, db):
        self.db = db

    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_train_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_tags != None:
            where = ' where intent="%s" '% intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        return sql

    # 전화번호 검색 쿼리
    def _search_tel_query(self, ner_name):
        sql = "select tel_num from chatbot_tel_data where dept like '%{}%'".format(ner_name)

        return sql

    # 전화번호 검색 쿼리
    def _search_dept_query(self, question):
        sql = "select dept from chatbot_question_data where question like '%{}%'".format(question)

        return sql

    # 답변 검색
    def search(self, intent_name, ner_tags=None, ner_name=None):
        # 의도명과 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)

        if ner_tags == 'B_QUES':
            sql = self._search_dept_query(ner_name)
            dept_name = self.db.select_one(sql)
            dept_name = dept_name['dept']
            sql = self._search_tel_query(dept_name)
            tel_num = self.db.select_one(sql)
            tel_num = tel_num['tel_num']

        elif ner_tags == 'B_DEPT':
            sql = self._search_tel_query(ner_name)
            tel_num = self.db.select_one(sql)
            tel_num = tel_num['tel_num']
            dept_name = ner_name

        else:
            # 검색되는 답변이 없으면 의도명만 검색
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)
            tel_num = None
            dept_name = None


        return answer['answer'], tel_num, dept_name

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer, tel_num=None, ner_set=None):
        for word, tag in ner_predicts:
            # 변환해야 하는 태그가 있는 경우 추가
            if tag == 'B_DEPT':
                answer = answer.replace(tag, word)
                answer = answer.replace('TEL', tel_num)
            if tag == 'B_QUES':
                answer = answer.replace(tag, word)
                for word, tag in ner_set:
                    if tag == 'B_DEPT':
                        answer = answer.replace(tag, word)
                        answer = answer.replace('TEL', tel_num)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer

if __name__ == "__main__":
    from config.DatabaseConfig import *
    from utils.Database import Database

    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    db.connect()  # 디비 연결
    answer_t = FindAnswer(db)
    ner_predict = [('휴학', 'B_QUES')]
    answer, tel_num, dept_name = answer_t.search('질문', ner_predict[0][1], ner_predict[0][0])

    if dept_name is not None:
        ner_set = [(dept_name, 'B_DEPT')]
        answer_f = answer_t.tag_to_word(ner_predict, answer, tel_num, ner_set)
    else:
        answer_f = answer_t.tag_to_word(ner_predict, answer, tel_num)

    print(answer_f)

