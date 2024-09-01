# Kakao-chatbot Response Components 패키지

kakao_chatbot.response.components 패키지는 Kakao 응답 컴포넌트를 정의합니다.
카카오 응답 컴포넌트는 카카오 응답 메시지를 구성하는 요소들을 의미합니다.

## 사용법

### Flask

```python
from flask import Flask
from kakao_chatbot.response import KakaoResponse
from kakao_chatbot.response.components import SimpleText

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    response = KakaoResponse()
    response.add_component(SimpleText("안녕하세요!"))
    return response.to_dict()
```

### FastAPI

```python
from fastapi import FastAPI
from kakao_chatbot.response import KakaoResponse
from kakao_chatbot.response.components import SimpleText

app = FastAPI()

@app.post("/webhook")
async def webhook():
    response = KakaoResponse()
    response.add_component(SimpleText("안녕하세요!"))
    return response.to_json()
```

## 모듈 및 하위 클래스 목록

```{toctree}
:maxdepth: 2

kakao_chatbot/response/components/card
kakao_chatbot/response/components/common
kakao_chatbot/response/components/itemcard
kakao_chatbot/response/components/simple
```
