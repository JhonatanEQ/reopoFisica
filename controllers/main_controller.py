from models.fisica_model import FisicaModel
from PyQt6.QtCore import QProcess
import sys
import json
import os

class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.proceso_manim = QProcess()
        self.proceso_manim.finished.connect(self.al_finalizar_render)
        
        # Sincronizar modelo inicial con los valores actuales de la UI
        self.model.v_auto_mru = self.view.panel_controles.ctrl_vel_auto.obtener_valor()
        self.model.a_camion_mrua = self.view.panel_controles.ctrl_acel_camion.obtener_valor()
        self.model.x0_camion = self.view.panel_controles.ctrl_ventaja.obtener_valor()
        
        # Conexiones
        self._conectar_senales()
        self._actualizar_resultados()

    def _conectar_senales(self):
        # Conectar deslizadores de la vista al controlador
        self.view.panel_controles.ctrl_vel_auto.valor_cambiado.connect(self.actualizar_auto)
        self.view.panel_controles.ctrl_acel_camion.valor_cambiado.connect(self.actualizar_camion)
        self.view.panel_controles.ctrl_ventaja.valor_cambiado.connect(self.actualizar_ventaja)
        
        # Conectar el botón de simulación
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
            
            # Actualizamos la vista (asumiendo que panel_resultados tiene estos métodos)
            self.view.panel_resultados.actualizar_encuentro1(f"{t1:.2f} s", f"{x1:.1f} m")
            self.view.panel_resultados.actualizar_velocidades_iguales(f"{t_ig:.1f} s", f"{dist_ig:.1f} m")
            self.view.panel_resultados.actualizar_encuentro2(f"{t2:.2f} s", f"{x2:.1f} m")

    def ejecutar_simulacion(self):
        """Lanza la animación de Manim con Seguridad de Caché y Limpieza de archivos"""
        # 1. Liberar el archivo en el reproductor para que Windows nos deje borrarlo
        self.view.limpiar_reproductor()

        # 2. Preparar parámetros JSON
        params = {
            "v_auto": self.model.v_auto_mru,
            "a_camion": self.model.a_camion_mrua,
            "dist": self.model.x0_camion
        }
        
        os.makedirs("simulacion", exist_ok=True)
        with open("simulacion/params.json", "w") as f:
            json.dump(params, f)

        # 2. CAPA DE SEGURIDAD 1: Prevención de Falsos Positivos
        # Eliminamos el video anterior si existe para evitar reproducir archivos 'viejos' si el render falla
        # La ruta debe coincidir exactamente con la que usa Manim para -ql
        ruta_esperada = "media/videos/escena_manim/480p15/SimulacionAutoCamion.mp4"
        if os.path.exists(ruta_esperada):
            try:
                os.remove(ruta_esperada)
                print(">>> System: Video previo eliminado correctamente.")
            except Exception as e:
                print(f">>> Warning: No se pudo eliminar el video previo: {e}")

        print(f"Lanzando Manim para: {params}")
        
        # Cambiamos a la pantalla del reproductor (estará en negro con el logo hasta que termine el render)
        self.view.iniciar_simulacion()
        
        # 3. CAPA DE SEGURIDAD 2: Manejo de Caché
        # Añadimos --disable_caching para forzar a Manim a ignorar su base de datos interna de renders
        args = [
            "-m", "manim", "-ql", "--media_dir", "./media", "--disable_caching",
            "simulacion/escena_manim.py", "SimulacionAutoCamion"
        ]
        
        # Iniciamos el proceso monitoreado
        self.proceso_manim.start(sys.executable, args)

    def al_finalizar_render(self):
        """Se ejecuta cuando Manim termina de generar el video (Con Debug Oculto)"""
        # 4. CAPA DE SEGURIDAD 3: Debug Oculto
        # Capturamos el StandardError del proceso para ver por qué falló si no hay video
        error_output = self.proceso_manim.readAllStandardError().data().decode('utf-8', errors='replace')
        if error_output:
            print("\n---------- DEBUG MANIM ERROR ----------")
            print(error_output)
            print("---------------------------------------\n")

        print("Renderizado finalizado. Comprobando salida...")
        
        ruta_video = "media/videos/escena_manim/480p15/SimulacionAutoCamion.mp4"
        
        if os.path.exists(ruta_video):
            # Cambiamos de pantalla de carga a reproductor
            self.view.finalizar_cargando()
            self.view.reproducir_simulacion(ruta_video)
        else:
            print(f">>> Critical Error: Manim terminó pero no generó el archivo en {ruta_video}")
            # Aquí podrías emitir una señal a la UI para mostrar un mensaje de error al usuario
