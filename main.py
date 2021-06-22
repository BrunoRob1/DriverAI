import math
import numpy as np
from matplotlib import pyplot as plt

from Simulation import *
from Vehicle import *
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_curves(t, y1, y2):
    plt.plot(t, y1, 'r')
    plt.plot(t, y2, 'b')
    plt.show()

def print_curve(t, y):
    plt.plot(t, y, 'b')
    plt.show()


def test_omega_veh_lane3_overtake_ego_lane2():
    simulation = Simulation()

    # Ego vehicle in the lane 2 (middle) in a highway
    simulation.get_traffic().set_ego(2, 120)

    # Vehicle in lane 3 (left) overtakes Ego vehicle in that highway
    simulation.get_traffic().add_vehicle(3, -50, 140, index=1)

    omega_higher_than_threshold = []
    omega0 = np.zeros(0)

    for i in range(0, 201):
        ang_speed = simulation.get_traffic().get_vehicles[0].angular_speed_of_vehicle_from_ego(1)*180/math.pi
        omega0 = np.append(omega0, ang_speed)
        if ang_speed >= 0.5:
            omega_higher_than_threshold.append(1)
        else:
            omega_higher_than_threshold.append(0)
        if i > 0:
            simulation.step()
            simulation.print_outputs()

    print_curves(simulation.time_values, omega_higher_than_threshold, np.log(omega0))


def test_front_vehicle_same_speed():
    simulation = Simulation()
    # Ego vehicle in the lane 2 (middle) in a highway
    simulation.get_traffic().set_ego(2, 120)

    # Vehicle in lane 3 (left) overtakes Ego vehicle in that highway
    def security_distance(speed_kmh):
        return speed_kmh/3.6 + 4.5

    simulation.get_traffic().add_vehicle(2, -security_distance(120)*0.2, 128, index=1)

    simulation.add_output("EGO.y", "simulation.get_traffic().get_vehicle(0).pos")
    simulation.add_output("EGO.Vy", "simulation.get_traffic().get_vehicle(0).v_kmh")

    simulation.add_output("VEH1.y", "simulation.get_traffic().get_vehicle(1).pos")
    simulation.add_output("VEH1.Vy", "simulation.get_traffic().get_vehicle(1).v_kmh")

    simulation.add_output("VEH1.security_time", "simulation.get_traffic().get_vehicle(1).current_security_time")

    simulation.print_outputs()

    for i in range(200):
        simulation.step()
        simulation.print_outputs()

    t = simulation.time_values

    print_curves(t, simulation.get_output("VEH1.y"), simulation.get_output("EGO.y"))
    print_curves(t, simulation.get_output("VEH1.Vy"), simulation.get_output("EGO.Vy"))
    print_curve(t, simulation.get_output("VEH1.security_time"))

    print("end of simulation")


def distance_criticity():
    critic = lambda d:  1/(1+math.exp(-d-5))
    criticity_data = []
    distance_data = []
    for i in range(-201, 1):
        d = i/20
        criticity_data.append(critic(d))
        distance_data.append(d)
    plt.plot(distance_data, criticity_data)
    plt.show()


if __name__ == '__main__':
    #test_omega_veh_lane3_overtake_ego_lane2()
    test_front_vehicle_same_speed()
    #distance_criticity()


