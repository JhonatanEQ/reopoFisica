from PyQt6.QtWidgets import QFrame, QGridLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import qtawesome as qta

class EncabezadoSeccion(QFrame):
    def __init__(self, icono_nom, titulo, subtitulo, es_ambar=False):
        super().__init__()
        self.setObjectName("encabezado_caja")
        self.setFixedHeight(68) # Fijamos altura para mayor control
        
        color_accent = "#FFC107" if es_ambar else "#00E5FF"
        
        # --- Layout Principal (GRID para control total) ---
        layout = QGridLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(0) # Sin espacio entre filas para que se toquen
        
        # --- 1. Icono (Spanning 2 rows) ---
        self.lbl_icono = QLabel()
        self.lbl_icono.setObjectName("icono_caja")
        self.lbl_icono.setFixedSize(44, 44) # Tamaño fijo garantizado
        self.lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = qta.icon(icono_nom, color=color_accent)
        self.lbl_icono.setPixmap(icon.pixmap(28, 28))
        
        # Añadimos el icono: Fila 0, Columna 0, Ocupa 2 Filas, 1 Columna
        layout.addWidget(self.lbl_icono, 0, 0, 2, 1, Qt.AlignmentFlag.AlignVCenter)
        
        # --- 2. Título (Fila 0, Columna 1) ---
        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setStyleSheet(f"color: {color_accent}; font-weight: 800; font-size: 14px; margin: 0; padding:0;")
        layout.addWidget(self.lbl_titulo, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        
        # --- 3. Subtítulo (Fila 1, Columna 1) ---
        self.lbl_subtitulo = QLabel(subtitulo)
        self.lbl_subtitulo.setStyleSheet("color: #AAAAAA; font-size: 11px; margin: 0; padding:0;")
        layout.addWidget(self.lbl_subtitulo, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # Estretch de columna 1 para empujar el contenido a la izquierda
        layout.setColumnStretch(1, 1)
        
        # Distribución de filas igualitaria (esto es lo que centra matemáticamente respecto al icono)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
