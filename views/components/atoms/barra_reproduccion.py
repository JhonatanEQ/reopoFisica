from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QFrame
from PyQt6.QtCore import Qt, QSize
import qtawesome as qta

class BarraReproduccion(QFrame):
    def __init__(self, reproductor):
        super().__init__()
        self.reproductor = reproductor
        self.setFixedHeight(60)
        
        # Estilo Material: Fondo oscuro, bordes suaves, sombra sutil
        self.setStyleSheet("""
            BarraReproduccion {
                background-color: #121212;
                border-top: 1px solid #333;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
            }
            QPushButton {
                background-color: transparent;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2A2A2A;
            }
            QComboBox {
                background-color: #2A2A2A;
                color: #A0A0A0;
                border: none;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #2A2A2A;
                color: #A0A0A0;
                selection-background-color: #00E5FF;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)

        self.btn_play = QPushButton()
        self.btn_play.setIcon(qta.icon("mdi6.play", color="#00E5FF"))
        self.btn_play.setIconSize(QSize(30, 30))
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_stop = QPushButton()
        self.btn_stop.setIcon(qta.icon("mdi6.stop", color="#FF4B2B"))
        self.btn_stop.setIconSize(QSize(25, 25))
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #00E5FF;
                width: 14px;
                height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #00B4D8;
            }
        """)
   
        self.combo_speed = QComboBox()
        self.combo_speed.addItems(["0.5x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.combo_speed.setCurrentText("1.0x")
        self.combo_speed.setFixedWidth(70)
        self.combo_speed.setCursor(Qt.CursorShape.PointingHandCursor)

        self.lbl_tiempo = QLabel("00:00 / 00:00")
        self.lbl_tiempo.setStyleSheet("color: #888; font-size: 11px; font-family: 'Consolas', monospace;")

        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.slider, stretch=1)
        layout.addWidget(self.combo_speed)
        layout.addWidget(self.lbl_tiempo)

        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_stop.clicked.connect(self.detener_video)
        self.slider.sliderMoved.connect(self.set_posicion_video)
        self.combo_speed.currentTextChanged.connect(self.cambiar_velocidad)

        self.reproductor.positionChanged.connect(self.actualizar_posicion_ui)
        self.reproductor.durationChanged.connect(self.actualizar_duracion_ui)
        self.reproductor.playbackStateChanged.connect(self.actualizar_iconos)
    
    def toggle_play(self):
        from PyQt6.QtMultimedia import QMediaPlayer
        if self.reproductor.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.reproductor.pause()
        else:
            self.reproductor.play()

    def detener_video(self):
        self.reproductor.stop()

    def set_posicion_video(self, posicion):
        self.reproductor.setPosition(posicion)

    def cambiar_velocidad(self, texto):
        taxa = float(texto.replace("x", ""))
        self.reproductor.setPlaybackRate(taxa)

    def actualizar_posicion_ui(self, posicion):
        self.slider.blockSignals(True)
        self.slider.setValue(posicion)
        self.slider.blockSignals(False)
        self.actualizar_etiqueta_tiempo()

    def actualizar_duracion_ui(self, duracion):
        self.slider.setRange(0, duracion)
        self.actualizar_etiqueta_tiempo()

    def actualizar_iconos(self, estado):
        from PyQt6.QtMultimedia import QMediaPlayer
        if estado == QMediaPlayer.PlaybackState.PlayingState:
            self.btn_play.setIcon(qta.icon("mdi6.pause", color="#00E5FF"))
        else:
            self.btn_play.setIcon(qta.icon("mdi6.play", color="#00E5FF"))

    def actualizar_etiqueta_tiempo(self):
        pos_segundos = self.reproductor.position() // 1000
        dur_segundos = self.reproductor.duration() // 1000
        pos_str = f"{pos_segundos // 60:02}:{pos_segundos % 60:02}"
        dur_str = f"{dur_segundos // 60:02}:{dur_segundos % 60:02}"
        self.lbl_tiempo.setText(f"{pos_str} / {dur_str}")
