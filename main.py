import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QTabBar, QStackedWidget, QLabel, QPushButton, QFrame, QScrollArea, QGridLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap


class Win11SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 11 Search")
        self.setMinimumSize(600, 400)
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(18)
        
        # 搜索框
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout(search_frame)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("在此键入以搜索")
        search_layout.addWidget(self.search_input)
        main_layout.addWidget(search_frame)
        
        # 标签栏
        self.tab_bar = QTabBar()
        self.tab_bar.addTab("All")
        self.tab_bar.addTab("Apps")
        self.tab_bar.addTab("Documents")
        self.tab_bar.addTab("Web")
        self.tab_bar.addTab("More")
        self.tab_bar.currentChanged.connect(self.change_tab)
        main_layout.addWidget(self.tab_bar)
        
        # 内容区域
        self.stacked_widget = QStackedWidget()
        
        # 创建各个标签页的内容
        self.create_all_page()
        self.create_apps_page()
        self.create_documents_page()
        self.create_web_page()
        self.create_more_page()
        
        main_layout.addWidget(self.stacked_widget)
        main_layout.addStretch()
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            #searchFrame {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit {
                border: none;
                font-size: 16px;
                padding: 5px;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin-right: 4px;
                border: none;
                background-color: transparent;
            }
            QTabBar::tab:selected {
                border-bottom: 2px solid #0078d4;
                color: #0078d4;
            }
            QPushButton {
                border: none;
                padding: 16px;
                background-color: white;
                border-radius: 8px;
                color: black;
                font-size: 15px;
                font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
            QLabel {
                color: black;
                font-size: 15px;
                font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            }
        """)

    def create_all_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Top apps 区域
        top_apps_label = QLabel("Top apps")
        top_apps_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(top_apps_label)
        
        apps_layout = QHBoxLayout()
        apps = [
            ("File Explorer", "file-explorer"),
            ("Settings", "settings"),
            ("Control Panel", "control-panel"),
            ("Microsoft Store", "store"),
            ("Groove Music", "music")
        ]
        
        for app_name, icon_name in apps:
            btn = QPushButton()
            btn.setFixedSize(120, 120)
            btn_layout = QVBoxLayout(btn)
            
            # 创建彩色块
            color_block = QLabel()
            color_block.setFixedSize(48, 48)
            colors = {
                "file-explorer": "#0078d4",
                "settings": "#50e6ff",
                "control-panel": "#8764b8",
                "store": "#107c10",
                "music": "#e81123"
            }
            color_block.setStyleSheet(f"background-color: {colors[icon_name]}; border-radius: 4px;")
            
            # 创建文本标签
            text_label = QLabel(app_name)
            text_label.setAlignment(Qt.AlignCenter)
            
            btn_layout.addWidget(color_block, alignment=Qt.AlignCenter)
            btn_layout.addWidget(text_label, alignment=Qt.AlignCenter)
            apps_layout.addWidget(btn)
        
        apps_layout.addStretch()
        layout.addLayout(apps_layout)
        
        # Recent 区域
        recent_label = QLabel("Recent")
        recent_label.setStyleSheet("font-size: 15px; font-weight: bold; margin: 18px 0 6px 0;")
        layout.addWidget(recent_label)
        
        recent_items = ["Registry Editor", "Run", "Control Panel", "Windows PowerShell"]
        recent_grid = QGridLayout()
        for idx, item in enumerate(recent_items):
            item_btn = QPushButton(item)
            item_btn.setStyleSheet("text-align: left; padding: 6px 14px; min-height: 32px; font-size: 14px; font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif; border-radius: 6px; margin-bottom: 6px;")
            row = idx // 2
            col = idx % 2
            recent_grid.addWidget(item_btn, row, col)
        layout.addLayout(recent_grid)
        
        # Quick searches 区域
        quick_searches_label = QLabel("Quick searches")
        quick_searches_label.setStyleSheet("font-size: 15px; font-weight: bold; margin: 18px 0 6px 0;")
        layout.addWidget(quick_searches_label)
        
        quick_items = ["Weather", "Top news", "Today in history", "Coronavirus tips"]
        quick_grid = QGridLayout()
        for idx, item in enumerate(quick_items):
            item_btn = QPushButton(item)
            item_btn.setStyleSheet("text-align: left; padding: 6px 14px; min-height: 32px; font-size: 14px; font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif; border-radius: 6px; margin-bottom: 6px;")
            row = idx // 2
            col = idx % 2
            quick_grid.addWidget(item_btn, row, col)
        layout.addLayout(quick_grid)
        
        layout.addStretch()
        
        self.stacked_widget.addWidget(page)

    def create_apps_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Apps Page Content"))
        self.stacked_widget.addWidget(page)

    def create_documents_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Documents Page Content"))
        self.stacked_widget.addWidget(page)

    def create_web_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Web Page Content"))
        self.stacked_widget.addWidget(page)

    def create_more_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("More Page Content"))
        self.stacked_widget.addWidget(page)

    def change_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Win11SearchWindow()
    window.show()
    sys.exit(app.exec())