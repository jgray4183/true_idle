from objects import *
from constants import BASE_PRICE
import time

points = 0 
running = True
gen_list =  [Genirator(1)]

def new_genirator(points):
    new_gen_number = len(gen_list)
    gen_list.append(Genirator(new_gen_number))
    points -= BASE_PRICE * new_gen_number

def main():
    global points
    while running == True:
        for gen in gen_list:
            points += gen.genirate()
        if points >= (len(gen_list) + 1) * 10:
            new_genirator(points)
        for gen in gen_list:
            if points >= gen.price:
                points = gen.buy(points)
    
        print(f"New Points {points}")

        time.sleep(1)

if __name__ == "__main__":
    main()