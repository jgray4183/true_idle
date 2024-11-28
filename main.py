from objects import *
from constants import BASE_PRICE
import time

points = 0 
max_pristege = 5
running = True
gen_list =  [Generator(1)]
upgrade_dict = {"buy_amount" : Upgrade("Buy Amount", 25, 3, 100), "tickspeed" : Upgrade("Tickspeed", 100, 100, 25), "unlock_bank" : UpgradeStoreValue("Unlock Bank", 250, 5, 100, 50)}

def new_generator(points):
    points_local = points + upgrade_dict["unlock_bank"].value
    new_gen_number = len(gen_list) + 1
    gen_list.append(Generator(new_gen_number))
    points_cost = gen_list[-1].price - upgrade_dict["unlock_bank"].value
    if gen_list[-1].price > upgrade_dict["unlock_bank"].value:
        upgrade_dict["unlock_bank"].value = 0
        return points_local - points_cost
    upgrade_dict["unlock_bank"].value -= gen_list[-1].price
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
        points -= upgrade_dict["unlock_bank"].add_value(int((points/50)//1))
        points_generated = points - points_start
        points_start = points
        #pristege a generator if possible
        for gen in gen_list:
                if gen.amount > gen.pristege_cost and gen.pristege < max_pristege:
                        gen_list.append(PristegedGenerator(gen))
                        gen_list.remove(gen)
                        gen_list.sort(key=lambda e:e.gen_val)
        #unlock new generator if possible
        if points + upgrade_dict["unlock_bank"].value >= BASE_PRICE ** (len(gen_list) + 1):
            points = new_generator(points)
            gen_list.sort(key=lambda e:e.gen_val)
        #buy upgrades as they are fewer and more impactful than gens
        for upgrade in upgrade_dict:
            if points >= upgrade_dict[upgrade].price and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
                upgrade_dict[upgrade].buy(points)
        #buy buy max of each generator that can be afforded starting at higest genirating
        for gen in reversed(gen_list):
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

        total_gens = 0
        for gen in gen_list:
                total_gens += gen.amount

        highest_gen = gen_list[-1]

        print ("============================================================")
        if len(gen_list) > gen_number_start:
            print (f"{highest_gen} unlocked")
        if highest_gen.amount == 1:
                if points_spent > 0:
                        print(f"{points_generated} points generated \n{points_spent} points spent \nYou have {total_gens} generators, {highest_gen.amount} is {highest_gen} \nNew Points {points}")
                else:
                        print(f"{points_generated} points generated \nYou have {total_gens} generators, {highest_gen.amount} is {highest_gen} \nNew Points {points}") 
        else:
                if points_spent > 0:
                        print(f"{points_generated} points generated \n{points_spent} points spent \nYou have {total_gens} generators, {highest_gen.amount} are {highest_gen} \nNew Points {points}")
                else:
                        print(f"{points_generated} points generated \nYou have {total_gens} generators, {highest_gen.amount} are {highest_gen} \nNew Points {points}")

        if upgrade_dict["unlock_bank"].value > 0:
                print (f"You have {upgrade_dict["unlock_bank"].value} points saved to unlock Tier {(len(gen_list) + 1)}")

        #sleep bassed on tickspeed upgrade

        if (0.01 * upgrade_dict["tickspeed"].tier) < 0.5:
                time.sleep(1 - (0.01 * upgrade_dict["tickspeed"].tier))
        else:
                time.sleep (0.5)

if __name__ == "__main__":
    main()