from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QDateEdit, QPushButton, QFrame, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QDate
import qtawesome as qta

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Solución para el texto invisible del calendario desplegable
        self.setStyleSheet("""
            QCalendarWidget QWidget { color: #2c3e50; background-color: white; }
            QCalendarWidget QToolButton { color: #2c3e50; background-color: #f8f9fa; font-weight: bold; border-radius: 4px; padding: 3px; }
            QCalendarWidget QToolButton:hover { background-color: #e2e8f0; }
            QCalendarWidget QMenu { background-color: white; color: #2c3e50; }
            QCalendarWidget QSpinBox { color: #2c3e50; background-color: white; }
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # Título
        lbl_titulo = QLabel("Reportes y Exportación")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # SECCIÓN 1: Filtros de Generación
        # ==========================================
        frame_filtros = QFrame()
        frame_filtros.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_filtros = QHBoxLayout(frame_filtros)
        layout_filtros.setSpacing(15)

        estilo_combo = "padding: 6px; font-size: 13px; background-color: white; border: 1px solid #ccc; border-radius: 4px;"

        estilo_combo = "padding: 6px; font-size: 13px; background-color: white; border: 1px solid #ccc; border-radius: 4px;"

        # --- Etiqueta con ícono para "Tipo" ---
        layout_tit_tipo = QHBoxLayout()
        ico_tipo = QLabel()
        ico_tipo.setPixmap(qta.icon('fa5s.file-alt', color='#2c3e50').pixmap(16, 16))
        layout_tit_tipo.addWidget(ico_tipo)
        layout_tit_tipo.addWidget(QLabel("Tipo:"))
        
        layout_filtros.addLayout(layout_tit_tipo)
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Reporte de Ausencias", "Reporte de Pasivos Laborales"])
        self.combo_tipo.setStyleSheet(estilo_combo)
        layout_filtros.addWidget(self.combo_tipo)

        # --- Etiqueta con ícono para "Rango" ---
        layout_tit_rango = QHBoxLayout()
        ico_rango = QLabel()
        ico_rango.setPixmap(qta.icon('fa5s.clock', color='#2c3e50').pixmap(16, 16))
        layout_tit_rango.addWidget(ico_rango)
        layout_tit_rango.addWidget(QLabel("Rango:"))
        
        layout_filtros.addLayout(layout_tit_rango)
        self.combo_tiempo = QComboBox()
        self.combo_tiempo.addItems([
            "Próximos 15 días", 
            "Mensual", 
            "Trimestral", 
            "Anual", 
            "Fechas Personalizadas"
        ])
        self.combo_tiempo.setStyleSheet(estilo_combo)
        layout_filtros.addWidget(self.combo_tiempo)

        # Fechas Personalizadas (Ocultas por defecto)
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate())
        self.date_inicio.setStyleSheet(estilo_combo)
        self.date_inicio.setVisible(False)

        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setStyleSheet(estilo_combo)
        self.date_fin.setVisible(False)

        self.lbl_a = QLabel(" a ")
        self.lbl_a.setVisible(False)

        layout_filtros.addWidget(self.date_inicio)
        layout_filtros.addWidget(self.lbl_a)
        layout_filtros.addWidget(self.date_fin)

        # Botón Generar Previsualización
        self.btn_generar = QPushButton(" Generar")
        self.btn_generar.setIcon(qta.icon('fa5s.sync-alt', color='white')) # Ícono de recargar/sincronizar
        self.btn_generar.setStyleSheet("""
            QPushButton { background-color: #2c3e50; color: white; font-weight: bold; padding: 6px 15px; border-radius: 4px; }
            QPushButton:hover { background-color: #34495e; }
        """)
        layout_filtros.addWidget(self.btn_generar)
        layout_filtros.addStretch()

        # ==========================================
        # SECCIÓN 2: Previsualización de Datos
        # ==========================================

        # --- ESTILO MODERNO PARA LA TABLA ---
        estilo_tabla = """
            QTableWidget {
                border: 1px solid #dee2e6;
                gridline-color: #dcdde1;
                font-size: 13px;
                color: #2f3640;
                border-radius: 5px;
                background-color: white;
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

        self.tabla_preview = QTableWidget()
        self.tabla_preview.setColumnCount(4)
        self.tabla_preview.setHorizontalHeaderLabels(["Empleado", "Departamento", "Días", "Detalle"])
        self.tabla_preview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_preview.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_preview.setStyleSheet(estilo_tabla)
        self.tabla_preview.verticalHeader().setVisible(False) # Oculta la columna de números
        self.tabla_preview.setAlternatingRowColors(True) # Activa las filas tipo cebra

        # ==========================================
        # SECCIÓN 3: Exportación
        # ==========================================
        
        layout_exportar = QHBoxLayout()
        
        self.btn_excel = QPushButton(" Exportar a Excel")
        self.btn_excel.setIcon(qta.icon('fa5s.file-excel', color='white'))
        self.btn_excel.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; padding: 10px; font-weight: bold; font-size: 14px; border-radius: 5px; }
            QPushButton:hover { background-color: #2ecc71; }
        """)

        self.btn_pdf = QPushButton(" Exportar a PDF")
        self.btn_pdf.setIcon(qta.icon('fa5s.file-pdf', color='white'))
        self.btn_pdf.setStyleSheet("""
            QPushButton { background-color: #c0392b; color: white; padding: 10px; font-weight: bold; font-size: 14px; border-radius: 5px; }
            QPushButton:hover { background-color: #e74c3c; }
        """)

        layout_exportar.addStretch()
        layout_exportar.addWidget(self.btn_excel)
        layout_exportar.addWidget(self.btn_pdf)

        # Armado final del layout principal
        layout_principal.addWidget(frame_filtros)
        layout_principal.addWidget(self.tabla_preview)
        layout_principal.addLayout(layout_exportar)

        # Conectar eventos
        self.combo_tiempo.currentIndexChanged.connect(self.toggle_fechas_personalizadas)
        self.btn_generar.clicked.connect(self.cargar_preview)

    # --- LÓGICA DE LA VISTA ---

    def toggle_fechas_personalizadas(self):
        """Muestra u oculta los selectores de fecha si se elige 'Fechas Personalizadas'"""
        es_personalizado = self.combo_tiempo.currentText() == "Fechas Personalizadas"
        self.date_inicio.setVisible(es_personalizado)
        self.lbl_a.setVisible(es_personalizado)
        self.date_fin.setVisible(es_personalizado)

    def cargar_preview(self):
        """Simula la carga de datos en la tabla según el tipo de reporte seleccionado"""
        tipo = self.combo_tipo.currentText()
        rango = self.combo_tiempo.currentText()
        
        # Adaptar las columnas según el reporte
        if tipo == "Reporte de Ausencias":
            self.tabla_preview.setHorizontalHeaderLabels(["Empleado", "Departamento", "Fechas de Ausencia", "Días a Faltar"])
            datos_mock = [("Ana García", "Recursos Humanos", "15/09 - 20/09", "4"), ("Juan Pérez", "Ventas", "01/10 - 05/10", "3")]
        else:
            self.tabla_preview.setHorizontalHeaderLabels(["Empleado", "Departamento", "Días Acumulados (Pasivo)", "Prima Vacacional Estimada"])
            datos_mock = [("Carlos Ruiz", "TI", "18", "Pendiente"), ("Ana García", "Recursos Humanos", "12", "Pagada")]

        self.tabla_preview.setRowCount(len(datos_mock))
        for fila, datos in enumerate(datos_mock):
            for columna, texto in enumerate(datos):
                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_preview.setItem(fila, columna, item)