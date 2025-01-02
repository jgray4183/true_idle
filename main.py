from objects import Generator, PrestigedGenerator, Upgrade, UpgradeStoreValue
from constants import BASE_PRICE, DISCOUNT
from askii import *
import time
import random
import pickle

def initilise_gens():
    gen_list = []
    for i in range(1, ascenssion_dict["starting_gen_amount"] + 1):
        gen_list.append(Generator(i, ascenssion_dict))
    return gen_list

def initilise_upgrades():
    return {"buy_amount" : Upgrade("Buy Amount", ascenssion_dict, 25, 3, 100 + ascenssion_dict["upgrade_scale"]), "tickspeed" : Upgrade("Tickspeed", ascenssion_dict, 100, 100, 25 + ascenssion_dict["upgrade_scale"]), "unlock_bank" : UpgradeStoreValue("Unlock Bank", ascenssion_dict, 250, 5, 100 + ascenssion_dict["upgrade_scale"], 50)}

#if a save exists import it otherwise start the game new
save = []
try:
    with open("save.pkl", "rb") as fp:
        save = pickle.load(fp)
except Exception as e:
    pass

if len(save) == 8:
    points = int(save[0])
    max_prestige = int(save[1])
    double_gen_ticks = int(save[2])
    tickspeed_boost_ticks = int(save[3])
    points_discount_boolean = save[4]
    ascenssion_dict = save[5]
    gen_list = save[6]
    upgrade_dict = save[7]
else:
    points = 0 
    max_prestige = 5
    double_gen_ticks = 0
    tickspeed_boost_ticks = 0
    points_discount_boolean = False
    ascenssion_dict = {"ascenssion_count" : 0, "ascenssion_goal" : 100000, "starting prestige" : 5, "upgrade_scale" : 0, "gen_price_upgrade" : 1, "gen_val_upgrade" : 1, "starting_gen_amount" : 1}
    gen_list =  initilise_gens()
    upgrade_dict = initilise_upgrades()

#establish anything not saved
random.seed()
running = True
save_countdown = 30

first_ascenssion_upgrades = ["increase gen amount", "reduce gen price"]
second_ascenssion_upgrades = ["increase max prestige by 5"]
third_ascenssion_upgrades = ["increase all upgrades", "increase starting gen number"]
forth_ascenssion_upgrades = ["increase all upgrades", "reduce gen price", "increase gen amount", "increase starting gen number"]
ascenssion_upgrades = ["increase max prestige by 5", "increase all upgrades", "reduce gen price", "increase gen amount", "increase starting gen number"]

ultra_rare_events = ["increase max prestige", "double gen for rounds", "unlock next tier"]
medium_rare_events = ["free upgrade", "free gens", "double savings"]
normal_rare_events = ["points discount", "tickspeed boost", "double points"]

#this function saves the game as a pickled list and creates a save if one dosen't exist
def save_game():
    save = [points, max_prestige, double_gen_ticks, tickspeed_boost_ticks, points_discount_boolean, ascenssion_dict, gen_list, upgrade_dict]
    try:    
        with open("save.pkl", "xb") as fp:
            pickle.dump(save, fp, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        with open("save.pkl", "wb") as fp:
            pickle.dump(save, fp, protocol=pickle.HIGHEST_PROTOCOL)

#this function takes the amount of points and amount of points in the unlock bank upgrade and uses to them to add a new tier of generator to the end gen list returning the cost of that new tier from the points total
def new_generator(points):
    new_gen_number = len(gen_list) + 1
    gen_list.append(Generator(new_gen_number, ascenssion_dict))
    if gen_list[-1].price > upgrade_dict["unlock_bank"].value:
        points_cost = gen_list[-1].price - upgrade_dict["unlock_bank"].value
        upgrade_dict["unlock_bank"].value -= 0
        return points_cost
    else:
        upgrade_dict["unlock_bank"].value -= gen_list[-1].price
        return 0

#this resets all aspects of the game except for upgrades unlocked by this function, allowing powerful upgrades at the cost of starting over 
#first it applies these upgrades then dose the reset
def ascend():
    global points, ascenssion_dict, max_prestige, upgrade_dict, gen_list, double_gen_ticks, tickspeed_boost_ticks, points_discount_boolean
    if points < ascenssion_dict["ascenssion_goal"]:
        raise Exception("not enough points")
        return None
    else:
        print_line()
        print (ascended_askii)
        print_line()
        time.sleep(2)
        ascenssion_dict["ascenssion_goal"] *= 10
        ascenssion_dict["ascenssion_count"] += 1
        if ascenssion_dict["ascenssion_count"] == 1:
            ascenssion_upgrade = first_ascenssion_upgrades[random.randint(0, len(first_ascenssion_upgrades) - 1)]
        if ascenssion_dict["ascenssion_count"] == 2:
            ascenssion_upgrade = second_ascenssion_upgrades[random.randint(0, len(second_ascenssion_upgrades) - 1)]
        if ascenssion_dict["ascenssion_count"] == 3:
            ascenssion_upgrade = third_ascenssion_upgrades[random.randint(0, len(third_ascenssion_upgrades) - 1)]
        if ascenssion_dict["ascenssion_count"] == 4:
            ascenssion_upgrade = forth_ascenssion_upgrades[random.randint(0, len(forth_ascenssion_upgrades) - 1)]
        else:
            ascenssion_upgrade = ascenssion_upgrades[random.randint(0, len(ascenssion_upgrades) - 1)]
        if ascenssion_upgrade == "increase max prestige by 5":
            ascenssion_dict["starting prestige"] += 5
            print_line()
            print (max_prestige_askii)
            print_line()
            print (f"New max prestige is {ascenssion_dict["starting prestige"]}")
            print_line()
            time.sleep(2)
        if ascenssion_upgrade == "increase all upgrades":
            ascenssion_dict["upgrade_scale"] += 5
            print_line()
            print (upgrade_askii)
            print_line()
            print (f"All upgrades starting and max levels increased by 5")
            print_line()
            time.sleep(2)
        if ascenssion_upgrade == "reduce gen price":
            ascenssion_dict["gen_price_upgrade"] += 1
            print_line()
            print (reduced_gen_askii)
            print_line()
            print (f"All Generator prices reduced")
            print_line()
            time.sleep(2)
        if ascenssion_upgrade == "increase gen amount":
            ascenssion_dict["gen_val_upgrade"] += 1
            print_line()
            print (increase_gen_askii)
            print_line()
            print (f"All Generator values increased")
            print_line()
            time.sleep(2)
        if ascenssion_upgrade == "increase starting gen number":
            ascenssion_dict["starting_gen_amount"] *= 2
            print_line()
            print (starting_gen_askii)
            print_line()
            print (f"You start with {ascenssion_dict["starting_gen_amount"]} gens")
            print_line()
            time.sleep(2)
        max_prestige = ascenssion_dict["starting prestige"]
        upgrade_dict = initilise_upgrades()
        gen_list = initilise_gens()
        points = 0 
        double_gen_ticks = 0
        tickspeed_boost_ticks = 0
        points_discount_boolean = False
        save_game()
        return


#when a random event is triggered then roll to decide what level of rarity it will be and pick one of the events from that rarity at random
def random_event_genirator(event_log):
    event = None
    roll = random.randint(1, 100)
    if roll >= 90:
        event = ultra_rare_events[random.randint(0, len(ultra_rare_events) - 1)]
        if event == "increase max prestige":
            event_log.append(f"Random Event! {increase_max_prestige()}")
        if event == "double gen for rounds":
            event_log.append(f"Random Event! {double_gen()}")
        if event == "unlock next tier":
            event_log.append(f"Random Event! {unlock_next_tier()}")
    if roll >= 60 and roll < 90:
        event = medium_rare_events[random.randint(0, len(ultra_rare_events) - 1)]
        if event == "free upgrade":
            event_log.append(f"Random Event! {free_upgrade()}")
        if event == "free gens":
            event_log.append(f"Random Event! {free_gens()}")
        if event == "double savings":
            event_log.append(f"Random Event! {double_savings()}")
    if roll < 60:
        event = normal_rare_events[random.randint(0, len(ultra_rare_events) - 1)]
        if event == "points discount":
            event_log.append(f"Random Event! {points_discount()}")
        if event == "tickspeed boost":
            event_log.append(f"Random Event! {tickspeed_boost()}")
        if event == "double points":
            event_log.append(f"Random Event! {double_points()}")
    return event_log

#random event functions
def double_points():
    global double_gen_ticks
    if double_gen_ticks == 0:
        double_gen_ticks = 1
        return "Point gen doubled this tick"
    return None

def tickspeed_boost():
    global tickspeed_boost_ticks
    tickspeed_boost_ticks = 30
    return "Tickspeed increased for 30 ticks"

def points_discount():
    global points_discount_boolean
    points_discount_boolean = True
    return "Costs discounted this tick"

def free_upgrade():
    valid_upgrade = False
    for upgrade in upgrade_dict:
        if upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
            valid_upgrade = True
    if valid_upgrade == False:
        return "No upgrades"
    random_upgrade = random.randint(0,len(upgrade_dict) - 1)
    for i, key in enumerate(upgrade_dict.keys()):
        if i == random_upgrade:
            random_upgrade = key
    if upgrade_dict[random_upgrade].tier >= upgrade_dict[random_upgrade].max:
        free_upgrade()
    upgrade_dict[random_upgrade].tier += 1
    return f"{upgrade_dict[random_upgrade].name} increased to tier {upgrade_dict[random_upgrade].tier} for free"

def free_gens():
    for gen in gen_list:
        gen.amount += int(gen.amount * 1.1)
    return "All gen amounts increased by 10%"

def double_savings():
    upgrade_dict["unlock_bank"].add_value(upgrade_dict["unlock_bank"].value)
    return "Savings doubled"

def increase_max_prestige():
    global max_prestige
    max_prestige += 1
    return f"Max prestige increased to {max_prestige}"

def double_gen():
    global double_gen_ticks
    double_gen_ticks += random.randint(1,10)
    return f"Geniration doubled for {double_gen_ticks} ticks"

def unlock_next_tier():
    new_generator(float('inf'))
    return "Next Tier unlocked for free"

#commonly used print
def print_line():
    print ("============================================================")

def main():
    global points, double_gen_ticks, tickspeed_boost_ticks, points_discount_boolean, save_countdown
    #this try statement is to allow the game to save if "closed" by keyboard interrupt
    try:
        while running == True:
            #this keeps track of any notable events from the tick and reports them at the end
            event_log = []
            #reset any veriables that should only act for one tick
            points_discount = False
            #random events to stop the game being determanistic
            if random.randint(1 + 40 - (len(gen_list) * 4), 100) == 100:
                event_log = random_event_genirator(event_log)
            #take readings so I can report output changes
            points_generated = 0
            gen_number_start = len(gen_list)
            #generate points for each generator and add 2% of the new points to the upgrade bank, runs a second time if the points genirated are being doubled
            for gen in gen_list:
                points += gen.generate()
                points_generated += gen.generate()
            if double_gen_ticks > 0:
                for gen in gen_list:
                    points += gen.generate()
                    points_generated += gen.generate()
                double_gen_ticks -= 1
            points -= upgrade_dict["unlock_bank"].add_value(int(points/50))
            #ascend if possible
            if points >= ascenssion_dict["ascenssion_goal"]:
                ascend()
                continue
            #take readings for how many points have been genirated then reset point starts to track points spent
            points_start = points
            #prestige a generator if possible
            for gen in gen_list:
                if gen.amount > gen.prestige_cost and gen.prestige < max_prestige:
                    gen_list.append(PrestigedGenerator(gen, ascenssion_dict))
                    gen_list.remove(gen)
                    event_log.append(f"Generator {gen_list[-1].tier} has reached prestige {gen_list[-1].prestige}")
                    gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #unlock new generator if possible
            if points + upgrade_dict["unlock_bank"].value >= int((BASE_PRICE * ((len(gen_list) + 1) / ascenssion_dict["gen_price_upgrade"])) ** ((len(gen_list) + 1) - ((len(gen_list) + 1) / 2))):
                points -= new_generator(points)
                event_log.append(f"Tier {len(gen_list)} unlocked")
                gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #buy upgrades as they are fewer and more impactful than gens, trying to buy with a discount first then at full price if discount isn't active
            if points_discount_boolean == True:
                for upgrade in upgrade_dict:
                    if points >= (upgrade_dict[upgrade].price * DISCOUNT) and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
                        points = upgrade_dict[upgrade].buy_discount(points)
                        event_log.append(f"{upgrade_dict[upgrade].name} Upgraded to rank {upgrade_dict[upgrade].tier}")
            else:
                for upgrade in upgrade_dict:
                    if points >= upgrade_dict[upgrade].price and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
                        points = upgrade_dict[upgrade].buy(points)
                        event_log.append(f"{upgrade_dict[upgrade].name} Upgraded to rank {upgrade_dict[upgrade].tier}")
            #buy buy max of each generator that can be afforded starting at higest genirating, trying to buy with a discount first then at full price if discount isn't active
            if points_discount_boolean == True:
                for gen in (gen_list):
                    if points >= gen.price * DISCOUNT:
                        buy_amount = int(points // gen.price)
                        if upgrade_dict["buy_amount"].tier < buy_amount:
                            buy_amount = upgrade_dict["buy_amount"].tier
                        buy_cost = buy_amount * int(gen.price * DISCOUNT)
                        for i in range(buy_amount):
                            gen.buy_discount(points)
                        points -= buy_cost
            else:
                for gen in (gen_list):
                    if points >= gen.price:
                        buy_amount = int(points // gen.price)
                        if upgrade_dict["buy_amount"].tier < buy_amount:
                            buy_amount = upgrade_dict["buy_amount"].tier
                        buy_cost = buy_amount * gen.price
                        for i in range(buy_amount):
                            gen.buy(points)
                        points -= buy_cost

            points_spent = points_start - points

            #every tick reduce the time till the next auto save then if enough ticks have passed complete a save
            save_countdown -= 1
            if save_countdown == 0:
                save_game()
                #this sacles with tickspeed to keep the auto saves roughly every 30 seconds
                save_countdown = int(30 + (upgrade_dict["tickspeed"].tier / (1 + (2/3))))
                if save_countdown > 60:
                    save_countdown = 60

    #below this line is all for output

            total_gens = 0
            for gen in gen_list:
                total_gens += gen.amount

            highest_gen = gen_list[0]

            print_line()

            #this prints events that might not happen every tick
            for event in event_log:
                if event == None:
                    pass
                else:
                    print (event)

            #this prints the points genirated, points spent if any were, running genirator count, and points total so this statement will print every tick, conditions to keep grama correct and provent empty statements
            if highest_gen.amount == 1:
                if points_spent > 0:
                    print(f"{format(points_generated, ",d")} points generated \n{format(points_spent, ",d")} points spent \nYou have {format(total_gens, ",d")} generators, {highest_gen.amount} is a {highest_gen} \nNew Points {format(points, ",d")}")
                else:
                    print(f"{format(points_generated, ",d")} points generated \nYou have {format(total_gens, ",d")} generators, {highest_gen.amount} is a {highest_gen} \nNew Points {format(points, ",d")}") 
            else:
                if points_spent > 0:
                    print(f"{format(points_generated, ",d")} points generated \n{format(points_spent, ",d")} points spent \nYou have {format(total_gens, ",d")} generators, {format(highest_gen.amount, ",d")} are {highest_gen}s \nNew Points {format(points, ",d")}")
                else:
                    print(f"{format(points_generated, ",d")} points generated \nYou have {format(total_gens, ",d")} generators, {format(highest_gen.amount, ",d")} are {highest_gen}s \nNew Points {format(points, ",d")}")

            if upgrade_dict["unlock_bank"].value > 0:
                print (f"You have {format(upgrade_dict["unlock_bank"].value, ",d")} points saved to unlock Tier {(len(gen_list) + 1)}")

            #prints the current assesion goal about every 30 seconds bassed off the save countdown to save adding another
            if save_countdown == 1:
                if ascenssion_dict["ascenssion_count"] >= 1:
                    print (f"You have ascended {ascenssion_dict["ascenssion_count"]} times \nYou need {format(ascenssion_dict["ascenssion_goal"], ",d")} points to Ascend")
                else:
                    print (f"You need {format(ascenssion_dict["ascenssion_goal"], ",d")} points to Ascend")

            #sleep bassed on if there is a boost event happening, then reducies the time bassed on the tickspeed upgrade with a hard limit to stop the game running too fast
            if tickspeed_boost_ticks > 0:
                if (0.01 * upgrade_dict["tickspeed"].tier) < 0.5:
                    time.sleep(1 - (0.01 * upgrade_dict["tickspeed"].tier)- 0.1)
                    tickspeed_boost_ticks -= 1
                else:
                    time.sleep (0.5 - 0.1)
                    tickspeed_boost_ticks -= 1
            else:
                if (0.01 * upgrade_dict["tickspeed"].tier) < 0.5:
                    time.sleep(1 - (0.01 * upgrade_dict["tickspeed"].tier))
                else:
                    time.sleep (0.5)

    #saves the game if "closed" by keyboard interrupt
    except KeyboardInterrupt:
        save_game()

if __name__ == "__main__":
    main()