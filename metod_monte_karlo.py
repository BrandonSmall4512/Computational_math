import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

class Server:
    def __init__(self, env, server_number, min_service_time, max_service_time):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.server_number = server_number
        self.min_service_time = min_service_time
        self.max_service_time = max_service_time
        self.total_clients = 0
        self.served_clients = 0
        self.queue_lengths = [] 

    def serve(self, client):
        yield self.env.timeout(random.uniform(self.min_service_time, self.max_service_time))
        self.served_clients += 1
        self.queue_lengths.append(len(self.server.queue)) 

def client_generator(env, servers):
    client_id = 1
    while True:
        yield env.timeout(random.expovariate(2))
        server = random.choice(servers)
        server.total_clients += 1
        env.process(client(env, f"Клиент {client_id}", server))
        client_id += 1

def client(env, name, server):
    arrival_time = env.now
    print(f"{name} прибыл в {arrival_time}, направлен на Сервер {server.server_number}, Время ожидания: {server.min_service_time}-{server.max_service_time}")
    with server.server.request() as request:
        yield request
        print(f"{name} вошел в сервер в {env.now}, обслуживается на Сервере {server.server_number}")
        yield env.process(server.serve(name))
        print(f"{name} покинул сервер в {env.now}, обслуживался на Сервере {server.server_number}")

env = simpy.Environment()

servers = [
    Server(env, 1, 0.5, 5.5),
    Server(env, 2, 2.0, 4.0),
    Server(env, 3, 2.8, 4.0),
    Server(env, 4, 1.2, 5.5),
    Server(env, 5, 1.7, 3.0)
]

env.process(client_generator(env, servers))
env.run(until=100)

total = 0
served = 0
for server in servers:
    print(f"Сервер {server.server_number}: Общее количество клиентов - {server.total_clients}, Обслужено клиентов - {server.served_clients}")
    print((server.served_clients / server.total_clients) * 100, '%')
    total += server.total_clients
    served += server.served_clients
print(f"На всех серверах общий процент обслуженных: {(served / total) * 100} %")


server_indices = np.arange(len(servers))

fig, axs = plt.subplots(2, 1, figsize=(8, 10)) 

total_clients_per_server = [server.total_clients for server in servers]
served_clients_per_server = [server.served_clients for server in servers]

axs[0].bar(server_indices - 0.2, total_clients_per_server, width=0.4, label='Общее количество клиентов', alpha=0.6)
axs[0].bar(server_indices + 0.2, served_clients_per_server, width=0.4, label='Обслужено клиентов', alpha=0.6)
axs[0].set_xlabel('Сервер')
axs[0].set_ylabel('Количество клиентов')
axs[0].set_title('Статистика клиентов по серверам')
axs[0].set_xticks(server_indices)
axs[0].set_xticklabels([f'Сервер {i+1}' for i in range(len(servers))])
axs[0].legend()


for server in servers:
    axs[1].plot(server.queue_lengths, label=f'Сервер {server.server_number}')
axs[1].set_xlabel('Время')
axs[1].set_ylabel('Длина очереди')
axs[1].set_title('Длина очереди на серверах')
axs[1].legend()

plt.tight_layout()  
plt.show()





