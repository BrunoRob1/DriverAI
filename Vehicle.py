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
        self.v_mps_eq = self.v_mps
        self.v_kmh = velocity_kmh
        self.traffic = traffic  # type: Traffic

        # other variables
        self.constrained = 0    # between 0 and 1
        self.equilibrium_security_time = 1.0    # for the current driver
        self.critical_security_time = 0.3
        self.current_security_time = 0

        # vehicle characteristics
        self.max_braking_acc = -6/3.6
        self.motor_brake_acc = -1.5/3.6
        self.acc_max = 3

        # vehicles monitored
        self.index_in_front = -1

    """
    Step : to the next time step t+dt
    """
    def step(self):
        dt = self.traffic.simulation.step_time
        # update of acceleration
        # self.acc = self.acc + ?
        if self.is_there_a_vehicle_in_front():
            self.index_in_front = self.index_of_front_vehicle()
            distance_to_front_veh = self.distance_to_front_vehicle()
            self.current_security_time = distance_to_front_veh / self.v_mps
        else:
            self.current_security_time = 0
            self.index_in_front = -1

        self.compute_acceleration()

        # update of speed
        self.v_mps = self.v_mps + self.acc * dt
        self.v_kmh = self.v_mps * 3.6

        # update of position
        self.pos = self.pos + (self.v_mps - self.traffic.vehicles[0].v_mps) * dt

    def compute_acceleration(self):
        def engine_braking():
            self.acc = self.motor_brake_acc

        def max_brake():
            self.acc = self.max_braking_acc

        def no_braking():
            self.acc = 0

        # y0: my position; v0: my speed
        # y1: position vehicle in front of me
        # y2: speed vehicle in front of me
        def time_before_collision(y0, v0, y1, v1):
            if v0 <= v1:
                return -1
            else:
                return (y1-y0)/(v1-v0)

        # simulate delay time of collision --> real parameter!
        cst = self.current_security_time

        if self.is_there_a_vehicle_in_front():
            veh_in_front_speed = self.traffic.vehicles[self.index_in_front].v_mps
            my_v_mps = self.v_mps
            veh_in_front_position = self.traffic.vehicles[self.index_in_front].pos
            my_position = self.pos

            time_of_collision = time_before_collision(my_position, my_v_mps, veh_in_front_position, veh_in_front_speed)

            if cst < self.equilibrium_security_time:
                # no collision anticipated
                if time_of_collision < 0:
                    engine_braking()
                elif time_of_collision < 2:
                    # collision in less than 2 seconds --> max brake
                    max_brake()
                elif time_of_collision < 6:
                    # collision in between 2 and 6 seconds --> continuum between motor brake and max brake
                    self.acc = self.max_braking_acc - \
                               (time_of_collision - 2) / 4 * (self.max_braking_acc - self.motor_brake_acc)
                elif time_of_collision < 20:
                    # above 6 seconds, motor brake
                    engine_braking()
                else:
                    no_braking()
            else:
                no_braking()

        def accelerate():
            v = self.v_mps
            v_eq = self.v_mps_eq
            acc_max = self.acc_max
            self.acc = max(2, abs(v - v_eq) * 0.3)
            self.acc = min(self.acc, acc_max)

        if self.acc == 0 and self.v_mps < self.v_mps_eq:
            accelerate()


    """
    Is there a vehicle in front of vehicle (only if distance < 200m)
    """
    def is_there_a_vehicle_in_front(self):
        vehicles = self.traffic.vehicles.values()
        print(len(vehicles))
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
        veh_indexes = self.traffic.vehicles.keys()
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
        veh_indexes = self.traffic.vehicles.keys()
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


