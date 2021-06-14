class Input:
    def __init__(self, type):
        self.type = type
        self.value = 0


class Algorithm:
    @staticmethod
    def evaluate_overtake_duration(speed_overtaker, y_overtaker, speed_overtaken, y_overtaken):
        # after overtake, braking distance to leave to overtaken car
        braking_distance = speed_overtaken # m.s-1
        delta_v = speed_overtaker - speed_overtaken
        overtake_duration = (y_overtaken - y_overtaker + braking_distance) / delta_v

        return overtake_duration

    @staticmethod
    def evaluate_min_speed_loss_for_overtaker(overtake_time_predicted, overtake_time_realized, y_overtaker_init, y_overtaker_end):
        d = y_overtaker_end - y_overtaker_init
        v_predicted = d / overtake_time_predicted
        v_realized = d / overtake_time_realized
        speed_loss = v_predicted - v_realized
        return speed_loss


class Neuron:
    def __init__(self):
        self.inputs = []    # type: Input
        self.output = []
        # reasons of goal not implemented for the moment
        self.goal = None
        self.weights = {}


    # to add new parameter to take into account for decision
    def add_input(self, input_type):
        pass

    def delete_input(self, input_to_delete):
        pass

    def calculate_output(self):
        pass

    def on_goal_changed(self):
        pass