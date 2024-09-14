# Kakao-chatbot Response 패키지

kakao_chatbot 패키지에서 응답을 구성하는 요소들을 정의합니다.
스킬 서버의 응답을 구성할 때 사용합니다.

## 사용법

간단한 예제를 통해 사용법을 설명합니다.

### 응답 형식을 스킬 서버로 사용하는 경우

다음은 간단한 텍스트 응답을 구성하는 예시입니다.

```python
from kakao_chatbot.response import KakaoResponse
from kakao_chatbot.response.components import SimpleText

response = KakaoResponse()
response.add_component(SimpleText("안녕하세요!"))
response.to_dict()
```

### 응답 형식을 값으로 사용하는 경우

만약, 챗봇 관리자센터의 봇 응답형식 설정(말풍선 설정)으로 `{{#webhook.<json_path>}}`과 같은 형태를 사용하는 경우, 다음과 같이 사용할 수 있습니다.

```python
from kakao_chatbot.response import KakaoResponse

response = KakaoResponse()
response.data = {"msg": "안녕하세요!"}
response.to_dict()
```

이 경우 말풍선 안에 `{{#webhook.msg}}`를 입력하면 "안녕하세요!"가 출력됩니다.

## 모듈 및 하위 클래스 목록

```{toctree}
:maxdepth: 2

kakao_chatbot/response/base
kakao_chatbot/response/interaction
```
