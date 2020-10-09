from .record import Records


class Amounts:
    
    def __init__(self, region):
        self.region = region
        self.which = region.which
        self.thrifts = Records()
        self.debits = Records()
        self.brought_forwards = Records()
        self.upfronts = Records()
        self.balances = Records()
        self.savings = Records()
        self.not_paids = Records()
        self.rate = rate
        self.r_upfronts = Records()
        self.p_upfronts = Records()
        
        if not self.isClient():
            self.btos = Records()
            self.excesses = Records()
            self.deficits = Records()
    
    def isClient(self): return self.which == 'client'