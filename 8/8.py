import sys
import math

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QTimer, QLineF

from design_8 import Ui_MainWindow


class LSystem(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle("L-система")
        self.ui.label_2.setText("Шаг:")

        # Определение переменных для хранения параметров L-системы
        self.system_name = ""
        self.turn_angle = 0.0
        self.axiom = ""
        self.rules = {}

        # Переменная для кэширования сгенерированных строк
        self.strings_cache = {}

        # Изначальная блокировка слайдера до загрузки файла
        self.ui.evolution_slider.setEnabled(False)
        self.ui.evolution_slider.setRange(0, 7)

        # Подключение событий
        self.ui.file_open.triggered.connect(self.load_file)
        self.ui.evolution_slider.valueChanged.connect(self.draw_system)

    def load_file(self) -> None:
        # Открытие диалогового окна, чтение конфигурации и запуск отрисовки первого шага
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл L-системы", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*)")

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Чтение файла с удалением пустых строк и лишних пробелов
                lines = [line.strip() for line in file.readlines() if line.strip()]

            if len(lines) < 4:
                raise ValueError("Файл не соответствует формату")

            # Чтение параметров системы
            self.system_name = lines[0]
            # Вычисление угла поворота: полная плоскость (360) делится на заданное число
            divisions = int(lines[1])
            self.turn_angle = 360.0 / divisions
            self.axiom = lines[2]

            # Чтение теорем
            self.rules = {}
            for line in lines[3:]:
                # Разделение строки по первому пробелу
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    self.rules[parts[0]] = parts[1].replace(' ', '')

            # Сброс кэша и обновление интерфейса
            self.strings_cache = {0: self.axiom}
            self.setWindowTitle(f"L-система: {self.system_name}")
            self.ui.evolution_slider.setEnabled(True)

            # Установка слайдера на 1
            self.ui.evolution_slider.setValue(1)
            self.draw_system()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось обработать файл:\n{e}")

    def generate_string(self, step: int) -> str:
        # Генерация строки команд на основе аксиомы и правил для заданного шага эволюции
        if step in self.strings_cache:
            return self.strings_cache[step]

        prev_string = self.generate_string(step - 1)
        new_string = []

        # Применение правил к каждому символу
        for char in prev_string:
            if char in self.rules:
                new_string.append(self.rules[char])
            else:
                new_string.append(char)

        result = "".join(new_string)
        self.strings_cache[step] = result  # Сохранение в кэш
        return result

    def calculate_bounds(self, commands: str) -> tuple:
        # Вычисление границ рисунка для последующего масштабирования
        x, y = 0.0, 0.0
        current_angle = 0.0

        # Стартовые границы
        min_x, max_x = 0.0, 0.0
        min_y, max_y = 0.0, 0.0

        stack = []  # Стек для сохранения координат
        for char in commands:
            if char in ('F', 'G'):  # Команда движения вперед
                # Перевод угла в радианы и вычисление смещения
                rad = math.radians(current_angle)
                x += math.cos(rad)
                y -= math.sin(rad)

                # Обновление границ
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
            elif char == '+':  # Поворот против часовой стрелки
                current_angle += self.turn_angle
            elif char == '-':  # Поворот по часовой стрелке
                current_angle -= self.turn_angle
            elif char == '[':  # Сохранение текущей позиции
                stack.append((x, y, current_angle))
            elif char == ']':  # Возврат к сохраненной позиции
                x, y, current_angle = stack.pop()

        return min_x, max_x, min_y, max_y

    def draw_system(self) -> None:
        # Масштабирование и отрисовка L-системы на основе сгенерированной строки
        if not self.axiom:
            return

        step = self.ui.evolution_slider.value()
        self.ui.label_2.setText(f"Шаг: {step}")

        # Генерация строки команд
        commands = self.generate_string(step)

        # Вычисление границ для центрирования и масштабирования
        min_x, max_x, min_y, max_y = self.calculate_bounds(commands)

        width = self.ui.label.width()
        height = self.ui.label.height()

        range_x = max_x - min_x
        range_y = max_y - min_y

        # Защита от деления на ноль
        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1

        # Вычисление коэффициента масштабирования
        scale = min(width / range_x, height / range_y) * 0.95

        # Вычисление отступов центрирования
        offset_x = (width - range_x * scale) / 2 - min_x * scale
        offset_y = (height - range_y * scale) / 2 - min_y * scale

        # Создание холста
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.white)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen_width = max(1, 3 - step // 2)
        painter.setPen(QPen(Qt.GlobalColor.darkBlue, pen_width))

        # Отрисовка
        x, y = 0.0, 0.0
        current_angle = 0.0
        stack = []

        for char in commands:
            if char in ('F', 'G'):
                rad = math.radians(current_angle)
                next_x = x + math.cos(rad)
                next_y = y - math.sin(rad)

                # Применение масштаба и отступов к координатам при отрисовке
                p1_x, p1_y = x * scale + offset_x, y * scale + offset_y
                p2_x, p2_y = next_x * scale + offset_x, next_y * scale + offset_y

                painter.drawLine(QLineF(p1_x, p1_y, p2_x, p2_y))

                x, y = next_x, next_y
            elif char == '+':
                current_angle += self.turn_angle
            elif char == '-':
                current_angle -= self.turn_angle
            elif char == '[':
                stack.append((x, y, current_angle))
            elif char == ']':
                x, y, current_angle = stack.pop()

        painter.end()
        self.ui.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LSystem()
    window.show()
    sys.exit(app.exec())
