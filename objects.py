from constants import BASE_GEN, BASE_PRICE

class Genirator():
    def __init__(self, tier):
        self.tier = tier
        self.amount = 1
        self.gen_val = None
        self.price = None
        self.get_gen()
        self.get_price()
        print (f"Genirator {self.tier} unlocked")

    def __str__(self):
        return f"Genirator {self.tier}"

    def get_gen(self):
        self.gen_val = BASE_GEN * self.tier

    def get_price(self):
        self.price = BASE_PRICE * self.tier

    def genirate(self):
        return self.gen_val * self.amount

    def buy(self, points):
        points_output = points
        self.amount += 1
        points_output -= (self.price)
        return points_output
