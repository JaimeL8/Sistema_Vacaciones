import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QHBoxLayout, QVBoxLayout, QPushButton, 
                             QStackedWidget, QFrame)

# Importar las 6 vistas
from views.dashboard import DashboardView
from views.empleados import EmpleadosView
from views.vacaciones import VacacionesView
from views.historial import HistorialView
from views.reportes import ReportesView
from views.configuracion import ConfiguracionView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Vacaciones")
        self.resize(1100, 650)

        # Contenedor principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout_principal = QHBoxLayout(main_widget)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # --- MENÚ LATERAL (SIDEBAR) ---
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_frame.setFixedWidth(220)
        sidebar = QVBoxLayout(sidebar_frame)
        
        estilo_btn = """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """

        # Creación de los 6 botones
        self.btn_dashboard = QPushButton("📊 Panel Principal")
        self.btn_empleados = QPushButton("👥 Gestión de Empleados")
        self.btn_vacaciones = QPushButton("🌴 Asignar Vacaciones")
        self.btn_historial = QPushButton("📁 Historial y Expediente")
        self.btn_reportes = QPushButton("📈 Reportes")
        self.btn_config = QPushButton("⚙️ Configuración")
        
        # Aplicar el estilo a todos los botones
        botones = [self.btn_dashboard, self.btn_empleados, self.btn_vacaciones, 
                   self.btn_historial, self.btn_reportes, self.btn_config]
        
        for btn in botones:
            btn.setStyleSheet(estilo_btn)
            sidebar.addWidget(btn)
            
        sidebar.addStretch()

       # --- ÁREA CENTRAL (VISTAS DINÁMICAS) ---
        self.stacked_widget = QStackedWidget()
        
        # 1. Guardamos el Dashboard en una variable para poder acceder a su botón
        self.vista_dashboard = DashboardView()
        
        # 2. Instanciar e insertar las vistas (Índices 0 al 5)
        self.stacked_widget.addWidget(self.vista_dashboard) # Índice 0
        self.stacked_widget.addWidget(EmpleadosView())      # Índice 1
        self.stacked_widget.addWidget(VacacionesView())     # Índice 2
        self.stacked_widget.addWidget(HistorialView())      # Índice 3
        self.stacked_widget.addWidget(ReportesView())       # Índice 4
        self.stacked_widget.addWidget(ConfiguracionView())  # Índice 5

        # 3. Conectar los clics del menú lateral con el cambio de pantalla
        self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_empleados.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_vacaciones.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_historial.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_reportes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_config.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        # 4. NUEVA CONEXIÓN: Botón verde del Dashboard -> Módulo de Vacaciones (Índice 2)
        self.vista_dashboard.btn_acceso_rapido.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        # Armar el layout principal
        layout_principal.addWidget(sidebar_frame)
        layout_principal.addWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())