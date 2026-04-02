import qtawesome as qta
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class WidgetBienvenida(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("caja_bienvenida")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.setSpacing(10)
        
        # --- 1. Círculo Glowing con Iconos ---
        self.circulo_glow = QFrame()
        self.circulo_glow.setObjectName("circulo_glow")
        layout_iconos = QHBoxLayout(self.circulo_glow)
        layout_iconos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_iconos.setSpacing(8)
        
        # Icono Auto (Cyan)
        lbl_auto = QLabel()
        icon_auto = qta.icon("ph.car-bold", color="#00E5FF")
        lbl_auto.setPixmap(icon_auto.pixmap(32, 32))
        
        # Icono Camión (Amber)
        lbl_camion = QLabel()
        icon_camion = qta.icon("ph.truck-bold", color="#FFC107")
        lbl_camion.setPixmap(icon_camion.pixmap(32, 32))
        
        layout_iconos.addWidget(lbl_auto)
        layout_iconos.addWidget(lbl_camion)
        
        # --- 2. Textos ---
        self.lbl_titulo = QLabel("Sistema Listo")
        self.lbl_titulo.setObjectName("titulo_bienvenida")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_subtitulo = QLabel(
            "Configura los parámetros y presiona \"Ejecutar Simulación\" para\n"
            "visualizar el encuentro entre ambos vehículos"
        )
        self.lbl_subtitulo.setObjectName("subtitulo_bienvenida")
        self.lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_subtitulo.setWordWrap(True)
        self.lbl_subtitulo.setFixedWidth(450) # Controlamos el ancho para que rompa igual que en la imagen
        
        # Añadir al layout principal
        # Añadimos un poco de estiramiento arriba y abajo para centrado perfecto
        layout_principal.addStretch()
        layout_principal.addWidget(self.circulo_glow, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.lbl_titulo)
        layout_principal.addWidget(self.lbl_subtitulo)
        layout_principal.addStretch()
