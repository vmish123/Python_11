import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QKeySequence

from design_2 import Ui_MainWindow


class TextEditor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Текстовый редактор")

        # Переменная для хранения пути к текущему открытому файлу
        self.current_file_path = None

        # Настройка горячих клавиш
        self.ui.create_new.setShortcut(QKeySequence("Ctrl+N"))
        self.ui.open_file.setShortcut(QKeySequence("Ctrl+O"))
        self.ui.save_file.setShortcut(QKeySequence("Ctrl+S"))

        self.ui.create_new.triggered.connect(self.create_new_file)
        self.ui.open_file.triggered.connect(self.open_file)
        self.ui.save_file.triggered.connect(self.save_file)
        self.ui.saveas_file.triggered.connect(self.save_file_as)

    def create_new_file(self) -> None:
        # Создание нового файла
        self.current_file_path = None
        self.ui.textBrowser.clear()

        # Поле доступно для редактирования
        self.ui.textBrowser.setReadOnly(False)

        self.setWindowTitle("Новый файл - Текстовый редактор")
        self.ui.statusbar.showMessage("Создан новый файл", 5000)

    def open_file(self) -> None:
        # Открытие файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовый файл (*.txt);;Все файлы (*)")

        if not file_path:
            return  # Пользователь отменил выбор

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            self.ui.textBrowser.setText(content)
            self.current_file_path = file_path

            # Поле доступно для редактирования
            self.ui.textBrowser.setReadOnly(False)

            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{filename} - Текстовый редактор")
            self.ui.statusbar.showMessage(f"Открыт файл: {filename}", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")
            self.ui.statusbar.showMessage("Ошибка при открытии файла.", 5000)

    def save_file(self) -> None:
        # Сохранение файла
        # Проверка, доступно ли поле для редактирования
        if self.ui.textBrowser.isReadOnly():
            self.ui.statusbar.showMessage("Нечего сохранять", 5000)
            return

        if self.current_file_path is None:
            # Если файл еще ни разу не сохранялся на диске
            self.save_file_as()
        else:
            # Перезапись файла
            self.write_to_disk(self.current_file_path)

    def save_file_as(self) -> None:
        # Сохранение файла в новом месте
        if self.ui.textBrowser.isReadOnly():
            self.ui.statusbar.showMessage("Нечего сохранять", 5000)
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как...", "", "Текстовый файл (*.txt);;Все файлы (*)")

        if file_path:
            self.write_to_disk(file_path)

    def write_to_disk(self, file_path: str) -> None:
        # Метод записи текста в файл
        try:
            content = self.ui.textBrowser.toPlainText()

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            self.current_file_path = file_path

            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{filename} - Текстовый редактор")
            self.ui.statusbar.showMessage(f"Сохранен файл: {filename}", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")
            self.ui.statusbar.showMessage("Ошибка при сохранении файла.", 5000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())
