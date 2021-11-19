from constants import Constant

def fact(n):
    res = 1
    for i in range(1, n+1):
        res *= i
    return res

def calc_p0():

    p = calc_p()
    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    s = 1 + sum([(p**k)/fact(k) for k in range(1, N + 1)])
    s0 = p**(N+1)*(1-(p/N)**M)/(fact(N)*(N-p))
    return 1 / (s + s0)

def calc_service_prob():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE

    p = calc_p()

    p0 = calc_p0()

    p_otk = p**(N + M) / ((N**M) * fact(N)) * p0

    return 1 - p_otk, p_otk


def calc_absolute():
    p_serv, _ = calc_service_prob()
    return p_serv * Constant.LAMBDA

def average_req_in_queue():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE

    p = Constant.LAMBDA / Constant.MU

    t1 = p**(N+1)/(N*fact(N))
    t2 = (1 - ((p/N)**M)*(M+1-M*p/N))/((1-p/N)**2)
    return t1*t2*calc_p0()

def average_req_in_system():
    return average_req_in_queue() + average_req_in_channels()

def average_time_in_system():
    return average_req_in_system() / calc_absolute()


def average_time_in_queue():
    return average_req_in_queue() / calc_absolute()

def average_req_in_channels():
    p = calc_p()
    return p * calc_service_prob()[0]


def calc_p():
    p = Constant.LAMBDA / Constant.MU
    return p


def calc_final_states():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    p = Constant.LAMBDA / Constant.MU

    result = {}
    p0 = calc_p0()
    result[0] = p0

    for k in range(1, N + 1):
        result[k] = (p**k)/fact(k)*p0

    for k in range(N+1, N+M+1):
        result[k] = p**k/(fact(N)*(N**(k-N)))*p0

    return result
