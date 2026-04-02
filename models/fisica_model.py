import math

class FisicaModel:
    def __init__(self):
        # Valores por defecto basados en Ejercicio 14
        self.v_auto_mru = 40.0      # m/s (144 km/h)
        self.a_camion_mrua = 4.0    # m/s^2
        self.x0_camion = 80.0       # m (adelante del auto)
        self.v0_camion = 0.0        # m/s (parte del reposo)

    def calcular_trayectorias(self, t_max=20, paso=0.1):
        """Genera puntos de posición para gráficas"""
        tiempos = []
        pos_auto = []
        pos_camion = []
        
        t = 0
        while t <= t_max:
            tiempos.append(t)
            # Auto: x = v * t
            pos_auto.append(self.v_auto_mru * t)
            # Camión: x = x0 + v0*t + 0.5*a*t^2
            pos_camion.append(self.x0_camion + self.v0_camion * t + 0.5 * self.a_camion_mrua * t**2)
            t += paso
            
        return tiempos, pos_auto, pos_camion

    def resolver_encuentros(self):
        """
        Resuelve la ecuación cuadrática: pos_auto = pos_camion
        v_a * t = x0_c + 0.5 * a_c * t^2
        0.5 * a_c * t^2 - v_a * t + x0_c = 0
        """
        a = 0.5 * self.a_camion_mrua
        b = -self.v_auto_mru
        c = self.x0_camion
        
        discriminante = b**2 - 4 * a * c
        
        if discriminante < 0:
            return None # No se encuentran
            
        t1 = (-b - math.sqrt(discriminante)) / (2 * a)
        t2 = (-b + math.sqrt(discriminante)) / (2 * a)
        
        x1 = self.v_auto_mru * t1
        x2 = self.v_auto_mru * t2
        
        return (t1, x1), (t2, x2)

    def calcular_igualdad_velocidades(self):
        """
        v_a = v_c(t)
        v_a = v0_c + a_c * t
        t = (v_a - v0_c) / a_c
        """
        t = (self.v_auto_mru - self.v0_camion) / self.a_camion_mrua
        x_a = self.v_auto_mru * t
        x_c = self.x0_camion + self.v0_camion * t + 0.5 * self.a_camion_mrua * t**2
        distancia = abs(x_a - x_c)
        
        return t, distancia
