from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QDateEdit, QPushButton, QFrame, 
                             QFormLayout, QCheckBox, QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt, QDate
import qtawesome as qta

class VacacionesView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Estilo global para corregir el texto invisible del calendario desplegable en PyQt6
        estilo_calendario = """
            QCalendarWidget QWidget { 
                color: #2c3e50; 
                background-color: white;
            }
            QCalendarWidget QToolButton { 
                color: #2c3e50; 
                background-color: #f8f9fa; 
                font-weight: bold;
                border-radius: 4px;
                padding: 3px;
            }
            QCalendarWidget QToolButton:hover { 
                background-color: #e2e8f0; 
            }
            QCalendarWidget QMenu { 
                background-color: white; 
                color: #2c3e50; 
            }
            QCalendarWidget QSpinBox { 
                color: #2c3e50; 
                background-color: white; 
            }
        """
        self.setStyleSheet(estilo_calendario)

        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        lbl_titulo = QLabel("Asignación y Control de Vacaciones")
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # SECCIÓN 1: Selección de Empleado
        # ==========================================
        frame_empleado = QFrame()
        frame_empleado.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_empleado = QHBoxLayout(frame_empleado)
        
        lbl_seleccionar = QLabel("Seleccionar Empleado:")
        lbl_seleccionar.setStyleSheet("font-size: 14px; font-weight: bold; border: none;")
        
        self.combo_empleados = QComboBox()
        self.combo_empleados.setStyleSheet("padding: 5px; font-size: 14px; background-color: white; border: 1px solid #ccc; border-radius: 4px;")
        self.combo_empleados.setMinimumWidth(250)
        # Mockup de datos (luego vendrán de Supabase)
        self.combo_empleados.addItems(["-- Seleccione un empleado --", "Juan Pérez López", "Ana García Méndez", "Carlos Ruiz"])
        
        self.lbl_saldo = QLabel("Saldo disponible: --")
        self.lbl_saldo.setStyleSheet("font-size: 14px; color: #27ae60; font-weight: bold; border: none; padding-left: 20px;")

        layout_empleado.addWidget(lbl_seleccionar)
        layout_empleado.addWidget(self.combo_empleados)
        layout_empleado.addWidget(self.lbl_saldo)
        layout_empleado.addStretch() # Empuja todo a la izquierda

        # Evento cuando cambia el empleado
        self.combo_empleados.currentIndexChanged.connect(self.actualizar_saldo)

        # ==========================================
        # SECCIÓN 2: Selección de Fechas
        # ==========================================
        frame_fechas = QFrame()
        frame_fechas.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #dee2e6;")
        layout_fechas = QFormLayout(frame_fechas)
        layout_fechas.setContentsMargins(20, 20, 20, 20)
        layout_fechas.setSpacing(15)

        estilo_fecha = "padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;"

        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True) # Muestra un calendario al hacer clic
        self.date_inicio.setDate(QDate.currentDate())
        self.date_inicio.setStyleSheet(estilo_fecha)

        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setStyleSheet(estilo_fecha)

        self.check_un_dia = QCheckBox("Es solo un día")
        self.check_un_dia.setStyleSheet("font-size: 13px; font-weight: bold; color: #34495e; border: none;")
        
        layout_fechas.addRow(QLabel(""), self.check_un_dia)
        layout_fechas.addRow(QLabel("Fecha de Inicio:"), self.date_inicio)
        layout_fechas.addRow(QLabel("Fecha de Fin:"), self.date_fin)

        # Eventos de fechas
        self.check_un_dia.toggled.connect(self.toggle_un_dia)
        self.date_inicio.dateChanged.connect(self.calcular_dias)
        self.date_fin.dateChanged.connect(self.calcular_dias)

        # ==========================================
        # SECCIÓN 3: Resumen y Guardado
        # ==========================================
        frame_resumen = QFrame()
        frame_resumen.setStyleSheet("background-color: #e8f4f8; border-radius: 8px; border: 1px solid #bce0fd;")
        layout_resumen = QHBoxLayout(frame_resumen)

        lbl_texto_descuento = QLabel("Días laborables a descontar:")
        lbl_texto_descuento.setStyleSheet("font-size: 16px; font-weight: bold; color: #2980b9; border: none;")
        
        self.lbl_dias_descontar = QLabel("0")
        self.lbl_dias_descontar.setStyleSheet("font-size: 32px; font-weight: bold; color: #e74c3c; border: none;")

        self.btn_guardar = QPushButton(" Guardar Vacaciones")
        self.btn_guardar.setIcon(qta.icon('fa5s.save', color='white'))
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white; padding: 12px 20px; 
                font-size: 14px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)

        layout_resumen.addWidget(lbl_texto_descuento)
        layout_resumen.addWidget(self.lbl_dias_descontar)
        layout_resumen.addStretch()
        layout_resumen.addWidget(self.btn_guardar)

        # Agregar todas las secciones al layout principal
        layout_principal.addWidget(frame_empleado)
        layout_principal.addWidget(frame_fechas)
        layout_principal.addWidget(frame_resumen)
        layout_principal.addStretch()

        # Calcular estado inicial
        self.calcular_dias()

    # --- FUNCIONES DE LÓGICA ---

    def actualizar_saldo(self):
        """Simula la consulta de días disponibles del empleado seleccionado"""
        if self.combo_empleados.currentIndex() == 0:
            self.lbl_saldo.setText("Saldo disponible: --")
            return
            
        # MOCKUP: Simulamos que todos tienen 12 días por ahora
        self.lbl_saldo.setText("Saldo disponible: 12 días")

    def toggle_un_dia(self, checked):
        """Si es solo un día, bloquea la fecha de fin y la iguala a la de inicio"""
        if checked:
            self.date_fin.setEnabled(False)
            self.date_fin.setDate(self.date_inicio.date())
        else:
            self.date_fin.setEnabled(True)
        self.calcular_dias()

    def calcular_dias(self):
        """Calcula los días entre fechas y valida el rango"""
        if self.check_un_dia.isChecked():
            self.date_fin.setDate(self.date_inicio.date())

        fecha_ini = self.date_inicio.date()
        fecha_fin = self.date_fin.date()

        # Validación: Fecha fin no puede ser antes que inicio
        if fecha_fin < fecha_ini:
            self.lbl_dias_descontar.setText("Error")
            self.lbl_dias_descontar.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c; border: none;")
            # Desactivar botón de guardar para evitar registros erróneos
            self.btn_guardar.setEnabled(False)
            self.btn_guardar.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6; color: white; padding: 12px 20px; 
                    font-size: 14px; font-weight: bold; border-radius: 6px;
                }
            """)
            return

        # Si el rango es correcto, se habilita el botón de guardar de nuevo
        self.btn_guardar.setEnabled(True)
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white; padding: 12px 20px; 
                font-size: 14px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)

        # Cálculo de días naturales
        dias_diferencia = fecha_ini.daysTo(fecha_fin) + 1 
        
        self.lbl_dias_descontar.setText(str(dias_diferencia))
        self.lbl_dias_descontar.setStyleSheet("font-size: 32px; font-weight: bold; color: #2980b9; border: none;")