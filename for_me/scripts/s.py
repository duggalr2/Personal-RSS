import sched, time
s = sched.scheduler(time.time, time.sleep)


def do_something():
    print("Doing stuff...")
    # do your stuff


def y():
    s.enter(2, 1, do_something) # this is what actually calls the function over and over again..

s.enter(2, 1, y) # this is executed once in the beginning
s.run()