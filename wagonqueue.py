import time
import traindata
import random


def timer():  # a 10 second timer
    start = time.time()
    time.process_time()
    elapsed = 0
    while elapsed < random.random():
        elapsed = time.time() - start
        print(elapsed)
        time.sleep(1)
    return True


def create_wagonqueue():
    wagontypes = [traindata.FirstClass(), traindata.SecondClass(), traindata.OnboardBistro()]
    wagonqueue = [random.choice(wagontypes)]

    while len(wagonqueue) < 20:
        if timer() is True:
            randomwagon = random.choice(wagontypes)
            print(str(randomwagon))
            wagonqueue.append(randomwagon)

        else:
            print("Timer Error")
            wagonqueue.append(random.choice(wagontypes))  # So the game can contine even if there is a timer error
    else:
        print("You lost!")
