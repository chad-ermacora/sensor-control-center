class Test1:
    def __init__(self):
        self.var1 = "test1: var1"
        self.var2 = "test1: var2"


class Test2:
    def __init__(self):
        self.var1 = "test2: var1"
        self.var2 = "test2: var2"


class Test3:
    def __init__(self):
        self.var1 = "test3: var1"
        self.var2 = "test3: var2"


def print_test(test):
    print(test.var1)
    print(test.var2)


def mod_var1(test):
    test.var1 = "Changed"


def mod_var2(test):
    test.var2 = "Changed2"


test_1 = Test1()
test_2 = Test2()
test_3 = Test3()

print_test(test_1)
print_test(test_2)
print_test(test_3)

mod_var1(test_1)
print_test(test_1)
print_test(test_2)
print_test(test_3)
mod_var2(test_3)

print_test(test_1)
print_test(test_2)
print_test(test_3)
