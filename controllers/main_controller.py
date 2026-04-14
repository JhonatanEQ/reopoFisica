from models.fisica_model import FisicaModel
from PyQt6.QtCore import QProcess, QProcessEnvironment
import sys
import json
import os

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.proceso_manim = QProcess()
        
        try:
            env = QProcessEnvironment.systemEnvironment()
            self.proceso_manim.setProcessEnvironment(env)
        except Exception:
            pass

        try:
            self.proceso_manim.setWorkingDirectory(os.getcwd())
        except Exception:
            pass
        
        self.proceso_manim.readyReadStandardError.connect(self._imprimir_stderr)
        self.proceso_manim.finished.connect(self.al_finalizar_render)

        self.model.v_auto_mru = self.view.panel_controles.ctrl_vel_auto.obtener_valor()
        self.model.a_camion_mrua = self.view.panel_controles.ctrl_acel_camion.obtener_valor()
        self.model.x0_camion = self.view.panel_controles.ctrl_ventaja.obtener_valor()

        self._conectar_senales()
        self._actualizar_resultados()

    def _conectar_senales(self):

        self.view.panel_controles.ctrl_vel_auto.valor_cambiado.connect(self.actualizar_auto)
        self.view.panel_controles.ctrl_acel_camion.valor_cambiado.connect(self.actualizar_camion)
        self.view.panel_controles.ctrl_ventaja.valor_cambiado.connect(self.actualizar_ventaja)

        self.view.panel_controles.btn_simular.clicked.connect(self.ejecutar_simulacion)

    def actualizar_auto(self, valor):
        self.model.v_auto_mru = float(valor)
        self._actualizar_resultados()

    def actualizar_camion(self, valor):
        self.model.a_camion_mrua = float(valor)
        self._actualizar_resultados()

    def actualizar_ventaja(self, valor):
        self.model.x0_camion = float(valor)
        self._actualizar_resultados()

    def _actualizar_resultados(self):
        """Calcula y actualiza los paneles de datos en tiempo real"""
        encuentros = self.model.resolver_encuentros()
        p_igualdad = self.model.calcular_igualdad_velocidades()
        
        if encuentros:
            (t1, x1), (t2, x2) = encuentros
            t_ig, dist_ig = p_igualdad

            self.view.panel_resultados.actualizar_encuentro1(f"{t1:.2f} s", f"{x1:.1f} m")
            self.view.panel_resultados.actualizar_velocidades_iguales(f"{t_ig:.1f} s", f"{dist_ig:.1f} m")
            self.view.panel_resultados.actualizar_encuentro2(f"{t2:.2f} s", f"{x2:.1f} m")

    def ejecutar_simulacion(self):
        """Lanza la animación de Manim con Seguridad de Caché y Limpieza de archivos"""

        self.view.limpiar_reproductor()

        params = {
            "v_auto": self.model.v_auto_mru,
            "a_camion": self.model.a_camion_mrua,
            "dist": self.model.x0_camion
        }
        
        os.makedirs("simulacion", exist_ok=True)
        with open("simulacion/params.json", "w") as f:
            json.dump(params, f)


        ruta_esperada = "media/videos/escena_manim/480p15/SimulacionAutoCamion.mp4"
        if os.path.exists(ruta_esperada):
            try:
                os.remove(ruta_esperada)
                print(">>> System: Video previo eliminado correctamente.")
            except Exception as e:
                print(f">>> Warning: No se pudo eliminar el video previo: {e}")

        print(f"Lanzando Manim para: {params}")

        self.view.iniciar_simulacion()
        
        args = [
            "-m", "manim", "-ql", "--media_dir", "./media", "--disable_caching",
            "simulacion/escena_manim.py", "SimulacionAutoCamion"
        ]

        try:
            self.proceso_manim.setWorkingDirectory(os.getcwd())
        except Exception:
            pass
        self.proceso_manim.start(sys.executable, args)

    def _imprimir_stderr(self):
        try:
            data = self.proceso_manim.readAllStandardError().data().decode('utf-8', errors='replace')
            if data:
                print("[manim stderr]", data)
        except Exception:
            pass

    def al_finalizar_render(self):
        """Se ejecuta cuando Manim termina de generar el video (Con Debug Oculto)"""

        error_output = self.proceso_manim.readAllStandardError().data().decode('utf-8', errors='replace')
        if error_output:
            print("\n---------- DEBUG MANIM ERROR ----------")
            print(error_output)
            print("---------------------------------------\n")

        print("Renderizado finalizado. Comprobando salida...")
        
        ruta_video = "media/videos/escena_manim/480p15/SimulacionAutoCamion.mp4"
        
        if os.path.exists(ruta_video):

            self.view.finalizar_cargando()
            self.view.reproducir_simulacion(ruta_video)
        else:
            print(f">>> Critical Error: Manim terminó pero no generó el archivo en {ruta_video}")

