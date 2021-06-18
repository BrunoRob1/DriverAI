import math

from matplotlib import pyplot as plt
"""
Criticity
Definition : measurement of how dangerous is a situation (state of vehicles (speed, position) at a certain time, knowing
some parameters of the vehicle (brake power, acceleration power).
Vehicles are supposed to be on the same lane, and near each other
"""
y_A0 = -10
acc_A = -2
acc_B = 0
v_A0 = 140/3.6
v_B0 = 120/3.6


# distance between veh A and veh B
coord = lambda t: y_A0 + (v_A0 - v_B0)*t + 0.5*acc_A*t*t

coord_data = []
time_data = []

for i in range(0, 201):
    t = i / 20
    coord_data.append(coord(t))
    time_data.append(t)
plt.plot(time_data, coord_data)
plt.show()

delta_v0 = v_A0 - v_B0
delta_a = acc_A - acc_B
delta = delta_v0*delta_v0 - 2*delta_a*y_A0

# Intersection with y = 0 line
if(abs(delta_a) != 0):

    if(delta >= 0):
        t1 = (-delta_v0 + math.sqrt(delta)) / delta_a
        print("t1(z=0)=" + str(t1))
        t2 = (-delta_v0 - math.sqrt(delta)) / delta_a
        print("t2(z=0)=" + str(t2))
    else:
        print("No solutions to y=0!")
else:
    t0 = -y_A0/delta_v0
    print("t(z=0)=" + str(t0))

# we know now how to calculate the time of collision if it exists
# but to get the criticity, the most important information is the y_max
# it can be obtained with dy/dt = 0
if delta_a == 0:
    # curve order 1
    if delta_v0 > 0:
        print("a collision is estimated")
else:
    t_max = -delta_v0/delta_a
    if t_max <= 0:
        print("a collision is estimated")
    else:
        y_max = coord(t_max)
        if y_max > 0:
            print("a collision is estimated")
        else:
            print("distance minimum with veh B is estimated at :" + str(-y_max))

# from y_max we estimate the dangerosity