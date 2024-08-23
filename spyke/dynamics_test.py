from dynamics import Counter


c = Counter(0, 1)
assert c.time_step == 0 and c.step == 1
c.update()
assert c.get_current_time_step == 1 and c.step == 1
c.update()
assert c.get_current_time_step == 2 and c.step == 1


c = Counter(-2, 2)
assert c.get_current_time_step == -2 and c.step == 2
c.update()
assert c.get_current_time_step == 0 and c.step == 2