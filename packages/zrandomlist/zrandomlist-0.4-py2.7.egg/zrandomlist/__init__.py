import random

def randList():
    """ This method will return a list 
    of 7 random numbers between 1 and 50.
    That's all!!
    """
    return [random.randint(1,50) for _ in range(7)]

