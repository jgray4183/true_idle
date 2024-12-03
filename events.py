import random
from main import new_generator

ultra_rare_events = {"increase max pristege", "double gen for rounds", "unlock next tier"}
medium_rare_events = {"free upgrade", "free gens", "double savings"}
normal_rare_events = {"points discount", "tickspeed boost", "double points"}

#when a random event is triggered then roll to decide what level of raity it will be and pick one of the events from that raritys set by cycling through the set and taking the last one to be assiged
def random_event_genirator(event_log):
        event = None
        roll = random.randint(1, 100)
        if roll >= 90:
                for events in ultra_rare_events:
                        event = events
                if event == "increase max pristege":
                        event_log.append(increase_max_pristege())
                if event == "double gen for rounds":
                        event_log.append(double_gen())
                if event == "unlock next tier":
                        event_log.append(unlock_next_tier())
        if roll >= 60 and roll < 90:
                for events in medium_rare_events:
                        event = events
                if event == "free upgrade":
                        event_log.append(free_upgrade())
                if event == "free gens":
                        event_log.append(free_gens())
                if event == "double savings":
                        event_log.append(double_savings())
        if roll < 60:
                for events in normal_rare_events:
                        event = events
                if event == "points discount":
                        event_log.append(points_discount())
                if event == "tickspeed boost":
                        event_log.append(tickspeed_boost())
                if event == "double points":
                        event_log.append(double_points())
        return event_log

#these functions are to resolve the random events but should also be able to be implimented elsewhere if needed

def double_points():
        points *= 2
        return "Points doubled"

def tickspeed_boost():
        tickspeed_boost_ticks = 30
        return "Tickspeed increased for 30 ticks"

def points_discount():
        points_discount_boolean = True
        return "Costs discounted this tick"

def free_upgrade():
        valid_upgrade = False
        for upgrade in upgrade_dict:
                if upgrade.tier < upgrade.max:
                        valid_upgrade = True
        if valid_upgrade == False:
                return None
        upgrade = upgrade_dict[random.randint(len(upgrade_dict))]
        if upgrade.tier >= upgrade.max:
                free_upgrade()
        upgrade_dict[upgrade].tier += 1
        return f"{upgrade} tier increased for free"

def free_gens():
        for gen in gen_list:
                gen.amount += int(gen.amount * 1.1 // 1)
        return "All gen amounts increased by 10%"

def double_savings():
        upgrade_dict["unlock_bank"].add_value(upgrade_dict["unlock_bank"].value)
        return "Savings doubled"

def increase_max_pristege():
        max_pristege += 1
        return "Max Pristege increased by 1"

def double_gen():
        double_gen_ticks += random.randint(1,10)
        return f"Geniration doubled for {double_gen_ticks} ticks"

def unlock_next_tier():
        new_generator(float('inf'))
        return "Next Tier unlocked for free"
