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


    modelo = FisicaModel()


    vista = SimuladorWindow()


    controlador = MainController(modelo, vista)

    vista.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()