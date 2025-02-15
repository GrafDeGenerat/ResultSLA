from datetime import time, timedelta


class SuperTime:
    """
    Class for storage and control SuperTime objects. /n
    Can compare, addit, subtract exemplars of class between them. /n
    """

    def __init__(self, time_or_seconds):
        self._time_or_seconds = time_or_seconds
        self._total_seconds = self.total_seconds

    @property
    def total_seconds(self) -> int:
        obj = self._time_or_seconds

        if isinstance(self._time_or_seconds, time):
            return obj.hour * 3600 + obj.minute * 60 + obj.second

        elif isinstance(obj, float):
            obj = timedelta(hours=obj).total_seconds()
            return int(obj)

        elif isinstance(obj, timedelta):
            return int(obj.total_seconds())

        elif isinstance(obj, int):
            return obj * 3600  # int at seconds

        elif isinstance(obj, SuperTime):
            return obj.total_seconds

        else:
            raise TypeError

    @staticmethod
    def __check_type(self_class, obj):
        if isinstance(obj, type(self_class)):
            return obj.total_seconds

        if isinstance(obj, int):
            return obj
        raise TypeError(f"{obj} is not of type {self_class.__class__.__name__} or int")

    def __repr__(self):
        h = self.total_seconds // 3600
        m = (self.total_seconds % 3600) // 60
        s = (self.total_seconds % 3600) % 60
        return f"{h:02}:{m:02}:{s:02}"

    def __sub__(self, other):
        if isinstance(other, int):
            cur: int = self.total_seconds
            return timedelta(seconds=cur) - timedelta(seconds=other)

        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, timedelta):
            cur: int = self.total_seconds
            return timedelta(seconds=cur) + other

        else:
            return NotImplemented

    def __lt__(self, other):
        cur: int = self.total_seconds
        oth: int = self.__check_type(self, other)
        return cur < oth

    def __gt__(self, other):
        cur: int = self.total_seconds
        oth: int = self.__check_type(self, other)
        return cur > oth

    def __le__(self, other):
        cur: int = self.total_seconds
        oth: int = self.__check_type(self, other)
        return cur <= oth

    def __eq__(self, other):
        cur: int = self.total_seconds
        oth: int = self.__check_type(self, other)
        return cur == oth


class SuperTimePeriod:
    """
    Class for storage and control 2 SuperTime /n
    objects (from time and to time). /n
    Can evaluate length of period. /n
    Iterable object
    """

    def __init__(self, time1: SuperTime, time2: SuperTime):
        self._time1 = time1
        self._time2 = time2
        self._period = self._calculate_period()

    @property
    def period(self):
        return self._period

    def _calculate_period(self):
        return [self._time1, self._time2]

    def __repr__(self):
        return f"{self._time1} - {self._time2}"

    def __len__(self):
        begin = self._time1.total_seconds
        end = self._time2.total_seconds
        return end - begin

    def __add__(self, other):
        if isinstance(other, SuperTimePeriod):
            self._time1 += other._time1
            self._time2 += other._time2
            self._calculate_period()

    def __sub__(self, other):
        if isinstance(other, SuperTimePeriod):
            self._time1 -= other._time1
            self._time2 -= other._time2
            self._calculate_period()

    def __iter__(self):
        for elem in self._period:
            yield elem


class TimesCollection:
    """
    Class for create, storage and control 1-2 SuperTimePeriod objects. /n
    Can evaluate day period, and intersect it with another STP exemplar. /n
    Can evaluate length of all inner periods. /n
    Can subtract from period some SuperTime object (SLA) /n
    for evaluating estimating SLA and estimating time (if SLA <= 0)

    """

    def __init__(self, *args):
        self._args = args
        self._periods = self._constructor()

    @property
    def periods(self):
        return self._periods

    def _constructor(self):
        """
        Builder method for periods property
        :return:
        """
        if len(self._args) == 2:
            if self._args[0] < self._args[1]:
                return [SuperTimePeriod(*self._args)]

            elif self._args[0] > self._args[1]:
                return (
                    SuperTimePeriod(SuperTime(0), self._args[1]),
                    SuperTimePeriod(self._args[0], SuperTime(24)),
                )

            elif self._args[0] == self._args[1]:
                return [SuperTimePeriod(SuperTime(0), SuperTime(24))]

        elif len(self._args) == 4:
            return (
                SuperTimePeriod(self._args[0], self._args[1]),
                SuperTimePeriod(self._args[2], self._args[3]),
            )

        else:
            return []

    def intersect(self, other):
        """
        Method for intersect time periods
        :param other: other SuperTime instance
        :return: new TimesCollection instance
        """
        if isinstance(other, SuperTime):
            result = []
            for begin, end in self._periods:
                if other <= begin:
                    result.extend([begin, end])

                elif begin <= other < end:
                    result.extend([other, end])

            return TimesCollection(*result)

    def __repr__(self):
        return f"TimesCollection{self._periods}"

    def __len__(self):
        return sum(map(len, self._periods))

    def __sub__(self, other):
        sla = other

        if isinstance(other, SuperTime):
            for p1, p2 in self._periods:
                sla = other - (p2.total_seconds - p1.total_seconds)

                if sla.total_seconds() <= 0:
                    return SuperTime(0), SuperTime(p2 + sla)

                other = SuperTime(sla)

        return SuperTime(sla), SuperTime(0)
