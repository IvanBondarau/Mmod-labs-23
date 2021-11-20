import logging
import matplotlib.pyplot as plt

from constants import Constant
from model.request import Request, Response, RequestState
from model.system import System
from model.utlis import generate_requests, calc_average_in_queue, calc_total_req, calc_average_in_channels, calc_states, \
    visualize, print_hist
from theor.stat import calc_absolute, calc_service_prob, average_req_in_queue, average_req_in_system, \
    average_time_in_system, average_time_in_queue, average_req_in_channels, calc_final_states

logging.basicConfig(filename='test.log', encoding='utf-8', level=logging.DEBUG)

system = System(Constant.CHANNELS_CNT, Constant.QUEUE_MAX_SIZE, Constant.MU, Constant.V)

requests = generate_requests(Constant.REQ_CNT, Constant.LAMBDA, Constant.MAX_TIME)

for req in requests:
    system.process_request(req)

system.flush(Constant.MAX_TIME)

for req in requests:
    logging.info(str(req))

accepted = list(filter(lambda req: req.response == Response.ACCEPTED, requests))
rejected = list(filter(lambda req: req.response == Response.REJECTED, requests))
queue_timeout = list(filter(lambda req: req.response == Response.QUEUE_TIMEOUT, requests))
queued = list(filter(lambda req: req.status['queue_started'] is not None, requests))
total_ac = len(accepted) + len(queue_timeout)

print('-'*100)
print(f'Всего запросов: {len(requests)}')
print(f'Принято:        {total_ac}')
print(f'Отклонено:      {len(rejected)}')

p_serv, p_rej = calc_service_prob()

print('-'*100)
print(f'Вероятность обслуживания (п): {round(total_ac/len(requests), 4)}')
print(f'Вероятность обслуживания (т): {round(p_serv, 4)}')
print(f'Вероятность отказа       (п): {round(len(rejected)/len(requests), 4)}')
print(f'Вероятность отказа       (т): {round(p_rej, 4)}')

print('-'*100)
absolute = calc_absolute()
print(f'Абсолютная пропускная способность (п): {round(total_ac/Constant.MAX_TIME, 4)}')
print(f'Абсолютная пропускная способность (т): {round(absolute, 4)}')


print('-'*100)
queue_av = average_req_in_queue()
print(f'Среднее число заявок в очереди (п): {round(calc_average_in_queue(), 4)}')
print(f'Среднее число заявок в очереди (т): {round(queue_av, 4)}')
print(f'Среднее число занятых каналов (п): {round(calc_average_in_channels(), 4)}')
print(f'Среднее число занятых каналов (т): {round(average_req_in_channels(), 4)}')
print(f'Среднее число заявок в системе (п): {round(calc_total_req(), 4)}')
print(f'Среднее число заявок в системе (т): {round(average_req_in_system(), 4)}')

print('-'*100)
av_system_time = sum([req.status['processing_finished'] - req.status['creation_time'] if req.status['processing_finished'] is not None else Constant.MAX_TIME - req.status['creation_time'] for req in accepted]) / len(accepted)
av_queue_time = sum([req.status['queue_finished'] - req.status['queue_started'] if req.status['queue_finished'] is not None else Constant.MAX_TIME - req.status['creation_time'] for req in queued]) / total_ac
print(f'Среднее время заявки в очереди (п): {round(av_queue_time, 4)}')
print(f'Среднее время заявки в очереди (т): {round(average_time_in_queue(), 4)}')
print(f'Среднее время заявки в системе (п): {round(av_system_time, 4)}')
print(f'Среднее время заявки в системе (т): {round(average_time_in_system(), 4)}')


print('-'*100)

states_p = calc_states()
final_states = calc_final_states()

final_states = dict(filter(lambda x: x[1] - 0 > 1e-5,final_states.items()))

print(f'Практ : {states_p}')
print(f'Теор  : {final_states}')


print_hist(states_p, 'r', 'Практические вероятности состояний')
print_hist(final_states, 'b', 'Теоретические вероятности состояний')

visualize()




