import math


class Vehicle:
    def __init__(self, index, lane, relative_pos, velocity_kmh, traffic):
        # physical variables
        self.length = 4.5
        self.width = 1.9

        self.acc = 0
        self.id = index
        self.lane = lane
        self.pos = relative_pos
        self.v_mps = velocity_kmh / 3.6
        self.traffic = traffic

        # other variables
        self.constrained = 0    # between 0 and 1
        self.equilibrium_security_time = 1.0
        self.force_security_time = 0.4

    def step(self):
        dt = self.traffic.simulation.step_time
        # update of acceleration
        # self.acc = self.acc + ?

        # update of speed
        self.v_mps = self.v_mps + self.acc * dt

        # update of position
        self.pos = self.pos + (self.v_mps - self.traffic.ego.v_mps) * dt

    def is_there_a_vehicle_in_front(self):
        vehicles = self.traffic.vehicles.values
        count = 0
        for veh in vehicles:
            if veh.lane == self.lane:
                distance = veh.pos - self.pos
                if (distance < 200) and (distance > 0):
                    count += 1
        if count > 0:
            return True
        return False

    def distance_to_front_vehicle(self):
        veh_indexes = self.traffic.vehicles.keys
        index_front = []
        distance_front = 500
        for index in veh_indexes:
            vehicle = self.traffic.vehicles[index]  # type: Vehicle
            if vehicle.lane == self.lane:
                distance = vehicle.pos - self.pos
                if (distance < 200) and (distance > 0):
                    if distance < distance_front:
                        distance_front = distance
        return distance_front

    def index_of_front_vehicle(self):
        veh_indexes = self.traffic.vehicles.keys
        index_front = []
        distance_front = 500
        for index in veh_indexes:
            vehicle = self.traffic.vehicles[index]  # type: Vehicle
            if vehicle.lane == self.lane:
                distance = vehicle.pos - self.pos
                if (distance < 200) and (distance > 0):
                    if distance < distance_front:
                        index_front = index
        return index_front

    def get_position(self):
        return self.pos

    def get_velocity(self):
        return self.v_mps

    def velocity_kmh(self):
        return self.v_mps * 3.6

    def print_position_and_speed(self):
        return str(self.pos) + ";" + str(self.velocity_kmh())


class EgoVehicle(Vehicle):
    def __init__(self, lane, velocity, traffic):
        super().__init__(0, lane, 0, velocity, traffic)

    def angular_speed_of_vehicle_from_ego(self, vehicle_id):
        if vehicle_id == 0:
            print("Vehicle ID cannot be Ego Id")
            return 0

        highway_lane_width: float
        # highway lane width = 3.5m
        highway_lane_width = 3.5
        y = self.traffic.vehicles[vehicle_id].pos
        v_y = (self.traffic.vehicles[vehicle_id].v_mps - self.v_mps)
        lane_b = self.traffic.vehicles[vehicle_id].lane
        lane_a = self.lane
        delta_lane = lane_b - lane_a
        if delta_lane == 0:
            return 0
        elif delta_lane > 0:
            return v_y * highway_lane_width / (y * y + highway_lane_width * highway_lane_width)
        elif delta_lane < 0:
            # Omega = Vy * w/(y²+w²)
            return - v_y * highway_lane_width / (y * y + highway_lane_width * highway_lane_width)


class Traffic:
    def __init__(self, simulation):
        self.simulation = simulation
        self.vehicles = {}  # type: dict[Vehicle]
        self.ego = None     # type: EgoVehicle

    def set_ego(self, lane, velocity):
        self.ego = EgoVehicle(lane, velocity)

    def add_vehicle(self, lane, relative_pos, velocity):
        index = len(self.vehicles)
        index = max(index, 1)   # index=0 is booked for ego vehicle
        new_vehicle = Vehicle(index, lane, relative_pos, velocity, self)
        self.vehicles[index] = new_vehicle

    def add_vehicle(self, lane, relative_pos, velocity, index):
        if index == 0:
            print("Index cannot be 0")
        else:
            new_vehicle = Vehicle(index, lane, relative_pos, velocity)
            self.vehicles[index] = new_vehicle

    def get_vehicle(self, index):
        if index == 0:
            return self.ego
        else:
            return self.vehicles[index]



class Output:
    def __init__(self, name, pointed_variable):
        self.name =
        self.pointed_variable = pointed_variable
        self.values = []

    def print(self):
        self.values.append(self.pointed_variable)



class Simulation:
    def __init__(self):
        self.step_time = 0.1
        self.time = None
        self.traffic = Traffic(self)     # type: Traffic
        self.outputs = []   #type: Output

    def get_traffic(self):
        return self.traffic

    def add_output(self, name, variable):
        new_output = Output(name, variable)
        self.outputs.append(new_output)

    def init_time(self):
        self.time = 0

    def step(self):
        dt = self.step_time
        self.time = self.time + dt
        # update position of vehicles
        for veh in self.traffic.vehicles.values():
            veh.step()

        # check if we need to add vehicles as input
        min_angular_speed_detectable = 0.01
        for index in self.traffic.vehicles.keys():
            vehicle = self.traffic.vehicles[index]
            if self.traffic.ego.angular_speed_of_vehicle_from_ego(index) > min_angular_speed_detectable:
                pass # vehicle is in neuron inputs

    def print(self):
        for output in self.outputs:
            output.print()
