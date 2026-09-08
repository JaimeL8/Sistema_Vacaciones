from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Panel Principal (Dashboard)")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Aquí agregaremos las tarjetas de indicadores, alertas, etc.
        layout.addWidget(titulo)
