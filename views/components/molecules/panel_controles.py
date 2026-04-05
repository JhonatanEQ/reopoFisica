from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from views.components.atoms.control_deslizante import ControlDeslizante
from views.components.atoms.encabezado_seccion import EncabezadoSeccion

class PanelControles(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("panel_elevado")
        layout = QVBoxLayout(self)
        layout.setSpacing(22)
        layout.setContentsMargins(22, 28, 22, 28)

        # SECCIÓN AUTO
        self.header_auto = EncabezadoSeccion("ph.car-bold", "Auto (MRU)", "Velocidad constante", es_ambar=False)
        layout.addWidget(self.header_auto)
        
        # Ajustamos a los valores del ejercicio 14: 144km/h = 40m/s
        self.ctrl_vel_auto = ControlDeslizante("Velocidad Constante", 10, 100, 40, "m/s", False)
        layout.addWidget(self.ctrl_vel_auto)

        # SECCIÓN CAMIÓN
        self.header_camion = EncabezadoSeccion("ph.truck-bold", "Camión (MRUA)", "Aceleración desde reposo", es_ambar=True)
        layout.addWidget(self.header_camion)
        
        # Ajustamos a los valores del ejercicio 14: Accel = 4, Ventaja = 80
        self.ctrl_acel_camion = ControlDeslizante("Aceleración", 1, 15, 4, "m/s²", True)
        self.ctrl_ventaja = ControlDeslizante("Ventaja Inicial", 0, 300, 80, "m", True)
        
        layout.addWidget(self.ctrl_acel_camion)
        layout.addWidget(self.ctrl_ventaja)

        layout.addStretch()

        # BOTÓN
        self.btn_simular = QPushButton("▶ Ejecutar Simulación")
        self.btn_simular.setObjectName("btn_primario")
        layout.addWidget(self.btn_simular)

    def obtener_parametros(self):
        # Función limpia para entregar los 3 valores al controlador
        return (
            self.ctrl_vel_auto.obtener_valor(),
            self.ctrl_acel_camion.obtener_valor(),
            self.ctrl_ventaja.obtener_valor()
        )