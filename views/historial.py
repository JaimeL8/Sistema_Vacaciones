from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QFrame, QCompleter, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
import qtawesome as qta

class HistorialView(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # Título del Módulo
        lbl_titulo = QLabel("Historial y Expediente de Vacaciones")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # SECCIÓN 1: Selector de Empleado
        # ==========================================
        frame_selector = QFrame()
        frame_selector.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_selector = QHBoxLayout(frame_selector)
        
        # Contenedor horizontal para juntar el ícono y el texto
        layout_lbl_empleado = QHBoxLayout()
        layout_lbl_empleado.setSpacing(5)
        
        lbl_icono = QLabel()
        # Convertimos el ícono vectorial en una imagen de 18x18 píxeles
        lbl_icono.setPixmap(qta.icon('fa5s.user', color='#2c3e50').pixmap(18, 18))
        lbl_icono.setStyleSheet("border: none;")
        
        lbl_empleado = QLabel("Seleccionar Empleado:")
        lbl_empleado.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; border: none;")
        
        layout_lbl_empleado.addWidget(lbl_icono)
        layout_lbl_empleado.addWidget(lbl_empleado)
        
        self.combo_empleados = QComboBox()
        self.combo_empleados.setStyleSheet("padding: 5px; font-size: 14px; background-color: white; border: 1px solid #ccc; border-radius: 4px;")
        self.combo_empleados.setMinimumWidth(350)
        
        # --- NUEVO: Convertir en barra de búsqueda con autocompletado ---
        self.combo_empleados.setEditable(True)
        self.combo_empleados.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.combo_empleados.lineEdit().setPlaceholderText("Buscar empleado por nombre...")
        
        # Agregamos SOLO los datos reales (quitamos el texto de "-- Seleccione --")
        self.combo_empleados.addItems([
            "Juan Pérez López", 
            "Ana García Méndez", 
            "Miguel Torres Esparza",
            "Isabel Martínez Rodríguez",
            "Marcos Moreno Flores",
            "Rachel Monyañez Alegría",
            "Pablo Ruiz Marmolejo",
            "Lizbeth Andrade Olivo"
        ])
        
        # Forzar a que inicie vacío para que se vea el texto fantasma
        self.combo_empleados.setCurrentIndex(-1)
        
        # Configurar el motor de búsqueda (QCompleter)
        completer = self.combo_empleados.completer()
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        # -----------------------------------------------------------------
        
        layout_selector.addLayout(layout_lbl_empleado)
        layout_selector.addWidget(self.combo_empleados)
        layout_selector.addStretch()

        # Conectar evento de selección
        self.combo_empleados.currentIndexChanged.connect(self.cargar_historial_empleado)

        # ==========================================
        # SECCIÓN 2: Bitácora Detallada (Tabla)
        # ==========================================´
        
        frame_bitacora = QFrame()
        frame_bitacora.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_bitacora = QVBoxLayout(frame_bitacora)
        layout_bitacora.setContentsMargins(20, 20, 20, 20)

        self.lbl_info_empleado = QLabel("Seleccione un empleado arriba para consultar su expediente histórico completo.")
        self.lbl_info_empleado.setStyleSheet("font-size: 14px; color: #7f8c8d; font-weight: bold; border: none;")

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
        
        # Tabla de Historial (Bloques de vacaciones)
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(6)
        self.tabla_historial.setHorizontalHeaderLabels([
            "Periodo LFT", "Fecha Inicio", "Fecha Fin", 
            "Días Descontados", "Fecha Registro", "Observaciones"
        ])
        
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        self.tabla_historial.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_historial.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # --- NUEVAS LÍNEAS DE DISEÑO APLICADAS ---
        self.tabla_historial.setStyleSheet(estilo_tabla)
        self.tabla_historial.verticalHeader().setVisible(False)
        self.tabla_historial.setAlternatingRowColors(True)
        # -----------------------------------------

        # --- NUEVO: Botones de Acción para el Historial ---
        layout_acciones = QHBoxLayout()
        layout_acciones.addStretch() # Empuja los botones a la derecha

        self.btn_editar = QPushButton(" Modificar Fechas")
        self.btn_editar.setIcon(qta.icon('fa5s.edit', color='white'))
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #f39c12; color: white; padding: 10px 20px; 
                font-size: 13px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #e67e22; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)

        self.btn_eliminar = QPushButton(" Cancelar Vacación")
        self.btn_eliminar.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; padding: 10px 20px; 
                font-size: 13px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #c0392b; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)

        # Los botones inician desactivados hasta que seleccionen una fila
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)

        layout_acciones.addWidget(self.btn_editar)
        layout_acciones.addWidget(self.btn_eliminar)
        
        # Conectar el clic en la tabla para activar los botones
        self.tabla_historial.itemSelectionChanged.connect(self.activar_botones_accion)

        # Armar el contenedor de la bitácora
        layout_bitacora.addWidget(self.lbl_info_empleado)
        layout_bitacora.addWidget(self.tabla_historial)
        layout_bitacora.addLayout(layout_acciones) # <--- Agregamos los botones aquí

        # Agregar todo al layout principal
        layout_principal.addWidget(frame_selector)
        layout_principal.addWidget(frame_bitacora)

    # --- LÓGICA DE LA VISTA ---

    def cargar_historial_empleado(self):
        """Carga los bloques históricos de vacaciones vinculados al empleado"""
        index = self.combo_empleados.currentIndex()
        if index == -1: # <--- Ahora verifica si está vacío
            self.lbl_info_empleado.setText("Seleccione un empleado arriba para consultar su expediente histórico completo.")
            self.tabla_historial.setRowCount(0)
            return

        nombre = self.combo_empleados.currentText()
        
        # Se simula el estatus (luego Supabase nos dará este dato real)
        # Por ejemplo: se hace que Carlos Ruiz aparezca como "Inactivo" basándonos en tu diseño anterior
        estatus = "Inactivo" if nombre == "Carlos Ruiz" else "Activo"
        
        # Se actualiza el encabezado de la tabla para incluir el estatus
        self.lbl_info_empleado.setText(
            f"Expediente Histórico de: {nombre} | Fecha de Ingreso: 15/03/2022 | Estatus: {estatus}"
        )
        # Mockup de datos que simulan registros de la tabla 'vacaciones' (incluyendo el 'periodo_anual')
        # Formato: (Periodo LFT, Inicio, Fin, Días, Registro, Observaciones)
        datos_mock = [
            ("Año 1", "10/04/2023", "15/04/2023", "5", "01/04/2023", "Vacaciones de primavera"),
            ("Año 1", "20/12/2023", "22/12/2023", "3", "10/12/2023", "Días decembrinos a cuenta de ley"),
            ("Año 2", "12/05/2024", "19/05/2024", "6", "02/05/2024", "Periodo vacacional anual"),
            ("Año 3", "10/08/2025", "15/08/2025", "5", "01/08/2025", "Asuntos personales")
        ]

        self.tabla_historial.setRowCount(len(datos_mock))
        for fila, datos in enumerate(datos_mock):
            for columna, texto in enumerate(datos):
                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if columna < 5 else Qt.AlignmentFlag.AlignLeft)
                self.tabla_historial.setItem(fila, columna, item)

    def activar_botones_accion(self):
        """Activa los botones de editar/eliminar solo si hay una fila seleccionada"""
        hay_seleccion = len(self.tabla_historial.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)