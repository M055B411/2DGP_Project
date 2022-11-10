
# layer 0: Background Objects
# layer 1: wall Objects
# layer 2: alive Object
# layer 3: bullet Object
# layer 4: ui things
objects = [[], [], [], [], []]


def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol


def remove_object(o):
    for layer in objects:
        try:
            layer.remove(o)
            del o
            return
        except:
            pass
    raise ValueError('Trying destroy non existing object')

def layer_objects(depth):
    for o in objects[depth]:
        yield o

def all_objects():
    for layer in objects:
        for o in layer:
            yield o


def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()



