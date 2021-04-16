import numpy as np
from abc import ABCMeta, abstractmethod
from copy import copy, deepcopy


class AbstractFeature(object, metaclass=ABCMeta):
    @abstractmethod
    def __choose_random_value__(self):
        pass

    @abstractmethod
    def __copy__(self):
        pass

    def mutate(self):
        new = copy(self)
        new.value = new.__choose_random_value__()
        return new

    @abstractmethod
    def get_value(self):
        pass


class IntFeature(AbstractFeature):
    def __init__(self, value, value_range, exp=1, enabled=True):
        self.value = value
        self.value_range = value_range
        self.exp = exp
        self.enabled = enabled

    def __choose_random_value__(self):
        return np.random.randint(self.value_range[0], self.value_range[1] + 1)

    def __copy__(self):
        return IntFeature(copy(self.value), copy(self.value_range), copy(self.exp))

    def get_value(self):
        return self.value * self.exp


class FloatFeature(AbstractFeature):
    def __init__(self, value, value_range, exp=1, enabled=True):
        self.value = value
        self.value_range = value_range
        self.exp = exp
        self.enabled = enabled

    def __choose_random_value__(self):
        return np.random.uniform(self.value_range[0], self.value_range[1])

    def __copy__(self):
        return FloatFeature(copy(self.value), copy(self.value_range), copy(self.exp))

    def get_value(self):
        return self.value * self.exp


class BoolFeature(AbstractFeature):
    def __init__(self, value, enabled=True):
        self.value = value
        self.enabled = enabled

    def __choose_random_value__(self):
        return np.random.choice([True, False])

    def __copy__(self):
        return BoolFeature(copy(self.value))

    def get_value(self):
        return self.value


class Mutation:
    def __init__(self, feature_name, old_value, new_value):
        self.feature_name = feature_name
        self.old_value = old_value
        self.new_value = new_value

    def __str__(self):
        return f"{self.feature_name}\nold value: {self.old_value}\nnew_value: {self.new_value}"


class Model:
    def __init__(self, features=[], mutations=[]):
        self.features = features
        self.result = None
        self.mutations = mutations

    def __copy__(self):
        return Model(deepcopy(self.features), deepcopy(self.mutations))

    def mutate(self):
        new_model = copy(self)
        random_feature = np.random.choice(list(filter(lambda x: new_model.features[x].enabled,
                                                      new_model.features.keys())))
        print(f"mutate '{random_feature}'")
        print(f"old value '{new_model.features[random_feature].get_value()}'")
        new_model.features[random_feature] = new_model.features[random_feature].mutate()
        print(f"new value '{new_model.features[random_feature].get_value()}'")
        new_model.mutations.append(
            Mutation(random_feature, {self.features[random_feature].get_value()}, {new_model.features[random_feature].get_value()}))
        return new_model

    def get_values(self):
        return {k: v.get_value() for k, v in self.features.items()}
