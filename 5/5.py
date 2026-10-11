import sys
import random

from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

from design_5 import Ui_flag


class FlagGenerator(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_flag()
        self.ui.setupUi(self)
        self.setWindowTitle("Флаг")

        # Подключение кнопок к методам
        self.ui.color_select.clicked.connect(self.request_color_count)
        self.ui.reset.clicked.connect(self.reset_view)

    def request_color_count(self) -> None:
        # Вызов диалогового окна с выбором количества цветов
        num_colors, ok = QInputDialog.getInt(
            self,
            "Количество цветов",
            "Введите количество полос:",
            value=3,
            min=1,
            max=30,
            step=1
        )

        if ok:
            self.draw_flag(num_colors)

    def draw_flag(self, num_stripes: int) -> None:
        # Генерация холста и вывод в QLabel
        width = self.ui.label.width()
        height = self.ui.label.height()

        # Создание пустого холста по размеру QLabel
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.white)

        painter = QPainter(pixmap)
        painter.setPen(Qt.PenStyle.NoPen)

        # Рисование горизонтальных полос
        for i in range(num_stripes):
            # Генерация случайных цветов
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            random_color = QColor(r, g, b)

            painter.setBrush(random_color)

            # Координаты по оси Y для текущей полосы
            y_start = int(i * height / num_stripes)
            y_end = int((i + 1) * height / num_stripes)
            stripe_height = y_end - y_start

            # Рисование прямоугольника
            painter.drawRect(0, y_start, width, stripe_height)

        painter.end()

        # Вывод флага на QLabel
        self.ui.label.setPixmap(pixmap)

    def reset_view(self) -> None:
        # Удаление флага
        self.ui.label.clear()
        self.ui.label.setText("Выберите цвета")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlagGenerator()
    window.show()
    sys.exit(app.exec())
