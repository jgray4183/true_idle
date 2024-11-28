from constants import BASE_GEN, BASE_PRICE

class Generator():
    def __init__(self, tier):
        self.tier = tier
        self.amount = 1
        self.gen_val = None
        self.price = None
        self.get_gen()
        self.get_price()

    def __str__(self):
        return f"Generator {self.tier}"

    def get_gen(self):
        self.gen_val = BASE_GEN * (self.tier ** 2)

    def get_price(self):
        self.price = BASE_PRICE ** self.tier

    def generate(self):
        return self.gen_val * self.amount

    def buy(self, points):
        if self.price > points:
            raise Exception("not enough points")
            return points
        else:
            self.amount += 1
            points_output = points - (self.price)
            return points_output

class Upgrade():
    def __init__(self, name, price, multiplier):
        self.name = name
        self.price = price
        self.multiplier = multiplier
        self.tier = 1

    def buy(self, points):
        if self.price > points:
            raise Exception("not enough points")
            return points
        else:
            self.tier += 1
            points_local = points - self.price
            self.price *= self.multiplier
            print (f"{self.name} Upgraded")
            return points_local
