from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QAction # type: ignore
from PyQt5.QtCore import QTimer # type: ignore
from PyQt5.QtGui import QIcon # type: ignore
import sys
import time

class StopwatchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stopwatch = Stopwatch()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

    def initUI(self):
        self.setWindowTitle("ストップウォッチ")
        self.setGeometry(100, 100, 300, 200)
        
        self.time_label = QLabel("00:00:00.00", self)
        self.start_stop_button = QPushButton("スタート", self)
        self.lap_button = QPushButton("ラップ", self)
        self.reset_button = QPushButton("リセット", self)
        self.lap_list = QListWidget(self)
        
        self.start_stop_button.clicked.connect(self.toggle)
        self.lap_button.clicked.connect(self.record_lap)
        self.reset_button.clicked.connect(self.reset)
        
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.lap_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.lap_list)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()
    
    def toggle(self):
        if self.stopwatch.running:
            self.stopwatch.stop()
            self.timer.stop()
            self.start_stop_button.setText("スタート")
        else:
            self.stopwatch.start()
            self.timer.start(10)
            self.start_stop_button.setText("ストップ")
    
    def update_time(self):
        elapsed = self.stopwatch.get_elapsed_time()
        self.time_label.setText(elapsed)
        self.tray_icon.setToolTip(elapsed)
    
    def record_lap(self):
        self.lap_list.addItem(self.stopwatch.get_elapsed_time())
    
    def reset(self):
        self.stopwatch.reset()
        self.timer.stop()
        self.time_label.setText("00:00:00.00")
        self.lap_list.clear()
        self.start_stop_button.setText("スタート")

class Stopwatch:
    def __init__(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time

    def reset(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.running:
            total_time = time.time() - self.start_time
        else:
            total_time = self.elapsed_time
        minutes, seconds = divmod(int(total_time), 60)
        hundredths = int((total_time - int(total_time)) * 100)
        return f"{minutes:02}:{seconds:02}:{hundredths:02}"

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__(parent)
        self.setToolTip("ストップウォッチ")
        self.setIcon(QIcon())
        self.menu = QMenu()
        self.show_action = QAction("ウィンドウを表示", self)
        self.exit_action = QAction("終了", self)
        self.exit_action.triggered.connect(sys.exit)
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StopwatchApp()
    window.show()
    sys.exit(app.exec())