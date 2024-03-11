FROM python

COPY . .
RUN pip install --upgrade pip
RUN apt update && apt install -y libgl1-mesa-glx && apt install -y libqt5gui5 libqt5widgets5 libqt5core5a
ENV ENV QT_QPA_PLATFORM=offscreen
ENV DISPLAY=:0
RUN pip install requests
RUN pip install loguru
RUN pip install opencv-python

CMD ["python", "video_cap.py"]