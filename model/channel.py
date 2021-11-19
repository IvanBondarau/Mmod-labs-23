from model.request import RequestState
from model.global_events import GlobalEvents


class Channel:

    COUNTER = 0

    def __init__(self):
        self.id = Channel.COUNTER
        Channel.COUNTER += 1
        self.request = None

    def pop(self, time):
        if self.request is None:
            return None
        else:
            if self.request.status['processing_finished'] <= time:

                result = self.request
                result.status['state'] = RequestState.FINISHED
                self.request = None

                GlobalEvents.EVENTS.append(
                    {
                        'time': result.status['processing_finished'],
                        'queue': 0,
                        'channels': -1
                    }
                )

                return result
            return None

    def empty(self):
        return self.request is None

    def push(self, request):
        if self.empty():
            self.request = request
            request.status['state'] = RequestState.PROCESSING
            return True
        else:
            return False

    def __str__(self):
        return f'Channel{{id={self.id}, request={self.request.id if self.request is not None else None}}}'


