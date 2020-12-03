""" Enhanced functions for list. This enhanced list is
    strictly typed """

from typing import Generic, TypeVar, Iterable, List

# generics datatype
T = TypeVar("T")

class EnhancedList(list, Generic[T]):
    """ extends list of a gerneric type """

    def __init__(self, *args:Iterable[T]):
        """ create a list type """
        list.__init__(self, *args)

    def __getitem__(self, key):
        """ receive one or multiple elements from list.
        If the key argument is of type "list" then this
        function returns a EnhancedList, the stored value else

        Arguments:
            key: int, List[int] or List[List[int]]

        Returns:
            value: EnhancedList or EnhancedList element
        """
        if isinstance(key, list):
            return EnhancedList([self[i] for i in key])
        else:
            return list.__getitem__(self,key)

    def reject_indices(self, indices: List[int]) -> EnhancedList:
        """ remove the elements utilizing a list

        Arguments:
            indices: List[int]

        Returns:
            list without rejected elements: EnhancedList
        """
        tmp_list = []
        for i, elem in enumerate(indices):
            if i not in indices:
                tmp_list.append(elem)

        return EnhancedList(tmp_list)
