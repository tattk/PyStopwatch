from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QAction # type: ignore
from PyQt5.QtCore import QTimer 
from PyQt5.QtGui import QIcon 
import sys
import time

class StopwatchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.stopwatch = Stopwatch()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()
        self.menubar_visible = True  # メニューバーの表示状態を管理

        
    def toggle_menubar(self, checked):
        self.menubar_visible = checked
        self.tray_icon.setVisible(self.menubar_visible)
            
    def initUI(self):
        self.setWindowTitle("ストップウォッチ")
        self.setGeometry(100, 100, 300, 200)
        
        self.time_label = QLabel("00:00:00.00", self)
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold;")
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
        hours, remainder = divmod(int(total_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        hundredths = int((total_time - int(total_time)) * 100)
        return f"{hours:02}:{minutes:02}:{seconds:02}:{hundredths:02}"
    

            
class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__()
        self.setToolTip("ストップウォッチ")
        self.setIcon(QIcon("app_icon_menu.png"))
        self.menu = QMenu()
        
        self.show_action = QAction("ウィンドウを表示", self)
        self.show_action.triggered.connect(parent.show)
        
        self.exit_action = QAction("終了", self)
        self.exit_action.triggered.connect(sys.exit)
        
        self.show_menu_action = QAction("メニューバーに表示", self, checkable=True)
        self.show_menu_action.setChecked(True)
        self.show_menu_action.toggled.connect(parent.toggle_menubar)
        
        self.menu.addAction(self.show_menu_action)
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)
        
        self.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app_icon_docks.png"))
    window = StopwatchApp()
    window.show()
    sys.exit(app.exec())