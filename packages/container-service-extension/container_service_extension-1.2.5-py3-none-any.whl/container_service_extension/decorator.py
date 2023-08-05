def rollbackdecorator(func):
    print ("In decorator function")
    def _fn():
        try:
            ret = func()
            return ret
        except ZeroDivisionError as e:
            print ("ZeroDivisionError error")
            rollback()
        except ValueError as e:
            print ("Value error")
            rollback2()
    return _fn


def rollback():
    print ("Rollback 1")


def rollback2():
    print ("Rollback 2")


@rollbackdecorator
def simpleDivide():
    print ("Inside simpleDivide")
    try:
        h = 5 / 0
    except Exception as e:
        print ("Inside zerodivision error")
        raise ZeroDivisionError()
    return h


if __name__ == '__main__':
    result = simpleDivide()
    print (result)
