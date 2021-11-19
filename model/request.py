from enum import Enum


class RequestState(Enum):
    CREATED = 1,
    IN_QUEUE = 2,
    PROCESSING = 3
    FINISHED = 4


class Response(Enum):
    ACCEPTED = 1,
    REJECTED = 2,
    QUEUE_TIMEOUT = 3


class Request:

    COUNTER = 0

    def __init__(self, creation_time, state=RequestState.CREATED, response=None):
        self.id = Request.COUNTER
        Request.COUNTER += 1
        self.status = {
            'state': state,
            'creation_time': creation_time,
            'queue_started': None,
            'queue_finished': None,
            'max_queue_time': None,
            'processing_started': None,
            'processing_finished': None
        }

        self.response = response

    def __str__(self):
        return f'Request{{id = {self.id}, status = {self.status}, response = {self.response}}}'


