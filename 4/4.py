import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

from PIL import Image
from PIL.ImageQt import ImageQt

from design_4 import Ui_MainWindow


class AlphaEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Редактор альфа-канала")

        # Переменная для хранения оригинального изображения PIL
        self.original_pil_image = None

        # Настройка слайдера
        self.ui.edit_alpha.setRange(0, 255)

        # Подключение изменения значения слайдера к функции обновления
        self.ui.edit_alpha.valueChanged.connect(self.update_transparency)

        # Подключение кнопки сброса
        self.ui.pushButton.clicked.connect(self.reset_view)

        # Подключение меню
        self.ui.open_file.triggered.connect(self.open_image_dialog)

        QTimer.singleShot(100, self.open_image_dialog)

    def open_image_dialog(self) -> None:
        # Загрузка изображения
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                   "Изображение (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)")

        if not file_path:
            return

        try:
            # Открытие картинки через PIL
            self.original_pil_image = Image.open(file_path).convert("RGBA")

            # Сброс слайдера
            self.reset_view()
            self.ui.statusbar.showMessage("Изображение загружено", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def reset_view(self) -> None:
        # Сброс прозрачности к исходному состоянию
        if self.original_pil_image is None:
            return

        self.ui.edit_alpha.setValue(255)
        self.update_transparency(255)

    def update_transparency(self, slider_value: int) -> None:
        # Изменение альфа-канала картинки на основе значения слайдера
        if self.original_pil_image is None:
            return

        r, g, b, a = self.original_pil_image.split()

        # Коэффициент прозрачности
        multiplier = slider_value / 255.0

        # Альфа-канал каждого пикселя умножается на коэффициент.
        # Это позволяет менять прозрачность даже у PNG картинок,
        # у которых изначально был прозрачный фон
        new_a = a.point(lambda pixel: int(pixel * multiplier))

        # Обратный сбор изображения
        processed_img = Image.merge("RGBA", (r, g, b, new_a))

        # Конвертация PIL изображения в формат QPixmap
        qimage = ImageQt(processed_img)
        pixmap = QPixmap.fromImage(qimage)

        # Вывод изображения в QLabel
        scaled_pixmap = pixmap.scaled(
            self.ui.image.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.image.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AlphaEditor()
    window.show()
    sys.exit(app.exec())
