import utils


def validate_train(train):
    i = 0
    for wagon in train:
        wagon_before = get_neighbour(i, train, -1)
        wagon_after = get_neighbour(i, train, 1)

        if wagon_before in wagon.blacklist or wagon_after in wagon.blacklist:
            return -1

        if len(wagon.needlist) > 0 and wagon_before not in wagon.needlist and wagon_after not in wagon.needlist:
            return -1

        i += 1
    return 1


def get_neighbour(wagon_index, train, offset):
    neighbour_index = wagon_index + offset
    neighbour = None
    if utils.is_in_range(neighbour_index, 0, len(train) - 1):
        neighbour = type(train[neighbour_index])

    return neighbour


class FirstClass:
    def __init__(self):
        self.blacklist = [SecondClass]
        self.whitelist = []
        self.needlist = [FirstClass, OnboardBistro]


class SecondClass:
    def __init__(self):
        self.blacklist = []
        self.whitelist = []
        self.needlist = [FirstClass, OnboardBistro, SecondClass]


class OnboardBistro:
    def __init__(self):
        self.blacklist = []
        self.whitelist = [OnboardBistro]
        self.needlist = [FirstClass, SecondClass]
