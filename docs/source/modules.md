# Kakao-chatbot 패키지

kakao-chatbot 패키지의 최상위 모듈에 대한 설명입니다.
이들은 kakao_chatbot.response 패키지 및 그 하위 패키지에 포함되지 않은 다른 모든 모듈입니다.
따라서 response가 아닌 기본 부모 클래스, 입력, 검증 등을 다룹니다.

## 사용법

### EventAPI 사용

EventAPI 클래스를 사용하여 이벤트를 생성하고 사용자를 추가할 수 있습니다.

아래 예제는 이벤트를 생성하고 사용자를 추가한 후 요청을 보내는 예제입니다.
예제를 실행하려면 `requests` 패키지가 필요합니다.

```bash
pip install requests
```

```python
from kakao_chatbot.event import EventAPI
import requests

event = EventAPI(bot_id="1234", api_key="abcd", event_name="event_name")
event.add_user(id_type="uuid", ID="1234")

response = requests.post(event.url, headers=event.headers, body=event.body)
```

### Payload 사용

Payload 클래스를 사용하여 입력 데이터를 파이썬 객체로 변환할 수 있습니다.

아래 예제는 JSON 형태의 입력 데이터를 파이썬 객체로 변환하는 예제입니다.

#### Flask

```python
from flask import Flask, request
from kakao_chatbot.input import Payload

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = Payload.from_dict(request.json)
    return "Success"
```

#### FastAPI(1)

```python
from fastapi import FastAPI, Request
from kakao_chatbot import Payload

app = FastAPI()

@app.post("/webhook")
async def webhook(reqeust: Request):
    payload = Payload.from_dict(await request.json())
    return "Success"
```

#### FastAPI(2)

```python
from fastapi import FastAPI, Request, Depends
from kakao_chatbot import Payload

async def parse_payload(request: Request) -> Payload:
    """Request에서 Payload를 추출합니다.

    Request에서 JSON 데이터를 추출하여 Payload 객체로 변환합니다.
    FastAPI의 Dependency Injection을 사용하기 위한 함수입니다.
    """
    data_dict = await request.json()
    return Payload.from_dict(data_dict)

app = FastAPI()

@app.post("/webhook")
async def webhook(payload: Payload = Depends(parse_payload)):
    return "Success"
```

## 모듈 및 하위 클래스 목록

```{toctree}
:maxdepth: 2

kakao_chatbot/event
kakao_chatbot/base
kakao_chatbot/context
kakao_chatbot/customerror
kakao_chatbot/input
kakao_chatbot/utils
kakao_chatbot/validation
```
