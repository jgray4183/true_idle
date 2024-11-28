from objects import *
from constants import BASE_PRICE
import time

points = 0 
running = True
gen_list =  [Generator(1)]
upgrade_dict = {"buy_amount" : Upgrade("Buy Amount", 25, 3)}

def new_generator(points):
    points_local = points
    new_gen_number = len(gen_list) + 1
    gen_list.append(Generator(new_gen_number))
    points_local -= gen_list[-1].price
    return points_local

def main():
    global points
    while running == True:
        #take readings so I can report output changes
        points_start = points
        gen_number_start = len(gen_list)
        #generate points for each generator
        for gen in gen_list:
            points += gen.generate()
        points_generated = points - points_start
        points_start = points
        #first unlock new generator if possible
        if points >= BASE_PRICE ** (len(gen_list) + 1):
            points = new_generator(points)
        #increase buy ammount if possible
        for upgrade in upgrade_dict:
            if points >= upgrade_dict[upgrade].price:
                upgrade_dict[upgrade].buy(points)
        #buy 1 of each generator that can be afforded starting at cheapest
        for gen in gen_list:
            if points >= gen.price:
                buy_amount = int(points // gen.price)
                if upgrade_dict["buy_amount"].tier < buy_amount:
                    buy_amount = upgrade_dict["buy_amount"].tier
                buy_cost = buy_amount * gen.price
                for i in range(buy_amount):
                    gen.buy(points)
                points -= buy_cost

        points_spent = points_start - points

#bellow this line is all for the user output

        highest_gen = gen_list[-1]

        print ("============================================")
        if len(gen_list) > gen_number_start:
            print (f"{highest_gen} unlocked")
        if points_spent > 0:
            print(f"{points_generated} points generated \n{points_spent} points spent \nYou have {highest_gen.amount} {highest_gen} \nNew Points {points}")
        else:
            print(f"{points_generated} points generated \nYou have {highest_gen.amount} {highest_gen}  \nNew Points {points}")

        time.sleep(1)

if __name__ == "__main__":
    main()