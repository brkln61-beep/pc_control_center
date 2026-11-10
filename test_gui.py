import sys
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar
from core.system_monitor import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage
)
class CpuGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.values = [0] * 60
        self.setMinimumHeight(180)

    def add_value(self, value):
        self.values.append(value)
        self.values = self.values[-60:]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        painter.setPen(QPen(Qt.GlobalColor.gray, 1))
        painter.drawText(10, 10, "CPU Usage History")

        painter.setPen(QPen(Qt.GlobalColor.darkGray, 1))

        for percent in range(0, 101, 25):
            y = height - 20 - (percent / 100) * (height - 45)

            painter.drawLine(40, int(y), width - 10, int(y))
            painter.drawText(5, int(y) + 5, f"{percent}%")

        points = []

        for i, value in enumerate(self.values):
            x = 10 + i * (width - 20) / 59
            y = height - 20 - (value / 100) * (height - 45)

            points.append(QPointF(x, y))

        painter.setPen(QPen(Qt.GlobalColor.cyan, 3))

        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)
layout.setSpacing(15)
layout.setContentsMargins(20, 20, 20, 20)
window.setWindowTitle("PC Control Center")
window.resize(900, 600)
window.setStyleSheet("background-color: #1e1e2e;")
title = QLabel("PC CONTROL CENTER")
layout.addWidget(title)
subtitle = QLabel("System Monitoring")
layout.addWidget(subtitle)
subtitle.setStyleSheet("color: #a6adc8; font-size: 16px;")
main_layout = QHBoxLayout()
layout.addLayout(main_layout)
# Левая боковая панель
sidebar = QWidget()
sidebar.setFixedWidth(200)
sidebar.setMinimumHeight(400)
sidebar.setStyleSheet("background-color: #181825;")

sidebar_layout = QVBoxLayout(sidebar)

# Заголовок панели
sidebar_title = QLabel("PC CONTROL")
sidebar_layout.addWidget(sidebar_title)

sidebar_title.setStyleSheet(
    "color: white; font-size: 18px; font-weight: bold;"
)

# Кнопка Dashboard
dashboard_btn = QPushButton("Dashboard")
sidebar_layout.addWidget(dashboard_btn)

dashboard_btn.setStyleSheet(
    "color: white; background-color: #313244; "
    "padding: 10px; border: none; text-align: left;"
)

# Кнопка Monitoring
monitoring_btn = QPushButton("Monitoring")
sidebar_layout.addWidget(monitoring_btn)

monitoring_btn.setStyleSheet(
    "color: white; background-color: #313244; "
    "padding: 10px; border: none; text-align: left;"
)

# Добавляем панель в основную горизонтальную область
main_layout.addWidget(sidebar)
content = QWidget()
content_layout = QVBoxLayout(content)
cards_layout = QHBoxLayout()
content_layout.addLayout(cards_layout)

main_layout.addWidget(content)
content_title = QLabel("System Overview")
content_layout.addWidget(content_title)
# Карточка процессора
cpu_card = QWidget()
cpu_card.setStyleSheet(
    "background-color: #313244; border-radius: 12px;"
)

cpu_card.setMinimumHeight(120)
cpu_layout = QVBoxLayout(cpu_card)
cpu_layout.setContentsMargins(20, 15, 20, 15)
cpu_layout.setSpacing(10)

cpu_title = QLabel("CPU Usage")
cpu_layout.addWidget(cpu_title)

cpu_title.setStyleSheet(
    "color: #a6e3a1; font-size: 16px; font-weight: bold;"
)

cpu_value = QLabel(f"{get_cpu_usage():.1f}%")
cpu_layout.addWidget(cpu_value)
cpu_bar = QProgressBar()
cpu_bar.setRange(0, 100)
cpu_bar.setValue(int(get_cpu_usage()))
cpu_bar.setTextVisible(False)

cpu_layout.addWidget(cpu_bar)

cpu_bar.setStyleSheet("""
    QProgressBar {
        background-color: #45475a;
        border: none;
        border-radius: 5px;
        height: 10px;
    }

    QProgressBar::chunk {
        background-color: #a6e3a1;
        border-radius: 5px;
    }
""")

cpu_value.setStyleSheet(
    "color: white; font-size: 28px; font-weight: bold;"
)
# Карточка оперативной памяти
ram_card = QWidget()
ram_card.setStyleSheet(
    "background-color: #313244; border-radius: 12px;"
)
ram_card.setMinimumHeight(120)

ram_layout = QVBoxLayout(ram_card)
ram_layout.setContentsMargins(20, 15, 20, 15)

ram_title = QLabel("RAM Usage")
ram_layout.addWidget(ram_title)
ram_title.setStyleSheet(
    "color: #89b4fa; font-size: 16px; font-weight: bold;"
)

ram_value = QLabel(f"{get_memory_usage():.1f}%")
ram_layout.addWidget(ram_value)
ram_bar = QProgressBar()
ram_bar.setRange(0, 100)
ram_bar.setValue(int(get_memory_usage()))
ram_bar.setTextVisible(False)

ram_layout.addWidget(ram_bar)

ram_bar.setStyleSheet("""
    QProgressBar {
        background-color: #45475a;
        border: none;
        border-radius: 5px;
        height: 10px;
    }

    QProgressBar::chunk {
        background-color: #89b4fa;
        border-radius: 5px;
    }
""")

ram_value.setStyleSheet(
    "color: white; font-size: 28px; font-weight: bold;"
)

# Карточка диска
disk_card = QWidget()
disk_card.setStyleSheet(
    "background-color: #313244; border-radius: 12px;"
)
disk_card.setMinimumHeight(120)

disk_layout = QVBoxLayout(disk_card)
disk_layout.setContentsMargins(20, 15, 20, 15)

disk_title = QLabel("Disk Usage")
disk_layout.addWidget(disk_title)
disk_title.setStyleSheet(
    "color: #f9e2af; font-size: 16px; font-weight: bold;"
)

disk_value = QLabel(f"{get_disk_usage()[0]:.1f}%")
disk_data = get_disk_usage()
used_gb = disk_data[1]
free_gb = disk_data[2]
disk_info = QLabel(
    f"Занято: {used_gb:.1f} GB\n"
    f"Свободно: {free_gb:.1f} GB"
)

disk_layout.addWidget(disk_info)

disk_info.setStyleSheet(
    "color: #a6adc8; font-size: 12px;"
)
disk_bar = QProgressBar()
disk_bar.setRange(0, 100)
disk_bar.setValue(int(disk_data[0]))
disk_bar.setTextVisible(False)

disk_layout.addWidget(disk_bar)

disk_bar.setStyleSheet("""
    QProgressBar {
        background-color: #45475a;
        border: none;
        border-radius: 5px;
        height: 10px;
    }

    QProgressBar::chunk {
        background-color: #f9e2af;
        border-radius: 5px;
    }
""")
disk_layout.addWidget(disk_value)
disk_value.setStyleSheet(
    "color: white; font-size: 28px; font-weight: bold;"
)

cards_layout.addWidget(disk_card)
cpu_graph = CpuGraph()
content_layout.addWidget(cpu_graph)
def update_stats():
    cpu = get_cpu_usage()
    cpu_graph.add_value(cpu)
    ram = get_memory_usage()
    disk = get_disk_usage()

    cpu_value.setText(f"{cpu:.1f}%")
    cpu_bar.setValue(int(cpu))

    ram_value.setText(f"{ram:.1f}%")
    ram_bar.setValue(int(ram))

    disk_value.setText(f"{disk[0]:.1f}%")
    disk_bar.setValue(int(disk[0]))
cards_layout.addWidget(ram_card)
cards_layout.addWidget(cpu_card)
content_title.setStyleSheet(
    "color: white; font-size: 22px; font-weight: bold;"
)
main_layout.setAlignment(sidebar, Qt.AlignmentFlag.AlignLeft)
layout.setAlignment(subtitle, Qt.AlignmentFlag.AlignCenter)
layout.setAlignment(title, Qt.AlignmentFlag.AlignCenter)
title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

timer = QTimer()
timer.timeout.connect(update_stats)
timer.start(2000)

window.show()

sys.exit(app.exec())