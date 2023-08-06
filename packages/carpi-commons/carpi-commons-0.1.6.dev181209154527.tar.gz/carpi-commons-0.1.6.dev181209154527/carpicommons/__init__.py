"""
CARPI COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

"""
CARPI DASH DAEMON
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from datetime import datetime, timedelta


class ExpiringDictionary(dict):
    def __init__(self, timeout=5.0, **kwargs):
        super().__init__(**kwargs)
        self._add_times = {}
        self._timeout: float = timeout

    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        self._timeout = value

    def __getitem__(self, key):
        if self.has_item_expired(key):
            # This will intentionally remove an item from the dict
            # and then raise an a KeyError because expired items
            # should not exist!
            self.__delitem__(key)

        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._add_times[key] = datetime.now()

    def __delitem__(self, v) -> None:
        super().__delitem__(v)
        del self._add_times[v]

    def get(self, key, default=None):
        try:
            self.__getitem__(key)
        except KeyError:
            return default

    def run_cleanup(self):
        remove_keys = []
        max_dif = timedelta(seconds=self._timeout)
        for key, time in self._add_times:
            if datetime.now() - time > max_dif:
                remove_keys.append(key)

        for key in remove_keys:
            self.__delitem__(key)

    def get_insertion_datetime(self, key) -> datetime:
        """
        Returns the date and time of the insertion of the given key.
        Returns `datetime.min` if the item doesn't exist
        """
        return self._add_times.get(key, datetime.min)

    def get_age(self, key) -> timedelta:
        """
        Returns the age of a given item
        """
        return datetime.now() - self.get_insertion_datetime(key)

    def has_item_expired(self, key) -> bool:
        """
        Returns `true` if an item has been persisted longer than <timeout> seconds ago.
        Returns `true` if an item doesn't exist.
        """
        return self.get_age(key) > timedelta(seconds=self._timeout)
