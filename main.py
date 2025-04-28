import simpy
import random

# Global variables
eventLog = []
waitingShoppers = []
idleTime = 0

# Shopper process
def shopper(env, id):
    arrive = env.now
    items = random.choices([5, 10, 15, 20], weights=[1, 3, 3, 1])[0]  # weighted random
    shoppingTime = (items // 2) + random.randint(-1, 1)  # slight shopping randomness
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

# Checker process
def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)  # wait 1 minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1  # 10 items per minute, at least 1 min
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

# Customer arrival process
def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(random.randint(1, 2))  # customers arrive every 1–2 minutes

# Process results
def processResults():
    totalWait = 0
    totalShoppers = len(eventLog)

    for e in eventLog:
        waitTime = e[4] - e[3]
        totalWait += waitTime

    avgWait = totalWait / totalShoppers


    print(f"The Average wait time was {avgWait:.2f} minutes")
    print(f"The Total idle time was {idleTime} minutes")

# Main function
def main():
    global numberCheckers
    numberCheckers = 2  # 1 checker

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180)  # 3 hours

    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()
