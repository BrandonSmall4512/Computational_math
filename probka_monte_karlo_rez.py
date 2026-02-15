import simpy
import random
import matplotlib.pyplot as plt
import numpy as np


def calculate_average_service_time(servers):
    average_service_times = []
    for server in servers:
        average_service_time = (server.min_service_time + server.max_service_time) / 2
        average_service_times.append(average_service_time)
    return average_service_times

def calculate_arrival_rate(servers, num_simulations, simulation_time):
    total_clients = sum([server.total_clients for server in servers])
    arrival_rate = total_clients / (num_simulations * simulation_time)
    return arrival_rate

def apply_erlang_method(arrival_rate, average_service_times):
    traffic_intensity = arrival_rate * np.array(average_service_times)
    total_traffic_intensity = sum(traffic_intensity)
    servers_needed = total_traffic_intensity / arrival_rate
    servers_needed = int(servers_needed)
    return servers_needed


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

def run_simulation(env, servers):
    def client_generator(env, servers):
        client_id = 1
        while True:
            yield env.timeout(random.expovariate(10)) 
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

    env.process(client_generator(env, servers))
    env.run(until=100) 

    total = 0
    served = 0
    return servers
    
def visualize(servers):
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

num_simulations = 3
simulated_results = []  

env = simpy.Environment() 
servers = [
    Server(env, 1, 0.1, 1.5),
    Server(env, 2, 0.1, 1.0),
    Server(env, 3, 0.1, 1.0),
    Server(env, 4, 0.2, 1.5),
    Server(env, 5, 0.7, 1.0)
]
result = run_simulation(env, servers)  
simulated_results.append(result)  

env = simpy.Environment() 
servers = [
    Server(env, 1, 0.7, 2.5),
    Server(env, 2, 0.6, 3.0),
    Server(env, 3, 0.9, 3.0),
    Server(env, 4, 0.8, 2.5),
    Server(env, 5, 0.7, 3.0)
]
result = run_simulation(env, servers) 
simulated_results.append(result)  

env = simpy.Environment()  
servers = [
    Server(env, 1, 3.1, 10.5),
    Server(env, 2, 3.1, 10.0),
    Server(env, 3, 3.1, 10.0),
    Server(env, 4, 3.2, 10.5),
    Server(env, 5, 3.7, 10.0)
]
result = run_simulation(env, servers) 
simulated_results.append(result) 

for idx, servers in enumerate(simulated_results):
    print(f"Результаты эксперимента {idx + 1}:")
    visualize(servers) 
    total = 0
    served = 0
    for server in servers:
        print(f"Сервер {server.server_number}: Общее количество клиентов - {server.total_clients}, Обслужено клиентов - {server.served_clients}")
        print((server.served_clients / server.total_clients) * 100, '%')
        total += server.total_clients
        served += server.served_clients

    average_service_times = calculate_average_service_time(servers)

    arrival_rate = calculate_arrival_rate(servers, num_simulations, simulation_time=100)

    servers_needed = apply_erlang_method(arrival_rate, average_service_times)

    print(f"Оценка методом Эрланга: Необходимое количество серверов - {servers_needed}")
        
    print(f"На всех серверах общий процент обслуженных: {(served / total) * 100} %")

