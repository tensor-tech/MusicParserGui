import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCursor


class MusicParser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.song_number = 1

    def initUI(self):
        self.setWindowTitle("音乐解析器")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("输入歌曲名称或歌词")
        self.input_box.returnPressed.connect(self.fetch_song_info)
        layout.addWidget(self.input_box)

        self.result_box = QTextEdit(self)
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def fetch_song_info(self):
        song_name = self.input_box.text()
        url = f"https://api.lolimi.cn/API/wydg/api.php?msg={song_name}&n={self.song_number}"
        response = requests.get(url)
        data = response.json()

        if data["code"] == 200:
            self.display_song_info(data)
            self.song_number += 1
        else:
            self.result_box.append(f"<span style='color:red;'>查询失败: {data['msg']}</span>")

    def display_song_info(self, data):
        song_name = data['name']
        author = data['author']
        mp3_url = data['mp3']

        self.result_box.moveCursor(QTextCursor.End)
        self.result_box.insertHtml(f"<p><b>序号 {self.song_number}:</b></p>")
        self.result_box.insertHtml(f"<p><span style='color:blue;'>歌曲名称:</span> {song_name}</p>")
        self.result_box.insertHtml(f"<p><span style='color:green;'>歌手名称:</span> {author}</p>")
        self.result_box.insertHtml(f"<p><a href='{mp3_url}' style='color:purple;'>点我</a></p>")
        self.result_box.insertHtml("<hr>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    parser = MusicParser()
    parser.show()
    sys.exit(app.exec())
