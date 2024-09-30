"""사용자 정의 예외를 처리하는 모듈입니다.

classes:
    - InvalidTypeError: 유효하지 않은 타입에 대한 예외를 처리하는 클래스
    - InvalidLinkError: Link 형식에 대한 예외를 처리하는 클래스
    - InvalidActionError: 유효하지 않은 action에 대한 예외를 처리하는 클래스
    - InvalidPayloadError: 유효하지 않은 payload에 대한 예외를 처리하는 클래스
"""


class InvalidTypeError(ValueError):
    """유효하지 않은 타입에 대한 예외를 처리하는 클래스입니다."""

    def __init__(self, message: str):
        """InvalidTypeError 인스턴스를 초기화합니다.

        Args:
            message (str): 오류를 설명하는 메시지.
        """
        super().__init__(message)


class InvalidLinkError(ValueError):
    """Link 형식에 대한 예외를 처리하는 클래스입니다."""

    def __init__(self, message: str):
        """InvalidLinkError 인스턴스를 초기화합니다.

        Args:
            message (str): 오류를 설명하는 메시지.
        """
        super().__init__(message)


class InvalidActionError(ValueError):
    """유효하지 않은 action에 대한 예외를 처리하는 클래스입니다."""

    def __init__(self, message: str):
        """InvalidActionError 인스턴스를 초기화합니다.

        Args:
            message (str): 오류를 설명하는 메시지.
        """
        super().__init__(message)


class InvalidPayloadError(ValueError):
    """유효하지 않은 payload에 대한 예외를 처리하는 클래스입니다."""

    def __init__(self, message: str):
        """InvalidPayloadError 인스턴스를 초기화합니다.

        Args:
            message (str): 오류를 설명하는 메시지.
        """
        super().__init__(message)
