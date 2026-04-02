from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

class TarjetaMetrica(QFrame):
    def __init__(self, titulo, valor_inicial="--", detalle_inicial="", es_ambar=False):
        super().__init__()
        self.setObjectName("tarjeta_metrica")
        if es_ambar:
            self.setProperty("es_ambar", True)
            
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setObjectName("resultado_titulo")
        
        self.lbl_valor = QLabel(valor_inicial)
        self.lbl_valor.setObjectName("resultado_valor")
        if es_ambar:
            self.lbl_valor.setProperty("es_ambar", True)
        
        self.lbl_detalle = QLabel(detalle_inicial)
        self.lbl_detalle.setObjectName("resultado_subtitulo")

        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_valor)
        layout.addWidget(self.lbl_detalle)
        layout.addStretch()

    def actualizar(self, valor, detalle=""):
        self.lbl_valor.setText(str(valor))
        self.lbl_detalle.setText(detalle)