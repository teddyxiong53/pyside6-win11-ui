import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QGroupBox, QFrame, QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

class IndustrialPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FAUI Industrial Solutions - OperationPanel")
        self.setMinimumSize(1400, 800)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # 左侧 - 轴承温度与状态
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.create_bearing_temp_group())
        left_panel.addStretch()
        main_layout.addLayout(left_panel, 2)

        # 中间 - 控制与状态
        center_panel = QVBoxLayout()
        center_panel.addWidget(self.create_test_rig_controls_group())
        center_panel.addWidget(self.create_shutdown_vibration_group())
        center_panel.addWidget(self.create_motor_lubrication_group())
        center_panel.addStretch()
        main_layout.addLayout(center_panel, 3)

        # 右侧 - 关断、速度、流量等
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.create_shutdown_temp_group())
        right_panel.addWidget(self.create_shutdown_speed_group())
        right_panel.addWidget(self.create_shutdown_flow_group())
        right_panel.addWidget(self.create_shutdown_axial_group())
        right_panel.addStretch()
        main_layout.addLayout(right_panel, 2)

    def create_bearing_temp_group(self):
        group = QGroupBox("TEST BEARING - OUTER TEMPS °F")
        layout = QGridLayout()
        bearings = [
            ("Outer Bearing 1 0deg", 80.9), ("Outer Bearing 1 180deg", 92.5),
            ("Outer Bearing 1 240deg", 47.5), ("Outer Bearing 2 0deg", 47.1),
            ("Outer Bearing 2 180deg", 36.2), ("Outer Bearing 2 240deg", 36.2),
            ("Inner Bearing 1 0deg", 106.0), ("Inner Bearing 1 180deg", 81.6),
            ("Inner Bearing 1 240deg", 36.2), ("Inner Bearing 2 0deg", 36.2),
            ("Inner Bearing 2 180deg", 36.2), ("Inner Bearing 2 240deg", 36.2),
            ("Shaft Temp 0deg", 41.5), ("Shaft Temp 180deg", 41.5)
        ]
        for i, (name, val) in enumerate(bearings):
            layout.addWidget(QLabel(name), i, 0)
            temp_label = QLabel(str(val))
            if val > 100:
                temp_label.setStyleSheet("background: yellow; color: black;")
            elif val > 80:
                temp_label.setStyleSheet("background: #ffcccc; color: black;")
            layout.addWidget(temp_label, i, 1)
        group.setLayout(layout)
        return group

    def create_test_rig_controls_group(self):
        group = QGroupBox("TEST RIG CONTROLS")
        layout = QGridLayout()
        # Motor/油泵/冷却等按钮
        buttons = ["Motor Speed", "Axial Load", "Oil Flow", "Oil Flow Bed", "Manifold Temp"]
        for i, name in enumerate(buttons):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLineEdit("0.0"), i, 1)
        # 控制按钮
        btn_names = ["Drive Motor", "Test Oil Pump", "Scavenge Pump", "Hydraulic Pump", "Motor Lube Pump", "Chiller Run"]
        for i, name in enumerate(btn_names):
            layout.addWidget(QPushButton("START"), i, 2)
            layout.addWidget(QPushButton("STOP"), i, 3)
        group.setLayout(layout)
        return group

    def create_shutdown_vibration_group(self):
        group = QGroupBox("SHUTDOWN VIBRATION")
        layout = QGridLayout()
        items = [
            ("Test Bearing 1 Vert MIN", 33.0), ("Test Bearing 2 Vert MAX", 33.0),
            ("Test Bearing Shaft Axial", 33.0), ("Motor Vert Coupled End", 33.0),
            ("Motor Vert Couple End", 33.0), ("Motor Axial MAX", 56.0)
        ]
        for i, (name, val) in enumerate(items):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLabel(str(val)), i, 1)
        group.setLayout(layout)
        return group

    def create_motor_lubrication_group(self):
        group = QGroupBox("MOTOR LUBRICATION")
        layout = QVBoxLayout()
        # 指示灯
        indicators = ["E-STOP LOCAL", "E-STOP REMOTE 1", "E-STOP REMOTE 2", "SAFETY RELAY", "HYDRAULIC PRESSURE SWITCH", "HYDRAULIC PUMP AUX", "HYDRAULIC OIL FLOW", "TEST OIL PUMP AUX"]
        grid = QGridLayout()
        for i, name in enumerate(indicators):
            grid.addWidget(QLabel(name), i, 0)
            led = QLabel()
            led.setFixedSize(18, 18)
            led.setStyleSheet("background: green; border-radius: 9px;")
            grid.addWidget(led, i, 1)
        layout.addLayout(grid)
        group.setLayout(layout)
        return group

    def create_shutdown_temp_group(self):
        group = QGroupBox("SHUTDOWN TEMPERATURES °F")
        layout = QGridLayout()
        items = [
            ("Outer Bearing 2 MAX", 41.0), ("Inner Bearing 1 MAX", 41.0),
            ("Inner Bearing 2 MAX", 41.0), ("Test Oil Out Housing 1", 41.0),
            ("Test Oil Out Housing 2", 41.0), ("Test Oil Out Cup 1", 41.0),
            ("Test Oil Out Cup 2", 41.0), ("Motor Winding Ph A MAX", 41.0),
            ("Motor Winding Ph B MAX", 41.0), ("Motor Winding Ph C MAX", 41.0),
            ("Couple End Bearing MAX", 41.0), ("Non-Coupled End Bearing MAX", 41.0),
            ("Shaft 180deg MAX", 17.9)
        ]
        for i, (name, val) in enumerate(items):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLabel(str(val)), i, 1)
            btn = QPushButton("OFF")
            btn.setFixedWidth(40)
            layout.addWidget(btn, i, 2)
        group.setLayout(layout)
        return group

    def create_shutdown_speed_group(self):
        group = QGroupBox("SHUTDOWN SPEEDS (RPM)")
        layout = QGridLayout()
        items = [("Motor Speed MAX", 5000), ("Bearing Shaft MAX", 1250)]
        for i, (name, val) in enumerate(items):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLabel(str(val)), i, 1)
        group.setLayout(layout)
        return group

    def create_shutdown_flow_group(self):
        group = QGroupBox("SHUTDOWN FLOWS (GPM)")
        layout = QGridLayout()
        items = [
            ("Test Oil Flow Bearing 1 MAX", 9.0), ("Test Oil Flow Bearing 2 MAX", 9.0),
            ("Test Oil Flow Bearing 2 MAX", 9.0)
        ]
        for i, (name, val) in enumerate(items):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLabel(str(val)), i, 1)
        group.setLayout(layout)
        return group

    def create_shutdown_axial_group(self):
        group = QGroupBox("SHUTDOWN AXIAL HYD PSI")
        layout = QGridLayout()
        items = [("Axial Hydraulic PSI MIN", 500), ("Axial Hydraulic PSI MAX", 360)]
        for i, (name, val) in enumerate(items):
            layout.addWidget(QLabel(name), i, 0)
            layout.addWidget(QLabel(str(val)), i, 1)
        group.setLayout(layout)
        return group

def main():
    app = QApplication(sys.argv)
    win = IndustrialPanel()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()