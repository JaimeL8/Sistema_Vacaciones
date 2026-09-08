from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Módulo de Configuración")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Aquí irá la gestión de días festivos y parámetros LFT
        layout.addWidget(titulo)