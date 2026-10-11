import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from PIL import Image
from PIL.ImageQt import ImageQt

from design_3 import Ui_MainWindow


class ImageEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Редактор изображений")

        # Переменные для хранения состояния
        self.original_pil_image = None
        self.current_rotation = 0
        self.current_channel = None

        # Подключение кнопок поворота
        self.ui.rotate_left.clicked.connect(lambda: self.rotate_image(90))
        self.ui.rotate_right.clicked.connect(lambda: self.rotate_image(-90))

        # Подключение радиокнопок
        self.ui.radio_red.toggled.connect(self.channel_changed)
        self.ui.radio_green.toggled.connect(self.channel_changed)
        self.ui.radio_blue.toggled.connect(self.channel_changed)

        # Подключение кнопки "Сброс вида"
        self.ui.pushButton.clicked.connect(self.reset_view)

        self.ui.open_file.triggered.connect(self.open_image_dialog)
        QTimer.singleShot(100, self.open_image_dialog)

    def open_image_dialog(self) -> None:
        # Диалоговое окно выбора
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                   "Изображение (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)")

        if not file_path:
            return

        try:
            # Открытие картинки через PIL
            self.original_pil_image = Image.open(file_path).convert("RGB")
            self.reset_view()
            self.ui.statusbar.showMessage("Изображение загружено", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def rotate_image(self, angle: int) -> None:
        # Изменение угла поворота
        if self.original_pil_image is None:
            return

        self.current_rotation = (self.current_rotation + angle) % 360
        self.update_display()

    def channel_changed(self) -> None:
        # Изменение цветового канала
        if self.ui.radio_red.isChecked():
            self.current_channel = 'red'
        elif self.ui.radio_green.isChecked():
            self.current_channel = 'green'
        elif self.ui.radio_blue.isChecked():
            self.current_channel = 'blue'
        else:
            self.current_channel = None

        self.update_display()

    def reset_view(self) -> None:
        # Сброс вида изображения
        if self.original_pil_image is None:
            return

        self.current_rotation = 0
        self.current_channel = None

        # Снятие выделения с RadioButton
        for radio in (self.ui.radio_red, self.ui.radio_green, self.ui.radio_blue):
            radio.setAutoExclusive(False)
            radio.setChecked(False)
            radio.setAutoExclusive(True)

        self.update_display()

    def update_display(self) -> None:
        # Применение поворота и цветового канала к изображению
        if self.original_pil_image is None:
            return

        # Получение копии оригинала изображение
        processed_img = self.original_pil_image.copy()

        # Поворот изображения
        if self.current_rotation != 0:
            processed_img = processed_img.rotate(self.current_rotation, expand=True)

        # Применение цветового канала
        if self.current_channel:
            r, g, b = processed_img.split()
            # Создание пустого черного канала размера изображения
            zero_band = Image.new('L', processed_img.size, 0)

            # Повторный сбор картинки
            if self.current_channel == 'red':
                processed_img = Image.merge("RGB", (r, zero_band, zero_band))
            elif self.current_channel == 'green':
                processed_img = Image.merge("RGB", (zero_band, g, zero_band))
            elif self.current_channel == 'blue':
                processed_img = Image.merge("RGB", (zero_band, zero_band, b))

        # Конвертация PIL изображения в формат QPixmap
        qimage = ImageQt(processed_img)
        pixmap = QPixmap.fromImage(qimage)

        # Вывод изображения в QLabel
        scaled_pixmap = pixmap.scaled(self.ui.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.ui.image.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec())
