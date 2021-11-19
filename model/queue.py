import numpy as np

from model.request import RequestState, Response
from model.global_events import GlobalEvents


class Queue:
    def __init__(self, capacity, v):
        self.capacity = capacity
        self.requests = []
        self.v = v

    def size(self):
        return len(self.requests)

    def empty(self):
        return len(self.requests) == 0

    def full(self):
        return len(self.requests) == self.capacity

    def flush(self, time):
        to_remove = []
        for req in self.requests:
            if req.status['max_queue_time'] < time:
                req.status['queue_finished'] = req.status['max_queue_time']
                req.status['state'] = RequestState.FINISHED
                req.response = Response.QUEUE_TIMEOUT
                to_remove.append(req)

        for req in to_remove:
            self.requests.remove(req)
            GlobalEvents.EVENTS.append(
                {
                    'time': req.status['max_queue_time'],
                    'queue': -1,
                    'channels': 0
                }
            )

    def push(self, request):
        if not self.full():
            request.status['state'] = RequestState.IN_QUEUE
            request.status['max_queue_time'] = request.status['queue_started'] + np.random.exponential(1 / self.v)
            self.requests.append(request)

            GlobalEvents.EVENTS.append(
                {
                    'time': request.status['queue_started'],
                    'queue': +1,
                    'channels': 0
                }
            )

        else:
            raise ValueError("Queue is full")

    def pop(self):
        if self.empty():
            return None
        else:
            resp = self.requests[0]
            self.requests = self.requests[1:len(self.requests)]

            return resp

    def __str__(self):
        return f'Queue{{capacity = {self.capacity}, items = {self.requests}}}'



