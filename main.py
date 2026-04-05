# main.py
import sys
from PyQt6.QtWidgets import QApplication
from models.fisica_model import FisicaModel
from views.main_window import SimuladorWindow
from controllers.main_controller import MainController

def main():
    """
    Punto de entrada principal de la aplicación.
    
    Orquesta la inicialización de los componentes del patrón MVC:
    1. Modelo: FisicaModel (Cálculos y datos)
    2. Vista: SimuladorWindow (Interfaz Gráfica)
    3. Controlador: MainController (Lógica de interconexión)
    """
    app = QApplication(sys.argv)

    # Inicializamos el Modelo de datos
    modelo = FisicaModel()

    # Inicializamos la Vista (ventana principal)
    vista = SimuladorWindow()

    # Inicializamos el Controlador pasando el modelo y la vista
    # Esto vincula los sliders y botones con la lógica física
    controlador = MainController(modelo, vista)

    # Desplegamos la interfaz al usuario
    vista.showMaximized()

    # Iniciamos el bucle de eventos de Qt
    sys.exit(app.exec())

if __name__ == "__main__":
    main()