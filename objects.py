from constants import BASE_GEN, BASE_PRICE

class Generator():
    def __init__(self, tier):
        self.tier = tier
        self.amount = 1
        self.pristege = 0
        self.pristege_cost = 100
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

class PristegedGenerator(Generator):
    def __init__(self, gen):
        super().__init__(gen.tier)
        self.gen_val = int((gen.gen_val * 1.5)//1)
        self.price = int((gen.price * 1.25)//1)
        self.pristege = gen.pristege + 1
        self.pristege_cost = int((gen.pristege_cost * 1.5)//1)
        print (f"Generator {self.tier} has reached Pristege {self.pristege}")

    def __str__(self):
        return f"Pristege {self.pristege} Generator {self.tier}"

class Upgrade():
    def __init__(self, name, price, multiplier, maximum):
        self.name = name
        self.price = price
        self.multiplier = multiplier
        self.max = maximum
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

class UpgradeStoreValue(Upgrade):
    def __init__(self, name, price, multiplier, maximum, value_max):
        super().__init__(name, price, multiplier, maximum)
        self.value = 0
        self.value_max = value_max

    def add_value(self, amount):
        if self.value + amount > self.value_max:
            diferance = self.value
            self.value = self.value_max
            return self.value_max - diferance
        else:
            self.value += amount
            return amount

    def buy(self, points):
        if self.price > points:
            raise Exception("not enough points")
            return points
        else:
            self.tier += 1
            points_local = points - self.price
            self.value_max *= self.value_max
            self.price *= self.multiplier
            print (f"{self.name} Upgraded")
            return points_local    
