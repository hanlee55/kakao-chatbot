"""EventAPI는 카카오톡 챗봇으로 알림을 보내는 API를 제공합니다.

EventAPI 클래스로 제공되는 객체를 이용하여 카카오톡 챗봇으로 메시지를 간단하게 보낼 수 있습니다.
"""

import datetime
import json
from typing import Optional, overload, List, Dict
from .base import BaseModel, ParentPayload
from .validation import validate_str, validate_type


class EventUser(BaseModel):
    """EventUser는 EventAPI 클래스의 사용자 정보를 담는 클래스입니다.

    EventAPI 클래스의 사용자 정보를 담는 클래스로, EventAPI 클래스의 users 프로퍼티에 추가합니다.

    id_type은 아래 중 하나여야 합니다.

    - appUserId
    - plusfriendUserKey
    - botUserKey

    Attributes:
        id_type (str): 사용자 ID 타입
        id (str): 사용자 ID
        properties (dict[str, str]): 기본값 None, 유저 별 추가 페이로드
            유저 별로 추가적으로 skill 서버에 전달할 데이터가 있을 경우
            properties 필드에 담긴 값이 skill payload 의
            userRequest.user.properties 필드에포함되어 전달됩니다.
            >>> Payload.user_request.user.properties
    """

    type_list = ["appUserId", "plusfriendUserKey", "botUserKey"]

    def __init__(
        self, id_type: str, ID: str, properties: Optional[Dict[str, str]] = None
    ):
        """EventUser의 생성자 메서드입니다.

        사용자의 ID 타입, ID, 그리고 추가 속성을 설정합니다. `id_type`은 사전에 정의된 타입 목록 중 하나여야 하며,
        `properties`는 유저 별 추가 페이로드를 담는 선택적 인자입니다.

        Args:
            id_type (str): 사용자 ID 타입
            ID (str): 사용자 ID
            properties (dict[str, str], optional): 유저 별 추가 페이로드. 기본값은 None입니다.
        """
        self.id_type = id_type
        self.id = ID
        self.properties = properties

    def validate(self):
        """EventUser의 유효성을 검사합니다.

        id_type, id, properties의 타입을 검사합니다.

        Raises:
            AssertionError: id_type이 허용되지 않는 값인 경우
            InvalidTypeError: id, properties가 허용되지 않는 타입인 경우
        """
        assert self.id_type in self.type_list
        validate_str(self.id, disallow_none=True)
        validate_type(dict, self.properties)

    def render(self):
        """EventUser 객체를 카카오톡 요청 규칙에 맞게 딕셔너리로 변환합니다.

        변환된 딕셔너리를 EventAPI 객체에서 body를 생성할 때 사용합니다.

        Returns:
            dict: EventUser 객체를 변환한 딕셔너리
        """
        temp = {
            "type": self.id_type,
            "id": self.id,
            "properties": self.properties,
        }
        return self.remove_none_item(temp)


class EventAPI(BaseModel):
    """EventAPI는 카카오톡 챗봇으로 알림을 보내는 API를 제공합니다.

    EventAPI 클래스로 제공되는 객체를 이용하여 카캉오톡 챗봇으로 알림을 간단하게 보낼 수 있습니다.

    EventAPI의 url 프로퍼티 값으로 post 요청을 headers와 body 프로퍼티 값과 함께 보내면 됩니다.

    Examples:
        >>> event = EventAPI(
        ...     bot_id="bot_id",
        ...     api_key="api_key",
        ...     event="event_name",
        ...    )
        >>> event.add_user(
        ...     id_type="appUserId",
        ...     ID="user_id",
        ... )

    Attributes:
        bot_id (str): 봇의 ID
        api_key (str): 카카오 디벨로퍼스 REST API 키
        event (str): 오픈빌더에서 설정한 이벤트 이름
        users (list[EventUser]): 기본값 None, 알림을 받을 사용자 정보 리스트
        data (dict): 기본값 None, 이벤트 데이터
            data 파라미터는 skill 서버까지 전달되는 파라미터로,
            오픈빌더에서 텍스트 영역에 {{#current.event.data.paramName}}을
            말풍선에 넣어 사용 가능합니다.
        params (dict): 기본값 None, event param (skill 서버까지 전달)
            skill 서버에서 request body 의 userRequest -> params로 값을 전달받을 수 있습니다.
            ```python
            >>> Payload.user_request.params
            ```
        option (dict): 기본값 None, Event API 사용 특수 옵션
        is_devchannel (bool): 기본값 False, 개발 채널 여부
            개발 채널의 경우 True로 설정
        max_user (int): 기본값 100, 최대 사용자 수
            현재 100명까지 가능합니다.
    """

    def __init__(
        self,
        bot_id: str,
        api_key: str,
        event: str,
        users: Optional[List[EventUser]] = None,
        data: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        option: Optional[Dict[str, str]] = None,
        is_devchannel: Optional[bool] = False,
        max_user: int = 100,
    ):
        """EventAPI의 생성자 메서드입니다.

        Args:
            bot_id (str): 봇의 ID
            api_key (str): 카카오 디벨로퍼스 REST API 키
            event (str): 오픈빌더에서 설정한 이벤트 이름
            users (list[EventUser], optional): 기본값 None, 알림을 받을 사용자 정보 리스트
            data (dict, optional): 기본값 None, 이벤트 데이터
            params (dict, optional): 기본값 None, event param (skill 서버까지 전달)
            option (dict, optional): 기본값 None, Event API 사용 특수 옵션
            is_devchannel (bool, optional): 기본값 False, 개발 채널 여부
            max_user (int, optional): 기본값 100, 최대 사용자 수
        """
        if is_devchannel and bot_id.endswith("!"):
            bot_id = bot_id[:-1]
        self.bot_id = bot_id
        self.api_key = api_key
        self.event = event
        if users is None:
            users = []
        self.users = users
        if data is None:
            data = {}
        self.data = data
        if params is None:
            params = {}
        self.params = params
        self.option = option
        self.is_devchannel = is_devchannel
        self.max_user = max_user

    def validate(self):
        """EventAPI의 유효성을 검사합니다.

        bot_id, api_key, event, users, params, option, data의 타입을 검사합니다.
        users의 길이를 검사합니다.

        Raises:
            InvalidTypeError: 검증하는 값이 허용되지 않는 타입인 경우
            AssertionError: users가 없는 경우
            AssertionError: users의 길이가 100을 초과하는 경우
        """
        validate_str(self.bot_id, self.api_key, self.event, disallow_none=True)
        if not self.users:
            raise AssertionError("users는 최소 1개 이상이어야 합니다.")
        if len(self.users) > self.max_user:
            raise AssertionError(f"users는 최대 {self.max_user}개 이하여야 합니다.")
        for user in self.users:
            user.validate()

        validate_type(dict, self.params, self.option, self.data)

    def render(self):
        """EventAPI 객체를 카카오톡 요청 규칙에 맞게 딕셔너리로 변환합니다.

        요청할 body를 반환합니다.

        Returns:
            dict: EventAPI 객체를 변환한 딕셔너리
        """
        event = {
            "name": self.event,
            "data": self.data if self.data else None,
        }
        event = self.remove_none_item(event)
        self.validate()
        temp = {
            "event": event,
            "user": ([user.render() for user in self.users] if self.users else None),
            "params": self.params if self.params else None,
            "option": self.option,
        }
        return self.remove_none_item(temp)

    @overload
    def add_user(self, user: EventUser) -> "EventAPI": ...

    @overload
    def add_user(
        self,
        id_type: str,
        ID: str,  # pylint: disable=invalid-name
        properties: Optional[Dict[str, str]] = None,
    ) -> "EventAPI": ...

    def add_user(self, *args, **kwargs) -> "EventAPI":
        """이벤트를 받을 사용자 정보를 추가합니다.

        이 메서드는 다음 두 가지 방법으로 호출할 수 있습니다:

        1. `EventUser` 객체를 직접 전달.
        2. `id_type`, `ID`, 및 선택적인 `properties`를 전달하여 `EventUser` 객체를 생성.

        Args:
          *args:
            - `EventUser`: 추가할 사용자 객체.
            - `id_type` (str): 사용자 ID 타입.
            - `ID` (str): 사용자 ID.
            - `properties` (dict[str, str], optional): 사용자 속성.
          **kwargs:
            - `user` (EventUser): 추가할 사용자 객체.
            - `id_type` (str): 사용자 ID 타입.
            - `ID` (str): 사용자 ID.
            - `properties` (dict[str, str], optional): 사용자 속성.

        Returns:
          EventAPI: 사용자 정보가 추가된 `EventAPI` 객체.

        Raises:
          TypeError: 유효한 인자가 제공되지 않은 경우.
        """
        if len(args) > 0 and isinstance(args[0], EventUser):
            self.users.append(args[0])
        elif kwargs.get("user", None) is not None:
            self.users.append(kwargs["user"])
        else:
            user = EventUser(*args, **kwargs)
            self.users.append(user)
        return self

    @property
    def headers(self) -> Dict[str, str]:
        """EventAPI의 헤더를 반환합니다.

        api_key가 "KakaoAK "로 시작하지 않는 경우 "KakaoAK "를 자동으로 추가합니다.

        Returns:
            dict[str, str]: API 요청 헤더
        """
        if not self.api_key.startswith("KakaoAK "):
            self.api_key = "KakaoAK " + self.api_key
        return {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    @property
    def url(self) -> str:
        """EventAPI의 URL을 반환합니다.

        bot_id를 이용하여 URL을 생성합니다.

        생성된 URL로 POST 요청을 보내면 됩니다.

        Returns:
            str: EventAPI의 URL
        """
        if self.is_devchannel:
            return f"https://dev-bot-api.kakao.com/v2/bots/'{self.bot_id}!'/talk"
        return f"https://bot-api.kakao.com/v2/bots/{self.bot_id}/talk"

    @property
    def body(self) -> Dict:
        """EventAPI의 body를 반환합니다.

        self.render()로 생성된 딕셔너리를 반환합니다.

        API 요청 시 body로 사용합니다.

        Returns:
            dict: EventAPI의 body
        """
        return self.render()


class EventAPIResponse(ParentPayload):
    """EventAPI의 응답을 담는 클래스입니다.

    EventAPI를 통해 보낸 post 요청에 대한 응답을 담는 클래스입니다.

    Attributes:
        task_id (str): 실행 결과를 조회하고자 하는 taskID
        status (str): SUCCESS나 FAIL중 하나
        message (str): 실행 결과에 대한 메시지
        timestamp (datetime.datetime): 응답 시간
    """

    def __init__(
        self, task_id: str, status: str, message: str, timestamp: datetime.datetime
    ):
        """EventAPIResponse 인스턴스를 초기화합니다.

        Args:
            task_id (str): 실행 결과를 조회하기 위한 taskID.
            status (str): SUCCESS나 FAIL 중 하나.
            message (str): 실행 결과에 대한 메시지.
            timestamp (datetime.datetime): 응답 시간.
        """
        self.task_id = task_id
        self.status = status
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def from_dict(cls, data: Dict) -> "EventAPIResponse":
        """EventAPIResponse 객체를 딕셔너리로부터 생성합니다.

        Args:
            data (dict): EventAPIResponse 객체를 생성할 딕셔너리

        Returns:
            EventAPIResponse: 생성된 EventAPIResponse 객체
        """
        return cls(
            task_id=data.get("task_id", ""),
            status=data.get("status", ""),
            message=data.get("message", ""),
            timestamp=datetime.datetime.fromtimestamp(data.get("timestamp", "")),
        )

    @classmethod
    def from_json(cls, data: str) -> "EventAPIResponse":
        """JSON 문자열로부터 EventAPIResponse 객체를 생성합니다.

        Args:
            data (str): JSON 문자열.

        Returns:
            EventAPIResponse: 생성된 EventAPIResponse 객체.
        """
        return cls.from_dict(json.loads(data))


class CheckEventAPI(BaseModel):
    """CheckEventAPI는 EventAPI 클래스의 이벤트 상태 확인 API를 제공합니다.

    CheckEventAPI 클래스로 제공되는 객체를 이용하여 카카오톡 챗봇으로 알림을 간단하게 보낼 수 있습니다.

    Attributes:
        task_id (str): 실행 결과를 조회하고자 하는 taskID
        api_key (str): 카카오 디벨로퍼스 REST API 키
    """

    def __init__(self, task_id: str, api_key: str):
        """CheckEventAPI의 생성자 메서드입니다.

        Args:
            task_id (str): 실행 결과를 조회하고자 하는 taskID
            api_key (str): 카카오 디벨로퍼스 REST API 키
        """
        self.task_id = task_id
        self.api_key = api_key

    def validate(self):
        """CheckEventAPI의 유효성을 검사합니다.

        task_id, api_key의 타입을 검사합니다.

        Raises:
            InvalidTypeError: 검증하는 값이 허용되지 않는 타입인 경우
        """
        validate_str(self.task_id, self.api_key, disallow_none=True)

    def render(self):
        """CheckEventAPI 객체를 카카오톡 요청 규칙에 맞게 딕셔너리로 변환합니다.

        요청할 headers를 반환합니다.
        api_key가 "KakaoAK "로 시작하지 않는 경우 "KakaoAK "를 자동으로 추가합니다.

        Returns:
            dict: CheckEventAPI 객체를 변환한 딕셔너리
        """
        self.validate()
        api_key = self.api_key
        if not api_key.startswith("KakaoAK "):
            api_key = "KakaoAK " + api_key
        temp = {
            "Authorization": api_key,
            "Content-Type": "application/json",
        }
        return temp

    @property
    def url(self) -> str:
        """CheckEventAPI의 URL을 반환합니다.

        task_id를 이용하여 URL을 생성합니다.

        생성된 URL로 POST 요청을 보내면 됩니다.

        Returns:
            str: CheckEventAPI의 URL
        """
        return f"https://bot-api.kakao.com/v2/tasks/{self.task_id}"

    @property
    def headers(self) -> Dict[str, str]:
        """CheckEventAPI를 이용해 요청할 헤더를 반환합니다.

        api_key가 "KakaoAK "로 시작하지 않는 경우 "KakaoAK "를 자동으로 추가합니다.

        Returns:
            dict[str, str]: API 요청 헤더
        """
        return self.render()


class CheckEventAPIResponse(ParentPayload):
    """CheckEventAPI의 응답을 담는 클래스입니다.

    CheckEventAPI를 통해 보낸 post 요청에 대한 응답을 담는 클래스입니다.

    Attributes:
        task_id (str): 실행 결과를 조회하고자 하는 taskID
        status (str): ALL SUCCESS나 N FAIL중 하나 (N은 실패 건수)
        all_request_count (int): 전체 요청 횟수
        success_count (int): 성공적으로 처리된 요청 횟수
        fail (Optional[dict]): 실패 결과에 대한 정보
    """

    def __init__(
        self,
        task_id: str,
        status: str,
        all_request_count: int,
        success_count: int,
        fail: Optional[Dict] = None,
    ):
        """CheckEventAPIResponse의 생성자 메서드입니다.

        Args:
            task_id (str): 실행 결과를 조회하고자 하는 taskID
            status (str): ALL SUCCESS나 N FAIL중 하나 (N은 실패 건수)
            all_request_count (int): 전체 요청 횟수
            success_count (int): 성공적으로 처리된 요청 횟수
            fail (Optional[dict], optional): 실패 결과에 대한 정보
        """
        self.task_id = task_id
        self.status = status
        self.all_request_count = all_request_count
        self.success_count = success_count
        self.fail = fail

    @classmethod
    def from_dict(cls, data: Dict) -> "CheckEventAPIResponse":
        """CheckEventAPIResponse 객체를 딕셔너리로부터 생성합니다.

        Args:
            data (dict): CheckEventAPIResponse 객체를 생성할 딕셔너리

        Returns:
            CheckEventAPIResponse: 생성된 CheckEventAPIResponse 객체
        """
        return cls(
            task_id=data.get("task_id", ""),
            status=data.get("status", ""),
            all_request_count=data.get("all_request_count", 0),
            success_count=data.get("success_count", 0),
            fail=data.get("fail", None),
        )

    @classmethod
    def from_json(cls, data: str) -> "CheckEventAPIResponse":
        """CheckEventAPIResponse 객체를 JSON 문자열로부터 생성합니다.

        생성된 CheckEventAPIResponse 객체를 반환합니다.

        Args:
            data (str): CheckEventAPIResponse 객체를 생성할 JSON 문자열

        Returns:
            CheckEventAPIResponse: 생성된 CheckEventAPIResponse 객체
        """
        return cls.from_dict(json.loads(data))

    @property
    def fail_count(self) -> int:
        """CheckEventAPI의 실패한 사용자 수를 반환합니다.

        Returns:
            int: 실패한 사용자 수
        """
        if self.fail is None:
            return 0
        return self.fail.get("count", 0)

    @property
    def fail_list(self) -> List[Dict[str, str]]:
        """CheckEventAPI의 실패한 사용자 리스트를 반환합니다.

        Returns:
            list[str]: 실패한 사용자 리스트
        """
        if self.fail is None:
            return []
        return self.fail.get("list", [])
