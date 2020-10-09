
from .user import User

class Super_User(User):
    super_user = True
    ADMIN = True
    class_name = "Super_User"
    def __init__(self, *args):
        super().__init__(*args) 
