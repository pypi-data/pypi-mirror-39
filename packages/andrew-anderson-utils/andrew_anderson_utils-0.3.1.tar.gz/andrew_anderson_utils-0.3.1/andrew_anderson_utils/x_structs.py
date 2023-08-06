def modify_struct(obj):
    if type(obj) is dict:
        return XDict(obj)
    if type(obj) is list:
        return XList(obj)
    return obj


class XDict(dict):
    def __init__(self, sample=None, **kwargs):
        if sample is None:
            dict.__init__(self, zip(kwargs.keys(),
                                    [modify_struct(o) for o in kwargs.values()]
                                    ))
        else:
            dict.__init__(self, zip(sample.keys(),
                                    [modify_struct(o) for o in sample.values()]
                                    ),
                          **kwargs)

    def __getattr__(self, name):
        return self[name]

    def __setitem__(self, name, value):
        dict.__setitem__(self, name, modify_struct(value))
        return value

    def __setattr__(self, name, value):
        self[name] = value
        return value

    def __delattr__(self, name):
        del self[name]


class XList(list):
    def __init__(self, sample):
        list.__init__(self, [modify_struct(o) for o in sample])

    def __setitem__(self, name, value):
        list.__setitem__(self, name, modify_struct(value))
        return value
