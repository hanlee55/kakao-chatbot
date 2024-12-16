"""컨텍스트 정보를 담는 클래스를 정의하는 모듈입니다.

컨텍스틑 정보는 Payload 및 Response에서 동일한 형태의 데이터로 사용되기 떄문에,
이를 통일된 형태로 관리하기 위해 별도의 모듈 및 클래스로 정의합니다.
"""

from typing import Optional, Dict
from .base import ParentPayload, SkillTemplate
from .validation import validate_int, validate_str, validate_type


class Context(ParentPayload, SkillTemplate):
    """컨텍스트 정보를 담는 클래스입니다.

    컨텍스트 정보는 봇과 사용자간의 문맥적 상황 공유를 위해 사용됩니다.
    컨텍스트 정보는 이름, 남은 횟수, 유지 시간, 추가 정보를 가집니다.
    챗봇 관리자센터에서 컨텍스트를 설정하지 않으면 이 정보는 무시됩니다.

    이 클래스는 Payload와 Response에서 사용될 수 있도록 공통된 형태로 정의됩니다.
    따라서 from_dict와 render 메서드를 함께 제공합니다.

    Args:
        name (str): 컨텍스트의 이름
        lifespan (int): 컨텍스트의 남은 횟수
        ttl (int, optional): 컨텍스트가 유지되는 시간
        params (Dict, optional): 컨텍스트의 추가 정보

    Attributes:
        name (str): 컨텍스트의 이름
        lifespan (int): 컨텍스트의 남은 횟수
        ttl (int): 컨텍스트가 유지되는 시간
        params (Dict[str, ContextParam]): 컨텍스트의 추가 정보

    Examples:
        >>> context = Context(
        ...     name="context_name",
        ...     lifespan=1,
        ...     ttl=600,
        ...     params={
        ...         "key": {
        ...             "value": "value",
        ...             "resolved_value": "resolved_value"
        ...         }
        ...     }
        ... )
        >>> context.render()
        {
            "name": "context_name",
            "lifespan": 1,
            "ttl": 600,
            "params": {
                "key": "value"
            }
        }
    """

    def __init__(
        self,
        name: str,
        lifespan: int,
        ttl: Optional[int] = None,
        params: Optional[Dict] = None,
    ):
        """Context 객체를 초기화합니다."""
        super().__init__()
        self.name = name
        self.lifespan = lifespan
        self.ttl = ttl
        self.params: Dict[str, ContextParam] = params or {}

    @classmethod
    def from_dict(cls, data: Dict) -> "Context":
        """딕셔너리를 Context 객체로 변환합니다.

        변환할 딕셔너리는 다음과 같은 형태입니다.

        Examples:
            >>> data = {
            ...     "name": "context_name",
            ...     "lifespan": 1,
            ...     "ttl": 600,
            ...     "params": {
            ...         "key": {
            ...             "value": "value",
            ...             "resolvedValue": "resolved_value"
            ...         }
            ...     }
            ... }

        Args:
            data (dict): 변환할 딕셔너리

        Returns:
            Context: 변환된 Context 객체
        """
        name = data.get("name", "")
        lifespan = data.get("lifespan", "")
        ttl = data.get("ttl", None)
        params = {
            key: ContextParam.from_dict(value)
            for key, value in data.get("params", {}).items()
        }
        return cls(name, lifespan, ttl, params)

    def render(self) -> Dict:
        """Context 객체를 카카오톡 응답 규칙에 맞게 딕셔너리로 변환합니다.

        params에 있는 ContextParam 객체는 render 메서드를 통해 value 값을 반환합니다.
        만약, params에 ContextParam 객체가 아닌 다른 객체가 들어있을 경우, 그대로 반환합니다.
        반환되는 딕셔너리는 다음과 같은 형태입니다.

        Examples:
            >>> self.render()
            ... {
            ...     "name": "context_name",
            ...     "lifespan": 1,
            ...     "ttl": 600,
            ...     "params": {
            ...         "key": "value"
            ...     }
            ... }

        Returns:
            dict: Context 객체를 변환한 딕셔너리
        """
        response = {
            "name": self.name,
            "lifeSpan": self.lifespan,
            "ttl": self.ttl,
            "params": {
                key: param.render() if isinstance(param, ContextParam) else param
                for key, param in self.params.items()
            } if self.params else None
        }
        return self.remove_none_item(response)

    def validate(self):
        """Context 객체의 유효성을 검사합니다.

        Raises:
            InvalidTypeError: name이 str이 아닐 경우 발생합니다.
            InvalidTypeError: lifespan이 int가 아닐 경우 발생합니다.
            InvalidTypeError: ttl이 int가 아닐 경우 발생합니다.
            InvalidTypeError: params가 dict가 아닐 경우 발생합니다.
        """
        validate_str(self.name)
        validate_int(self.lifespan, self.ttl)
        validate_type(dict, self.params)


class ContextParam(ParentPayload, SkillTemplate):
    """컨텍스트의 Param 정보를 담는 클래스입니다.

    컨텍스트의 Param 정보는 컨텍스트 정보에 추가적인 정보를 담을 때 사용됩니다.
    Payload에 담겨지는 컨텍스트 정보의 Params는 Stringfy된 JSON 형태로 전달됩니다.
    이떄, `{key : {"value" : value, "resolved_value" : resolved_value}}` 형태로 전달됩니다.
    이후 `Response`에서는 `[key : value]` 형태로 전달해야합니다.
    이 클래스는 이러한 특성에 맞게, `value`와 `resolved_value`를 가지도록 정의됩니다.
    또한, `render()` 메서드를 통해 `value` 값 만을 반환하도록 정의됩니다.

    Args:
        value (str): 컨텍스트의 Param의 value
        resolved_value (str): 컨텍스트의 Param의 resolved_value

    Attributes:
        value (str): 컨텍스트의 Param의 value
        resolved_value (str): 컨텍스트의 Param의 resolved_value

    Examples:
        >>> context_param = ContextParam(
        ...     value="value_str",
        ...     resolved_value="resolved_value"
        ... )
        >>> context_param.render()
        "value_str"
    """

    def __init__(self, value: str, resolved_value: str):
        """ContextParam 객체를 초기화합니다."""
        self.value = value
        self.resolved_value = resolved_value

    @classmethod
    def from_dict(cls, data: dict) -> 'ContextParam':
        """딕셔너리를 ContextParam 객체로 변환합니다.

        변환할 딕셔너리는 다음과 같은 형태입니다.

        Examples:
            >>> data = {
            ...     "value": "value",
            ...     "resolvedValue": "resolved_value"
            ... }

        Args:
            data (dict): 변환할 딕셔너리

        Returns:
            ContextParam: 변환된 ContextParam 객체
        """
        value = data.get("value", "")
        resolved_value = data.get("resolvedValue", "")
        return cls(value, resolved_value)

    def render(self) -> str:  # type: ignore
        """ContextParam 객체의 value를 반환합니다.

        이 패키지의 다른 클래스들과 달리, ContextParam 객체는 value만을 반환해야 합니다.
        이는 ContextParam 객체의 특성에 맞게, value 값만을 반환하기 위함입니다

        Returns:
            str: ContextParam 객체의 value

        Examples:
            >>> context_param = ContextParam(
            ...     value="value_str",
            ...     resolved_value="resolved_value"
            ... )
            >>> context_param.render()
            "value_str"
        """
        self.validate()
        return self.value

    def validate(self):
        """ContextParam 객체의 유효성을 검사합니다.

        Raises:
            InvalidTypeError: value가 str이 아닐 경우 발생합니다.
            InvalidTypeError: resolved_value가 str이 아닐 경우 발생합니다.
        """
        validate_str(self.value, self.resolved_value)
