import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from design_1 import Ui_Form


class Analysis(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Анализ файлов")

        # Флаг для проверки наличия загруженных данных
        self.data_loaded = False

        self.ui.load.clicked.connect(self.load_data)
        self.ui.save.clicked.connect(self.save_data)

    def load_data(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовый файл (*.txt);;Все файлы (*)")

        if not file_path:
            return  # Пользователь отменил выбор файла

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split текста по пробелам
            raw_data = content.split()

            if not raw_data:
                QMessageBox.critical(self, "Ошибка", "Выбран пустой файл")
                return

            # Преобразование в целые числа
            numbers = [int(item) for item in raw_data]

            # Вычисление максимального, минимального и среднего значений
            max_val = max(numbers)
            min_val = min(numbers)
            avg_val = sum(numbers) / len(numbers)

            self.ui.max.setText(str(max_val))
            self.ui.min.setText(str(min_val))
            self.ui.avg.setText(f"{avg_val:.2f}")

            self.data_loaded = True

        except ValueError:
            # В файле есть что-то кроме целых чисел
            QMessageBox.critical(self, "Ошибка", "Ожидаются только целые числа, разделенные пробелами")
            self.clear_fields()
        except Exception as e:
            # Обработка непредвиденных ошибок
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{e}")
            self.clear_fields()

    def save_data(self) -> None:
        if not self.data_loaded:
            QMessageBox.warning(self, "Внимание", "Нет данных для сохранения")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовый файл (*.txt);;Все файлы (*)")

        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Максимальное значение: {self.ui.max.text()}\n")
                file.write(f"Минимальное значение: {self.ui.min.text()}\n")
                file.write(f"Среднее значение: {self.ui.avg.text()}\n")
            QMessageBox.information(self, "Успешно", "Данные сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def clear_fields(self) -> None:
        # Очистка полей и сброс флага
        self.ui.max.clear()
        self.ui.min.clear()
        self.ui.avg.clear()
        self.data_loaded = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Analysis()
    window.show()
    sys.exit(app.exec())
