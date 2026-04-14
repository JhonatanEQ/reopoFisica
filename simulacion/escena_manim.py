from manim import *
import json
import os
import numpy as np

class SimulacionAutoCamion(MovingCameraScene):
    def construct(self):

        self.camera.background_color = "#0A0A0A"

        try:
            with open("simulacion/params.json", "r") as f:
                data = json.load(f)
                v_auto = data.get("v_auto", 40.0)
                a_camion = data.get("a_camion", 4.0)
                x0_camion = data.get("dist", 80.0)
        except:
            v_auto, a_camion, x0_camion = 40.0, 4.0, 80.0

        t_max = 22.0

        t_v_igual = v_auto / a_camion

        disc = v_auto**2 - 2 * a_camion * x0_camion
        t_e1, t_e2 = 0, 0
        if disc >= 0:
            t_e1 = (v_auto - np.sqrt(disc)) / a_camion
            t_e2 = (v_auto + np.sqrt(disc)) / a_camion

        grid = NumberPlane(
            x_range=[0, 25, 2], y_range=[0, 950, 100],
            background_line_style={"stroke_opacity": 0.05, "stroke_color": WHITE}
        ).scale(0.85).shift(DOWN * 1.5)
        self.add(grid)

        pista = NumberLine(
            x_range=[0, 950, 100], length=12, include_numbers=True,
            font_size=16, color=BLUE_E
        ).shift(UP * 3.2 + RIGHT * 1.2).scale(0.85)

        ejes = Axes(
            x_range=[0, t_max, 2], y_range=[0, 950, 100],
            x_length=10, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 16, "color": GRAY},
            y_axis_config={"numbers_to_exclude": [0]},
        ).shift(DOWN * 1.5).scale(0.85)
        
        lbl_ejes = ejes.get_axis_labels(
            x_label=MathTex("t\\,(s)", font_size=20, color=GRAY), 
            y_label=MathTex("x\\,(m)", font_size=20, color=GRAY)
        )

        auto_viz = SVGMobject("assets/v_auto.svg").scale(0.3).flip(UP)
        camion_viz = SVGMobject("assets/a_camion.svg").scale(0.3).flip(UP)
        tiempo = ValueTracker(0)

        tele_box = RoundedRectangle(corner_radius=0.1, width=2.4, height=1.2).set_fill(BLACK, opacity=0.7).set_stroke(GRAY, opacity=0.2)
        tele_box.to_corner(UL, buff=0.2)
        t_text = MathTex("t = ", color=WHITE, font_size=18)
        t_val = DecimalNumber(0, num_decimal_places=2, color=WHITE, font_size=18).add_updater(lambda d: d.set_value(tiempo.get_value()))
        va_text = MathTex("v_a = ", color="#00E5FF", font_size=16)
        va_val = DecimalNumber(v_auto, num_decimal_places=1, color=WHITE, font_size=16)
        vc_text = MathTex("v_c = ", color="#FFC107", font_size=16)
        vc_val = DecimalNumber(0, num_decimal_places=1, color=WHITE, font_size=16).add_updater(lambda d: d.set_value(a_camion * tiempo.get_value()))
        tele_lines = VGroup(
            VGroup(t_text, t_val).arrange(RIGHT, buff=0.1),
            VGroup(va_text, va_val).arrange(RIGHT, buff=0.1),
            VGroup(vc_text, vc_val).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(tele_box)
        dashboard = VGroup(tele_box, tele_lines)

        auto_viz.add_updater(lambda m: m.move_to(pista.n2p(v_auto * tiempo.get_value()) + UP*0.4))
        camion_viz.add_updater(lambda m: m.move_to(pista.n2p(x0_camion + 0.5 * a_camion * tiempo.get_value()**2) + DOWN*0.4))

        v_arrow_a = always_redraw(lambda: Arrow(
            start=auto_viz.get_center(), end=auto_viz.get_center() + RIGHT*(v_auto/35),
            color="#00E5FF", buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.2, stroke_opacity=0.6
        ))
        v_arrow_c = always_redraw(lambda: Arrow(
            start=camion_viz.get_center(), end=camion_viz.get_center() + RIGHT*((a_camion*tiempo.get_value())/35),
            color="#FFC107", buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.2, stroke_opacity=0.6
        ))

        c_auto = always_redraw(lambda: ejes.plot(lambda t: v_auto * t, x_range=[0, max(0.01, tiempo.get_value())], color="#00E5FF", stroke_width=4))
        c_camion = always_redraw(lambda: ejes.plot(lambda t: x0_camion + 0.5 * a_camion * t**2, x_range=[0, max(0.01, tiempo.get_value())], color="#FFC107", stroke_width=4))

        eq_a = MathTex("x = vt", color="#00E5FF", font_size=20).add_updater(lambda m: m.next_to(ejes.c2p(tiempo.get_value(), v_auto*tiempo.get_value()), UR, buff=0.25))
        eq_c = MathTex(r"x = x_0 + \frac{1}{2}at^2", color="#FFC107", font_size=20).add_updater(lambda m: m.next_to(ejes.c2p(tiempo.get_value(), x0_camion + 0.5*a_camion*tiempo.get_value()**2), DR, buff=0.25))

        self.add(pista, ejes, lbl_ejes, dashboard, auto_viz, camion_viz, v_arrow_a, v_arrow_c, c_auto, c_camion, eq_a, eq_c)

        self.play(tiempo.animate.set_value(t_e1), run_time=5, rate_func=linear)
        self.wait(0.5)

        pos_e1 = pista.n2p(v_auto * t_e1)
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(0.5).move_to(pos_e1 + UP*0.2), run_time=1.5)

        calc1 = VGroup(
            Text("1er Encuentro", font_size=20, color=WHITE),
            MathTex(r"x_{a} = x_{0c} + \tfrac{1}{2}at^2", font_size=14, color=GRAY),
            MathTex(f"t = {t_e1:.2f}\\text{{ s}}", font_size=24, color="#00E5FF"),
            MathTex(f"x = {v_auto*t_e1:.1f}\\text{{ m}}", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.15).next_to(auto_viz, UP, buff=0.3)
        bg1 = SurroundingRectangle(calc1, color=BLUE, fill_opacity=0.9, fill_color=BLACK, buff=0.2)
        lbl1 = VGroup(bg1, calc1)
        
        self.play(FadeIn(lbl1))
        self.wait(4)
        self.play(FadeOut(lbl1), Restore(self.camera.frame), run_time=1.5)

        self.play(tiempo.animate.set_value(t_v_igual), run_time=4, rate_func=linear)
        self.wait(0.5)

        self.play(self.camera.frame.animate.scale(0.6).move_to(pista.get_center() + UP*2.5), run_time=1.5)
        
        sep_max = abs(v_auto*t_v_igual - (x0_camion + 0.5*a_camion*t_v_igual**2))
        calc2 = VGroup(
            Text("Velocidades Iguales", font_size=20, color=WHITE),
            MathTex(r"v_c = at = v_a", font_size=14, color=GRAY),
            MathTex(f"t = {t_v_igual:.1f}\\text{{ s}}", font_size=24, color="#FFC107"),
            MathTex(f"\\text{{Sep: }}{sep_max:.1f}\\text{{ m}}", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.15).move_to(self.camera.frame.get_center())
        bg2 = SurroundingRectangle(calc2, color=YELLOW, fill_opacity=0.9, fill_color=BLACK, buff=0.2)
        lbl2 = VGroup(bg2, calc2)
        
        self.play(FadeIn(lbl2))
        self.wait(4)
        self.play(FadeOut(lbl2), Restore(self.camera.frame), run_time=1.5)

        self.play(tiempo.animate.set_value(t_e2), run_time=5, rate_func=linear)
        self.wait(0.5)

        pos_e2 = pista.n2p(v_auto * t_e2)
        self.play(self.camera.frame.animate.scale(0.5).move_to(pos_e2 + UP*0.2), run_time=1.5)
        
        calc3 = VGroup(
            Text("2do Encuentro", font_size=20, color=WHITE),
            MathTex(f"t = {t_e2:.2f}\\text{{ s}}", font_size=24, color="#00E5FF"),
            MathTex(f"x = {v_auto*t_e2:.1f}\\text{{ m}}", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.15).next_to(auto_viz, UP, buff=0.3)
        bg3 = SurroundingRectangle(calc3, color=BLUE, fill_opacity=0.9, fill_color=BLACK, buff=0.2)
        lbl3 = VGroup(bg3, calc3)
        
        self.play(FadeIn(lbl3))
        self.wait(4)
        self.play(FadeOut(lbl3), Restore(self.camera.frame), run_time=1.5)

        self.play(tiempo.animate.set_value(t_max), run_time=2, rate_func=linear)
        self.wait(3)
