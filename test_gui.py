import sys
import psutil

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QProgressBar,
    QStackedWidget
)

from core.system_monitor import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_system_info,
    format_uptime
)

from core.temperature_monitor import get_all_temperatures

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

        polygon_points = points + [
            QPointF(self.width() - 10, self.height() - 20),
            QPointF(10, self.height() - 20)
        ]

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(137, 220, 235, 75))
        painter.drawPolygon(QPolygonF(polygon_points))

        painter.setBrush(Qt.BrushStyle.NoBrush)
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

dashboard_btn.setStyleSheet("""
    QPushButton {
        color: white;
        background-color: #313244;
        padding: 10px;
        border: none;
        text-align: left;
    }

    QPushButton:hover {
        color: #89b4fa;
        background-color: #45475a;
        text-decoration: underline;
    }
""")

# Кнопка Monitoring
monitoring_btn = QPushButton("Monitoring")
sidebar_layout.addWidget(monitoring_btn)

monitoring_btn.setStyleSheet("""
    QPushButton {
        color: white;
        background-color: #313244;
        padding: 10px;
        border: none;
        text-align: left;
    }

    QPushButton:hover {
        color: #89b4fa;
        background-color: #45475a;
        text-decoration: underline;
    }
""")

# Кнопка System Info
system_info_btn = QPushButton("System Info")
sidebar_layout.addWidget(system_info_btn)

system_info_btn.setCursor(Qt.CursorShape.PointingHandCursor)

system_info_btn.setStyleSheet("""
    QPushButton {
        color: white;
        background-color: #313244;
        padding: 10px;
        border: none;
        text-align: left;
    }

    QPushButton:hover {
        color: #89b4fa;
        background-color: #45475a;
        text-decoration: underline;
    }
""")

def set_active_button(active_button):
    buttons = [dashboard_btn, monitoring_btn, system_info_btn]

    for button in buttons:
        if button == active_button:
            button.setStyleSheet("""
                QPushButton {
                    color: #89b4fa;
                    background-color: #45475a;
                    padding: 10px;
                    border: none;
                    border-left: 3px solid #89b4fa;
                    text-align: left;
                    font-weight: bold;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: #313244;
                    padding: 10px;
                    border: none;
                    text-align: left;
                }
                QPushButton:hover {
                    color: #89b4fa;
                    background-color: #45475a;
                    text-decoration: underline;
                }
            """)

dashboard_btn.clicked.connect(
    lambda: (
        pages.setCurrentWidget(dashboard_page),
        set_active_button(dashboard_btn)
    )
)

system_info_btn.clicked.connect(
    lambda: (
        pages.setCurrentWidget(system_info_page),
        set_active_button(system_info_btn)
    )
)

monitoring_btn.clicked.connect(
    lambda: (
        pages.setCurrentWidget(monitoring_page),
        set_active_button(monitoring_btn)
    )
)


set_active_button(dashboard_btn)

# Добавляем панель в основную горизонтальную область
main_layout.addWidget(sidebar)
pages = QStackedWidget()

dashboard_page = QWidget()
content_layout = QVBoxLayout(dashboard_page)

cards_layout = QHBoxLayout()
content_layout.addLayout(cards_layout)
monitoring_page = QWidget()
monitoring_layout = QVBoxLayout(monitoring_page)

system_info_page = QWidget()
system_info_layout = QVBoxLayout(system_info_page)

pages.addWidget(dashboard_page)
pages.addWidget(monitoring_page)
pages.addWidget(system_info_page)
system_title = QLabel("System Information")
system_info_layout.addWidget(system_title)

system_title.setStyleSheet(
    "color: white; font-size: 24px; font-weight: bold;"
)
monitoring_title = QLabel("Advanced Monitoring")
monitoring_layout.addWidget(monitoring_title)

monitoring_title.setStyleSheet(
    "color: white; font-size: 24px; font-weight: bold;"
)
cpu_details = QLabel()
monitoring_layout.addWidget(cpu_details)

cpu_details.setStyleSheet(
    "color: #a6e3a1; font-size: 18px; "
    "background-color: #313244; padding: 15px; "
    "border-radius: 8px;"
)
ram_details = QLabel()
monitoring_layout.addWidget(ram_details)

ram_details.setStyleSheet(
    "color: #89b4fa; font-size: 18px; "
    "background-color: #313244; padding: 15px; "
    "border-radius: 8px;"
)

disk_details = QLabel()
monitoring_layout.addWidget(disk_details)

disk_details.setStyleSheet(
    "color: #f9e2af; font-size: 18px; "
    "background-color: #313244; padding: 15px; "
    "border-radius: 8px;"
)

temperature_details = QLabel()
monitoring_layout.addWidget(temperature_details)

temperature_details.setStyleSheet(
    "color: #fab387; font-size: 18px; "
    "background-color: #313244; padding: 15px; "
    "border-radius: 8px;"
)

info = get_system_info()

system_labels = [
    ("Operating System", info["os"]),
    ("OS Version", info["os_version"]),
    ("Kernel", info["kernel"]),
    ("Architecture", info["architecture"]),
    ("Hostname", info["hostname"]),
    ("Processor", info["cpu"]),
    ("CPU Cores", str(info["cpu_cores"])),
    ("Total RAM", f'{info["ram_total"]} GB'),
    ("Uptime", format_uptime(info["uptime"]))
]

for title, value in system_labels:
    label = QLabel(f"{title}:  {value}")
    label.setStyleSheet(
        "color: white; font-size: 14px; "
        "background-color: #313244; padding: 12px; "
        "border-radius: 8px;"
    )
    system_info_layout.addWidget(label)

main_layout.addWidget(pages)

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

    cpu_details.setText(
        f"CPU Load: {cpu:.1f}%\n"
        f"Logical Cores: {get_system_info()['cpu_cores']}"
    )

    cpu_graph.add_value(cpu)

    ram = get_memory_usage()
    memory = psutil.virtual_memory()

    ram_details.setText(
        f"RAM Usage: {ram:.1f}%\n"
        f"Used: {memory.used / (1024 ** 3):.2f} GB\n"
        f"Available: {memory.available / (1024 ** 3):.2f} GB"
    )

    disk = get_disk_usage()

    disk_details.setText(
        f"Disk Usage: {disk[0]:.1f}%\n"
        f"Used: {disk[1]:.2f} GB\n"
        f"Free: {disk[2]:.2f} GB"
    )

    temperatures = get_all_temperatures()
    colors = {
    "normal": "#a6e3a1",
    "warning": "#fab387",
    "critical": "#f38ba8"
}
    cpu_temperature = None
    gpu_temperature = None

    for device in temperatures:
        if device["device"] == "coretemp":
            for sensor in device["sensors"]:
                if sensor["label"] == "Package id 0":
                    cpu_temperature = sensor["temperature"]

        elif device["device"] == "radeon":
            if device["sensors"]:
                gpu_temperature = device["sensors"][0]["temperature"]

    if cpu_temperature is not None:
        cpu_temp_value.setText(f"{cpu_temperature:.1f} °C")

        cpu_status = next(
            (sensor["status"] for device in temperatures
             if device["device"] == "coretemp"
             for sensor in device["sensors"]
             if sensor["label"] == "Package id 0"),
            "normal"
        )

        cpu_temp_status.setText(cpu_status.upper())
        cpu_temp_status.setStyleSheet(
            f"color: {colors.get(cpu_status, '#ffffff')}; "
            "font-size: 14px;"
        )
    else:
        cpu_temp_value.setText("N/A")
        cpu_temp_status.setText("N/A")

    if gpu_temperature is not None:
        gpu_temp_value.setText(f"{gpu_temperature:.1f} °C")

        gpu_status = next(
            (sensor["status"] for device in temperatures
             if device["device"] == "radeon"
             for sensor in device["sensors"]),
            "normal"
        )

        gpu_temp_status.setText(gpu_status.upper())
        gpu_temp_status.setStyleSheet(
            f"color: {colors.get(gpu_status, '#ffffff')}; "
            "font-size: 14px;"
        )
    else:
        gpu_temp_value.setText("N/A")
        gpu_temp_status.setText("N/A")
    temperature_lines = ["<b>TEMPERATURES</b>"]

    colors = {
        "normal": "#a6e3a1",
        "warning": "#fab387",
        "critical": "#f38ba8"
    }

    for device in temperatures:
        temperature_lines.append(
            f"<br><b>{device['device']}</b>"
        )

        for sensor in device["sensors"]:
            status = sensor["status"]
            color = colors.get(status, "#ffffff")

            temperature_lines.append(
                f'<span style="color: {color};">'
                f'{sensor["label"]}: '
                f'{sensor["temperature"]:.1f} °C'
                f'</span>'
            )

    temperature_details.setText(
        "<br>".join(temperature_lines)
    )

    cpu_value.setText(f"{cpu:.1f}%")
    cpu_bar.setValue(int(cpu))

    ram_value.setText(f"{ram:.1f}%")
    ram_bar.setValue(int(ram))

    disk_value.setText(f"{disk[0]:.1f}%")
    disk_bar.setValue(int(disk[0]))

# Карточки температуры CPU и GPU
temperature_cards_layout = QHBoxLayout()
content_layout.addLayout(temperature_cards_layout)

cpu_temp_card = QWidget()
cpu_temp_card.setStyleSheet(
    "background-color: #313244; border-radius: 12px;"
)

cpu_temp_layout = QVBoxLayout(cpu_temp_card)

cpu_temp_title = QLabel("CPU Temperature")
cpu_temp_layout.addWidget(cpu_temp_title)

cpu_temp_title.setStyleSheet(
    "color: #a6e3a1; font-size: 16px; font-weight: bold;"
)

cpu_temp_value = QLabel("-- °C")
cpu_temp_layout.addWidget(cpu_temp_value)

cpu_temp_value.setStyleSheet(
    "color: white; font-size: 28px; font-weight: bold;"
)
cpu_temp_status = QLabel("N/A")
cpu_temp_layout.addWidget(cpu_temp_status)

cpu_temp_status.setStyleSheet(
    "color: #a6e3a1; font-size: 14px;"
)

gpu_temp_card = QWidget()
gpu_temp_card.setStyleSheet(
    "background-color: #313244; border-radius: 12px;"
)

gpu_temp_layout = QVBoxLayout(gpu_temp_card)

gpu_temp_title = QLabel("GPU Temperature")
gpu_temp_layout.addWidget(gpu_temp_title)

gpu_temp_title.setStyleSheet(
    "color: #89b4fa; font-size: 16px; font-weight: bold;"
)

gpu_temp_value = QLabel("-- °C")
gpu_temp_layout.addWidget(gpu_temp_value)

gpu_temp_value.setStyleSheet(
    "color: white; font-size: 28px; font-weight: bold;"
)

gpu_temp_status = QLabel("N/A")
gpu_temp_layout.addWidget(gpu_temp_status)

gpu_temp_status.setStyleSheet(
    "color: #a6e3a1; font-size: 14px;"
)

temperature_cards_layout.addWidget(cpu_temp_card)
temperature_cards_layout.addWidget(gpu_temp_card)

cards_layout.addWidget(ram_card)
cards_layout.addWidget(cpu_card)
content_title.setStyleSheet(
    "color: white; font-size: 22px; font-weight: bold;"
)
main_layout.setAlignment(sidebar, Qt.AlignmentFlag.AlignLeft)

timer = QTimer()
timer.timeout.connect(update_stats)
timer.start(2000)

window.show()

sys.exit(app.exec())