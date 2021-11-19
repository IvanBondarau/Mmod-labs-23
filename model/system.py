from model.channel import Channel
from model.queue import Queue
from model.request import Response, RequestState
import numpy as np

from model.global_events import GlobalEvents


class System:

    STATES = []

    def __init__(self, channels, queue_size, l, v):

        self.channels = [Channel() for _ in range(channels)]
        self.queue = Queue(queue_size, v)
        self.l = l

    def free_channels(self):
        return sum(channel.empty() for channel in self.channels)

    def flush(self, time):
        self.channels = sorted(self.channels,
                        key=lambda channel: channel.request.status['processing_finished'] if channel.request is not None else 100000000)
        empty_channel = False
        for channel in self.channels:
            processed_request = channel.pop(time)
            if processed_request is not None:
                empty_channel = True
                self.queue.flush(processed_request.status['processing_finished'])
                queued = self.queue.pop()

                if queued is not None:
                    GlobalEvents.EVENTS.append(
                        {
                            'time': processed_request.status['processing_finished'],
                            'queue': -1,
                            'channels': 0
                        }
                    )

                    queued.status['queue_finished'] = processed_request.status['processing_finished']
                    queued.status['processing_started'] = queued.status['queue_finished']
                    queued.status['processing_finished'] = queued.status['processing_started'] + np.random.exponential(1/self.l)
                    channel.push(queued)

                    GlobalEvents.EVENTS.append(
                        {
                            'time': queued.status['processing_started'],
                            'queue': 0,
                            'channels': +1
                        }
                    )
                    break
        if empty_channel:
            self.flush(time)


    def process_request(self, request):
        time = request.status['creation_time']

        self.flush(time)
        self.queue.flush(time)

        if self.free_channels() == 0 and self.queue.full():
            request.response = Response.REJECTED
            request.status['state'] = RequestState.FINISHED
            return False

        request.response = Response.ACCEPTED

        for channel in self.channels:
            if channel.push(request):
                request.status['processing_started'] = time
                request.status['processing_finished'] = time + np.random.exponential(1 / self.l)

                GlobalEvents.EVENTS.append(
                    {
                        'time': request.status['processing_started'],
                        'queue': 0,
                        'channels': +1
                    }
                )

                return True

        request.status['queue_started'] = time
        self.queue.push(request)
        return True

    def log(self):
        print(f'{self.queue}')
        for channel in self.channels:
            print(f'{channel}')



