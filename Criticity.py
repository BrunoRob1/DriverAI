import math

from matplotlib import pyplot as plt
"""
Criticity
Definition : measurement of how dangerous is a situation (state of vehicles (speed, position) at a certain time, knowing
some parameters of the vehicle (brake power, acceleration power).
Vehicles are supposed to be on the same lane, and near each other
"""



# scenario : Vehicle A is behind vehicle B
# distance between veh A and veh B forecasted at time > 0 if their acceleration stays constant
# is a function of initial position y0_A of vehicle A and its initial speed v0_A,
# behind vehicle B (y0 = 0) with initial v0_B
def distance_AB(time, y0_A, v0_A, v0_B, acc_A, acc_B):
    return y0_A + (v0_A - v0_B)*time + 0.5*(acc_A - acc_B)*time*time


def braking(d_min, d_eq, brake_max, motor_brake):
    return (brake_max - motor_brake)/(1+(math.exp((d_min-d_eq)/(0.2*d_eq)))) + motor_brake


def plot_distance_AB_forecasted(y_A0, v_A0, v_B0, acc_A, acc_B):
    coord_data = []
    time_data = []
    for i in range(0, 201):
        t = i / 20
        coord_data.append(distance_AB(t, y_A0, v_A0, v_B0, acc_A, acc_B))
        time_data.append(t)
    plt.plot(time_data, coord_data)
    plt.xlabel("time (sec)")
    plt.ylabel("distance A-B")
    plt.show()


def forecast_minimum_distance_AB(y_A0, v_A0, v_B0, acc_A, acc_B):
    delta_v0 = v_A0 - v_B0
    delta_a = acc_A - acc_B
    delta = delta_v0*delta_v0 - 2*delta_a*y_A0

    estimated_time = None
    # Intersection with y = 0 line
    if abs(delta_a) != 0:

        if delta >= 0:
            t1 = (-delta_v0 + math.sqrt(delta)) / delta_a
            print("t1(z=0)=" + str(t1))
            t2 = (-delta_v0 - math.sqrt(delta)) / delta_a
            print("t2(z=0)=" + str(t2))
            if t1 > 0:
                estimated_time = t1
            elif t2 > 0:
                estimated_time = t2
        else:
            print("No solutions to y=0!")
    else:
        t0 = -y_A0/delta_v0
        print("t(z=0)=" + str(t0))
        estimated_time = t0

    # we know now how to calculate the time of collision if it exists
    # but to get the criticity, the most important information is the y_max
    # it can be obtained with dy/dt = 0
    y_max = None
    if delta_a == 0:
        # curve order 1
        if delta_v0 > 0:
            print("a collision is estimated")
            y_max = 0
    else:
        t_max = -delta_v0/delta_a
        if t_max <= 0:
            print("a collision is estimated")
            y_max = 0
        else:
            y_max = distance_AB(t, y_A0, v_A0, v_B0, acc_A, acc_B)
            if y_max > 0:
                print("a collision is estimated")
                y_max = 0
            else:
                print("distance minimum with veh B is estimated at :" + str(-y_max))
            return math.abs(y_max)

    return y_max, estimated_time

def test_function_braking():
    distances = []
    braking_list = []
    for i in range(0, 201):
        d_min = i*0.3
        distances.append(d_min)
        braking_list.append(braking(d_min, 15, -8, -1.5))
    plt.plot(distances, braking_list)
    plt.xlabel("min distance estimated")
    plt.ylabel("braking (km/h)")
    plt.xlim(0, 20)
    plt.show()


print(braking(15, 15, 8, 1.5))


if __name__ == '__main__':
    y_A0 = -10
    acc_A = -2
    acc_B = 0
    v_A0 = 140 / 3.6
    v_B0 = 120 / 3.6

    #forecast_minimum_distance_AB(y_A0, v_A0, v_B0, acc_A, acc_B)
    test_function_braking()
    # from y_max we should estimate the dangerousness = f(criticity, assessment of driver)