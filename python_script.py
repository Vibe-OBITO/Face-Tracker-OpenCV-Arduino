import cv2
import serial
import time

# Загрузка каскада Хаара для обнаружения лиц
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Инициализация видеозахвата с камеры
cap = cv2.VideoCapture(1)

# Инициализация соединения с Arduino по последовательному порту
ArduinoSerial = serial.Serial('com7', 9600, timeout=0.1)

# Задержка для установления связи с Arduino
time.sleep(1)

while cap.isOpened():
    # Считывание кадра с камеры
    ret, frame = cap.read()

    # Отражение изображения по горизонтали (зеркальное отображение)
    frame = cv2.flip(frame, 1)

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц на кадре
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)

    for x, y, w, h in faces:
        # Отправка координат лица в Arduino
        string = 'X{0:d}Y{1:d}'.format((x + w // 2), (y + h // 2))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))

        # Отрисовка центра лица
        cv2.circle(frame, (x + w // 2, y + h // 2), 2, (0, 255, 0), 2)

        # Отрисовка прямоугольника вокруг лица
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    # Отрисовка прямоугольника в центре экрана
    cv2.rectangle(frame, (640 // 2 - 30, 480 // 2 - 30), (640 // 2 + 30, 480 // 2 + 30), (255, 255, 255), 3)

    # Отображение кадра
    cv2.imshow('img', frame)

    # Нажмите 'q' для выхода
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
