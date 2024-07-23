import numpy as np
import matplotlib.pyplot as plt

#3 чтение мниста
def load_dataset():
	with np.load("mnist.npz") as f:
		# конвертация ргв в чб
		x_train = f['x_train'].astype("float32") / 255

		# перепись (60000, 28, 28) в (60000, 784)
		x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))

		# получение значения правильного ответа
		y_train = f['y_train']

		# конвертация выходного формата
		y_train = np.eye(10)[y_train]

		return x_train, y_train

# Запуск подпрограммы считывания мниста
images, labels = load_dataset()    

# 1 Расставляем рандомно веса в синапсы между входным и скрытым; скрытым и выходным сооьветственно; слоем
weights_input_to_hidden = np.random.uniform(-0.5, 0.5, (20, 784))
weights_hidden_to_output = np.random.uniform(-0.5, 0.5, (10, 20))

# 2 Нейроны смещения (всегда = 1) служит для получения результата путём сдвига графика активации в право иои в лево

bias_input_to_hidden = np.zeros((20, 1))
bias_hidden_to_output = np.zeros((10, 1))

# Процесс коррекции весов

# Создание эпох
epochs = 3
e_loss = 0
e_correct = 0
learning_rate = 0.02

for epoch in range(epochs):
    print(f"Epoch № {epoch}")
    
    # итерируем изобржения
    for image, label in zip(images, labels):
        #перебрассываем изо и его класс в форму двумерного масива
        image = np.reshape(image, (-1, 1))
        label = np.reshape(label, (-1, 1))

        # первое действее в подгонки весов; передаём данные (рандомные значения заданные ранее) в скрытый слой 
        hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ image
        
        # 4 нормализация нейронов (приведение к значению от 0 до 1), функция артивации
        hidden = 1 / (1 + np.exp(-hidden_raw)) # 5 - использование сигмоиды

        # Передаём данные из скрытого слоя в выходной
        output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
        output = 1 / (1 + np.exp(-output_raw)) # 5 - использование сигмоиды

        # 6 использования формулу для вырывнивания весов
        e_loss += 1 / len(output) * np.sum((output - label) ** 2, axis = 0)
        e_correct += int(np.argmax(output) == np.argmax(label))

        # 7 функция приведения значения нейрона скрытого слоя (корректировка весов)
        delta_output = output - label
        weights_hidden_to_output += -learning_rate * delta_output @ np.transpose(hidden)
        bias_hidden_to_output += -learning_rate * delta_output

        # 7 функция приведения значения нейрона выходного слоя (корректировка весов)
        delta_hidden = np.transpose(weights_hidden_to_output) @ delta_output * (hidden * (1 - hidden))
        weights_input_to_hidden += -learning_rate * delta_hidden @ np.transpose(image)
        bias_input_to_hidden += -learning_rate * delta_hidden

        
    print(f"Loss: {round((e_loss[0] / images.shape[0]) * 100, 3)}%")
    print(f"Accuracy: {round((e_correct / images.shape[0]) * 100, 3)}%")
    e_loss = 0
    e_correct = 0

# проверка с кастомным изо
test_image = plt.imread("custom.jpg", format="jpeg")

# конвертация ргв в чб
gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114]) 
test_image = 1 - (gray(test_image).astype("float32") / 255)

# перепись
test_image = np.reshape(test_image, (test_image.shape[0] * test_image.shape[1]))

# получение значения правильного ответа
image = np.reshape(test_image, (-1, 1))

# запуск перехода на скрытый слой
hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ image
hidden = 1 / (1 + np.exp(-hidden_raw)) # сигмоида

# запуск перехода на выходной слой
output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
output = 1 / (1 + np.exp(-output_raw)) # сигмоида

plt.imshow(test_image.reshape(28, 28), cmap="Greys")
plt.title(f"CUSTOM number is: {output.argmax()}")
plt.show()























        
