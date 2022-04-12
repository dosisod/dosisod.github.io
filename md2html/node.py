from dataclasses import dataclass, field
from typing import List


@dataclass(kw_only=True)
class Node:
    contents: str = ""


@dataclass(kw_only=True)
class CommentNode(Node):
    pass


@dataclass(kw_only=True)
class DataNode(Node):
    data: List[str] = field(default_factory=list)


@dataclass(kw_only=True)
class ListNode(DataNode):
    pass


@dataclass(kw_only=True)
class BulletNode(ListNode):
    pass


@dataclass(kw_only=True)
class NumListNode(ListNode):
    pass


@dataclass(kw_only=True)
class CheckboxNode(Node):
    checked: bool


@dataclass(kw_only=True)
class TextNode(Node):
    pass


@dataclass(kw_only=True)
class CodeblockNode(DataNode):
    pass


@dataclass(kw_only=True)
class PythonNode(Node):
    pass


@dataclass(kw_only=True)
class HtmlNode(Node):
    pass


@dataclass(kw_only=True)
class HeaderNode(Node):
    level: int = 1


@dataclass(kw_only=True)
class NewlineNode(Node):
    contents: str = ""


@dataclass(kw_only=True)
class BlockquoteNode(Node):
    pass
