class Rule:
    def __init__(self, name, condition, action, weight):
        self.name = name
        self.condition = condition
        self.action = action
        self.weight = weight

    def evaluate(self, agent):
        return self.condition.evaluate(agent) * self.weight
