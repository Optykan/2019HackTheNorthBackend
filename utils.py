class AssertType:
    type = str
    length = -1
    min = 0
    max = 0
    check_range = False

    def __init__(self, type, length=-1, check_range=False, minimum=0, maximum=0):
        self.type = type
        self.length = length
        self.min = minimum
        self.max = maximum
        self.check_range = check_range

    def check_value(self, value):
        if not isinstance(value, self.type):
            print("Instance fail")
            return False
        if self.length > -1:
            print("length check")
            return 0 <= len(value) <= self.length
        if self.check_range:
            print("range check")
            return self.min <= value <= self.max
        return True


def assert_type(check, types):
    for key in types:
        if not types[key].check_value(check[key]):
            print(f'Validation error {key} {type(check[key])}')
            raise TypeError(f'Validation error on {key} with value {check[key]}')
    print("Validation passed")