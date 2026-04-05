from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QGraphicsDropShadowEffect, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QPoint
from PyQt6.QtGui import QColor, QFont
import qtawesome as qta

class WidgetCargando(QWidget):
    def __init__(self):
        super().__init__()
        # Fondo oscuro puro y liso
        self.setStyleSheet("background-color: #0F0F0F; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)
        
        # 1. CONTENEDOR DE ICONOS (Nuevo diseño del usuario)
        self.circulo_glow = QFrame()
        self.circulo_glow.setStyleSheet("background: transparent; border: none;")
        layout_iconos = QHBoxLayout(self.circulo_glow)
        layout_iconos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_iconos.setSpacing(15)
        
        # Icono Auto (Cyan)
        lbl_auto = QLabel()
        icon_auto = qta.icon("ph.car-bold", color="#00E5FF")
        lbl_auto.setPixmap(icon_auto.pixmap(40, 40))
        
        # Icono Camión (Amber)
        lbl_camion = QLabel()
        icon_camion = qta.icon("ph.truck-bold", color="#FFC107")
        lbl_camion.setPixmap(icon_camion.pixmap(42, 42))
        
        # Resplandor cian sutil detrás del conjunto
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(40)
        sh.setColor(QColor(0, 229, 255, 40))
        sh.setOffset(0, 0)
        self.circulo_glow.setGraphicsEffect(sh)
        
        layout_iconos.addWidget(lbl_auto)
        layout_iconos.addWidget(lbl_camion)

        # 2. TIPOGRAFÍA CLEAN (Sin fondos, solo luz)
        self.lbl_texto = QLabel("SINTETIZANDO ANIMACIÓN...")
        self.lbl_texto.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background: transparent;
                font-size: 13px;
                font-weight: 400;
                letter-spacing: 5px;
                font-family: 'Segoe UI', Roboto, Helvetica, Arial;
            }
        """)
        self.lbl_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 3. BARRA DE PROGRESO DE LUZ (Muy fina)
        self.progreso = QProgressBar()
        self.progreso.setRange(0, 0)
        self.progreso.setFixedWidth(240)
        self.progreso.setFixedHeight(2)
        self.progreso.setStyleSheet("""
            QProgressBar {
                background: #1A1A1A;
                border: none;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #00E5FF;
            }
        """)
        
        # 4. SUBTEXTO
        self.lbl_sub = QLabel("Procesando vectores cinemáticos...")
        self.lbl_sub.setStyleSheet("color: #444444; font-size: 11px; background: transparent;")
        self.lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch(1)
        layout.addWidget(self.circulo_glow)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.progreso, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_sub)
        layout.addStretch(1)
