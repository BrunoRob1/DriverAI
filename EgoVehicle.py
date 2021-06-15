import Vehicle as Veh


class EgoVehicle(Veh.Vehicle):
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


