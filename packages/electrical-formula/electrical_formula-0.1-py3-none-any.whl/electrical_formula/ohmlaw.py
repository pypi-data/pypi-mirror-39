class Ohm:
    
    @staticmethod
    def current(voltage,resistance):
        i = voltage/resistance
        print(i)
        return i
    @staticmethod
    def resistance_basic(resistivity,length,area):
        r =resistivity*(length/area)
        print(r)
        return r
    @staticmethod
    def resistance(current,voltage):
        r2 = current/voltage
        print(r2)
        return r2
    @staticmethod
    def voltage(current,resistance):
        v = current*resistance
        print(v)
        return  v

class Mho(Ohm):
    def __init__(self):
        super(Mho,self).__init__()
    def mho (self,resistance):
        m = 1/resistance
        print(m)
        return m



