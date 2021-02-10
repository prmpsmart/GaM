from ..core.bases import ObjectSort

class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsBySeasons(self, date, _type=[], subsAttr=[]):
        types = {'year': 'isSameYear', 'month': 'isSameMonth', 'week', 'isSameWeek', 'day': 'isSameDay', 'date': 'isSameDate'}
        subs = []

        pass

    def sortSubsBySeasons(self): pass








