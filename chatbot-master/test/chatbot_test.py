from config.DatabaseConfig import *
from utils.Database import Database
from utils.Preprocess import Preprocess

# 전처리 객체 생성
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()    # 디비 연결


# 원문
query = "휴학은 어디로 전화해야하나요?"

# 의도 파악
from models.intent.IntentModel import IntentModel
intent = IntentModel(model_name='../models/intent/intent_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식
from models.ner.NerModel import NerModel
ner = NerModel(model_name='../models/ner/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)


for i in range(len(predicts)):
    #if predicts[i][1] == ner_tags[0]:
    try:
        if predicts[i][1] in ner_tags:
            only_tag_name = predicts[i][0]
            predict_tuple = predicts[i]
            predicts = [predict_tuple]

            print(only_tag_name)
            print(predict_tuple)
    except:
        break

#튜플로 전달시
#f.search(intent_name, predict_tuple)
#따로 따로 전달시
#f.search(intent_name, only_tag_name, ner_tags[0])




"""
f = FindAnswer(db)
answer, tel_num, dept_name = f.search(intent_name, only_tag_name, ner_tags[0])
if dept_name is not None:
    ner_set = [(dept_name, 'B_DEPT')]
    answer_f = f.tag_to_word(predict_tuple, answer, tel_num, ner_set)
else:
    answer_f = f.tag_to_word(predict_tuple, answer, tel_num)
"""

# 답변 검색
from utils.FindAnswer import FindAnswer
try:
    f = FindAnswer(db)
    answer_text, tel_num, dept_name = f.search(intent_name, predicts[0][1], predicts[0][0])
    if dept_name is not None:
        ner_set = [(dept_name, 'B_DEPT')]
        answer = f.tag_to_word(predicts, answer_text, tel_num, ner_set)
    else:
        answer = f.tag_to_word(predicts, answer_text, tel_num)

except:
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변 : ", answer)

db.close() # 디비 연결 끊음
