import sys
import requests
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                               QTableWidgetItem)
from PySide6.QtCore import Qt, QThreadPool, QRunnable, Signal, QObject
from PySide6.QtGui import QColor, QDesktopServices, QPixmap
from PySide6.QtCore import QUrl


# 定义了一个信号类，用于在歌曲信息获取完成后发出信号。
class FetchSongWorkerSignals(QObject):
    result = Signal(dict)


# 这是一个工作线程类，负责向 API 发送请求并处理响应。成功获取数据后会发出 result 信号。
class FetchSongWorker(QRunnable):
    def __init__(self, msg, n):
        super().__init__()
        self.msg = msg
        self.n = n
        self.signals = FetchSongWorkerSignals()

    def run(self):
        url = f"https://api.lolimi.cn/API/wydg/api.php?msg={self.msg}&n={self.n}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if result['code'] == 200:
                    self.signals.result.emit(result)
            elif response.status_code == 500:
                print("请求失败的n = ", self.n)
        except requests.RequestException as e:
            print(e)


# 这是主窗口类，负责初始化和显示用户界面
class MusicParser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread_pool = QThreadPool()

    # 初始化用户界面
    def initUI(self):
        self.setWindowTitle('奈特椅子音乐解析器')
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowIcon(QPixmap('music.png'))

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('请输入歌曲名字或歌词...')
        input_layout.addWidget(self.input_field)

        self.parse_button = QPushButton('解析', self)
        self.parse_button.clicked.connect(self.start_parsing)
        input_layout.addWidget(self.parse_button)

        layout.addLayout(input_layout)

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['歌曲名', '作者名', 'MP3下载链接'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.result_table)

        self.setLayout(layout)

        # Connect the signal once during initialization
        self.result_table.cellClicked.connect(self.open_link)

    # 当用户点击“解析”按钮时，会启动多个工作线程向 API 发送请求，并清空表格显示区域
    def start_parsing(self):
        msg = self.input_field.text()
        if not msg:
            return

        self.result_table.setRowCount(0)
        for n in range(1, 11):
            worker = FetchSongWorker(msg, n)
            worker.signals.result.connect(self.display_result)
            self.thread_pool.start(worker)

    # 将获取到的歌曲信息添加到表格中，并设置下载链接的显示和点击事件
    def display_result(self, result):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)

        self.result_table.setItem(row_position, 0, QTableWidgetItem(result['name']))
        self.result_table.setItem(row_position, 1, QTableWidgetItem(result['author']))

        mp3_item = QTableWidgetItem(result['mp3'])
        mp3_item.setForeground(QColor(Qt.blue))
        mp3_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        mp3_item.setTextAlignment(Qt.AlignCenter)
        self.result_table.setItem(row_position, 2, mp3_item)

        mp3_item.setData(Qt.UserRole, QUrl(result['mp3']))

    # 当用户点击表格中的链接时，使用默认浏览器打开对应的MP3下载链接。
    def open_link(self, row, column):
        if column == 2:
            item = self.result_table.item(row, column)
            if item:
                QDesktopServices.openUrl(item.data(Qt.UserRole))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser = MusicParser()
    parser.show()
    sys.exit(app.exec())
