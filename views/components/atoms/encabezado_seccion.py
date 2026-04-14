from PyQt6.QtWidgets import QFrame, QGridLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import qtawesome as qta

class EncabezadoSeccion(QFrame):
    def __init__(self, icono_nom, titulo, subtitulo, es_ambar=False):
        super().__init__()
        self.setObjectName("encabezado_caja")
        self.setFixedHeight(68) 
        
        color_accent = "#FFC107" if es_ambar else "#00E5FF"

        layout = QGridLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(0) 

        self.lbl_icono = QLabel()
        self.lbl_icono.setObjectName("icono_caja")
        self.lbl_icono.setFixedSize(44, 44) 
        self.lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = qta.icon(icono_nom, color=color_accent)
        self.lbl_icono.setPixmap(icon.pixmap(28, 28))

        layout.addWidget(self.lbl_icono, 0, 0, 2, 1, Qt.AlignmentFlag.AlignVCenter)
  
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setStyleSheet(f"color: {color_accent}; font-weight: 800; font-size: 14px; margin: 0; padding:0;")
        layout.addWidget(self.lbl_titulo, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self.lbl_subtitulo = QLabel(subtitulo)
        self.lbl_subtitulo.setStyleSheet("color: #AAAAAA; font-size: 11px; margin: 0; padding:0;")
        layout.addWidget(self.lbl_subtitulo, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout.setColumnStretch(1, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
