# 학교 부서 전화번호 알리미 챗봇

해당 챗봇은 "처음 배우는 딥러닝 챗봇" 책을 기반으로 만들었습니다.


## 구성
- 챗봇 엔진 : bot.py
- 챗봇 api : chatbot_api/app.py

## 코드 구조
<pre>
/
    /chatbot_api    -> 챗봇과 카카오 api 연동 코드
    /config         -> 데이터 베이스 연결에 필요한 코드
    /models         -> 챗봇에 사용되는 모델 학습 코드
    /test           -> 챗봇을 로컬에서 테스트 하는 코드
    /train_tools    -> 챗봇을 사용하는데 필요한 데이터 생성 코드
    /utils          -> 챗봇 엔진 구동시 사용되는 코드
</pre>

## 사용 방법
1. config 폴더의 DatabaseConfig.py 에서 데이터베이스와 연결
2. bot.py 실행
3. chatbot_apt 폴더의 app.py 실행
4. 연결된 카카오 채널에 들어가서 문의 사항 채팅
