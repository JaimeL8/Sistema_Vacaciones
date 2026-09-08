from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Módulo de Reportes")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Aquí irán los filtros y botones de exportación a Excel/PDF
        layout.addWidget(titulo)