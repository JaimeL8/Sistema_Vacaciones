from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class HistorialView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Módulo de Historial y Expediente")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Aquí irá la bitácora completa por empleado
        layout.addWidget(titulo)