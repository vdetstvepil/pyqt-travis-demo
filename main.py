from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QColorDialog
import sys
import resources_rc

class TextEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.ui", self)

        # Инициализация переменных
        self.current_file = None  # Путь к открытому файлу

        # Привязываем кнопки к функциям
        self.btn_new.clicked.connect(self.new_file)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)

        # Привязываем элементы форматирования
        self.fontComboBox.currentFontChanged.connect(self.change_font)
        self.sizeComboBox.currentTextChanged.connect(self.change_font_size)
        self.btn_bold.clicked.connect(self.toggle_bold)
        self.btn_italic.clicked.connect(self.toggle_italic)
        self.btn_underline.clicked.connect(self.toggle_underline)
        self.btn_textColor.clicked.connect(self.change_text_color)
        self.btn_bgColor.clicked.connect(self.change_bg_color)

        # Устанавливаем текст "Новый файл" при старте
        self.fileLabel.setText("Новый файл")

        self.text_changed = False
        self.textEdit.textChanged.connect(self.mark_text_as_changed)

    def new_file(self):
        """Создаёт новый файл, проверяя несохранённые изменения."""
        if not self.confirm_save():
            return  # Если выбрали "Отмена" – не продолжаем

        self.textEdit.clear()
        self.current_file = None
        self.fileLabel.setText("Новый файл")
        self.text_changed = False  # Сбрасываем флаг изменений

    def open_file(self):
        """Открывает HTML-файл, запрашивая сохранение перед этим."""
        if not self.confirm_save():
            return  # Если выбрали "Отмена" – не продолжаем

        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "HTML файлы (*.html);;Все файлы (*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.textEdit.setHtml(file.read())
            self.current_file = file_path
            self.fileLabel.setText(file_path)
            self.text_changed = False  # Сбрасываем флаг изменений

    def save_file(self):
        """Сохраняет файл в HTML, чтобы сохранить стиль текста."""
        if not self.current_file:
            self.current_file, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "HTML файлы (*.html);;Все файлы (*)"
            )

        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.textEdit.toHtml())  # Сохраняем в HTML
            self.fileLabel.setText(self.current_file)

    def change_font(self, font):
        """Меняет шрифт выделенного текста."""
        fmt = self.textEdit.currentCharFormat()
        fmt.setFont(font)
        self.textEdit.setCurrentCharFormat(fmt)

    def change_font_size(self, size):
        """Меняет размер шрифта."""
        if size.isdigit():
            fmt = self.textEdit.currentCharFormat()
            fmt.setFontPointSize(int(size))
            self.textEdit.setCurrentCharFormat(fmt)

    def toggle_bold(self):
        """Переключает жирный шрифт."""
        fmt = self.textEdit.currentCharFormat()
        fmt.setFontWeight(QFont.Bold if fmt.fontWeight() != QFont.Bold else QFont.Normal)
        self.textEdit.setCurrentCharFormat(fmt)

    def toggle_italic(self):
        """Переключает курсив."""
        fmt = self.textEdit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.textEdit.setCurrentCharFormat(fmt)

    def toggle_underline(self):
        """Переключает подчеркивание."""
        fmt = self.textEdit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.textEdit.setCurrentCharFormat(fmt)

    def change_text_color(self):
        """Открывает диалог выбора цвета текста."""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.textEdit.currentCharFormat()
            fmt.setForeground(color)
            self.textEdit.setCurrentCharFormat(fmt)

    def change_bg_color(self):
        """Открывает диалог выбора цвета фона текста."""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.textEdit.currentCharFormat()
            fmt.setBackground(color)
            self.textEdit.setCurrentCharFormat(fmt)

    def mark_text_as_changed(self):
        """Помечает текст как изменённый."""
        self.text_changed = True

    def confirm_save(self):
        """Проверяет, нужно ли сохранить файл перед важными действиями."""
        if not self.text_changed:
            return True  # Если изменений нет, продолжаем

        reply = QtWidgets.QMessageBox.question(
            self, "Сохранение", "Сохранить изменения перед продолжением?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.save_file()
            return True
        elif reply == QtWidgets.QMessageBox.No:
            return True
        else:
            return False  # Отмена действия

    def closeEvent(self, event):
        """Обрабатывает закрытие окна, запрашивая сохранение."""
        if self.confirm_save():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
