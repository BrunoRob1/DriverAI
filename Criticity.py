import math

from matplotlib import pyplot as plt
"""
Criticity
Definition : measurement of how dangerous is a situation (state of vehicles (speed, position) at a certain time, knowing
some parameters of the vehicle (brake power, acceleration power).
Vehicles are supposed to be on the same lane, and near each other
"""

"""
Scenario : Vehicle A is behind vehicle B
Distance between veh A and veh B forecasted at time > 0, assuming their acceleration stays constant.
Is a function of vehicle A initial position (y0_A)  and initial speed (v0_A),
and of vehicle B position (yB = 0, stays constant as B is the reference frame) with initial v0_B
"""
# TODO: Vehicle A must be the reference frame
def distance_AB(time, y0_A, v0_A, v0_B, acc_A, acc_B):
    return y0_A + (v0_A - v0_B)*time + 0.5*(acc_A - acc_B)*time*time


"""
Returns the braking that must be applied as a function of the minimum distance predicted by the model
"""
def braking(d_min, d_eq, brake_max, motor_brake):
    return brake_max/(1+(math.exp((d_min-d_eq)/(0.2*d_eq))))


"""
Models of braking willingness vs the distance of a vehicle B in front from ego vehicle (A)
0 : behavior is to tend to our equilibrium speed
1 : braking is applied to avoid potential collision 
"""
def braking_will(d, d_eq):
    return 1 / (1 + math.exp((d - d_eq)/5.0))



def test_plot_distance_AB_predicted(y_A0, v_A0, v_B0, acc_A, acc_B):
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

def test_plot_braking_will(d_eq):
    braking_will_data = []
    distance_data = []
    for i in range(0, 301):
        d = i
        braking_will_data.append(braking_will(d, d_eq))
        distance_data.append(d)
    plt.plot(distance_data, braking_will_data)
    plt.xlabel("distance (m)")
    plt.ylabel("braking will")
    plt.show()


def predict_minimum_distance_AB(y_A0, v_A0, v_B0, acc_A, acc_B):
    delta_v0 = v_A0 - v_B0
    delta_a = acc_A - acc_B
    delta = delta_v0*delta_v0 - 2*delta_a*y_A0

    #test_plot_distance_AB_predicted(y_A0, v_A0, v_B0, acc_A, acc_B)

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
            y_max = distance_AB(t_max, y_A0, v_A0, v_B0, acc_A, acc_B)
            if y_max > 0:
                print("a collision is estimated")
                y_max = 0
            else:
                print("distance minimum with veh B is estimated at :" + str(-y_max))
                y_max = - y_max

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


if __name__ == '__main__':
    y_A0 = -10
    acc_A = -2
    acc_B = 0
    v_A0 = 140 / 3.6
    v_B0 = 120 / 3.6

    predict_minimum_distance_AB(y_A0, v_A0, v_B0, acc_A, acc_B)
    test_function_braking()
    test_plot_braking_will(70)
    # from y_max we should estimate the dangerousness = f(criticity, assessment of driver)