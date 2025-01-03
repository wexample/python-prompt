from enum import Enum


class ResponseType(Enum):
    PLAIN = "plain"
    TABLE = "table"
    LIST = "list"
    TREE = "tree"
    PROGRESS = "progress"
