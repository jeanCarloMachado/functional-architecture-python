from typing import Generic, TypeVar, List

CommandData = TypeVar('CommandData')

class Command(Generic[CommandData]):
    def __init__(self, data: CommandData, timestamp, user_id):
        self.data = data
        self.timestap = timestamp
        self.user_id = user_id


ListMember = TypeVar('ListMember')
class NonEmptyList(Generic[ListMember]):
    def __init__(self, x: List[ListMember]):
        if not x:
            raise BaseException("List cannot be empty")
        self.value = x
