from ..core.bases import ObjectSort

class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsBySeasons(self, date, seasons=[], attrs=[], attr='', **kwargs):
        _types = {'year': 'isSameYear', 'month': 'isSameMonth', 'week': 'isSameWeek', 'day': 'isSameDay', 'date': 'isSameDate'}

        validations = []

        for season in seasons:
            validation = dict()

    def sortSubsBySeasons(self): pass













