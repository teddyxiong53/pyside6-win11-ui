import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QFrame, QComboBox, QSpinBox, QCheckBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
import numpy as np

class ChartWidget(QWidget):
    def __init__(self, x, y, title, color, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.title = title
        self.color = color
        self.setMinimumSize(220, 220)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255,255,255))
        margin = 35
        w, h = self.width(), self.height()
        # 坐标轴
        painter.setPen(QPen(Qt.gray, 2))
        painter.drawLine(margin, h-margin, w-margin, h-margin)
        painter.drawLine(margin, h-margin, margin, margin)
        # 标题
        painter.setPen(Qt.black)
        painter.drawText(margin, 20, self.title)
        # 曲线
        if len(self.x) > 1:
            painter.setPen(QPen(self.color, 2))
            scale_x = (w-2*margin)/(max(self.x)-min(self.x))
            scale_y = (h-2*margin)/(max(self.y)-min(self.y)) if max(self.y)!=min(self.y) else 1
            points = [
                (margin + (xi-min(self.x))*scale_x, h-margin - (yi-min(self.y))*scale_y)
                for xi, yi in zip(self.x, self.y)
            ]
            for i in range(len(points)-1):
                painter.drawLine(int(points[i][0]), int(points[i][1]), int(points[i+1][0]), int(points[i+1][1]))
        # 锁图标 emoji
        painter.drawText(w-margin-20, margin+10, "🔒")
        painter.drawText(margin+5, h-margin-5, "m")

class CrossoverWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(260, 220)
        # mock数据
        self.freq = np.logspace(1.8, 4, 100)
        self.low = -20 + 20/(1+np.exp((self.freq-1000)/200))
        self.high = -20 + 20/(1+np.exp((1000-self.freq)/200))
        self.sum = np.maximum(self.low, self.high)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255,255,255))
        margin = 35
        w, h = self.width(), self.height()
        # 坐标轴
        painter.setPen(QPen(Qt.gray, 2))
        painter.drawLine(margin, h-margin, w-margin, h-margin)
        painter.drawLine(margin, h-margin, margin, margin)
        # 频率刻度
        for i, f in enumerate([100, 1000, 10000]):
            x = margin + (w-2*margin)*(np.log10(f)-2)/(4-2)
            painter.drawText(int(x)-10, h-margin+18, f"{f}")
        # 曲线
        def draw_curve(y, color):
            painter.setPen(QPen(color, 2))
            for i in range(len(self.freq)-1):
                x1 = margin + (w-2*margin)*(np.log10(self.freq[i])-2)/(4-2)
                y1 = h-margin - (y[i]+30)*(h-2*margin)/60
                x2 = margin + (w-2*margin)*(np.log10(self.freq[i+1])-2)/(4-2)
                y2 = h-margin - (y[i+1]+30)*(h-2*margin)/60
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        draw_curve(self.low, QColor(0,0,255))
        draw_curve(self.high, QColor(255,0,0))
        draw_curve(self.sum, QColor(200,0,200))
        # 图例
        painter.setPen(Qt.blue)
        painter.drawText(w-margin-60, margin+10, "Low Band")
        painter.setPen(Qt.red)
        painter.drawText(w-margin-60, margin+30, "High Band")
        painter.setPen(QColor(200,0,200))
        painter.drawText(w-margin-60, margin+50, "Sum")

class AudioDRCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("音频处理台 🎵")
        self.setMinimumSize(1100, 650)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # 左侧低频
        low_x = np.linspace(-120, 0, 50)
        low_y = np.clip(low_x+120, 0, 120)-120
        low_chart = ChartWidget(low_x, low_y, "低频 (<1000Hz)", QColor(0, 120, 255))
        low_panel = QVBoxLayout()
        low_panel.addWidget(QLabel("Low 🎚️"))
        low_panel.addWidget(low_chart)
        low_panel.addWidget(QCheckBox("ON"))
        low_panel.addWidget(QLabel("Solo  Mute  Mixer Gain 1"))
        low_panel.addWidget(QPushButton("Basic"))
        low_panel.addWidget(QLabel("Threshold (dB)"))
        low_panel.addWidget(QSlider(Qt.Horizontal))
        low_panel.addWidget(QLabel("Attack(ms)  Release(ms)  Energy(ms)"))
        low_panel.addStretch()
        main_layout.addLayout(low_panel, 3)

        # 中间高频
        high_x = np.linspace(-120, 0, 50)
        high_y = np.clip(high_x+120, 0, 120)-120
        high_chart = ChartWidget(high_x, high_y, "高频 (>1000Hz)", QColor(255, 120, 0))
        high_panel = QVBoxLayout()
        high_panel.addWidget(QLabel("High 🎚️"))
        high_panel.addWidget(high_chart)
        high_panel.addWidget(QCheckBox("ON"))
        high_panel.addWidget(QLabel("Solo  Mute  Mixer Gain 1"))
        high_panel.addWidget(QPushButton("Basic"))
        high_panel.addWidget(QLabel("Threshold (dB)"))
        high_panel.addWidget(QSlider(Qt.Horizontal))
        high_panel.addWidget(QLabel("Attack(ms)  Release(ms)  Energy(ms)"))
        high_panel.addStretch()
        main_layout.addLayout(high_panel, 3)

        # 右侧分频器
        crossover_panel = QVBoxLayout()
        crossover_panel.addWidget(QLabel("Crossover 🎛️"))
        crossover_panel.addWidget(CrossoverWidget())
        crossover_panel.addWidget(QLabel("Filter Type: ButterWorth 2"))
        crossover_panel.addWidget(QLabel("Low FC1(Hz): 1000"))
        crossover_panel.addStretch()
        main_layout.addLayout(crossover_panel, 4)

        # 右上角开关
        onoff = QCheckBox("ON")
        onoff.setChecked(True)
        onoff.setStyleSheet("font-size: 18px;")
        self.statusBar().addPermanentWidget(onoff)


def main():
    app = QApplication(sys.argv)
    win = AudioDRCWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()