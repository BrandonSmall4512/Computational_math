import random
import matplotlib.pyplot as plt

def monte_carlo_simulation(arrival_rate, service_rate, num_simulations):
    total_time_spent = 0
    waiting_times = []
    num_in_queue = 0
    total_waiting_time = 0
    system_busy_time = 0

    for _ in range(num_simulations):
        interarrival_time = random.expovariate(arrival_rate)
        service_time = random.expovariate(service_rate)

        if _ == 0:
            service_end_time = interarrival_time + service_time
        else:
            service_end_time = max(service_end_time + interarrival_time, arrival_time) + service_time

        arrival_time = service_end_time - service_time
        waiting_time = max(0, arrival_time - service_end_time + service_time)

        waiting_times.append(waiting_time)
        total_time_spent += waiting_time + service_time

        if waiting_time > 0:
            num_in_queue += 1
            total_waiting_time += waiting_time

        system_busy_time += service_time

    avg_waiting_time = sum(waiting_times) / num_simulations
    avg_system_time = total_time_spent / num_simulations
    avg_queue_length = total_waiting_time / system_busy_time if system_busy_time != 0 else 0
    system_utilization = system_busy_time / service_end_time

    return (
        avg_waiting_time, avg_system_time, waiting_times,
        avg_queue_length, system_utilization
    )

def visualize_simulation(waiting_times):
    plt.rcParams['font.family'] = 'DejaVu Sans'  
    plt.rcParams['font.size'] = 12 

    plt.figure(figsize=(10, 6))
    plt.hist(waiting_times, bins=30, density=True, alpha=0.7, color='blue')
    plt.title('Гистограмма времени ожидания в очереди')  
    plt.xlabel('Время ожидания')  # Время ожидания
    plt.ylabel('Плотность вероятности')  # Плотность вероятности
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    arrival_rate = 80
    service_rate = 0.01
    num_simulations = 100000

    (
        avg_waiting_time, avg_system_time, waiting_times,
        avg_queue_length, system_utilization
    ) = monte_carlo_simulation(
        arrival_rate, service_rate, num_simulations
    )

    print(f"Среднее время ожидания в очереди: {avg_waiting_time:.2f} единиц времени")  
    print(f"Среднее время в системе: {avg_system_time:.2f} единиц времени")  
    print(f"Средняя длина очереди: {avg_queue_length:.2f} заявок")  
    print(f"Загрузка системы: {system_utilization:.2%}")  

    visualize_simulation(waiting_times)

