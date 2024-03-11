import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QTextEdit, QTextBrowser, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from loguru import logger

class StudentPortal(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Запускаем таймер, который будет вызывать update_data() каждую секунду
        self.initUI()

    def update_data(self):
        try:
            name = self.load_name_from_cache()
            self.hello_label.setText(f"Привет, {name}")

            schedule = self.load_schedule_from_cache()
            schedule_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(schedule)])
            self.schedule_widget.setText(schedule_text)

            news = self.load_news_from_cache()
            news_count = len(news)

            # Удаляем все текущие виджеты новостей
            while self.news_layout.count() > 0:
                item = self.news_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Создаем виджеты заново для всех новостей
            for i in range(news_count):
                news_id, news_item = list(news.items())[i]
                news_text = f"<b>{news_item['title']}</b>: {news_item['content']}"
                news_block = QTextEdit()
                news_block.setReadOnly(True)
                news_block.setStyleSheet("background-color: white; padding: 10px; margin-bottom: 10px; border-radius: 5px; color: #05336e;")
                news_block.setText(news_text)
                news_block.setMinimumHeight(50)
                self.news_layout.addWidget(news_block)
        except Exception as e:
            logger.error(f"Ошибка обновления, пробую снова: {e}")
    def initUI(self):
        layout = QVBoxLayout(self)
        self.header_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        self.setStyleSheet("background-color: #05336e; color: white; font-size: 16px; font-family: Arial;")

        # Блок с приветствием и именем студента
        self.hello_label = QLabel()
        name = self.load_name_from_cache()
        self.hello_label.setStyleSheet("background-color: #bb8d54; padding: 20px; font-size: 24px; font-weight: bold;")
        self.hello_label.setText(f"Привет, {name}!")
        self.hello_label.setMaximumHeight(100)
        self.header_layout.addWidget(self.hello_label)
        self.header_layout.setAlignment(self.hello_label, Qt.AlignTop)
        self.hello_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Блок расписания из файла cache.json
        schedule_layout = QVBoxLayout()

        schedule_label = QLabel("Расписание")
        schedule_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        schedule_layout.addWidget(schedule_label)  # Добавление заголовка "Расписание" в лейаут расписания

        self.schedule_widget = QTextEdit()
        self.schedule_widget.setReadOnly(True)
        schedule = self.load_schedule_from_cache()
        schedule_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(schedule)])
        self.schedule_widget.setStyleSheet("background-color: #bb8d54; padding: 10px; border-radius: 5px; color: white;")
        self.schedule_widget.setText(schedule_text)
        self.schedule_widget.setMaximumWidth(350)
        self.schedule_widget.setAlignment(Qt.AlignTop)
        schedule_layout.addWidget(self.schedule_widget)

        main_layout.addLayout(schedule_layout)  # Добавление лейаута расписания в основной лейаут

        # Блок прокрутки для новостей
        self.news_area = QScrollArea()
        self.news_area.setWidgetResizable(True)
        self.news_area.setStyleSheet("background-color: #05336e; border-radius: 5px;")
        self.news_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.news_layout = QVBoxLayout()
        news_label = QLabel("Новости")
        news_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.news_layout.addWidget(news_label)

        news = self.load_news_from_cache()
        for news_id, news_item in news.items():
            news_text = f"<b>{news_item['title']}</b>: {news_item['content']}"
            news_block = QTextEdit()
            news_block.setReadOnly(True)
            news_block.setStyleSheet("background-color: white; padding: 10px; margin-bottom: 10px; border-radius: 5px; color: #05336e;")
            news_block.setText(news_text)
            news_block.setMinimumHeight(50)
            self.news_layout.addWidget(news_block)

        news_widget = QWidget()
        news_widget.setLayout(self.news_layout)
        self.news_area.setWidget(news_widget)

        main_layout.addWidget(self.news_area)

        layout.addLayout(self.header_layout)
        layout.addLayout(main_layout)
        self.setLayout(layout)
        self.setWindowTitle('Студенческий портал')
        self.show()

    # Остальной код без изменений








    def load_name_from_cache(self):
        with open('cache.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return f"{data['first_name']} {data['last name']}"

    def load_news_from_cache(self):
        with open('cache.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['новости']


    def load_schedule_from_cache(self):
        with open('cache.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['пары']

def main():
    app = QApplication(sys.argv)
    portal = StudentPortal()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
