
class Img_Tk:
    def __init__(self, img, size):
        self.img = img
        self.size = size
    
    def offset(self, parent, child):
        half_parent = int(parent/2)
        half_child = int(child/2)
        o_s = half_parent - half_child
        return o_s
    
    def calc_geo(self, root):
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        x, y = self.size
        offset_x = self.offset(w, x)
        offset_y = self.offset(h, y)
        
        geo = '%dx%d+%d+%d'%(x,y,offset_x,offset_y)
        return geo
    
    def calc_bar(self):
        x, y = self.size

        


if __name__ == "__main__":
    pa = Img_Tk("isdhs", (552, 502))
    d = pa.offset(1600, 552)
    print(d)



