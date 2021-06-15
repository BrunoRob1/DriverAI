class Output:
    def __init__(self, name, pointed_variable, simulation):
        self.name = name
        self.pointed_variable = pointed_variable
        self.values = []
        self.simulation = simulation

    def get_values(self):
        return self.values

    def print(self):
        value = eval("self." + self.pointed_variable)
        self.values.append(value)

