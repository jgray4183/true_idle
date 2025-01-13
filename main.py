from objects import Generator, PrestigedGenerator, Upgrade, UpgradeStoreValue
from constants import BASE_PRICE, DISCOUNT, GAME_VERSION
from askii import *
import time
import random
import pickle
import math

#the list of genirators is a core part of the game and needs to be reset by mutiples functions in the game, it is also called when making a save
def initilise_gens(ascenssion_dict):
    gen_list = []
    for i in range(1, ascenssion_dict["starting_gen_amount"] + 1):
        gen_list.append(Generator(i, ascenssion_dict))
    return gen_list

#the dict of upgrades is a core part of the game and needs to be reset by mutiples functions in the game, it is also called when making a save
def initilise_upgrades(ascenssion_dict):
    ascenssion_dict = ascenssion_dict
    upgrade_dict = {"buy_amount" : Upgrade("Buy Amount", ascenssion_dict, 25, 9, 100 + ascenssion_dict["upgrade_scale"]), "tickspeed" : Upgrade("Tickspeed", ascenssion_dict, 100, 100, 25 + ascenssion_dict["upgrade_scale"]), "unlock_bank" : UpgradeStoreValue("Unlock Bank", ascenssion_dict, 250, 7.5, 100 + ascenssion_dict["upgrade_scale"], 50, 5)}
    for upgrade in upgrade_dict:
        upgrade_dict[upgrade].tier += ascenssion_dict["upgrade_scale"]
    return upgrade_dict

#this function will try and convert an old save to work on new versions of the game
def convert_save(save):
    save_version = save[0]
    veriables_dict = save[1]
    ascenssion_dict = save[2]
    gen_list = save[3]
    upgrade_dict = save[4]
    
    #points used to be where save version now is in the save, this converts the old points into a current save version
    points = None
    if save_version > 1:
        points = save[0]
        save_version = GAME_VERSION
    if save_version < GAME_VERSION:
        old_save_version = save_version
        save_version = GAME_VERSION
    
    #this tests if the old save is before save numbers and converts it to the new save format
    if points == int:
        veriables_dict = {"points": save[0], "max_prestige": save[1], "double_gen_ticks": save[2], "tickspeed_boost_ticks": save[3], "points_discount_boolean": save[4], "random_event_chance": 90}
        ascenssion_dict = save[5]
        gen_list = save[6]
        upgrade_dict = save[7]
    
    #this regenirates anything that has been changed since old saves
    for gen in list(gen_list):
        new_gen = Generator(gen.tier, ascenssion_dict)
        for prestige in range(gen.prestige):
            new_gen = PrestigedGenerator(new_gen, ascenssion_dict)
        new_gen.amount = gen.amount
        gen_list.append(new_gen)
        gen_list.remove(gen)
    upgrade_dict_new = initilise_upgrades(ascenssion_dict)
    for upgrade in upgrade_dict_new:
        upgrade_dict_new[upgrade].tier = upgrade_dict[upgrade].tier
        for i in range (upgrade_dict_new[upgrade].tier):
            upgrade_dict_new[upgrade].price *= upgrade_dict_new[upgrade].multiplier
    #upgrades that hold value have extra veriables that need to be recaluculated
    for i in range(upgrade_dict_new["unlock_bank"].tier):
        upgrade_dict_new["unlock_bank"].max_value *= upgrade_dict_new["unlock_bank"].multipler_value
    if upgrade_dict["unlock_bank"].value >= upgrade_dict_new["unlock_bank"].max_value:
        upgrade_dict["unlock_bank"].value = upgrade_dict_new["unlock_bank"].value
    else:
        upgrade_dict_new["unlock_bank"].value = upgrade_dict_new["unlock_bank"].max_value
    #changes the original upgrade dict to the new one
    upgrade_dict = upgrade_dict_new
    
    #repaack and return the save
    save = [save_version, veriables_dict, ascenssion_dict, gen_list, upgrade_dict]
    return save
    
#this function tests that the save is one that will be compatable with the game
def interrupt_save(save):
    #first test if the save has the right amount of items in it and that its compatable with the current version of the game
    if len(save) == 5 and save[0] == GAME_VERSION:
        return save
    #if no save exists then create one
    elif len(save) == 0:
        save_version = GAME_VERSION
        veriables_dict = {"points": 0, "max_prestige": 5, "double_gen_ticks": 0, "tickspeed_boost_ticks": 0, "points_discount_boolean": False, "random_event_chance": 90}
        ascenssion_dict = {"ascenssion_count" : 0, "ascenssion_goal" : 100000, "starting prestige" : 5, "upgrade_scale" : 0, "gen_price_upgrade" : 1, "gen_val_upgrade" : 1, "starting_gen_amount" : 1}
        gen_list =  initilise_gens(ascenssion_dict)
        upgrade_dict = initilise_upgrades(ascenssion_dict)
        save = [save_version, veriables_dict, ascenssion_dict, gen_list, upgrade_dict]
        return save
    #this first gives the player a chance to try and convert an old save to a new save, if they don't they will need to delete there save and run the game again
    else:
        print ("Old save detected, do you want to try and convert to current build? (Not the best experiance, quite buggy)\n Y/N")
        save_convert_answer = input()
        print (save_convert_answer)
        if save_convert_answer.startswith("y") or save_convert_answer.startswith("Y"):
            save = convert_save(save)
            #test the save that was genirated again using recusion to make sure this was sussecul
            return interrupt_save(save)
        elif save_convert_answer.startswith("n") or save_convert_answer.startswith("N"):
            print ("Do you want to reset your save to play the new version?\n Y/N")
            reset_answer = input()
            if reset_answer.startswith("y") or reset_answer.startswith("Y"):
                save = []
                return interrupt_save(save)
            elif reset_answer.startswith("n") or reset_answer.startswith("N"):
                raise Exception("Incompatable save")
            else:
                raise Exception("Invalid answer")
                return interrupt_save(save)
        else:
            raise Exception("Invalid answer")
            return interrupt_save(save)


#if a save exists import it otherwise allow a new save to be genirated
save = []
try:
    with open("save.pkl", "rb") as fp:
        save = pickle.load(fp)
except Exception as e:
    pass

#call the function to make sure a full compatable save will be loaded
save = interrupt_save(save)

#set the veriables stored in the save at global scope
save_version = save[0]
veriables_dict = save[1]
ascenssion_dict = save[2]
gen_list = save[3]
upgrade_dict = save[4]

#establish anything not saved
random.seed()
running = True
save_countdown = 30
event_log = []

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

#this function takes the amount of points and amount of points in the unlock bank upgrade and uses to them to add a new tier of generator to the end gen list returning the amount that needs to be deducted from points
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
        #bad luck protection is in place to make sure an even amount of certan upgrades are aquired early in the game
        #this is done by testing the ascenssion that is taking place and then calling a reduced amount of options for the upgrade
        if ascenssion_dict["ascenssion_count"] == 1:
            ascenssion_upgrade = first_ascenssion_upgrades[random.randint(0, len(first_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 2:
            ascenssion_upgrade = second_ascenssion_upgrades[random.randint(0, len(second_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 3:
            ascenssion_upgrade = third_ascenssion_upgrades[random.randint(0, len(third_ascenssion_upgrades) - 1)]
        elif ascenssion_dict["ascenssion_count"] == 4:
            ascenssion_upgrade = forth_ascenssion_upgrades[random.randint(0, len(forth_ascenssion_upgrades) - 1)]
        #if bad luck protection is over it calls a full list of all avalable upgrades
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
        upgrade_dict = initilise_upgrades(ascenssion_dict)
        gen_list = initilise_gens(ascenssion_dict)
        veriables_dict["points"] = 0 
        veriables_dict["double_gen_ticks"] = 0
        veriables_dict["tickspeed_boost_ticks"] = 0
        veriables_dict["random_event_chance"] = 95
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
        if upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max_tier:
            valid_upgrade = True
    if valid_upgrade == False:
        return "No upgrades"
    random_upgrade = random.randint(0,len(upgrade_dict) - 1)
    for i, key in enumerate(upgrade_dict.keys()):
        if i == random_upgrade:
            random_upgrade = key
    if upgrade_dict[random_upgrade].tier >= upgrade_dict[random_upgrade].max_tier:
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
            if veriables_dict["points"] >= (upgrade_dict[upgrade].price * DISCOUNT) and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max_tier:
                veriables_dict["points"] = upgrade_dict[upgrade].buy_discount(veriables_dict["points"])
                event_log.append(f"{upgrade_dict[upgrade].name} Upgraded to rank {upgrade_dict[upgrade].tier}")
    else:
        for upgrade in upgrade_dict:
            if veriables_dict["points"] >= upgrade_dict[upgrade].price and upgrade_dict[upgrade].tier < upgrade_dict[upgrade].max_tier:
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

#this function takes the event log and tests if the event is a Generator prestiging by looking if the first word is "Generator"
#then if more than 5 Generators have presteged in one tick it will replace all those messages with one message reporting how many presteged and how many got to the highest tier reached that tick
def reduce_prestige_events(event_log):
    prestige_count = 0
    prestige_log = {}
    for i in range(1, veriables_dict["max_prestige"] + 1):
        prestige_log[f"{i}"] = 0
    for event in event_log:
        event_local = event.split()
        if event_local[0] == "Generator":
            prestige_count += 1
            prestige_log[event_local[-1]] += 1
    if prestige_count >= 4:
        for event in list(event_log):
            event_local = event.split()
            if event_local[0] == "Generator":
                event_log.remove(event)
        for key, value in dict(prestige_log).items():
            if value == 0:
                del prestige_log[key]
        event_log.append(f"{prestige_count} Generators have prestiged, {list(prestige_log.values())[-1]} of them reached prestige {list(prestige_log)[-1]}")
    return event_log

#this function prints out the report of what has happened each tick
def print_report(gen_list, event_log, points_spent, points_generated, veriables_dict, upgrade_dict, ascenssion_dict):
    total_gens = 0
    for gen in gen_list:
        total_gens += gen.amount

    highest_gen = gen_list[0]
    
    print_break()

    #reduce amount of messages in event log if too many gens prestiged at once
    event_log = reduce_prestige_events(event_log)

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

    #prints the current assesion goal about every 30 seconds bassed off the save countdown to save adding another veriable
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
            #reset part of the game that should only be held for one tick
            event_log = []
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
                    event_log.append(f"Generator {format(gen_list[-1].tier, ",d")} has reached prestige {format(gen_list[-1].prestige, ",d")}")
                    gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #unlock new generator if possible
            if veriables_dict["points"] + upgrade_dict["unlock_bank"].value >= int((250 * (math.sqrt((len(gen_list) + 1) ** 1.9))) - 330):
                veriables_dict["points"] -= new_generator(False)
                event_log.append(f"Tier {format(len(gen_list), ",d")} unlocked")
                gen_list.sort(key=lambda gens:gens.gen_price_ratio)
            #buy upgrades as they are fewer and more impactful than gens
            buy_upgrades(veriables_dict["points_discount_boolean"], upgrade_dict, event_log)
            #calls the function to buy more of already unlocked genirators
            buy_gens(veriables_dict["points_discount_boolean"], gen_list, upgrade_dict)
            #takes a reading of how many points have been spent for the logs
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