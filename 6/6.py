import sys

from PyQt6.QtWidgets import QApplication, QWidget, QColorDialog
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QTimer

from design_6 import Ui_Form


class Smiley(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Смайлик")

        # Установка цвета по умолчанию
        self.current_color = QColor(255, 204, 0)

        # Настройка слайдера
        self.ui.size_slider.setRange(10, 100)
        self.ui.size_slider.setValue(100)

        self.ui.color_change.clicked.connect(self.choose_color)
        self.ui.size_slider.valueChanged.connect(self.draw_smiley)

        # Задержка перед первоначальной отрисовкой смайлика
        QTimer.singleShot(50, self.draw_smiley)

    def choose_color(self) -> None:
        # Диалоговое окно выбора цвета
        # QColorDialog возвращает выбранный цвет
        color = QColorDialog.getColor(self.current_color, self, "Выберите цвет смайлика")

        # Изменение смайлика в случае, если цвет выбран
        if color.isValid():
            self.current_color = color
            self.draw_smiley()

    def draw_smiley(self) -> None:
        # Отрисовка смайлика на холсте в соответствии с цветом и масштабом
        width = self.ui.label.width()
        height = self.ui.label.height()

        # Создание холста
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)

        # Создание кисти
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Множитель размера
        scale_factor = self.ui.size_slider.value() / 100.0
        # Максимальный диаметр смайлика
        max_size = min(width, height) - 20
        # Текущий диаметр
        current_size = max_size * scale_factor

        # Координаты X и Y верхнего левого угла для центрирования
        x = (width - current_size) / 2
        y = (height - current_size) / 2

        # Динамическая толщина линий
        line_width = int(max(1.0, current_size * 0.03))

        # Отрисовка лица
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(QPen(Qt.GlobalColor.black, line_width))
        painter.drawEllipse(int(x), int(y), int(current_size), int(current_size))

        # Отрисовка глаз
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        eye_size = current_size * 0.12  # Глаз = 12% от размера лица

        # Координаты левого глаза
        left_eye_x = x + current_size * 0.28
        left_eye_y = y + current_size * 0.25
        painter.drawEllipse(int(left_eye_x), int(left_eye_y), int(eye_size), int(eye_size))

        # Координаты правого глаза
        right_eye_x = x + current_size * 0.60
        right_eye_y = y + current_size * 0.25
        painter.drawEllipse(int(right_eye_x), int(right_eye_y), int(eye_size), int(eye_size))

        # Отрисовка рта
        painter.setBrush(Qt.BrushStyle.NoBrush)
        mouth_x = x + current_size * 0.20
        mouth_y = y + current_size * 0.25
        mouth_size = current_size * 0.60
        start_angle = 0 * 16
        span_angle = -180 * 16

        painter.drawArc(int(mouth_x), int(mouth_y), int(mouth_size), int(mouth_size), start_angle, span_angle)

        painter.end()

        # Расположение смайлика на QLabel
        self.ui.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Smiley()
    window.show()
    sys.exit(app.exec())
