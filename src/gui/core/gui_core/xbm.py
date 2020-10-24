

class Xbm:
    
    @classmethod
    def files(cls):
        path = os.path
        dn = path.dirname
        dir_ = dn(dn(dn(dn(__file__))))
        file = path.join(dir_, 'img/profile_pix.png')
        return file
    
    @classmethod
    def filesDict(cls):
        pass
    
    @classmethod
    def filesList(cls):
        pass
    
    @classmethod
    def get(cls, bitmap):
        if isinstance(bitmap, int):
            pass
        
        elif isinstance(bitmap, str):
            pass