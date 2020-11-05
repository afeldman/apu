from typing import Generic, TypeVar, Iterable, List

T = TypeVar("T")

class EnhancedList(list, Generic[T]):

    def __init__(self, *args:Iterable[T]):
        list.__init__(self, *args)

    def __getitem__(self, key):
        if isinstance(key, list):
            return EnhancedList([self[i] for i in key])
        else:
            return list.__getitem__(self,key)

    def reject_indices(self, indices: List[int]) -> EnhancedList:
        tmp_list = []
        for i, elem in enumerate(indices):
            if i not in indices:
                tmp_list.append(elem)

        return EnhancedList(tmp_list)
