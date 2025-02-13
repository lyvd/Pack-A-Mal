# FILE: sample_module.py

class SampleClass:
    def __init__(self, value):
        self.value = value

    def method1(self):
        print('Hello from method1')
        return self.value * 2

    def method2(self):
        print('Hello from method2')
        return self.value + 10

def sample_function(x):
    print('Hello from sample_function')
    return x * x

def sample_function2(x):
    print('Hello from sample_function2')
    return x + 10