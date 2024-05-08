def my_decorator(func):
    def wrap_function():
        print("*"*100)
        result = func()
        print("*"*100)

        return result

    return wrap_function

def test():
    print("Hello Python")

@my_decorator
def test2():
    print("Wow!")

if __name__ == "__main__":
    test()
    test2()