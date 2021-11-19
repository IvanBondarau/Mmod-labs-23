import numpy as np
from matplotlib import pyplot as plt

from constants import Constant
from model.global_events import GlobalEvents
from model.request import Request


def generate_requests(requests_num, lambda_, max_time):
    requests = []
    cur_time = 0

    for _ in range(requests_num):
        cur_time += np.random.exponential(1 / lambda_)
        if cur_time > max_time:
            break
        new_request = Request(cur_time)
        requests.append(new_request)

    return requests

def calc_average_in_queue():

    queue = 0
    total = 0
    previous_event = {'time': 0}
    for event in GlobalEvents.EVENTS:
        total += (event['time'] - previous_event['time']) * queue
        queue += event['queue']
        previous_event = event

    if Constant.MAX_TIME > previous_event['time']:
        total += (Constant.MAX_TIME - previous_event['time']) * queue

    return total / Constant.MAX_TIME


def calc_average_in_channels():

    channels = 0
    total = 0
    previous_event = {'time': 0}
    for event in GlobalEvents.EVENTS:
        total += (event['time'] - previous_event['time']) * channels
        channels += event['channels']
        previous_event = event

    if Constant.MAX_TIME > previous_event['time']:
        total += (Constant.MAX_TIME - previous_event['time']) * channels

    return total / Constant.MAX_TIME


def calc_total_req():

    total_time = 0
    queue = 0
    channels = 0
    previous_event = {'time': 0}
    for event in GlobalEvents.EVENTS:
        total_time += (event['time'] - previous_event['time']) * (queue + channels)
        queue += event['queue']
        channels += event['channels']

        previous_event = event

    if Constant.MAX_TIME > previous_event['time']:
        total_time += (Constant.MAX_TIME - previous_event['time']) * (queue + channels)

    return total_time / Constant.MAX_TIME

def calc_states():
    queue = 0
    channels = 0
    GlobalEvents.EVENTS = sorted(GlobalEvents.EVENTS, key=lambda x: x['time'])
    dict_total_time = {}
    previous_event = {'time': 0}
    for event in GlobalEvents.EVENTS:
        state = queue + channels

        if state in dict_total_time.keys():
            dict_total_time[state] += event['time'] - previous_event['time']
        else:
            dict_total_time[state] = event['time'] - previous_event['time']

        queue += event['queue']
        channels += event['channels']
        # print(f'event = {event}, queue = {queue}, channels = {channels}')
        previous_event = event

    if previous_event['time'] < Constant.MAX_TIME:
        state = queue + channels
        if state in dict_total_time.keys():
            dict_total_time[state] += Constant.MAX_TIME - previous_event['time']
        else:
            dict_total_time[state] = Constant.MAX_TIME - previous_event['time']

    for state in dict_total_time.keys():
        dict_total_time[state] /= Constant.MAX_TIME

    return dict_total_time

def print_hist(states, color, label):
    weights = [states[state] for state in states.keys()]
    bins = list(states.keys()) + [list(states.keys())[-1] + 1]

    plt.hist(states.keys(), bins=bins, weights=weights, color=color, label=label)

    plt.show()

def visualize():
    queue = 0
    channels = 0
    GlobalEvents.EVENTS = sorted(GlobalEvents.EVENTS, key=lambda x: x['time'])

    previous_event = {'time': 0}
    points = [0]
    values = [0]
    for event in GlobalEvents.EVENTS:
        state = queue + channels
        values.append(state)
        points.append(event['time'])

        queue += event['queue']
        channels += event['channels']
        # print(f'event = {event}, queue = {queue}, channels = {channels}')
        previous_event = event

    if previous_event['time'] < Constant.MAX_TIME:
        state = queue + channels
        values.append(state)
        points.append(Constant.MAX_TIME)

    plt.plot(points, values)
    plt.axhline(y=Constant.CHANNELS_CNT, color='r', linestyle='-')
    plt.show()

