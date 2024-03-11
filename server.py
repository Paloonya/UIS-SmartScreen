from flask import Flask, request, jsonify
import face_recognition
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from data_mapping import ProfileMapping, ScheduleMapping, NewsMapping
from loguru import logger

app = Flask(__name__)

known_faces = {
    "069217": "persons/person1.jpg"
}


known_face_encodings = []
known_face_names = []
for name, image_path in known_faces.items():
    img = face_recognition.load_image_file(image_path)
    img_encoding = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(img_encoding)
    known_face_names.append(name)

@app.route('/process', methods=['POST'])
def recognize_faces():
    try:
        image_data = request.form['image']
        decoded_image = base64.b64decode(image_data)
        image = face_recognition.load_image_file(BytesIO(decoded_image))

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        recognized_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            recognized_names.append(name)
        profile = ProfileMapping(recognized_names[0])
        schedule = { "пары" : ScheduleMapping(profile['group'], profile['faculty'])}
        news = {'новости': NewsMapping(profile['faculty'])}
        result = {**profile, **schedule, **news}
        logger.info("Запрос успешно обработан")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Возникла ошибка обработки изображения {e}!")
        return "Error processing image", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
