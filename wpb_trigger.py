import sys
import time
import PyTango

p1, p2 = 0, 10

m = PyTango.DeviceProxy('mot05')
t0 = time.time()

m_state = None
m_position = None


def state_cb(event):
    global m_state
    m_state = event.attr_value.value


def position_cb(event):
    global m_position
    m_position = event.attr_value.value


def raise_error():
    print('found!')
    print('##################  TRACE IT AT:  #######################')
    print('grep write_Position /tmp/tango-sicilia/Pool/gcwpb/log.txt')
    print('#########################################################')
    raise Exception('bug!')


def move_event(end):
    global m_state
    global m_position
    m.position = end
    t = time.time()
    while round(m_position) != end or m_state == PyTango.DevState.MOVING:
        if time.time() - t > 3:
            raise_error()


def move_event_state(end):
    global m_state
    m.position = end
    t = time.time()
    while round(m.position) != end or m_state == PyTango.DevState.MOVING:
        if time.time() - t > 3:
            raise_error()


def move_event_position(end):
    global m_position
    m.position = end
    t = time.time()
    while round(m_position) != end or m.state() == PyTango.DevState.MOVING:
        if time.time() - t > 3:
            raise_error()


def move_read(end):
    m.position = end
    t = time.time()
    # the order of reads and evaluation does not matter
    while round(m.position) != end or m.state() == PyTango.DevState.MOVING:
        if time.time() - t > 3:
            raise_error()


def test_read():
    for i in range(50000):
        move_read(p2)
        move_read(p1)


def test_event():
    global m
    m.subscribe_event("state", PyTango.EventType.CHANGE_EVENT, state_cb)
    m.subscribe_event("position", PyTango.EventType.CHANGE_EVENT, position_cb)
    for i in range(50000):
        move_event(p2)
        move_event(p1)

# does not happen after runnint tests for 1 h
def test_event_state():
    global m
    m.subscribe_event("state", PyTango.EventType.CHANGE_EVENT, state_cb)
    for i in range(50000):
        move_event_state(p2)
        move_event_state(p1)


# does not happen after running tests for 16 h
def test_event_position():
    global m
    m.subscribe_event("position", PyTango.EventType.CHANGE_EVENT, position_cb)
    for i in range(50000):
        move_event_position(p2)
        move_event_position(p1)


if __name__ == "__main__":
    test = sys.argv[1]
    if test == "read":
        test_read()
    elif test == "event":
        test_event()
    elif test == "event_position":
        test_event_position()
    elif test == "event_state":
        test_event_state()
