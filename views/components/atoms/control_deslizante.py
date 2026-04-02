from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt, pyqtSignal

class ControlDeslizante(QWidget):
    # Señal personalizada que enviará el nuevo valor hacia afuera
    valor_cambiado = pyqtSignal(float)

    def __init__(self, titulo, min_val, max_val, default_val, unidad, es_ambar=False):
        super().__init__()
        # --- Layout Principal ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(8)

        # --- Fila Superior: Título y SpinBox ---
        fila_superior = QHBoxLayout()
        
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setStyleSheet("font-size: 13px; font-weight: 500; color: #FFFFFF;")
        
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(default_val)
        self.spinbox.setDecimals(1)
        self.spinbox.setFixedWidth(85)
        self.spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if es_ambar:
            self.spinbox.setProperty("es_ambar", True)
        
        self.lbl_unidad = QLabel(unidad)
        self.lbl_unidad.setObjectName("resultado_unidad")
        self.lbl_unidad.setStyleSheet("font-size: 11px; color: #666666;")

        fila_superior.addWidget(self.lbl_titulo)
        fila_superior.addStretch()
        fila_superior.addWidget(self.spinbox)
        fila_superior.addWidget(self.lbl_unidad)

        # --- Fila Inferior: Slider ---
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 10), int(max_val * 10))
        self.slider.setValue(int(default_val * 10))
        
        if es_ambar:
            self.slider.setProperty("es_ambar", True)

        layout.addLayout(fila_superior)
        layout.addWidget(self.slider)

        # --- Lógica de Sincronización Interna ---
        self.slider.valueChanged.connect(self._sync_spinbox)
        self.spinbox.valueChanged.connect(self._sync_slider)

    def _sync_spinbox(self, value):
        # Actualiza el spinbox cuando se mueve el slider
        self.spinbox.blockSignals(True)
        nuevo_valor = value / 10.0
        self.spinbox.setValue(nuevo_valor)
        self.spinbox.blockSignals(False)
        self.valor_cambiado.emit(nuevo_valor)

    def _sync_slider(self, value):
        # Actualiza el slider cuando se escribe en el spinbox
        self.slider.blockSignals(True)
        self.slider.setValue(int(value * 10))
        self.slider.blockSignals(False)
        self.valor_cambiado.emit(value)

    def obtener_valor(self):
        return self.spinbox.value()