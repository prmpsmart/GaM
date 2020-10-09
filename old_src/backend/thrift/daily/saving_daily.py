
class Saving_Daily:
    area_dailies = []
    area_dailies_names = []
    @classmethod
    def add(cls, area_daily):
        if area_daily.name in cls.area_dailies_names: pass
        else:
            cls.area_dailies.append(area_daily)
            cls.area_dailies_names.append(area_daily.name)
    @classmethod
    def get(cls, name):
        if name in cls.area_dailies_names:
            for area_daily in cls.area_dailies:
                if area_daily.name == name: return area_daily
