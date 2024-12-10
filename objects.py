from constants import BASE_GEN, BASE_PRICE, DISCOUNT

#Generators are the main way of genirating points, they start with values bassed on constants and there tier

class Generator():
    def __init__(self, tier):
        self.tier = tier
        self.amount = 1
        self.pristege = 0
        self.pristege_cost = 150
        self.gen_val = None
        self.price = None
        self.gen_price_ratio = None
        self.get_gen()
        self.get_price()
        self.get_ratio()

    def __str__(self):
        return f"Tier {self.tier} Generator"

    def get_gen(self):
        if self.tier > 1:
            self.gen_val = int((BASE_GEN + self.tier - 1) * ((self.tier - (self.tier / 2)) ** 3))
        else:
            self.gen_val = BASE_GEN ** self.tier

    def get_price(self):
        if self.tier > 1:
            self.price = int((BASE_PRICE * self.tier) ** (self.tier - (self.tier / 2)))
        else:
            self.price = BASE_PRICE ** self.tier
    
    def get_ratio(self):
        self.gen_price_ratio = self.price / self.gen_val

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

    def buy_discount(self, points):
        if int(self.price * DISCOUNT) > points:
            raise Exception("not enough points")
            return points
        else:
            self.amount += 1
            points_output = points - int(self.price * DISCOUNT)
            return points_output

#Through the game genirators will pristege to genirate more points at a higher cost bassed on what there previous gen ammount and cost were

class PristegedGenerator(Generator):
    def __init__(self, gen):
        super().__init__(gen.tier)
        self.gen_val = int((gen.gen_val + gen.tier) * 1.5)
        self.price = int((gen.price + gen.tier) * 1.10)
        self.pristege = gen.pristege + 1
        self.pristege_cost = int(gen.pristege_cost * 1.5)
        self.get_ratio()

    def __str__(self):
        return f"Pristege {self.pristege} Tier {self.tier} Generator"

#Upgrades make the game easier and are upgrades in a similar way to generators

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
            self.price = int(self.price * self.multiplier)
            return points_local

    def buy_discount(self, points):
        if (int((self.price * DISCOUNT)//1)) > points:
            raise Exception("not enough points")
            return points
        else:
            self.tier += 1
            points_local = points - int(self.price * DISCOUNT)
            self.price = int(self.price * self.multiplier)
            return points_local

#Some upgrades have to store a value beyond there tier this allows they to add and "spend" that value

class UpgradeStoreValue(Upgrade):
    def __init__(self, name, price, multiplier, maximum, value_max):
        super().__init__(name, price, multiplier, maximum)
        self.value = 0
        self.value_max = value_max

    #this function takes the amount to add to the stored value and returns the amount thats been added
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
            self.value_max = int(self.value_max * self.multiplier)
            self.price = int(self.price * self.multiplier)
            return points_local

    def buy_discount(self, points):
        if (int((self.price * DISCOUNT)//1)) > points:
            raise Exception("not enough points")
            return points
        else:
            self.tier += 1
            points_local = points - int(self.price * DISCOUNT)
            self.value_max = int(self.value_max * self.multiplier)
            self.price = int(self.price * self.multiplier)
            return points_local 
