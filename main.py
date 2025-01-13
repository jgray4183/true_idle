from objects import Generator, PrestigedGenerator, Upgrade, UpgradeStoreValue
from constants import BASE_PRICE, DISCOUNT
from askii import *
import time
import random
import pickle
import math

def initilise_gens():
    gen_list = []
    for i in range(1, ascenssion_dict["starting_gen_amount"] + 1):
        gen_list.append(Generator(i, ascenssion_dict))
    return gen_list

def initilise_upgrades():
    return {"buy_amount" : Upgrade("Buy Amount", ascenssion_dict, 25, 9, 100 + ascenssion_dict["upgrade_scale"]), "tickspeed" : Upgrade("Tickspeed", ascenssion_dict, 100, 100, 25 + ascenssion_dict["upgrade_scale"]), "unlock_bank" : UpgradeStoreValue("Unlock Bank", ascenssion_dict, 250, 5, 100 + ascenssion_dict["upgrade_scale"], 50)}

#if a save exists import it otherwise start the game new
save = []
try:
    with open("save.pkl", "rb") as fp:
        save = pickle.load(fp)
except Exception as e:
    pass

if len(save) == 5 and save[0] == 0.22001:
    veriables_dict = save[1]
    ascenssion_dict = save[2]
    gen_list = save[3]
    upgrade_dict = save[4]
elif len(save) == 0:
    save_version = 0.22001
    veriables_dict = {"points": 0, "max_prestige": 5, "double_gen_ticks": 0, "tickspeed_boost_ticks": 0, "points_discount_boolean": False, "random_event_chance": 90}
    ascenssion_dict = {"ascenssion_count" : 0, "ascenssion_goal" : 100000, "starting prestige" : 5, "upgrade_scale" : 0, "gen_price_upgrade" : 1, "gen_val_upgrade" : 1, "starting_gen_amount" : 1}
    gen_list =  initilise_gens()
    upgrade_dict = initilise_upgrades()
else:
    raise Exception("save index wrong")

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
    save = [save_version, veriables_dict, ascenssion_dict, gen_list, upgrade_dict]
    try:    
        with open("save.pkl", "xb") as fp:
            pickle.dump(save, fp, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        with open("save.pkl", "wb") as fp:
            pickle.dump(save, fp, protocol=pickle.HIGHEST_PROTOCOL)

#this function takes the amount of points and amount of points in the unlock bank upgrade and uses to them to add a new tier of generator to the end gen list returning the cost of that new tier from the points total
def new_generator(is_free):
    new_gen_number = len(gen_list) + 1
    gen_list.append(Generator(new_gen_number, ascenssion_dict))
    if is_free == True:
        return 0
    elif gen_list[-1].price > upgrade_dict["unlock_bank"].value:
        points_cost = gen_list[-1].price - upgrade_dict["unlock_bank"].value
        upgrade_dict["unlock_bank"].value = 0
        return points_cost
    else:
        upgrade_dict["unlock_bank"].value -= gen_list[-1].price
        return 0

#this resets all aspects of the game except for upgrades unlocked by this function, allowing powerful upgrades at the cost of starting over 
#first it applies these upgrades then dose the reset
def ascend():
    global veriables_dict, ascenssion_dict, upgrade_dict, gen_list
    if veriables_dict["points"] < ascenssion_dict["ascenssion_goal"]:
        raise Exception("not enough points")
        return None
    else:
        print_break()
        print (ascended_askii)
        print_break()
        time.sleep(2)
        ascenssion_dict["ascenssion_goal"] *= 10
        ascenssion_dict["ascenssion_count"] += 1
        if ascenssion_dict["ascenssion_count"] == 1:
            ascenssion_upgrade = first_ascenssion_upgrades[random.randint(0, len(first_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 2:
            ascenssion_upgrade = second_ascenssion_upgrades[random.randint(0, len(second_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 3:
            ascenssion_upgrade = third_ascenssion_upgrades[random.randint(0, len(third_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 4:
            ascenssion_upgrade = forth_ascenssion_upgrades[random.randint(0, len(forth_ascenssion_upgrades) - 1)]
        else:
            ascenssion_upgrade = ascenssion_upgrades[random.randint(0, len(ascenssion_upgrades) - 1)]
        if ascenssion_upgrade == "increase max prestige by 5":
            ascenssion_dict["starting prestige"] += 5
            print_break()
            print (max_prestige_askii)
            print_break()
            print (f"New max prestige is {ascenssion_dict["starting prestige"]}")
            print_break()
            time.sleep(2)
        if ascenssion_upgrade == "increase all upgrades":
            ascenssion_dict["upgrade_scale"] += 5
            print_break()
            print (upgrade_askii)
            print_break()
            print (f"All upgrades starting and max levels increased by 5")
            print_break()
            time.sleep(2)
        if ascenssion_upgrade == "reduce gen price":
            ascenssion_dict["gen_price_upgrade"] += 1
            print_break()
            print (reduced_gen_askii)
            print_break()
            print (f"All Generator prices reduced")
            print_break()
            time.sleep(2)
        if ascenssion_upgrade == "increase gen amount":
            ascenssion_dict["gen_val_upgrade"] += 1
            print_break()
            print (increase_gen_askii)
            print_break()
            print (f"All Generator values increased")
            print_break()
            time.sleep(2)
        if ascenssion_upgrade == "increase starting gen number":
            ascenssion_dict["starting_gen_amount"] *= 2
            print_break()
            print (starting_gen_askii)
            print_break()
            print (f"You start with {ascenssion_dict["starting_gen_amount"]} gens")
            print_break()
            time.sleep(2)
        veriables_dict["max_prestige"] = ascenssion_dict["starting prestige"]
        upgrade_dict = initilise_upgrades()
        gen_list = initilise_gens()
        veriables_dict["points"] = 0 
        veriables_dict["double_gen_ticks"] = 0
        veriables_dict["tickspeed_boost_ticks"] = 0
        save_game()
        return


#when a random event is triggered then roll to decide what level of rarity it will be and pick one of the events from that rarity at random
def random_event_genirator(event_log):
    if veriables_dict["random_event_chance"] < 100:
        veriables_dict["random_event_chance"] += 1
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
    global veriables_dict
    if veriables_dict["double_gen_ticks"] == 0:
        veriables_dict["double_gen_ticks"] = 1
        return "Point gen doubled this tick"
    return None

def tickspeed_boost():
    global veriables_dict
    veriables_dict["tickspeed_boost_ticks"] = 30
    return "Tickspeed increased for 30 ticks"

def points_discount():
    global veriables_dict
    veriables_dict["points_discount_boolean"] = True
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
    global veriables_dict
    veriables_dict["max_prestige"] += 1
    return f"Max prestige increased to {veriables_dict["max_prestige"]}"

def double_gen():
    global veriables_dict
    veriables_dict["double_gen_ticks"] += random.randint(1,10)
    return f"Geniration doubled for {veriables_dict["double_gen_ticks"]} ticks"

def unlock_next_tier():
    new_generator(True)
    return "Next Tier unlocked for free"

#commonly used print
def print_break():
    print ("============================================================")

#this function will go through all the upgrades and try to buy a new tier if possible, reporting it in the event log if it takes place
#trying to buy with a discount first then at full price if discount isn't active
def buy_upgrades(points_discount_boolean, upgrade_dict, event_log):
    global veriables_dict
    if points_discount_boolean == True:
        for upgrade in upgrade_dict:
            if veriables_dict["points"] >= (upgrade_dict[upgrade].price * DISCOUNT) and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
                veriables_dict["points"] = upgrade_dict[upgrade].buy_discount(veriables_dict["points"])
                event_log.append(f"{upgrade_dict[upgrade].name} Upgraded to rank {upgrade_dict[upgrade].tier}")
    else:
        for upgrade in upgrade_dict:
            if veriables_dict["points"] >= upgrade_dict[upgrade].price and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max:
                veriables_dict["points"] = upgrade_dict[upgrade].buy(veriables_dict["points"])
                event_log.append(f"{upgrade_dict[upgrade].name} Upgraded to rank {upgrade_dict[upgrade].tier}")

#buy max of each generator that can be afforded starting with the generator that makes the most points for it cost
#trying to buy with a discount first then at full price if discount isn't active
def buy_gens(points_discount_boolean, gen_list, upgrade_dict):
    global veriables_dict
    if points_discount_boolean == True:
        for gen in (gen_list):
            if veriables_dict["points"] >= gen.price * DISCOUNT:
                buy_amount = int(veriables_dict["points"] // gen.price)
                if upgrade_dict["buy_amount"].tier < buy_amount:
                    buy_amount = upgrade_dict["buy_amount"].tier
                buy_cost = buy_amount * int(gen.price * DISCOUNT)
                for i in range(buy_amount):
                    gen.buy_discount(veriables_dict["points"])
                veriables_dict["points"] -= buy_cost
    else:
        for gen in (gen_list):
            if veriables_dict["points"] >= gen.price:
                buy_amount = int(veriables_dict["points"] // gen.price)
                if upgrade_dict["buy_amount"].tier < buy_amount:
                    buy_amount = upgrade_dict["buy_amount"].tier
                buy_cost = buy_amount * gen.price
                for i in range(buy_amount):
                    gen.buy(veriables_dict["points"])
                veriables_dict["points"] -= buy_cost

#this function prints out the report of what has happened each tick
def print_report(gen_list, event_log, points_spent, points_generated, veriables_dict, upgrade_dict, ascenssion_dict):
    total_gens = 0
    for gen in gen_list:
        total_gens += gen.amount

    highest_gen = gen_list[0]
    
    print_break()

    #this prints events that might not happen every tick
    for event in event_log:
        if event == None:
            pass
        else:
            print (event)

    #this prints the points genirated, points spent if any were, running genirator count, and points total so this statement will print every tick, conditions to keep grama correct and provent empty statements
    if highest_gen.amount == 1:
        if points_spent > 0:
            print(f"{format(points_generated, ",d")} points generated \n{format(points_spent, ",d")} points spent \nYou have {format(total_gens, ",d")} generators, {highest_gen.amount} is a {highest_gen} \nNew Points {format(veriables_dict["points"], ",d")}")
        else:
            print(f"{format(points_generated, ",d")} points generated \nYou have {format(total_gens, ",d")} generators, {highest_gen.amount} is a {highest_gen} \nNew Points {format(veriables_dict["points"], ",d")}") 
    else:
        if points_spent > 0:
            print(f"{format(points_generated, ",d")} points generated \n{format(points_spent, ",d")} points spent \nYou have {format(total_gens, ",d")} generators, {format(highest_gen.amount, ",d")} are {highest_gen}s \nNew Points {format(veriables_dict["points"], ",d")}")
        else:
            print(f"{format(points_generated, ",d")} points generated \nYou have {format(total_gens, ",d")} generators, {format(highest_gen.amount, ",d")} are {highest_gen}s \nNew Points {format(veriables_dict["points"], ",d")}")

    if upgrade_dict["unlock_bank"].value > 0:
        print (f"You have {format(upgrade_dict["unlock_bank"].value, ",d")} points saved to unlock Tier {(len(gen_list) + 1)}")

    #prints the current assesion goal about every 30 seconds bassed off the save countdown to save adding another
    if save_countdown == 1:
        if ascenssion_dict["ascenssion_count"] >= 1:
            print (f"You have ascended {ascenssion_dict["ascenssion_count"]} times \nYou need {format(ascenssion_dict["ascenssion_goal"], ",d")} points to Ascend")
        else:
            print (f"You need {format(ascenssion_dict["ascenssion_goal"], ",d")} points to Ascend")

def main():
    global veriables_dict, save_countdown
    #this try statement is to allow the game to save if "closed" by keyboard interrupt
    try:
        while running == True:
            #this keeps track of any notable events from the tick and reports them at the end
            event_log = []
            #reset any veriables that should only act for one tick
            veriables_dict["points_discount_boolean"] = False
            #random events to stop the game being determanistic
            if random.randint(1, 100) >= veriables_dict["random_event_chance"]:
                event_log = random_event_genirator(event_log)
            #take readings so I can report output changes
            points_generated = 0
            gen_number_start = len(gen_list)
            #generate points for each generator and add 2% of the new points to the upgrade bank, runs a second time if the points genirated are being doubled
            for gen in gen_list:
                veriables_dict["points"] += gen.generate()
                points_generated += gen.generate()
            if veriables_dict["double_gen_ticks"] > 0:
                for gen in gen_list:
                    veriables_dict["points"] += gen.generate()
                    points_generated += gen.generate()
                veriables_dict["double_gen_ticks"] -= 1
            veriables_dict["points"] -= upgrade_dict["unlock_bank"].add_value(int(veriables_dict["points"]/50))
            #ascend if possible
            if veriables_dict["points"] >= ascenssion_dict["ascenssion_goal"]:
                ascend()
                continue
            #take readings for how many points have been genirated then reset point starts to track points spent
            points_start = veriables_dict["points"]
            #prestige a generator if possible
            for gen in gen_list:
                if gen.amount > gen.prestige_cost and gen.prestige < veriables_dict["max_prestige"]:
                    gen_list.append(PrestigedGenerator(gen, ascenssion_dict))
                    gen_list.remove(gen)
                    event_log.append(f"Generator {gen_list[-1].tier} has reached prestige {gen_list[-1].prestige}")
                    gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #unlock new generator if possible
            if veriables_dict["points"] + upgrade_dict["unlock_bank"].value >= int((250 * (math.sqrt((len(gen_list) + 1) ** 1.9))) - 330):
                veriables_dict["points"] -= new_generator(False)
                event_log.append(f"Tier {len(gen_list)} unlocked")
                gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #buy upgrades as they are fewer and more impactful than gens
            buy_upgrades(veriables_dict["points_discount_boolean"], upgrade_dict, event_log)
            #calls the function to buy more of already unlocked genirators
            buy_gens(veriables_dict["points_discount_boolean"], gen_list, upgrade_dict)

            points_spent = points_start - veriables_dict["points"]

            #every tick reduce the time till the next auto save then if enough ticks have passed complete a save
            save_countdown -= 1
            if save_countdown == 0:
                save_game()
                #this sacles with tickspeed to keep the auto saves roughly every 30 seconds
                save_countdown = int(30 + (upgrade_dict["tickspeed"].tier / (1 + (2/3))))
                if save_countdown > 60:
                    save_countdown = 60

            #report what has happened this tick to the player
            print_report(gen_list, event_log, points_spent, points_generated, veriables_dict, upgrade_dict, ascenssion_dict)

            #sleep bassed on if there is a boost event happening, then reducies the time bassed on the tickspeed upgrade with a hard limit to stop the game running too fast
            if veriables_dict["tickspeed_boost_ticks"] > 0:
                if (0.01 * upgrade_dict["tickspeed"].tier) < 0.5:
                    time.sleep(1 - (0.01 * upgrade_dict["tickspeed"].tier)- 0.1)
                    veriables_dict["tickspeed_boost_ticks"] -= 1
                else:
                    time.sleep (0.5 - 0.1)
                    veriables_dict["tickspeed_boost_ticks"] -= 1
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