"""카카오톡 출력 요소 Card 관련 클래스를 정의한 모듈입니다.

카카오톡 출력 요소 Card는 텍스트, 이미지, 버튼 등을 포함하는 카드 컴포넌트입니다.

Classes:
    - TextCardComponent: 카카오톡 출력 요소 TextCard의 객체를 생성하는 클래스
    - BasicCardComponent: 카카오톡 출력 요소 BasicCard의 객체를 생성하는 클래스
    - CommerceCardComponent: 카카오톡 출력 요소 CommerceCard의 객체를 생성하는 클래스
    - ListCardComponent: 카카오톡 출력 요소 ListCard의 객체를 생성하는 클래스
    - ItemCardComponent: 카카오톡 출력 요소 ItemCard의 객체를 생성하는 클래스
"""

from abc import ABCMeta, abstractmethod
from typing import Optional, overload, Union, List, Dict


from ..base import ParentComponent
from .common import Button, Link, ListItem, Profile, Thumbnail
from ..interaction import ActionEnum
from .itemcard import ImageTitle, Item, ItemListSummary, ItemProfile, ItemThumbnail
from ...validation import validate_int, validate_str, validate_type

__all__ = [
    "TextCardComponent",
    "BasicCardComponent",
    "CommerceCardComponent",
    "ListCardComponent",
    "ItemCardComponent",
]


class ParentCardComponent(ParentComponent, metaclass=ABCMeta):
    """Component 출력 요소중 Card 종류의 부모 클래스입니다.

    Card 출력 요소는 TextCardComponent, BasicCardComponent,
    CommerceCardComponent, ListCardComponent, ItemCardComponent가 있습니다.
    이 클래스는 Card 출력 요소의 공통 속성과 메서드를 정의합니다.
    주로 Button 객체를 조작하는 메서드를 제공합니다.

    Attributes:
        buttons (list[Button], optional): 버튼 객체입니다.
    """

    def __init__(self, buttons: Optional[List[Button]] = None):
        """ParentCard 객체를 생성합니다.

        buttons가 None인 경우 빈 리스트로 초기화합니다.

        Args:
            buttons (Optional[list[Button]], optional): 버튼 객체.
        """
        if buttons is None:
            buttons = []
        self.buttons = buttons

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        Raises:
            InvalidTypeError: 받거나 생성한 Button 객체가 Button이 아닌 경우
        """
        super().validate()
        if self.buttons:
            for button in self.buttons:
                validate_type(Button, button)

    @overload
    def add_button(self, button: Button) -> "ParentCardComponent": ...

    @overload
    def add_button(
        self,
        label: str,
        action: Union[str, ActionEnum],
        web_link_url: Optional[str] = None,
        message_text: Optional[str] = None,
        phone_number: Optional[str] = None,
        block_id: Optional[str] = None,
        extra: Optional[Dict] = None
    ) -> "ParentCardComponent": ...

    def add_button(self, *args, **kwargs) -> "ParentCardComponent":
        """버튼을 추가합니다.

        Button 객체 또는 Button 생성 인자를 받아 버튼 리스트에 추가합니다.

        Args:
            *args (Button | str | ActionEnum | Dict[str, Any]): 추가할 Button 객체 또는 Button 생성 인자.
                - Button 객체를 직접 전달할 수 있습니다.
                - Button 생성에 필요한 인자들을 전달할 수 있습니다.
            **kwargs (Any): Button 생성 인자.
                - label (str): 버튼에 적히는 문구입니다.
                - action (str | ActionEnum): 버튼 클릭 시 수행될 작업입니다. ('message', 'block', 등)
                - web_link_url (Optional[str]): 웹 브라우저를 열고 이동할 주소입니다. (action이 'webLink'일 경우 필수)
                - message_text (Optional[str]): action이 'message'인 경우 사용자 측으로 발화될 텍스트입니다.
                - phone_number (Optional[str]): action이 'phone'일 경우 전화번호입니다.
                - block_id (Optional[str]): action이 'block'일 경우 호출할 block의 ID입니다.
                - extra (Optional[dict]): 스킬 서버에 추가로 전달할 데이터입니다.

        Returns:
            ParentCardComponent: Button 객체가 추가된 ParentCardComponent 객체.

        Raises:
            InvalidTypeError: 받거나 생성한 Button 객체가 Button이 아닌 경우.
        """
        if len(args) == 1 and isinstance(args[0], Button):
            self.buttons.append(args[0])
        elif len(args) == 0 and "button" in kwargs:
            self.buttons.append(kwargs["button"])
        else:
            button = Button(*args, **kwargs)
            self.buttons.append(button)
        return self

    def remove_button(self, button: Button):
        """버튼을 제거합니다.

        Button 객체를 받아 버튼 리스트에서 제거합니다.

        Parameters:
            button: 제거할 버튼 객체
        """
        self.buttons.remove(button)

    @abstractmethod
    def render(self): ...


class TextCardComponent(ParentCardComponent):
    """카카오톡 출력 요소 TextCard의 객체를 생성하는 클래스입니다.

    TextCardComponent는 제목과 설명을 출력하는 요소입니다.
    텍스트 카드는 간단한 텍스트에 버튼을 추가하거나, 텍스트를 케로셀형으로 전달하고자 할 때 사용됩니다.
    title과 description 중 최소 하나는 None이 아니어야 합니다.

    Args:
        title (Optional[str], optional): 카드 제목. Defaults to None.
        description (Optional[str], optional): 카드 설명. Defaults to None.
        buttons (Optional[list[Button]], optional): 버튼 리스트. Defaults to None.

    Examples:
        >>> text_card = TextCardComponent(title="제목", description="설명")
        >>> text_card.add_button(
                label="버튼 1", action="message", message_text="버튼 1 클릭"
            )
        >>> text_card.render()
        {
            "title": "제목",
            "description": "설명",
            "buttons": [
                {
                    "label": "버튼 1",
                    "action": "message",
                    "messageText": "버튼 1 클릭"
                }
            ]
        }
    """

    name = "textCard"

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        buttons: Optional[List[Button]] = None,
    ):
        """TextCardComponent 객체를 생성합니다.

        title과 description 중 최소 하나는 None이 아니어야 합니다.

        Args:
            title (Optional[str], optional): 카드의 제목.
            description (Optional[str], optional): 카드 상세 설명.
            buttons (Optional[list[Button]], optional): 카드의 버튼들.
        """
        super().__init__(buttons=buttons)
        self.title = title
        self.description = description

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        title과 description 중 최소 하나는 None이 아니어야 합니다.

        raise:
            ValueError: title과 description 중 최소 하나는 None이 아니어야 합니다.
        """
        super().validate()
        if self.title is None and self.description is None:
            raise ValueError(
                "title과 description 중 최소 하나는 None이 아니어야 합니다."
            )
        if self.title is None:
            validate_str(self.description)
        else:
            validate_str(self.title)

    def render(self):
        """객체의 응답 내용을 반환합니다.

        TextCardComponent 객체의 응답 내용을 반환합니다.
        이 응답 내용을 이용하여 render() 메서드에서 최종 응답을 생성합니다.

        Returns:
            dict: 응답 내용

        Examples:
            >>> self.render()
            {
                "title": "제목", # 제목이 없을 경우 미표시
                "description": "설명", # 설명이 없을 경우 미표시
                "buttons": buttons.get_response_content()
            }
        """
        self.validate()
        response = {
            "title": self.title,
            "description": self.description,
            "buttons": (
                [button.render() for button in self.buttons] if self.buttons else None
            ),
        }
        return self.remove_none_item(response)


class BasicCardComponent(ParentCardComponent):
    """카카오톡 출력 요소 BasicCard의 객체를 생성하는 클래스입니다.

    BasicCardComponent는 소셜, 썸네일, 프로필 등을 통해서 사진이나 글, 인물 정보 등을 공유할 수 있습니다.
    제목과 설명 외에 썸네일 그룹, 프로필, 버튼 그룹, 소셜 정보를 추가로 포함합니다.
    Thumbnail 객체는 반드시 포함되어야 합니다. 제목과 설명만 있는 TextCardComponent와의 차이점입니다.

    Args:
        thumbnail (Thumbnail): 카드의 상단 이미지
        title (Optional[str] optional): 카드 제목. Defaults to None.
        description (Optional[str] optional): 카드 상세 설명. Defaults to None.
        buttons (Optional[list[Button]], optional): 버튼 리스트. Defaults to None.

    Examples:
        >>> basic_card = BasicCardComponent(
        ...     thumbnail=Thumbnail(
        ...         image_url="https://example.com/image.jpg",
        ...         link=Link(web="https://example.com")
        ...     ),
        ...     title="제목",
        ...     description="설명"
        ... )
        >>> basic_card.add_button(
        ...     label="버튼 1", action="message", message_text="버튼 1 클릭"
        ... )
        >>> basic_card.render()
        {
            "thumbnail": {
                "imageUrl": "https://example.com/image.jpg",
                "link": {
                    "web": "https://example.com"
                }
            },
            "title": "제목",
            "description": "설명",
            "buttons": [
                {
                    "label": "버튼 1",
                    "action": "message",
                    "messageText": "버튼 1 클릭"
                }
            ]
        }
    """

    name = "basicCard"

    def __init__(
        self,
        thumbnail: Thumbnail,
        title: Optional[str] = None,
        description: Optional[str] = None,
        buttons: Optional[List[Button]] = None,
        forwardable: bool = False,
    ):
        """BasicCardComponent 객체를 생성합니다.

        Args:
            thumbnail (Thumbnail): 카드의 상단 이미지
            title (str, optional): 카드 제목. Defaults to None.
            description (str optional): 카드 상세 설명. Defaults to None.
            buttons (list[Button], optional): 버튼 리스트. Defaults to None.
            forwardable (bool, optional): 공유하기 버튼 표시 여부. Defaults to False.
        """
        super().__init__(buttons=buttons)
        self.thumbnail = thumbnail
        self.title = title
        self.description = description
        self.forwardable = forwardable

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        Thumbnail 객체는 반드시 포함되어야 합니다.
        제목과 설명은 문자열이어야 합니다.

        raise:
            InvalidTypeError: Thumbnail 객체가 Thumbnail이 아닌 경우
            ValueError: title과 description이 문자열이 아니어야 합니다.
        """
        super().validate()
        validate_type(Thumbnail, self.thumbnail)
        validate_str(self.title, self.description)

    def render(self):
        """객체의 응답 내용을 반환합니다.

        BasicCard 객체의 응답 내용을 반환합니다.

        Examples:
            >>> self.render()
            {
                "thumbnail": thumbnail.get_response_content(),
                "title": "제목",
                "description": "설명",
                "buttons": buttons.get_response_content(),
                "forwardable": True
            }

        Returns:
            dict: 응답 내용
        """
        self.validate()
        response = {
            "thumbnail": self.thumbnail.render(),
            "title": self.title,
            "description": self.description,
            "buttons": (
                [button.render() for button in self.buttons] if self.buttons else None
            ),
            "forwardable": self.forwardable if self.forwardable else None,
        }
        return self.remove_none_item(response)


class CommerceCardComponent(ParentCardComponent):
    """카카오톡 출력 요소 CommerceCard의 객체를 생성하는 클래스입니다.

    CommerceCardComponent는 제품에 대한 소개, 구매 안내 등을 사용자에게 전달할 수 있습니다.
    커머스 카드는 제목과 설명 외에 썸네일 그룹, 프로필, 버튼 그룹, 가격 정보를 추가로 포함합니다.

    discountedPrice 가 존재하면 price, discount, discountRate 과 관계 없이
    무조건 해당 값이 사용자에게 노출됩니다.
    discountRate은 discountedPrice를 필요로 합니다.
    discountedPrice가 주어지지 않으면 사용자에게 >discountRate을 노출하지 않습니다.
    discountRate과 discount가 동시에 있는 경우, discountRate을 우선적으로 노출합니다.

    Examples:
        >>> commerce_card = CommerceCardComponent(
        ...     price=10999,
        ...     thumbnails=[
        ...         Thumbnail(image_url="https://example.com/image1.jpg"),
        ...     ],
        ...     title="커머스 카드",
        ...     description="커머스 카드 설명",
        ...     buttons=[
        ...             Button(
        ...                 label="구매하기", action="webLink",
        ...                 web_link_url="https://example.com")
        ...         ]
        ...     ),
        ...     profile=Profile(
        ...         nickname="제품 이름",
        ...         image_url="https://example.com/image.jpg"
        ...     ),
        ...     currency="won",
        ...     discount=1000,
        ...     discount_rate=10,
        ...     discount_price=9000
        ... )
        >>> commerce_card.render()
        {
            "price": 10999,
            "thumbnails": {
                "thumbnails": [
                    {
                        "imageUrl": "https://example.com/image1.jpg"
                    }
                ]
            },
            "title": "커머스 카드",
            "description": "커머스 카드 설명",
            "currency": "won",
            "discount": "1000",
            "discountRate": "10",
            "discountPrice": "9000",
            "profile": {
                "nickname": "제품 이름",
                "imageUrl": "https://example.com/image.jpg"
            },
            "buttons": {
                "buttons": [
                    {
                        "label": "구매하기",
                        "action": "webLink",
                        "webLinkUrl": "https://example.com"
                    }
                ]
            }
        }

    Attributes:
        price (int): 제품 가격
        thumbnails (list[Thumbnail]): 제품에 대한 사진(현재는 1개만 지원)
        title (Optional[str], optional): 제품의 이름. Defaults to None.
        description (Optional[str], optional): 제품에 대한 상세 설명. Defaults to None.
        buttons (Optional[list[Button]], optional): 버튼 리스트. Defaults to None.
        profile (Optional[Profile], optional): 제품을 판매하는 프로필. Defaults to None.
        currency (Optional[str], optional): 제품을 가격의 통화(현재는 won만 가능).
            Defaults to None.
        discount (Optional[str], optional): 제품의 가격에 대한 할인할 금액.
            Defaults to None.
        discount_rate (Optional[str], optional): 제품의 가격에 대한 할인율.
            Defaults to None.
        discount_price (Optional[str], optional): 제품의 가격에 대한 할인가(할인된 가격).
            discountRate을 쓰는 경우 필수.
            Defaults to None.


    """

    name = "commerceCard"

    def __init__(
        self,
        price: int,
        thumbnails: Union[List[Thumbnail], Thumbnail],
        title: Optional[str] = None,
        description: Optional[str] = None,
        buttons: Optional[List[Button]] = None,
        profile: Optional[Profile] = None,
        currency: Optional[str] = None,
        discount: Optional[int] = None,
        discount_rate: Optional[int] = None,
        discount_price: Optional[int] = None,
    ):
        """CommerceCardComponent 객체를 생성합니다."""
        super().__init__(buttons=buttons)
        self.price = price
        if isinstance(thumbnails, Thumbnail):
            thumbnails = [thumbnails]
        self.thumbnails = thumbnails
        self.title = title
        self.description = description
        self.currency = currency
        self.discount = discount
        self.discount_rate = discount_rate
        self.discount_price = discount_price
        self.profile = profile

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        raise:
            ValueError: price가 int가 아닌 경우
            ValueError: title, description이 문자열이 아닌 경우
            AssertionError: currency가 "won"이 아닌 경우
            ValueError: discount, discount_price, discount_rate가 int가 아닌 경우
            InvalidTypeError: thumbnails의 각 요소가 Thumbnail이 아닌 경우
            InvalidTypeError: profile이 Profile이 아닌 경우
        """
        super().validate()
        validate_int(self.price, disallow_none=True)
        for thumbnail in self.thumbnails:
            validate_type(Thumbnail, thumbnail)
        validate_str(self.title, self.description)
        if self.currency:
            assert self.currency == "won"
        validate_int(
            self.discount, self.discount_price, self.discount_rate, self.discount_price
        )
        validate_type(Profile, self.profile)

    def render(self) -> Dict:
        """객체의 응답 내용을 반환합니다.

        CommerceCardComponent 객체의 응답 내용을 반환합니다.
        None인 속성은 미표시됩니다.

        Returns:
            dict: 응답 내용

        Examples:
            >>> self.render()
            {
                "price": 10999,
                "thumbnails": [
                    thumbnail.render() for thumbnail in self.thumbnails
                ],
                "title": "커머스 카드",
                "description": "커머스 카드 설명",
                "currency": "won",
                "discount": 1000,
                "discountRate": 10,
                "discountPrice": 9000,
                "profile": profile.render(),
                "buttons": [button.render() for button in self.buttons]
            }
        """
        self.validate()
        response = {
            "price": self.price,
            "thumbnails": [thumbnail.render() for thumbnail in self.thumbnails],
            "title": self.title,
            "description": self.description,
            "currency": self.currency,
            "discount": self.discount,
            "discountRate": self.discount_rate,
            "discountPrice": self.discount_price,
            "profile": self.profile.render() if self.profile else None,
            "buttons": (
                [button.render() for button in self.buttons] if self.buttons else None
            ),
        }
        return self.remove_none_item(response)


class ListCardComponent(ParentCardComponent):
    """카카오톡 출력 요소 ListCard의 객체를 생성하는 클래스입니다.

    ListCardComponent는 헤더와 아이템을 포함하며, 헤더는 리스트 카드의 상단에 위치합니다.
    리스트 상의 아이템은 각각의 구체적인 형태를 보여주며, 제목과 썸네일, 상세 설명을 포함합니다.
    header는 ListItem 객체이어야 하지만, str으로 입력받을 경우 ListItem으로 변환됩니다.

    Examples:
        >>> list_card = ListCardComponent(
        ...     header="리스트 카드"
        ... )
        >>> list_card.add_item(
        ...     ListItem(
        ...         title="아이템 1",
        ...         description="아이템 1 설명",
        ...         image_url="https://example.com/image1.jpg"
        ...     )
        ... )
        >>> list_card.render()
        {
            "header": {
                "title": "리스트 카드"
            },
            "items": [
                {
                    "title": "아이템 1",
                    "description": "아이템 1 설명",
                    "imageUrl": "https://example.com/image1.jpg"
                }
            ]
        }

    Attributes:
        header (ListItem): 리스트 카드의 헤더
        items (ListItems): 리스트 카드의 아이템들
        max_buttons (int): 버튼 최대 개수. Defaults to 2.
        max_items (int): 아이템 최대 개수. Defaults to 5.
            ListCardComponent가 Carousel로 나타나는 경우 최대 4개로 제한되어 있기 때문에,
            값을 4로 수정해야 합니다.
    """

    name = "listCard"

    def __init__(
        self,
        header: Union[ListItem, str],
        items: Optional[List[ListItem]] = None,
        buttons: Optional[List[Button]] = None,
        max_buttons: int = 2,
        max_items: int = 5,
    ):
        """ListCard 객체를 생성합니다.

        Args:
            header (Union[ListItem, str]): 리스트 카드의 상단 항목 str인 경우 ListItem으로 변환됩니다.
            items (ListItems): 리스트 카드의 각각 아이템
            buttons (Optional[list[Button]], optional): 리스트 카드의 버튼들.
                                                    Defaults to None.
            max_buttons (int, optional): 버튼 최대 개수. Defaults to 2.
            max_items (int, optional): 아이템 최대 개수. Defaults to 5.
        """
        super().__init__(buttons=buttons)
        if isinstance(header, str):
            self.header = ListItem(title=header)
        else:
            self.header = header
        if items is None:
            items = []
        self.items = items
        self.max_buttons = max_buttons
        self.max_items = max_items

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        raise:
            InvalidTypeError: header가 ListItem이 아닌 경우
            AssertionError: items가 비어있는 경우
            InvalidTypeError: items가 ListItems가 아닌 경우
        """
        super().validate()
        if len(self.items) < 1:
            raise AssertionError(
                "ListCardComponent는 최소 1개의 아이템을 포함해야 합니다."
            )
        if len(self.items) > self.max_items:
            raise AssertionError(
                f"ListCard는 최대 {self.max_items}개의 아이템을 포함할 수 있습니다."
            )
        if len(self.buttons) > self.max_buttons:
            raise AssertionError(
                f"ListCard는 최대 {self.max_buttons}개의 버튼을 포함할 수 있습니다."
            )
        validate_type(ListItem, self.header, disallow_none=True)
        validate_type(ListItem, *self.items)

    def render(self):
        """객체의 응답 내용을 반환합니다.

        ListCardComponent 객체의 응답 내용을 반환합니다.
        이 응답 내용을 이용하여 render() 메서드에서 최종 응답을 생성합니다.

        Examples:
            >>> self.render()
            {
                "header": header.get_response_content(),
                "items": items.get_response_content(),
                "buttons": buttons.get_response_content()
            }

        Returns:
            dict: 응답 내용
        """
        self.validate()
        response = {
            "header": self.header.render(),
            "items": ([item.render() for item in self.items] if self.items else None),
            "buttons": (
                [button.render() for button in self.buttons] if self.buttons else None
            ),
        }
        return self.remove_none_item(response)

    @overload
    def add_item(
        self,
        title: str,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        link: Optional[Link] = None,
        action: Optional[Union[str, ActionEnum]] = None,
        block_id: Optional[str] = None,
        message_text: Optional[str] = None,
        extra: Optional[Dict] = None
    ) -> "ListCardComponent": ...

    @overload
    def add_item(self, item: ListItem) -> "ListCardComponent": ...

    def add_item(self, *args, **kwargs) -> "ListCardComponent":
        """ListCardComponent에 아이템을 추가합니다.

        ListItem 객체 또는 ListItem 생성 인자를 받아 아이템 리스트에 추가합니다.

        Args:
            *args: ListItem 생성 인자 또는 ListItem 객체
            **kwargs: ListItem 생성 인자 또는 ListItem 객체

        Returns:
            ListCardComponent: ListItem이 추가된 객체
        """
        if len(args) == 1 and isinstance(args[0], ListItem):
            self.items.append(args[0])
        elif len(args) == 0 and "item" in kwargs:
            self.items.append(kwargs["item"])
        else:
            item = ListItem(*args, **kwargs)
            self.items.append(item)
        return self

    def remove_item(self, item: ListItem) -> "ListCardComponent":
        """ListCardComponent에서 아이템을 제거합니다.

        Args:
            item (ListItem): 제거할 ListItem 객체
        """
        assert isinstance(item, ListItem)
        if item not in self.items:
            raise ValueError("해당 아이템이 존재하지 않습니다.")
        self.items.remove(item)

        return self


class ItemCardComponent(ParentCardComponent):
    """카카오톡 출력 요소 ItemCard의 객체를 생성하는 클래스입니다.

    ItemCardComponent는 메시지 목적에 따른 유관 정보들을 (가격 정보 포함)
    사용자에게 일목요연한 리스트 형태로 전달할 수 있습니다.
    ItemCardComponent는 아이템리스트, 제목, 설명 외에
    썸네일, 프로필, 헤드, 이미지타이틀, 버튼 그룹을 추가로 포함합니다.

    Examples:
        >>> item_card = ItemCardComponent(
        ...     item_list=[
        ...         Item(title="아이템 1", description="아이템 1 설명"),
        ...         Item(title="아이템 2", description="아이템 2 설명")
        ...     ],
        ...     thumbnail=ItemThumbnail(
        ...         image_url="https://example.com/image.jpg"
        ...     ),
        ...     head="헤드",
        ...     profile=ItemProfile(
        ...         title="프로필",
        ...         image_url="https://example.com/image.jpg"
        ...     ),
        ...     image_title=ImageTitle(
        ...         title="이미지 타이틀",
        ...         description="이미지 타이틀 설명",
        ...         image_url="https://example.com/image.jpg"
        ...     ),
        ...     item_list_alignment="left",
        ...     item_list_summary=ItemListSummary(
        ...         price=10000
        ...     ),
        ...     title="타이틀",
        ...     description="설명",
        ...     buttons=[
        ...         Button(
        ...             label="버튼 1",
        ...             action="message",
        ...             message_text="버튼 1 클릭"
        ...         )
        ...     ],
        ...     button_layout="vertical"
        ... )
        >>> item_card.render()
        {
            "thumbnail": {
                "imageUrl": "https://example.com/image.jpg"
            },
            "head": {
                "title": "헤드"
            },
            "profile": {
                "title": "프로필",
                "imageUrl": "https://example.com/image.jpg"
            },
            "imageTitle": {
                "title": "이미지 타이틀",
                "description": "이미지 타이틀 설명",
                "imageUrl": "https://example.com/image.jpg"
            },
            "itemList": [
                {
                    "title": "아이템 1",
                    "description": "아이템 1 설명"
                },
                {
                    "title": "아이템 2",
                    "description": "아이템 2 설명"
                }
            ],
            "itemListAlignment": "left",
            "itemListSummary": {
                "price": 10000
            },
            "title": "타이틀",
            "description": "설명",
            "buttonLayout": "vertical",
            "buttons": [
                {
                    "label": "버튼 1",
                    "action": "message",
                    "messageText": "버튼 1 클릭"
                }
            ]
        }

    Attributes:
        item_list (list[Item]): Item 객체들이 포함된 리스트
        thumbnail (ItemThumbnail): 상단 이미지
            - 단일형: 이미지 비율 2:1 (800*400), 1:1 (800*800)사용 가능
            - 케로셀형: 이미지 비율 2:1 (800*400)만 사용 가능
        head (str): 헤드 정보입니다. 프로필과 함께 사용할 수 없습니다.
        profile (ItemProfile): 프로필 정보. 헤드와 함께 사용할 수 없습니다.
        image_title (ImageTitle): 이미지를 동반하는 제목 및 설명 정보입니다.
            이미지 우측 정렬 고정 (위치 변경 불가)
        item_list_alignment (str): itemList 및 itemListAlignment 정렬 정보입니다.
            (left, right 중 선택)
        item_list_summary (ItemListSummary): 아이템 가격 정보입니다.
            사용시 item_list_alignment는 right 권장.
        title (str): 타이틀 정보. description을 넣는 경우, title이 필수입니다.
        description (str): 설명. 사용시 title이 필수입니다.
        button_layout (str): 버튼 정렬 정보. 단일형에서만 사용 가능.
            (vertical, horizontal 중 선택)
            미입력시 자동 선택
        buttons (Optional[list[Button]], optional): 버튼 리스트. Defaults to None.
            - 단일형: 최대 3개까지 사용 가능
            - 케로셀형: 최대 2개까지 사용 가능
    """

    name = "itemCard"

    def __init__(
        self,
        item_list: List[Item],
        thumbnail: Optional[ItemThumbnail] = None,
        head: Optional[str] = None,
        profile: Optional[ItemProfile] = None,
        image_title: Optional[ImageTitle] = None,
        item_list_alignment: Optional[str] = None,
        item_list_summary: Optional[ItemListSummary] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        buttons: Optional[List[Button]] = None,
        button_layout: Optional[str] = None,
    ):
        """ItemCardComponent 객체를 생성합니다.

        Args: class Docstring 참고
        """
        super().__init__(buttons=buttons)
        self.item_list = item_list
        self.thumbnail = thumbnail
        self.head = head
        self.profile = profile
        self.image_title = image_title
        self.item_list_alignment = item_list_alignment
        self.item_list_summary = item_list_summary
        self.title = title
        self.description = description
        self.button_layout = button_layout

    def validate(self):
        """객체가 카카오톡 출력 요소에 맞는지 확인합니다.

        raise:
            InvalidTypeError: item_list의 각 요소가 Item이 아닌 경우
            InvalidTypeError: thumbnail가 ItemThumbnail 아닌 경우
            InvalidTypeError: head가 Head가 아닌 경우
            InvalidTypeError: profile가 ItemProfile이 아닌 경우
            InvalidTypeError: image_title가 ImageTitle이 아닌 경우
            InvalidTypeError: item_list_summary가 ItemListSummary이 아닌 경우
            ValueError: title, description, button_layout이 문자열이 아닌 경우
        """
        super().validate()
        for item in self.item_list:
            validate_type(Item, item)
        validate_type(ItemThumbnail, self.thumbnail)
        validate_type(ItemProfile, self.profile)
        validate_type(ImageTitle, self.image_title)
        validate_type(ItemListSummary, self.item_list_summary)
        validate_str(self.head, self.title, self.description, self.button_layout)

    def render(self):
        """객체의 응답 내용을 반환합니다.

        ItemCardComponent 객체의 응답 내용을 반환합니다.
        이 응답 내용을 이용하여 render() 메서드에서 최종 응답을 생성합니다.
        None인 속성은 미반환 됩니다.

        Examples:
            >>> self.render()
            {
                "thumbnail": thumbnail.get_response_content(),
                "head": {"title": "헤드"},
                "profile": profile.get_response_content(),
                "imageTitle": image_title.get_response_content(),
                "itemList": [item.render() ...]
                "itemListAlignment": "left",
                "itemListSummary": item_list_summary.get_response_content(),
                "title": "타이틀",
                "description": "설명",
                "buttonLayout": "vertical",
                "buttons": buttons.get_response_content()
            }

        Returns:
            dict: 응답 내용
        """
        self.validate()
        assert self.item_list is not None

        response = {
            "thumbnail": self.thumbnail.render() if self.thumbnail else None,
            "head": {"title": self.head} if self.head else None,
            "profile": self.profile.render() if self.profile else None,
            "imageTitle": (self.image_title.render() if self.image_title else None),
            "itemList": [item.render() for item in self.item_list],
            "itemListAlignment": self.item_list_alignment,
            "itemListSummary": (
                self.item_list_summary.render() if self.item_list_summary else None
            ),
            "title": self.title,
            "description": self.description,
            "buttonLayout": self.button_layout,
            "buttons": (
                [button.render() for button in self.buttons] if self.buttons else None
            ),
        }
        return self.remove_none_item(response)

    @overload
    def add_item(self, item: Item): ...

    @overload
    def add_item(self, title: str, description: str): ...

    def add_item(self, *args, **kwargs):
        """아이템을 추가합니다.

        Item 객체 또는 Item 생성 인자를 받아 아이템 리스트에 추가합니다.

        Args:
            *args (Item | str): 추가할 Item 객체 또는 Item 생성 인자.
                - Item 객체를 직접 전달할 수 있습니다.
                - Item 생성에 필요한 인자들을 전달할 수 있습니다.
            **kwargs (Any): 추가할 Item 생성 인자.
                - item (Item): 추가할 Item 객체.
                - title (str): 아이템의 제목.
                - description (str): 아이템의 설명.

        Returns:
            ParentCardComponent: 아이템이 추가된 ParentCardComponent 객체.

        Raises:
            ValueError: Item 객체와 함께 다른 인자를 주는 경우.
            ValueError: `item` 키워드에 Item 객체가 아닌 것을 주거나,
                        `title` 또는 `description`이 누락된 경우.
        """
        if len(args) == 1:
            if isinstance(args[0], Item):
                self.item_list.append(args[0])
            elif "description" in kwargs:
                self.item_list.append(Item(*args, **kwargs))
        else:
            if "item" in kwargs:
                self.item_list.append(kwargs["item"])
            self.item_list.append(Item(*args, **kwargs))

    @overload
    def remove_item(self, item: Item): ...

    @overload
    def remove_item(self, index: int): ...

    def remove_item(self, *args, **kwargs):
        """아이템을 제거합니다.

        Item 객체 또는 인덱스를 받아 아이템 리스트에서 제거합니다.

        Args:
            *args (Item | int): 제거할 Item 객체 또는 아이템의 인덱스.
                - Item 객체를 직접 전달할 수 있습니다.
                - 아이템의 인덱스를 전달할 수 있습니다.
            **kwargs (Any): 제거할 Item 객체 또는 아이템의 인덱스를 키워드 인자로 전달할 수 있습니다.
                - `item` (Item): 제거할 Item 객체.
                - `index` (int): 제거할 아이템의 인덱스.

        Returns:
            SomeClass: 아이템이 제거된 `SomeClass` 객체.

        Raises:
            ValueError: Item 객체와 함께 다른 인자를 주는 경우.
            ValueError: `item` 키워드에 Item 객체가 아닌 것을 주거나,
                        `index` 키워드에 정수가 아닌 값을 주는 경우.
        """
        if isinstance(args[0], Item):
            self.item_list.remove(args[0])
        elif isinstance(args[0], int):
            self.item_list.pop(args[0])
        elif "item" in kwargs:
            self.item_list.remove(kwargs["item"])
        elif "index" in kwargs:
            self.item_list.pop(kwargs["index"])
