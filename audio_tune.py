import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QFrame, QMenuBar, QMenu, QComboBox, QSpinBox, QDial, QCheckBox)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class AudioTuneWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("汽车调音台 🎚️")
        self.setMinimumSize(1100, 650)
        self.init_ui()

    def init_ui(self):
        # 顶部菜单栏
        menubar = QMenuBar(self)
        file_menu = QMenu("文件", self)
        config_menu = QMenu("配置", self)
        device_menu = QMenu("未连接设备", self)
        preset_menu = QMenu("预设存储", self)
        menubar.addMenu(file_menu)
        menubar.addMenu(config_menu)
        menubar.addMenu(device_menu)
        menubar.addMenu(preset_menu)
        self.setMenuBar(menubar)

        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(10)
        self.setCentralWidget(main_widget)

        # 左侧汽车视图和参数
        left_panel = QVBoxLayout()
        car_frame = QFrame()
        car_layout = QVBoxLayout(car_frame)
        car_label = QLabel("🚗\n\n前\n⬆️\n\n后")
        car_label.setAlignment(Qt.AlignCenter)
        car_label.setStyleSheet("font-size: 32px;")
        car_layout.addWidget(car_label)
        # 环绕喇叭 emoji
        surround_layout = QHBoxLayout()
        surround_layout.addWidget(QLabel("🔊"))
        surround_layout.addStretch()
        surround_layout.addWidget(QLabel("🔊"))
        car_layout.addLayout(surround_layout)
        left_panel.addWidget(car_frame)
        # 低音/高音/重置等按钮
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("高级"))
        btn_layout.addWidget(QPushButton("重置"))
        left_panel.addLayout(btn_layout)
        # 参数区
        param_grid = QGridLayout()
        param_grid.addWidget(QLabel("高通类型"), 0, 0)
        param_grid.addWidget(QComboBox(), 0, 1)
        param_grid.addWidget(QLabel("低通类型"), 1, 0)
        param_grid.addWidget(QComboBox(), 1, 1)
        param_grid.addWidget(QLabel("高通频率"), 2, 0)
        param_grid.addWidget(QSpinBox(), 2, 1)
        param_grid.addWidget(QLabel("低通频率"), 3, 0)
        param_grid.addWidget(QSpinBox(), 3, 1)
        left_panel.addLayout(param_grid)
        left_panel.addStretch()
        main_layout.addLayout(left_panel, 2)

        # 中间均衡器区
        eq_panel = QVBoxLayout()
        # 频率点标签
        freq_layout = QHBoxLayout()
        for freq in ["20Hz", "50Hz", "100Hz", "200Hz", "500Hz", "1kHz", "2kHz", "5kHz", "10kHz", "20kHz"]:
            freq_label = QLabel(freq)
            freq_label.setAlignment(Qt.AlignCenter)
            freq_layout.addWidget(freq_label)
        eq_panel.addLayout(freq_layout)
        # 均衡器滑块
        slider_layout = QHBoxLayout()
        self.sliders = []
        for i in range(10):
            vbox = QVBoxLayout()
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-20)
            slider.setMaximum(20)
            slider.setValue(0)
            slider.setTickInterval(5)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setFixedHeight(180)
            slider.valueChanged.connect(self.update_eq_label)
            self.sliders.append(slider)
            vbox.addWidget(slider)
            val_label = QLabel("0dB")
            val_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(val_label)
            slider.val_label = val_label
            slider_layout.addLayout(vbox)
        eq_panel.addLayout(slider_layout)
        # 通道选择
        ch_layout = QHBoxLayout()
        for ch in range(1, 7):
            btn = QPushButton(f"CH{ch}")
            btn.setCheckable(True)
            if ch == 1:
                btn.setChecked(True)
            ch_layout.addWidget(btn)
        eq_panel.addLayout(ch_layout)
        main_layout.addLayout(eq_panel, 6)

        # 右侧音量和限制器
        right_panel = QVBoxLayout()
        # 主音量
        main_vol_label = QLabel("主音量 🎚️")
        main_vol_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(main_vol_label)
        main_vol_slider = QSlider(Qt.Vertical)
        main_vol_slider.setMinimum(-60)
        main_vol_slider.setMaximum(12)
        main_vol_slider.setValue(0)
        main_vol_slider.setTickInterval(6)
        main_vol_slider.setTickPosition(QSlider.TicksBothSides)
        main_vol_slider.setFixedHeight(140)
        right_panel.addWidget(main_vol_slider)
        right_panel.addWidget(QLabel("0dB", alignment=Qt.AlignCenter))
        # 各通道音量
        ch_vol_grid = QGridLayout()
        for i, name in enumerate(["前左", "前右", "后左", "后右", "CH5", "CH6"]):
            ch_label = QLabel(f"{name}")
            ch_slider = QSlider(Qt.Horizontal)
            ch_slider.setMinimum(-60)
            ch_slider.setMaximum(12)
            ch_slider.setValue(0)
            ch_slider.setTickInterval(6)
            ch_slider.setTickPosition(QSlider.TicksBothSides)
            ch_vol_grid.addWidget(ch_label, i, 0)
            ch_vol_grid.addWidget(ch_slider, i, 1)
            ch_vol_grid.addWidget(QLabel("0dB"), i, 2)
        right_panel.addLayout(ch_vol_grid)
        # 限制器
        limiter_label = QLabel("限制器 🛑")
        limiter_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(limiter_label)
        limiter_grid = QGridLayout()
        limiter_grid.addWidget(QLabel("启动时间"), 0, 0)
        limiter_grid.addWidget(QComboBox(), 0, 1)
        limiter_grid.addWidget(QLabel("释放时间"), 1, 0)
        limiter_grid.addWidget(QComboBox(), 1, 1)
        limiter_grid.addWidget(QLabel("阈值"), 2, 0)
        limiter_grid.addWidget(QSpinBox(), 2, 1)
        right_panel.addLayout(limiter_grid)
        right_panel.addStretch()
        main_layout.addLayout(right_panel, 3)

    def update_eq_label(self):
        for slider in self.sliders:
            slider.val_label.setText(f"{slider.value()}dB")

def main():
    app = QApplication(sys.argv)
    win = AudioTuneWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()