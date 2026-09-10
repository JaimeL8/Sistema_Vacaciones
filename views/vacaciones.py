from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QDateEdit, QPushButton, QFrame, 
                             QFormLayout, QCheckBox, QMessageBox, QGridLayout,
                             QCompleter,QLineEdit) 
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

        # --- NUEVO: Convertir en barra de búsqueda con autocompletado ---
        self.combo_empleados.setEditable(True) # Permite escribir en la caja
        self.combo_empleados.setInsertPolicy(QComboBox.InsertPolicy.NoInsert) # Evita que guarden nombres inventados

        # Mockup de datos (luego vendrán de Supabase)
        self.combo_empleados.lineEdit().setPlaceholderText("Buscar empleado por nombre...")
        # 2. Agregar SOLO los datos reales 
        self.combo_empleados.addItems(["Juan Pérez López", "Ana García Méndez", "Carlos Ruiz"])
        
        # 3. Forzar a que el buscador inicie completamente vacío para que se vea el texto fantasma
        self.combo_empleados.setCurrentIndex(-1)

        # Configurar el motor de búsqueda (QCompleter)
        completer = self.combo_empleados.completer()
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        # MatchContains permite que si escribes "García", te encuentre a "Ana García"
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        
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
        layout_fechas = QVBoxLayout(frame_fechas)
        layout_fechas.setContentsMargins(25, 25, 25, 25)
        layout_fechas.setSpacing(20)

        # 1. Contenedor superior para el Checkbox e Ícono separados
        layout_top_fechas = QHBoxLayout()
        layout_top_fechas.setSpacing(8)
        
        ico_calendario = QLabel()
        ico_calendario.setPixmap(qta.icon('fa5s.calendar-day', color='#34495e').pixmap(18, 18))
        ico_calendario.setStyleSheet("border: none;")
        
        self.check_un_dia = QCheckBox("Es solo un día")
        self.check_un_dia.setStyleSheet("""
            QCheckBox { 
                font-size: 14px; 
                font-weight: bold; 
                color: #34495e; 
                border: none;
            }
        """)
        
        layout_top_fechas.addWidget(ico_calendario)
        layout_top_fechas.addWidget(self.check_un_dia)
        layout_top_fechas.addStretch()

        # 2. Contenedor para las cajas de fecha (Lado a lado)
        layout_inputs = QHBoxLayout()
        layout_inputs.setSpacing(30)

        estilo_fecha = """
            QDateEdit {
                padding: 8px 15px; 
                font-size: 14px; 
                color: #2c3e50;
                background-color: #f8f9fa;
                border: 1px solid #ced4da; 
                border-radius: 6px;
            }
            QDateEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
            QDateEdit:disabled {
                background-color: #e9ecef;
                color: #a6b0b8;
                border: 1px solid #e9ecef;
            }
        """

        # Bloque Fecha de Inicio
        layout_inicio = QVBoxLayout()
        lbl_inicio = QLabel("Fecha de Inicio")
        lbl_inicio.setStyleSheet("font-size: 13px; font-weight: bold; color: #7f8c8d; border: none; margin-bottom: 2px;")
        
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate())
        self.date_inicio.setMinimumWidth(220)
        self.date_inicio.setStyleSheet(estilo_fecha)
        
        layout_inicio.addWidget(lbl_inicio)
        layout_inicio.addWidget(self.date_inicio)

        # Bloque Fecha de Fin
        layout_fin = QVBoxLayout()
        lbl_fin = QLabel("Fecha de Fin")
        lbl_fin.setStyleSheet("font-size: 13px; font-weight: bold; color: #7f8c8d; border: none; margin-bottom: 2px;")
        
        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setMinimumWidth(220)
        self.date_fin.setStyleSheet(estilo_fecha)
        
        layout_fin.addWidget(lbl_fin)
        layout_fin.addWidget(self.date_fin)

        # Ensamblar los campos lado a lado
        layout_inputs.addLayout(layout_inicio)
        layout_inputs.addLayout(layout_fin)
        layout_inputs.addStretch()

# --- NUEVO: Bloque de Observaciones ---
        layout_obs = QVBoxLayout()
        layout_obs.setSpacing(5)
        
        lbl_obs = QLabel("Observaciones (Opcional)")
        lbl_obs.setStyleSheet("font-size: 13px; font-weight: bold; color: #7f8c8d; border: none; margin-top: 10px;")
        
        self.input_observaciones = QLineEdit()
        self.input_observaciones.setPlaceholderText("Ej. Periodo vacacional anual, asuntos personales...")
        self.input_observaciones.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px; 
                font-size: 14px; 
                color: #2c3e50;
                background-color: #f8f9fa;
                border: 1px solid #ced4da; 
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """)
        
        layout_obs.addWidget(lbl_obs)
        layout_obs.addWidget(self.input_observaciones)
        # --------------------------------------

        # Agregar todo al marco principal de fechas
        layout_fechas.addLayout(layout_top_fechas)
        layout_fechas.addLayout(layout_inputs)
        layout_fechas.addLayout(layout_obs) # <--- Se agregan las observaciones al contenedor principal

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
            
        # MOCKUP: Se simula que todos tienen 12 días por ahora
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