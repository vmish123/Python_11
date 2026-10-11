import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

from design_7 import Ui_MainWindow


class Piano(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Фортепиано")

        # Инициализация переменных для хранения партитуры и текущего шага
        self.score = []
        self.current_note_index = 0

        # Определение словаря для сопоставления названий нот и аудиофайлов
        self.note_files = {
            "C": "C_major.wav",
            "D": "D_major.wav",
            "E": "E_major.wav",
            "F": "F_minor.wav",
            "G": "G_minor.wav",
            "A": "A_minor.wav",
            "B": "B_major.wav",
            "C2": "C2_major.wav"
        }

        # Создание словаря для звуков и вызов метода их предзагрузки
        self.sounds = {}
        self.init_audio()

        # Подключение кнопок клавиатуры к методу воспроизведения соответствующих нот
        self.ui.C_button.clicked.connect(lambda: self.play_note("C"))
        self.ui.D_button.clicked.connect(lambda: self.play_note("D"))
        self.ui.E_button.clicked.connect(lambda: self.play_note("E"))
        self.ui.F_button.clicked.connect(lambda: self.play_note("F"))
        self.ui.G_button.clicked.connect(lambda: self.play_note("G"))
        self.ui.A_button.clicked.connect(lambda: self.play_note("A"))
        self.ui.B_button.clicked.connect(lambda: self.play_note("B"))
        self.ui.C2_button.clicked.connect(lambda: self.play_note("C2"))

        # Подключение действия меню к методу загрузки партитуры
        self.ui.open_file.triggered.connect(self.load_score)

    def init_audio(self) -> None:
        # Предзагрузка аудиофайлов в память для воспроизведения без задержек

        # Определение путей к текущей директории и папке со звуковыми файлами
        base_dir = os.path.dirname(os.path.abspath(__file__))
        notes_dir = os.path.join(base_dir, "notes")

        # Проверка существования папки с аудиофайлами
        if not os.path.exists(notes_dir):
            QMessageBox.warning(self, "Внимание", "Поместите звуковые файлы в директорию ./notes/")
            return

        # Итерация по словарю файлов и загрузка каждого звука в объект QSoundEffect
        for note, filename in self.note_files.items():
            file_path = os.path.join(notes_dir, filename)

            # Проверка наличия конкретного файла перед его загрузкой
            if os.path.exists(file_path):
                effect = QSoundEffect()
                effect.setSource(QUrl.fromLocalFile(file_path))
                effect.setVolume(1.0)
                self.sounds[note] = effect

    def load_score(self) -> None:
        # Чтение текстового файла с нотами

        # Вызов диалогового окна для выбора текстового файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть партитуру", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*)")

        # Прерывание выполнения, если пользователь отменил выбор
        if not file_path:
            return

        try:
            # Чтение содержимого файла с удалением лишних пробелов
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

            # Отображение сообщения, если файл оказался пустым
            if not content:
                QMessageBox.warning(self, "Внимание", "Файл пуст")
                return

            # Разбиение текста на слова и фильтрация только известных нот
            raw_notes = content.split()
            self.score = [n for n in raw_notes if n in self.note_files]

            # Вывод предупреждения, если корректных нот не найдено
            if not self.score:
                QMessageBox.warning(self, "Ошибка", "В файле нет известных нот")
                return

            # Сброс счетчика прогресса, обновление экрана и вывод статуса
            self.current_note_index = 0
            self.update_score_display()
            self.ui.statusbar.showMessage("Партитура загружена", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{e}")

    def play_note(self, note: str) -> None:
        # Воспроизведение звука и проверка попадания в ноты партитуры

        # Воспроизведение звука нажатой клавиши
        if note in self.sounds:
            self.sounds[note].play()

        # Прерывание проверки, если партитура пуста или уже пройдена до конца
        if not self.score or self.current_note_index >= len(self.score):
            return

        # Сравнение нажатой ноты с ожидаемой
        expected_note = self.score[self.current_note_index]
        if note == expected_note:
            self.current_note_index += 1
            self.update_score_display()

    def update_score_display(self) -> None:
        # Обновление интерфейса с использованием HTML для эффекта бегущей строки

        if self.current_note_index >= len(self.score):
            self.ui.label.setText("Импортируйте партитуру")
            self.score = []
            return

        # Формирование срезов для прошедших, текущей и будущих нот
        past_notes = self.score[max(0, self.current_note_index - 4): self.current_note_index]
        current_note = self.score[self.current_note_index]
        future_notes = self.score[self.current_note_index + 1: self.current_note_index + 8]

        # Объединение нот в строки с использованием неразрывных пробелов для предотвращения переноса строк
        past_str = "&nbsp;&nbsp;&nbsp;".join(past_notes)
        future_str = "&nbsp;&nbsp;&nbsp;".join(future_notes)

        # Создание HTML-таблицы для выравнивания элементов на экране
        html = f"""
        <table width="100%" height="100%">
            <tr>
                <td width="40%" align="right" valign="middle" style="color: #b0b0b0; font-size: 32px;">
                    {past_str}&nbsp;&nbsp;
                </td>

                <td width="20%" align="center" valign="middle" style="color: #d32f2f; font-size: 64px; font-weight: bold;">
                    {current_note}
                </td>

                <td width="40%" align="left" valign="middle" style="color: #212121; font-size: 32px;">
                    &nbsp;&nbsp;{future_str}
                </td>
            </tr>
        </table>
        """

        # Установка сформированного HTML-кода в QLabel
        self.ui.label.setText(html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Piano()
    window.show()
    sys.exit(app.exec())
