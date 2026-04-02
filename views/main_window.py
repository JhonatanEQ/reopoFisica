from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QStackedWidget
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from views.style_loader import StyleLoader
from views.components.molecules.panel_controles import PanelControles
from views.components.molecules.panel_resultados import PanelResultados
from views.components.molecules.widget_bienvenida import WidgetBienvenida
from views.components.atoms.barra_reproduccion import BarraReproduccion
from views.components.molecules.widget_cargando import WidgetCargando
from models.fisica_model import FisicaModel
from controllers.main_controller import MainController
import os

class SimuladorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador Cinemático 1D")
        # Cargamos los estilos modulares
        self.setStyleSheet(StyleLoader.load_styles())
        
        # Inicializamos el modelo de física
        self.modelo = FisicaModel()

        widget_central = QWidget()
        widget_central.setObjectName("central_widget")
        self.setCentralWidget(widget_central)
        layout_maestro = QHBoxLayout(widget_central)
        layout_maestro.setContentsMargins(20, 20, 20, 20)
        layout_maestro.setSpacing(20)
        
        # --- Sidebar (Panel Izquierdo) ---
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(350)
        col_izq = QVBoxLayout(sidebar)
        col_izq.setContentsMargins(0, 0, 0, 0)
        
        col_izq.addWidget(QLabel("Simulador Cinemático 1D", objectName="titulo_principal"))
        col_izq.addWidget(QLabel("Auto vs Camión: MRU encuentra MRUA", objectName="subtitulo_principal"))
        
        col_izq.addSpacing(10)
        
        self.panel_controles = PanelControles()
        col_izq.addWidget(self.panel_controles)
        col_izq.addStretch()

        # --- Main Area (Panel Derecho) ---
        col_der = QVBoxLayout()
        col_der.setSpacing(20)
        
        # Contenedor con STACKED WIDGET para cambiar entre Bienvenida y Reproductor
        self.stacked_grafico = QStackedWidget()
        self.stacked_grafico.setObjectName("panel_elevado")
        
        # 1. Crear el reproductor de video
        self.reproductor = QMediaPlayer()
        
        # 2. El widget donde se proyectará el video
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: #0A0A0A; border-radius: 15px;")
        
        # 3. Conectar el reproductor al widget de salida
        self.reproductor.setVideoOutput(self.video_widget)
        
        # 4. Barra de Reproducción (Controles de Play/Pause, Seek, etc.)
        self.barra_video = BarraReproduccion(self.reproductor)
        
        # 5. Contenedor que agrupa Video + Controles
        self.contenedor_simulacion = QWidget()
        layout_sim = QVBoxLayout(self.contenedor_simulacion)
        layout_sim.setContentsMargins(0, 0, 0, 0)
        layout_sim.setSpacing(10)
        layout_sim.addWidget(self.video_widget)
        layout_sim.addWidget(self.barra_video)
        
        # Estado 0: Bienvenida
        self.pantalla_bienvenida = WidgetBienvenida()
        
        # Estado 2: Cargando (Spinner)
        self.pantalla_cargando = WidgetCargando()
        
        # Estado 1: Simulación (Reproductor + Barra)
        self.stacked_grafico.addWidget(self.pantalla_bienvenida)
        self.stacked_grafico.addWidget(self.contenedor_simulacion)
        self.stacked_grafico.addWidget(self.pantalla_cargando)
        
        # Panel de Resultados
        self.panel_resultados = PanelResultados()
        
        col_der.addWidget(self.stacked_grafico, stretch=3)
        col_der.addWidget(self.panel_resultados, stretch=1)

        # Restauramos la conexión de los layouts al maestro
        layout_maestro.addWidget(sidebar, stretch=1)
        layout_maestro.addLayout(col_der, stretch=4)

        # Inicializamos el Controlador para conectar todo
        self.controlador = MainController(self.modelo, self)
        
    def iniciar_simulacion(self):
        """Muestra la pantalla de carga mientras Manim trabaja"""
        self.stacked_grafico.setCurrentIndex(2)

    def limpiar_reproductor(self):
        """Libera el archivo de video para evitar bloqueos de Windows"""
        from PyQt6.QtCore import QUrl
        self.reproductor.stop()
        self.reproductor.setSource(QUrl())

    def finalizar_cargando(self):
        """Muestra el reproductor cuando el video está listo"""
        self.stacked_grafico.setCurrentIndex(1)

    def reproducir_simulacion(self, ruta_video):
        """Carga y reproduce el video generado por Manim"""
        ruta_absoluta = os.path.abspath(ruta_video)
        print(f"Reproduciendo desde: {ruta_absoluta}")
        self.reproductor.setSource(QUrl.fromLocalFile(ruta_absoluta))
        self.reproductor.play()