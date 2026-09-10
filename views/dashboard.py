from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QGridLayout)
from PyQt6.QtCore import Qt
import qtawesome as qta

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # ==========================================
        # SECCIÓN 1: Encabezado y Acceso Rápido
        # ==========================================
        layout_header = QHBoxLayout()
        
        layout_titulos = QVBoxLayout()
        lbl_titulo = QLabel("Panel Principal")
        lbl_titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50;")
        lbl_subtitulo = QLabel("Resumen general del estado de vacaciones del personal")
        lbl_subtitulo.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        layout_titulos.addWidget(lbl_titulo)
        layout_titulos.addWidget(lbl_subtitulo)
        
        self.btn_acceso_rapido = QPushButton(" Registrar Nueva Vacación")
        self.btn_acceso_rapido.setIcon(qta.icon('fa5s.umbrella-beach', color='white'))
        self.btn_acceso_rapido.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 12px 20px; 
                font-size: 14px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        
        layout_header.addLayout(layout_titulos)
        layout_header.addStretch()
        layout_header.addWidget(self.btn_acceso_rapido)

        # ==========================================
        # SECCIÓN 2: Tarjetas de Indicadores (KPIs)
        # ==========================================
        layout_kpis = QGridLayout()
        layout_kpis.setSpacing(15)

        self.kpi_activos = self.crear_tarjeta_kpi("Empleados Activos", "45", "#2980b9")
        self.kpi_vacaciones = self.crear_tarjeta_kpi("Empleados de Vacaciones (Esta Semana)", "3", "#8e44ad")
        self.kpi_alertas = self.crear_tarjeta_kpi("Empleados con vacaciones por caducar", "2", "#e74c3c")

        layout_kpis.addWidget(self.kpi_activos, 0, 0)
        layout_kpis.addWidget(self.kpi_vacaciones, 0, 1)
        layout_kpis.addWidget(self.kpi_alertas, 0, 2)

        # ==========================================
        # SECCIÓN 3: Tablas de Resumen
        # ==========================================
        layout_tablas = QHBoxLayout()
        layout_tablas.setSpacing(20)

        # --- ESTILO MODERNO PARA LAS TABLAS ---
        estilo_tabla = """
            QTableWidget {
                border: none;
                gridline-color: #dcdde1;
                font-size: 13px;
                color: #2f3640;
            }
            QHeaderView::section {
                background-color: #f5f6fa;
                color: #2c3e50;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #bdc3c7;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """

        # Tabla 1: Ausencias Actuales
        frame_ausencias = QFrame()
        frame_ausencias.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_ausencias = QVBoxLayout(frame_ausencias)

        layout_tit_aus = QHBoxLayout()
        layout_tit_aus.setSpacing(8)
        ico_aus = QLabel()
        ico_aus.setPixmap(qta.icon('fa5s.calendar-alt', color='#34495e').pixmap(18, 18))
        ico_aus.setStyleSheet("border: none;")

        lbl_ausencias = QLabel("Ausencias de este mes")
        lbl_ausencias.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e; border: none;")

        layout_tit_aus.addWidget(ico_aus)
        layout_tit_aus.addWidget(lbl_ausencias)
        layout_tit_aus.addStretch()
        
        layout_ausencias.addLayout(layout_tit_aus) # Se agrega el contenedor dle titulo

        self.tabla_ausencias = QTableWidget()
        self.tabla_ausencias.setColumnCount(3)
        self.tabla_ausencias.setHorizontalHeaderLabels(["Empleado", "Depto.", "Regresa el"])
        self.tabla_ausencias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ausencias.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_ausencias.setStyleSheet(estilo_tabla)
        self.tabla_ausencias.verticalHeader().setVisible(False) # Para ocultar los número 1, 2, 3, ...
        self.tabla_ausencias.setAlternatingRowColors(True) # Filas cebra

        layout_ausencias.addWidget(lbl_ausencias)
        layout_ausencias.addWidget(self.tabla_ausencias)

        # Tabla 2: Alertas de Pasivos Laborales
        frame_pasivos = QFrame()
        frame_pasivos.setStyleSheet("background-color: #fff3f3; border-radius: 8px; border: 1px solid #f5b7b1;")
        layout_pasivos = QVBoxLayout(frame_pasivos)

        # --- Nuevo título con ícono para Pasivos ---
        layout_tit_pasivos = QHBoxLayout()
        layout_tit_pasivos.setSpacing(8)
        ico_pasivos = QLabel()
        ico_pasivos.setPixmap(qta.icon('fa5s.exclamation-triangle', color='#c0392b').pixmap(18, 18))
        ico_pasivos.setStyleSheet("border: none; background-color: transparent;")
        
        lbl_pasivos = QLabel("Riesgo de Pasivos (Días acumulados)")
        lbl_pasivos.setStyleSheet("font-size: 16px; font-weight: bold; color: #c0392b; border: none; background-color: transparent;")
        
        layout_tit_pasivos.addWidget(ico_pasivos)
        layout_tit_pasivos.addWidget(lbl_pasivos)
        layout_tit_pasivos.addStretch()
        
        layout_pasivos.addLayout(layout_tit_pasivos)

        self.tabla_pasivos = QTableWidget()
        self.tabla_pasivos.setColumnCount(3)
        self.tabla_pasivos.setHorizontalHeaderLabels(["Empleado", "Días Libres", "Caducidad Próxima"])
        self.tabla_pasivos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_pasivos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_pasivos.setStyleSheet(estilo_tabla)
        self.tabla_pasivos.verticalHeader().setVisible(False)
        self.tabla_pasivos.setAlternatingRowColors(True)

        layout_pasivos.addWidget(lbl_pasivos)
        layout_pasivos.addWidget(self.tabla_pasivos)

        layout_tablas.addWidget(frame_ausencias)
        layout_tablas.addWidget(frame_pasivos)

        # Ensamblar todo
        layout_principal.addLayout(layout_header)
        layout_principal.addLayout(layout_kpis)
        layout_principal.addLayout(layout_tablas)

        self.cargar_datos_mock()

    def crear_tarjeta_kpi(self, titulo, valor, color):
        """Genera una tarjeta visual para los indicadores clave"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: white; border-radius: 8px; border-left: 5px solid {color};")
        layout = QVBoxLayout(frame)
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("font-size: 13px; color: #7f8c8d; border: none; font-weight: bold;")
        
        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color}; border: none;")
        
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_valor)
        return frame

    def cargar_datos_mock(self):
        """Carga datos de prueba en las tablas del dashboard"""
        # Ausencias
        ausencias = [("Ana García", "RH", "12/09/2026"), ("Luis Sánchez", "Ventas", "15/09/2026")]
        self.tabla_ausencias.setRowCount(len(ausencias))
        for f, (emp, depto, regreso) in enumerate(ausencias):
            self.tabla_ausencias.setItem(f, 0, QTableWidgetItem(emp))
            self.tabla_ausencias.setItem(f, 1, QTableWidgetItem(depto))
            self.tabla_ausencias.setItem(f, 2, QTableWidgetItem(regreso))

        # Pasivos
        pasivos = [("Carlos Ruiz", "22 días", "30/09/2026"), ("María López", "18 días", "15/10/2026")]
        self.tabla_pasivos.setRowCount(len(pasivos))
        for f, (emp, dias, cad) in enumerate(pasivos):
            self.tabla_pasivos.setItem(f, 0, QTableWidgetItem(emp))
            self.tabla_pasivos.setItem(f, 1, QTableWidgetItem(dias))
            self.tabla_pasivos.setItem(f, 2, QTableWidgetItem(cad))