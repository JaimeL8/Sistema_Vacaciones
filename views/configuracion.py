from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QTabWidget, QLineEdit, QDateEdit, QFormLayout)
from PyQt6.QtCore import Qt, QDate

class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Solución para el calendario flotante
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
        lbl_titulo = QLabel("Configuración del Sistema")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # CONTENEDOR DE PESTAÑAS
        # ==========================================
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 10px 20px; font-weight: bold; color: #7f8c8d; }
            QTabBar::tab:selected { background: white; border-bottom-color: white; color: #2980b9; }
            QTabWidget::pane { border: 1px solid #bdc3c7; background: white; border-radius: 4px; }
        """)
        
        # Pestaña 1: Días Festivos
        self.tab_festivos = QWidget()
        self.configurar_tab_festivos()
        
        # Pestaña 2: Parámetros LFT
        self.tab_lft = QWidget()
        self.configurar_tab_lft()

        tabs.addTab(self.tab_festivos, "📅 Calendario de Días Festivos")
        tabs.addTab(self.tab_lft, "⚖️ Parámetros de la LFT")

        layout_principal.addWidget(tabs)

    # --- DISEÑO DE LA PESTAÑA: FESTIVOS ---
    def configurar_tab_festivos(self):
        layout = QHBoxLayout(self.tab_festivos)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Lado Izquierdo: Formulario para añadir festivo
        frame_form = QFrame()
        frame_form.setFixedWidth(300)
        layout_form = QVBoxLayout(frame_form)
        layout_form.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_instruccion = QLabel("Añadir Nuevo Día Inhábil:")
        lbl_instruccion.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e; margin-bottom: 10px;")

        form = QFormLayout()
        self.date_festivo = QDateEdit()
        self.date_festivo.setCalendarPopup(True)
        self.date_festivo.setDate(QDate.currentDate())
        self.date_festivo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;")

        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Ej. Día de la Independencia")
        self.txt_descripcion.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;")

        form.addRow("Fecha:", self.date_festivo)
        form.addRow("Descripción:", self.txt_descripcion)

        self.btn_agregar_festivo = QPushButton("➕ Agregar al Calendario")
        self.btn_agregar_festivo.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 5px; margin-top: 10px;")

        layout_form.addWidget(lbl_instruccion)
        layout_form.addLayout(form)
        layout_form.addWidget(self.btn_agregar_festivo)

        # Lado Derecho: Tabla de Festivos Registrados
        layout_der = QVBoxLayout()
        self.tabla_festivos = QTableWidget()
        self.tabla_festivos.setColumnCount(2)
        self.tabla_festivos.setHorizontalHeaderLabels(["Fecha Exacta", "Festividad Oficial"])
        self.tabla_festivos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_festivos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_festivos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_festivos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.btn_eliminar_festivo = QPushButton("🗑️ Eliminar Seleccionado")
        self.btn_eliminar_festivo.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        
        layout_der.addWidget(self.tabla_festivos)
        layout_der.addWidget(self.btn_eliminar_festivo, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(frame_form)
        layout.addLayout(layout_der)

        self.cargar_mock_festivos()

    # --- DISEÑO DE LA PESTAÑA: LFT ---
    def configurar_tab_lft(self):
        layout = QVBoxLayout(self.tab_lft)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_info = QLabel("Tabla Oficial de Asignación de Vacaciones (Ley Federal del Trabajo)")
        lbl_info.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e; margin-bottom: 10px;")
        
        lbl_aviso = QLabel("⚠️ Modifique estos valores únicamente si ocurre una reforma constitucional.")
        lbl_aviso.setStyleSheet("font-size: 13px; color: #e67e22; font-weight: bold; margin-bottom: 15px;")

        self.tabla_lft = QTableWidget()
        self.tabla_lft.setColumnCount(2)
        self.tabla_lft.setHorizontalHeaderLabels(["Años de Antigüedad", "Días de Vacaciones Otorgados"])
        self.tabla_lft.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Aquí SÍ se permite edición para que el administrador pueda cambiar los números
        
        self.btn_guardar_lft = QPushButton("💾 Guardar Nueva Configuración")
        self.btn_guardar_lft.setStyleSheet("background-color: #2980b9; color: white; padding: 12px; font-weight: bold; font-size: 14px; border-radius: 5px;")
        
        layout.addWidget(lbl_info)
        layout.addWidget(lbl_aviso)
        layout.addWidget(self.tabla_lft)
        layout.addWidget(self.btn_guardar_lft, alignment=Qt.AlignmentFlag.AlignRight)

        self.cargar_mock_lft()

    # --- CARGA DE DATOS DE PRUEBA ---
    def cargar_mock_festivos(self):
        datos = [
            ("01/01/2026", "Año Nuevo"),
            ("02/02/2026", "Día de la Constitución Mexicana (Recorrido)"),
            ("16/09/2026", "Día de la Independencia"),
            ("25/12/2026", "Navidad")
        ]
        self.tabla_festivos.setRowCount(len(datos))
        for fila, (fecha, desc) in enumerate(datos):
            item_f = QTableWidgetItem(fecha)
            item_f.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_festivos.setItem(fila, 0, item_f)
            self.tabla_festivos.setItem(fila, 1, QTableWidgetItem(desc))

    def cargar_mock_lft(self):
        # Datos de la reforma de Vacaciones Dignas (2023)
        datos = [
            ("Año 1", "12"), ("Año 2", "14"), ("Año 3", "16"), 
            ("Año 4", "18"), ("Año 5", "20"), ("Años 6 a 10", "22"), 
            ("Años 11 a 15", "24"), ("Años 16 a 20", "26")
        ]
        self.tabla_lft.setRowCount(len(datos))
        for fila, (anio, dias) in enumerate(datos):
            item_a = QTableWidgetItem(anio)
            item_a.setFlags(item_a.flags() & ~Qt.ItemFlag.ItemIsEditable) # El año no se edita
            item_a.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            item_d = QTableWidgetItem(dias)
            item_d.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.tabla_lft.setItem(fila, 0, item_a)
            self.tabla_lft.setItem(fila, 1, item_d)