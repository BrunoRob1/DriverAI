import math

import numpy as np
from matplotlib import pyplot as plt


from Vehicle import *
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_curves(t, y1, y2):
    plt.plot(t, y1, 'r')
    plt.plot(t, y2, 'b')
    plt.show()


def test_omega_veh_lane3_overtake_ego_lane2():
    simulation = Simulation()
    simulation.init_time()

    # Ego vehicle in the lane 2 (middle) in a highway
    simulation.get_traffic().set_ego(2, 120)

    # Vehicle in lane 3 (left) overtakes Ego vehicle in that highway
    simulation.get_traffic().add_vehicle(3, -50, 140, index=1)

    time = []
    y0 = []
    vy0 = []
    omega0 = np.zeros(0)
    y1 = []
    vy1 = []
    omega_higher_than_threshold = []

    for i in range(200):
        ang_speed = simulation.get_traffic().angular_speed_of_vehicle_from_ego(1)*180/math.pi
        time.append(simulation.time)
        omega0 = np.append(omega0, ang_speed)
        if ang_speed >= 0.5:
            omega_higher_than_threshold.append(1)
        else:
            omega_higher_than_threshold.append(0)

        y0.append(simulation.get_traffic().get_vehicle(0).pos)
        vy0.append(simulation.get_traffic().get_vehicle(0).velocity_kmh())

        y1.append(simulation.get_traffic().get_vehicle(1).pos)
        vy1.append(simulation.get_traffic().get_vehicle(1).velocity_kmh())
        simulation.step()

    print_curves(time, omega_higher_than_threshold, np.log(omega0))


def test_front_vehicle():
    simulation = Simulation()
    simulation.init_time()

    # Ego vehicle in the lane 2 (middle) in a highway
    simulation.get_traffic().set_ego(2, 120)

    # Vehicle in lane 3 (left) overtakes Ego vehicle in that highway
    simulation.get_traffic().add_vehicle(2, -300, 140, index=1)




if __name__ == '__main__':
    test_omega_veh_lane3_overtake_ego_lane2()


