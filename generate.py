import time
import random

class Generate:
    """
    Generate Sensor Data
    """
    def gen_data(self):
        t1 = round(random.uniform(55.5, 75.5), 2)
        h1 = round(random.uniform(15, 55), 2)
        data = []
        for i in range(24):
            temp = round(random.uniform(t1-1, t1+1), 2)
            humidity = round(random.uniform(h1-1, h1+1), 2)
            # day = (temp, humidity, i+1)
            day = (temp, humidity)
            data.append(day)
        return data

    # def __init__(self):
    #     self.gen_data = gen_data(self)

    # def gen_hr(self, day):
    #     uday = day
    #     h24 = round(random.uniform(day[0]-1.5, day[0]+1.5), 2)
    #     uday.pop(0)
    #     uday.append(h24)
    #     return day

if __name__ == '__main__':
    x  = Generate()
    day = x.gen_data()
    print(day)
