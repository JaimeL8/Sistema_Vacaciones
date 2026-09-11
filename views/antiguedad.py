from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout,QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QDate
import qtawesome as qta
import pandas as pd

class AntiguedadView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Contenedor del título con ícono
        layout_titulo = QHBoxLayout()
        ico_titulo = QLabel()
        ico_titulo.setPixmap(qta.icon('fa5s.award', color='#2c3e50').pixmap(24, 24))
        
        lbl_titulo = QLabel("Listado de Antigüedad de Empleados")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        
        layout_titulo.addWidget(ico_titulo)
        layout_titulo.addWidget(lbl_titulo)
        layout_titulo.addStretch()

        # Contenedor de la tabla
        frame_tabla = QFrame()
        frame_tabla.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_tabla = QVBoxLayout(frame_tabla)
        layout_tabla.setContentsMargins(20, 20, 20, 20)

        # --- ESTILO MODERNO DE TABLA (Consistente con el resto del sistema) ---
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
                padding: 8px 5px;
            }
        """

        # Configuración de la tabla
        self.tabla_antiguedad = QTableWidget()
        self.tabla_antiguedad.setColumnCount(3)
        self.tabla_antiguedad.setHorizontalHeaderLabels(["Nombre del Empleado", "Fecha de Ingreso", "Años de Antigüedad"])
        
        header = self.tabla_antiguedad.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tabla_antiguedad.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_antiguedad.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_antiguedad.setStyleSheet(estilo_tabla)
        self.tabla_antiguedad.verticalHeader().setVisible(False)
        self.tabla_antiguedad.setAlternatingRowColors(True)

        layout_tabla.addWidget(self.tabla_antiguedad)

        # Agregar al layout principal
        layout_principal.addLayout(layout_titulo)
        layout_principal.addWidget(frame_tabla)

        # --- NUEVO: Botones de Exportación ---
        layout_botones = QHBoxLayout()
        layout_botones.addStretch() # Empuja los botones hacia la derecha

        self.btn_exportar_excel = QPushButton(" Exportar a Excel")
        self.btn_exportar_excel.setIcon(qta.icon('fa5s.file-excel', color='white'))
        self.btn_exportar_excel.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 10px 20px; 
                font-size: 13px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)

        self.btn_exportar_pdf = QPushButton(" Exportar a PDF")
        self.btn_exportar_pdf.setIcon(qta.icon('fa5s.file-pdf', color='white'))
        self.btn_exportar_pdf.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; padding: 10px 20px; 
                font-size: 13px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)

        layout_botones.addWidget(self.btn_exportar_excel)
        layout_botones.addWidget(self.btn_exportar_pdf)

        # Se agregan los botones al final de la pantalla
        layout_principal.addLayout(layout_botones)
        # -------------------------------------

        # --- NUEVO: Conectar el botón a la función ---
        self.btn_exportar_excel.clicked.connect(self.exportar_excel)

        # Cargar los 10 registros de prueba
        self.cargar_datos_prueba()
    def cargar_datos_prueba(self):
        """Carga 10 empleados mock calculando la antigüedad y ordenándolos de mayor a menor"""
        # Formato de prueba: (Nombre, Año, Mes, Día)
        datos = [
            ("Juan Pérez López", QDate(2015, 3, 10)),     # Más de 11 años
            ("Ana García Méndez", QDate(2026, 8, 15)),    # Menos de 1 año (aparecerá vacío)
            ("Carlos Ruiz", QDate(2020, 11, 20)),         # 5 años
            ("María Fernández", QDate(2010, 1, 5)),       # Más de 16 años
            ("Luis Sánchez", QDate(2026, 2, 28)),         # Menos de 1 año
            ("Elena Gómez", QDate(2021, 7, 12)),          # 5 años
            ("Jorge Ramírez", QDate(2019, 9, 25)),        # 6 años
            ("Sofía Castro", QDate(2023, 4, 18)),         # 3 años
            ("Miguel Torres", QDate(2024, 10, 5)),        # 1 año
            ("Lucía Morales", QDate(2026, 9, 1))          # Menos de 1 año
        ]

        fecha_actual = QDate.currentDate()
        
        # 1. Pre-calcular la antigüedad de todos ANTES de pasarlos a la tabla
        datos_calculados = []
        for nombre, fecha_ingreso in datos:
            # Cálculo de años exactos
            anios_exactos = fecha_actual.year() - fecha_ingreso.year()
            if (fecha_ingreso.month() > fecha_actual.month() or 
               (fecha_ingreso.month() == fecha_actual.month() and fecha_ingreso.day() > fecha_actual.day())):
                anios_exactos -= 1
                
            # Días totales desde que ingresó (usado para un ordenamiento perfecto)
            dias_totales = fecha_ingreso.daysTo(fecha_actual)
            
            # Guardamos un diccionario con toda su info
            datos_calculados.append({
                'nombre': nombre,
                'fecha_ingreso': fecha_ingreso,
                'anios': anios_exactos,
                'dias_totales': dias_totales
            })

        # 2. ORDENAR LA LISTA: Usamos los 'dias_totales' de mayor a menor (reverse=True)
        datos_calculados.sort(key=lambda empleado: empleado['dias_totales'], reverse=True)

        # 3. Ahora sí, construimos la tabla con los datos ya ordenados
        self.tabla_antiguedad.setRowCount(len(datos_calculados))
        
        for fila, emp in enumerate(datos_calculados):
            # Regla solicitada: Si es menor a 1 año, dejamos el campo vacío
            texto_antiguedad = f"{emp['anios']} años" if emp['anios'] >= 1 else ""

            # Crear celdas
            item_nombre = QTableWidgetItem(emp['nombre'])
            item_ingreso = QTableWidgetItem(emp['fecha_ingreso'].toString("dd/MM/yyyy"))
            item_antiguedad = QTableWidgetItem(texto_antiguedad)
            
            # Centrar el texto de las columnas de fechas y años
            item_ingreso.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_antiguedad.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Insertar en la tabla
            self.tabla_antiguedad.setItem(fila, 0, item_nombre)
            self.tabla_antiguedad.setItem(fila, 1, item_ingreso)
            self.tabla_antiguedad.setItem(fila, 2, item_antiguedad)

    def exportar_excel(self):
        """Extrae los datos de la tabla visual y los guarda en un archivo Excel"""
        # 1. Abrir ventana de diálogo para elegir dónde guardar
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar reporte en Excel", 
            "Reporte_Antiguedad.xlsx", # Nombre por defecto
            "Archivos Excel (*.xlsx);;Todos los archivos (*)"
        )
        
        # Si el usuario cancela la ventana, no hacemos nada
        if not ruta_archivo:
            return

        try:
            # 2. Extraer los encabezados de la tabla
            columnas = []
            for col in range(self.tabla_antiguedad.columnCount()):
                item = self.tabla_antiguedad.horizontalHeaderItem(col)
                columnas.append(item.text() if item else f"Columna {col}")

            # 3. Extraer los datos fila por fila
            datos = []
            for fila in range(self.tabla_antiguedad.rowCount()):
                fila_datos = []
                for col in range(self.tabla_antiguedad.columnCount()):
                    item = self.tabla_antiguedad.item(fila, col)
                    # Si la celda está vacía, guardamos un string vacío
                    fila_datos.append(item.text() if item else "")
                datos.append(fila_datos)

            # 4. Crear un DataFrame de Pandas y exportarlo
            df = pd.DataFrame(datos, columns=columnas)
            df.to_excel(ruta_archivo, index=False, engine='openpyxl')

            # 5. Mostrar mensaje de éxito
            QMessageBox.information(
                self, 
                "Exportación Exitosa", 
                f"El archivo se guardó correctamente en:\n{ruta_archivo}"
            )

        except Exception as e:
            # Manejo de errores (por ejemplo, si el archivo Excel ya está abierto por el usuario y el sistema no deja sobreescribirlo)
            QMessageBox.critical(
                self, 
                "Error de Exportación", 
                f"Ocurrió un error al intentar guardar el archivo:\n{str(e)}"
            )