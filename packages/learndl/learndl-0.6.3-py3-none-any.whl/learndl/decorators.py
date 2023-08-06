def log(process):
    def outer(func):
        def inner(*args, **kw):
            print('>>>' + process + ' Running<<<')
            func(*args, **kw)
            print('>>>' + process + ' Done<<<')
            print()
        return inner
    return outer
