from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QFrame, QGridLayout, QComboBox)
from PyQt6.QtCore import Qt
import qtawesome as qta

class EmpleadosView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal horizontal (divide la pantalla en Izquierda y Derecha)
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # ==========================================
        # PANEL IZQUIERDO: Directorio y Controles
        # ==========================================
        panel_izquierdo = QWidget()
        layout_izq = QVBoxLayout(panel_izquierdo)
        layout_izq.setContentsMargins(0, 0, 0, 0)

        # 1. Título y Barra de búsqueda
        lbl_titulo = QLabel("Directorio de Empleados")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        
        # --- NUEVO: Contenedor horizontal para Buscador + Filtro ---
        layout_filtros = QHBoxLayout()
        layout_filtros.setSpacing(15)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar empleado por nombre...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px; 
                font-size: 14px; 
                color: #2c3e50;
                background-color: white;
                border: 1px solid #ced4da; 
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        self.combo_filtro_depto = QComboBox()
        self.combo_filtro_depto.addItems([
            "Todos los departamentos", 
            "Recursos Humanos", 
            "Ventas", 
            "TI",
            "Finanzas",
            "Operaciones"
        ])
        self.combo_filtro_depto.setStyleSheet("""
            QComboBox {
                padding: 10px 15px; 
                font-size: 14px; 
                color: #2c3e50;
                background-color: #f8f9fa;
                border: 1px solid #ced4da; 
                border-radius: 6px;
            }
            QComboBox:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """)
        
        layout_filtros.addWidget(self.search_bar, stretch=2)
        layout_filtros.addWidget(self.combo_filtro_depto, stretch=1)
        # -----------------------------------------------------------

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

        # 2. Tabla de Empleados
        self.tabla_empleados = QTableWidget()
        self.tabla_empleados.setColumnCount(3)
        self.tabla_empleados.setHorizontalHeaderLabels(["Nombre Completo", "Departamento", "Estatus"])
        # Hacer que la tabla ocupe todo el espacio disponible
        self.tabla_empleados.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabla_empleados.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_empleados.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_empleados.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Seleccionar fila completa
        self.tabla_empleados.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Solo lectura

        self.tabla_empleados.setStyleSheet(estilo_tabla)
        self.tabla_empleados.verticalHeader().setVisible(False) # Oculta la columna de números
        self.tabla_empleados.setAlternatingRowColors(True) # Activa el diseño de filas "cebra"

        # Conectar el clic en la tabla a la función de resumen
        self.tabla_empleados.itemSelectionChanged.connect(self.mostrar_resumen_empleado)

        # 3. Botones de Acción (CRUD)
        layout_botones = QHBoxLayout()
        self.btn_nuevo = QPushButton(" Nuevo Empleado")
        self.btn_editar = QPushButton(" Editar")
        self.btn_baja = QPushButton(" Dar de Baja")
        
        # Inyectar los íconos de qtawesome
        self.btn_nuevo.setIcon(qta.icon('fa5s.user-plus', color='white'))
        self.btn_editar.setIcon(qta.icon('fa5s.edit', color='white'))
        self.btn_baja.setIcon(qta.icon('fa5s.user-times', color='white'))
        
        estilo_btn = "padding: 10px; font-size: 13px; font-weight: bold; border-radius: 5px;"
        self.btn_nuevo.setStyleSheet(estilo_btn + "background-color: #27ae60; color: white;")
        self.btn_editar.setStyleSheet(estilo_btn + "background-color: #f39c12; color: white;")
        self.btn_baja.setStyleSheet(estilo_btn + "background-color: #e74c3c; color: white;")

        layout_botones.addWidget(self.btn_nuevo)
        layout_botones.addWidget(self.btn_editar)
        layout_botones.addWidget(self.btn_baja)

        # Armar panel izquierdo
        layout_izq.addWidget(lbl_titulo)
        layout_izq.addLayout(layout_filtros)
        layout_izq.addWidget(self.tabla_empleados)
        layout_izq.addLayout(layout_botones)

        # ==========================================
        # PANEL DERECHO: Resumen del Empleado
        # ==========================================
        self.panel_derecho = QFrame()
        self.panel_derecho.setStyleSheet("background-color: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6;")
        self.panel_derecho.setFixedWidth(350)
        layout_der = QVBoxLayout(self.panel_derecho)
        layout_der.setAlignment(Qt.AlignmentFlag.AlignTop)

        titulo_resumen = QLabel("Resumen del Empleado")
        titulo_resumen.setStyleSheet("font-size: 18px; font-weight: bold; border: none; border-bottom: 2px solid #ccc; padding-bottom: 5px;")
        
        # Etiquetas de información (se llenarán dinámicamente)
        estilo_lbl_datos = "font-size: 14px; border: none;"
        self.lbl_nombre = QLabel("Selecciona un empleado...")
        self.lbl_nombre.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; border: none; margin-top: 15px;")
        self.lbl_nombre.setWordWrap(True)

        self.lbl_depto = QLabel("Departamento: -")
        self.lbl_depto.setStyleSheet(estilo_lbl_datos)
        self.lbl_ingreso = QLabel("Fecha de Ingreso: -")
        self.lbl_ingreso.setStyleSheet(estilo_lbl_datos)
        self.lbl_antiguedad = QLabel("Antigüedad: -")
        self.lbl_antiguedad.setStyleSheet(estilo_lbl_datos)

        # Tarjetas de Estadísticas de Vacaciones
        layout_stats = QGridLayout()
        
        # Tarjeta 1: Días por Ley
        self.caja_dias_ley = self.crear_tarjeta_stat("Días por Ley", "0", "#34495e")
        # Tarjeta 2: Días Disponibles (La más importante)
        self.caja_dias_disp = self.crear_tarjeta_stat("Días Disponibles", "0", "#27ae60")

        layout_stats.addWidget(self.caja_dias_ley, 0, 0)
        layout_stats.addWidget(self.caja_dias_disp, 0, 1)

        # Armar panel derecho
        layout_der.addWidget(titulo_resumen)
        layout_der.addWidget(self.lbl_nombre)
        layout_der.addWidget(self.lbl_depto)
        layout_der.addWidget(self.lbl_ingreso)
        layout_der.addWidget(self.lbl_antiguedad)
        layout_der.addSpacing(20)
        layout_der.addLayout(layout_stats)

        # Agregar paneles al layout principal
        layout_principal.addWidget(panel_izquierdo)
        layout_principal.addWidget(self.panel_derecho)

        # Cargar datos de prueba (MOCK)
        self.cargar_datos_prueba()

    def crear_tarjeta_stat(self, titulo, valor, color):
        """Función auxiliar para crear las cajitas de estadísticas"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 2px solid {color};")
        layout = QVBoxLayout(frame)
        
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("font-size: 12px; color: #7f8c8d; border: none;")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_valor = QLabel(valor)
        lbl_valor.setObjectName("valor_numero") # <--- CLAVE: Nombre interno para encontrarlo luego
        lbl_valor.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color}; border: none;")
        lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_valor)
        return frame

    def cargar_datos_prueba(self):
        """Método temporal para visualizar cómo se verá la tabla. 
        Luego lo reemplazaremos con la consulta a Supabase."""
        datos = [
            ("Juan Pérez López", "Ventas", "Activo"),
            ("Ana García Méndez", "Recursos Humanos", "Activo"),
            ("Carlos Ruiz", "TI", "Inactivo")
        ]
        
        self.tabla_empleados.setRowCount(len(datos))
        for fila, (nombre, depto, estatus) in enumerate(datos):
            self.tabla_empleados.setItem(fila, 0, QTableWidgetItem(nombre))
            self.tabla_empleados.setItem(fila, 1, QTableWidgetItem(depto))
            self.tabla_empleados.setItem(fila, 2, QTableWidgetItem(estatus))

    def mostrar_resumen_empleado(self):
        """Se activa al dar clic en una fila de la tabla"""
        filas_seleccionadas = self.tabla_empleados.selectedItems()
        if not filas_seleccionadas:
            return
            
        # Obtener datos de la fila seleccionada
        fila = filas_seleccionadas[0].row()
        nombre = self.tabla_empleados.item(fila, 0).text()
        depto = self.tabla_empleados.item(fila, 1).text()
        
        # Aquí es donde, en el futuro, se buscará la fecha_ingreso en Supabase
        # y se ejecutará la fórmula matemática para calcular días.
        # Por ahora, se actualiza la interfaz con datos de ejemplo:
        self.lbl_nombre.setText(nombre)
        self.lbl_depto.setText(f"Departamento: {depto}")
        self.lbl_ingreso.setText("Fecha de Ingreso: 15/03/2022")
        self.lbl_antiguedad.setText("Antigüedad: 4 años")
        
        # Se actualizan las tarjetas buscando específicamente el texto llamado "valor_numero"
        self.caja_dias_ley.findChild(QLabel, "valor_numero").setText("18") 
        self.caja_dias_disp.findChild(QLabel, "valor_numero").setText("12")