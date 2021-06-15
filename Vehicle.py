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
        self.v_kmh = velocity_kmh
        self.traffic = traffic  # type: Traffic

        # other variables
        self.constrained = 0    # between 0 and 1
        self.equilibrium_security_time = 1.0
        self.force_security_time = 0.4

    """
    Step : to the next time step t+dt
    """
    def step(self):
        dt = self.traffic.simulation.step_time
        # update of acceleration
        # self.acc = self.acc + ?

        # update of speed
        self.v_mps = self.v_mps + self.acc * dt
        self.v_kmh = self.v_mps * 3.6

        # update of position
        self.pos = self.pos + (self.v_mps - self.traffic.ego.v_mps) * dt

    """
    Is there a vehicle in front of EGO (only if distance < 200m)
    """
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


