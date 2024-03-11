import cv2
import base64
import json
import requests
from loguru import logger
import threading
import queue
import time

server_url = 'http://91.222.239.38:5678/process'
frame_queue = queue.Queue()
exit_flag = False
loading_text = "Loading..."

def send_frame_to_server(frame, faces):
    global loading_text
    if frame is not None:
        _, img_encoded = cv2.imencode('.jpg', frame)
        if img_encoded is not None:
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    payload = {'image': img_base64}
    try:
        response = requests.post(server_url, data=payload)
        if response.status_code == 200:
            data = response.json()
            loading_text = f"{data['first_name']} {data['last name']}"
            with open('cache.json', 'w', encoding='utf-8') as cache_file:
                json.dump(data, cache_file, indent=4, ensure_ascii=False)
            logger.info("Данные успешно направлены в кеш")
        else:
            data = {
                "faculty": "unknown",
                "first_name": "unknown",
                "group": "unknown",
                "last name": "",
                "новости": "unknown",
                "пары": ["unknown"]
            }
            loading_text = "Loading..."
            with open('cache.json', 'w', encoding='utf-8') as cache_file:
                json.dump(data, cache_file, indent=4, ensure_ascii=False)
            logger.error(f"Сервер вернул код ответа {response.status_code}, данные не были распознаны")
    except Exception as e:
        loading_text = "Loading..."
        logger.error(f"Ошибка при отправке данных на сервер: {e}")

def render_frames():
    cv2.namedWindow("Ne slishkom umniy stend", cv2.WINDOW_NORMAL)
    while not exit_flag:
        try:
            frame = frame_queue.get(timeout=1)
            for (x, y, w, h) in frame['faces']:
                cv2.rectangle(frame['data'], (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame['data'], loading_text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow("Ne slishkom umniy stend", frame['data'])
            cv2.waitKey(1)
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f'Ошибка отображения кадра {e}')

def detect_faces_send_to_server():
    global exit_flag
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)

    frame_count = 0
    frame_limit = 15  # Ограничение скорости кадров


    while not exit_flag:
        ret, frame = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            # Отправляем запрос на сервер только каждый 10-й кадр
            if frame_count >= frame_limit:
                threading.Thread(target=send_frame_to_server, args=(frame, faces)).start()
                frame_count = 0
            else:
                frame_count += 1

        # Сохранение данных о лицах в кадре
        frame = {
            'data': frame,
            'faces': faces
        }

        frame_queue.put(frame)

    video_capture.release()

def main():
    global exit_flag
    renderer = threading.Thread(target=render_frames)
    detector = threading.Thread(target=detect_faces_send_to_server)

    renderer.start()
    detector.start()

    renderer.join()
    detector.join()

    cv2.destroyAllWindows()
    exit_flag = True

if __name__ == "__main__":
    main()
