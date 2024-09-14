# 개요

**Kakao-chatbot** 패키지는 카카오 i 오픈빌더를 이용한 카카오톡 챗봇 개발을 위한 패키지입니다. 오픈빌더에서 설정한 스킬 서버를 구현하는 데 필요한 요소들을 제공합니다.

이 패키지는 다음과 같은 주요 기능을 포함합니다:

- **스킬 서버 구현**: 오픈빌더와 통신하기 위한 스킬 서버를 손쉽게 구축할 수 있는 도구를 제공합니다.
- **입력 및 출력 처리**: 사용자 입력을 처리하고, 적절한 형태로 응답을 생성할 수 있는 유틸리티를 포함하고 있습니다.
- **컨텍스트 관리**: 사용자와의 대화 상태를 유지하고, 적절한 응답을 제공하기 위한 컨텍스트 관리 기능을 지원합니다.
- **유효성 검사**: 입력 데이터의 유효성을 검사하고, 오류를 처리하기 위한 기능을 제공합니다.
- **커스터마이징**: 다양한 커스터마이징 옵션을 통해 챗봇의 동작을 세밀하게 제어할 수 있습니다.

이 패키지는 카카오톡 챗봇 개발을 보다 효율적으로 수행할 수 있도록 돕기 위해 설계되었습니다. 개발자는 이 패키지를 사용하여 복잡한 작업을 단순화하고, 챗봇의 다양한 기능을 손쉽게 구현할 수 있습니다.

## 라이브러리 구조

이 라이브러리는 [카카오 비즈니스 가이드](https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format)에서 제공하는 스킬 서버 구현 가이드를 기반으로 설계되었습니다. 이에 따라 라이브러리는 가이드에서 제시하는 구조를 최대한 그대로 따르기 위해 복잡한 구조를 갖게 되었습니다.

![상속 관계 이미지](/source/image/class_inheritance_relationship.png)
[다운로드](/source/image/class_inheritance_relationship.png)
![라이브러리 위치 구조 이미지](/source/image/class_position_relationship.png)
[다운로드](/source/image/class_position_relationship.png)

위 이미지에 표시된 것처럼, 라이브러리는

- `Base(BaseModel)`
- `ParentPayload`

위 두 클래스를 기반으로 입력, 반환을 다루는 클래스들이 구현되어 있습니다.

### Payload(입력)

모든 입력은 ParentPayload 클래스를 상속받아 구현되어 있습니다. 또한 전부 `input.py` 파일에 구현되어 있어, `kakao_chatbot.input` 모듈에서 모두 import할 수 있습니다.
`from_dict` 또는 `from_json` 메서드를 통해 JSON 형태의 입력을 파이썬 객체로 변환해 사용할 수 있습니다. `Paylaod` 또는 `ValidationPayload로` 변환하면 하위 멤버들을 통해 입력 데이터를 쉽게 접근할 수 있습니다.

### Response(반환)

반환에 관련된 클래스들은 모두 `kakao_chatbot.response` 패키지에 구현되어 있습니다. 따라서 `kakao_chatbot.response`를 통해 import할 수 있습니다.

`KakaoResponse`에 컴포넌트를 추가하거나 데이터를 추가하는 등의 작업을 수행한 후, 딕셔너리나 JSON 형태로 변환하여 반환할 수 있습니다.

#### 컴포넌트

`ParentComponent` 클래스를 상속받아 다양한 컴포넌트들이 구현되어 있습니다. 컴포넌트는 skilltemplate을 구성하는 요소입니다.

### Context(컨텍스트)

컨텍스트는 사용자와의 대화 상태를 유지하고, 적절한 응답을 제공하기 위한 기능을 제공합니다. Context 객체는 Payload 객체의 멤버로 존재하며, KakaoResponse 객체를 반환할 때 이를 포함하여 반환할 수 있습니다. 따라서, 입력과 반환의 역할을 모두 수행할 수 있기 떄문에 `input`모듈이나 `response`패키지가 아닌 별도의 `context`모듈로 구현되어 있습니다.

### Event(이벤트)

이벤트는 EventAPI를 이용하기 위한 클래스들을 포함하고 있습니다. 이벤트는 `kakao_chatbot.event` 모듈을 통해 import할 수 있습니다. 이벤트는 `BaseEvent` 클래스를 상속받아 구현되어 있습니다. 이벤트를 발생시키고 발생 결과를 확인하기 위한 클래스들이 구현되어 있습니다. 또한 이 과정은 입력과 반환을 다루는 과정과는 별개로 이루어지기 때문에 별도의 모듈로 구현되어 있습니다.

## 설치

이 라이브러리는 PyPI에 등록되어 있습니다. 따라서 pip를 통해 간단히 설치할 수 있습니다.

```bash
pip install kakao-chatbot
```
