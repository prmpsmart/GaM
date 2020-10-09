from ..core.details import Detail, DetailsManager


class DCManagerDetail(Detail):
    pass

class CoopManagerDetail(Detail):
    pass

class OfficeManagerDetail(Detail):
    pass


class DCManagerDetailsManager(DetailsManager):
    detailClass = DCManagerDetail
    
class CoopManagerDetailsManager(DetailsManager):
    detailClass = CoopManagerDetail
    
class OfficeManagerDetailsManager(DetailsManager):
    detailClass = OfficeManagerDetail
    
    




