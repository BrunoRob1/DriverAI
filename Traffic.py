from Vehicle import *


class Traffic:
    def __init__(self, simulation):
        self.simulation = simulation
        self.vehicles = {}  # type: dict[Vehicle]

    def set_ego(self, lane, velocity):
        import EgoVehicle
        self.vehicles[0] = EgoVehicle.EgoVehicle(lane, velocity, self)

    def add_vehicle(self, lane, relative_pos, velocity):
        index = len(self.vehicles)
        index = max(index, 1)   # index=0 is booked for ego vehicle
        new_vehicle = Vehicle(index, lane, relative_pos, velocity, self)
        self.vehicles[index] = new_vehicle

    def add_vehicle(self, lane, relative_pos, velocity, index):
        if index == 0:
            print("Index cannot be 0")
        else:
            new_vehicle = Vehicle(index, lane, relative_pos, velocity, self)
            self.vehicles[index] = new_vehicle

    def get_vehicle(self, index):
        return self.vehicles[index]