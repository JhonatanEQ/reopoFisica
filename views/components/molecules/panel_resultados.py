from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from views.components.atoms.tarjeta_metrica import TarjetaMetrica

class PanelResultados(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # Título de Sección con Barra Azul
        lbl_seccion = QLabel("Resultados del Análisis")
        lbl_seccion.setObjectName("titulo_seccion")
        main_layout.addWidget(lbl_seccion)

        # Contenedor de Tarjetas
        pnl_tarjetas = QWidget()
        layout_cards = QHBoxLayout(pnl_tarjetas)
        layout_cards.setContentsMargins(0, 0, 0, 0)
        layout_cards.setSpacing(15)

        # Instanciamos 3 tarjetas reutilizables
        self.tarjeta_1 = TarjetaMetrica("1ER ENCUENTRO")
        self.tarjeta_2 = TarjetaMetrica("VELOCIDADES IGUALES", es_ambar=True)
        self.tarjeta_3 = TarjetaMetrica("2DO ENCUENTRO")

        layout_cards.addWidget(self.tarjeta_1)
        layout_cards.addWidget(self.tarjeta_2)
        layout_cards.addWidget(self.tarjeta_3)
        
        main_layout.addWidget(pnl_tarjetas)

    def actualizar_encuentro1(self, tiempo, posicion):
        self.tarjeta_1.actualizar(tiempo, posicion)
        
    def actualizar_velocidades_iguales(self, tiempo, distancia):
        self.tarjeta_2.actualizar(tiempo, f"Sep: {distancia}")
        
    def actualizar_encuentro2(self, tiempo, posicion):
        self.tarjeta_3.actualizar(tiempo, posicion)