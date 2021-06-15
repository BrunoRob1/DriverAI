from Vehicle import *
from Output import *
from Traffic import *


class Simulation:
    def __init__(self):
        self.step_time = 0.1
        self.time_values = []
        self.current_time = 0
        self.traffic = Traffic(self)    # type: Traffic
        self.outputs = {}               # type: Output

        self.time_values.append(self.current_time)

    def get_traffic(self):
        return self.traffic

    def add_output(self, name, variable):
        new_output = Output(name, variable, self)
        self.outputs[name] = new_output

    def get_output(self, name):
        return self.outputs[name].get_values()

    def init_time(self):
        self.current_time = 0

    def step(self):
        dt = self.step_time
        self.time_values.append(self.current_time)
        self.current_time = self.current_time + dt
        # update position of vehicles
        for veh in self.traffic.vehicles.values():
            veh.step()

        # check if we need to add vehicles as input
        min_angular_speed_detectable = 0.01
        for index in self.traffic.vehicles.keys():
            vehicle = self.traffic.vehicles[index]
            if self.traffic.ego.angular_speed_of_vehicle_from_ego(index) > min_angular_speed_detectable:
                pass # vehicle is in neuron inputs

    def print_outputs(self):
        for output in self.outputs.values():
            output.print()
