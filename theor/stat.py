from constants import Constant

def fact(n):
    res = 1
    for i in range(1, n+1):
        res *= i
    return res

def calc_p():
    p = Constant.LAMBDA / Constant.MU
    return p

def calc_beta():
    return Constant.V / Constant.MU

def calc_beta_mult(i):
    res = 1
    betha = calc_beta()
    N = Constant.CHANNELS_CNT
    for l in range(1, i+1):
        res *= (N + l*betha)
    return res

def calc_p0():

    p = calc_p()
    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    s = 1 + sum([(p**k)/fact(k) for k in range(1, N + 1)])
    s0 = p**N/fact(N)*sum((p**i) / calc_beta_mult(i) for i in range(1, M+1))
    return 1 / (s + s0)


def calc_final_states():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    p = calc_p()

    result = {}
    p0 = calc_p0()
    result[0] = p0

    for k in range(1, N + 1):
        result[k] = (p**k)/fact(k)*p0

    for i in range(1, M+1):
        result[N+i] = result[N]*p**i/calc_beta_mult(i)

    return result



def calc_service_prob():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    p = calc_p()
    p0 = calc_p0()

    p_otk = (p**N/fact(N)*p0)*p**M/calc_beta_mult(M)

    return 1 - p_otk, p_otk


def calc_absolute():
    p_serv, _ = calc_service_prob()
    return p_serv * Constant.LAMBDA

def average_req_in_queue():

    N = Constant.CHANNELS_CNT
    M = Constant.QUEUE_MAX_SIZE
    p = calc_p()

    p_states = calc_final_states()

    return sum([i*p_states[N+i] for i in range(1, M+1)])

def average_req_in_system():
    return average_req_in_queue() + average_req_in_channels()

def average_time_in_system():
    return average_req_in_system() / calc_absolute()


def average_time_in_queue():
    return average_req_in_queue() / calc_absolute()

def average_req_in_channels():
    p = calc_p()
    return p * calc_service_prob()[0]


