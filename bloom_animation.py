import json
from pathlib import Path
import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent
BG = "#0C1220"
PANEL = "#151F30"
MUTED = "#A6B5CB"
INK = "#F2F6FC"
TEAL = "#44E0BE"
PURPLE = "#B89AFF"
AMBER = "#FFC46B"
RED = "#FF7B8C"
STROKE = "#35465E"
FONT = "DejaVu Sans"


def label(s, size=26, color=INK, max_width=12.4):
    t = Text(str(s), font=FONT, font_size=size, color=color,
             disable_ligatures=True, line_spacing=1.15)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def panel(w, h, at, color=STROKE):
    return RoundedRectangle(width=w, height=h, corner_radius=0.16,
                            stroke_color=color, stroke_width=1.5,
                            fill_color=PANEL, fill_opacity=1).move_to(at)


class BloomCompleto(Scene):
    def construct(self):
        self.camera.background_color = BG
        data = json.loads((ROOT / "trace.json").read_text(encoding="utf-8"))
        self.events = {e["tag"]: e for e in data["events"]}
        self.m, self.k = data["m"], data["k"]
        if self.m != 12 or self.k != 2:
            raise ValueError("Este guion visual esta disenado para m=12 y k=2")
        self.chapters = []
        self.introduction()
        self.hash_explanation()
        self.operation("empty", "03", "Caso borde: filtro vacío",
                       "Si nunca insertamos nada, todos los bits están en cero.",
                       "Basta encontrar un 0 para descartar el elemento.", 7)
        self.operation("insert5", "04", "Insertar el primer elemento",
                       "insert(5) marca las posiciones que calculan sus hashes.",
                       "Se guardan marcas; el número 5 no queda almacenado.", 8)
        self.operation("insert17", "05", "Insertar y compartir un bit",
                       "insert(17) usa las posiciones 5 y 4.",
                       "El bit 5 ya era 1. Compartir una posición es normal.", 8)
        self.operation("present", "06", "Consultar un elemento insertado",
                       "contains(5) revisa las mismas posiciones: 5 y 3.",
                       "Todos son 1: posiblemente está. El filtro no lo confirma.", 8)
        self.operation("absent", "07", "Descartar un elemento",
                       "contains(8) encuentra un 0 en la posición 8.",
                       "Definitivamente no está: si se insertara, ese bit sería 1.", 8)
        self.operation("false_positive", "08", "El falso positivo, paso a paso",
                       "Nunca insertamos 15. Sus hashes apuntan a 3 y 4.",
                       "Esos bits los marcaron 5 y 17: aparece un falso positivo.", 12)
        self.operation("duplicate", "09", "Reinsertar no cambia los bits",
                       "Volvemos a ejecutar insert(17).",
                       "Poner un 1 sobre otro 1 no añade información ni cuenta copias.", 6)
        self.deletion_explanation()
        self.clear_explanation()
        self.application()
        self.complexity()
        self.ending()
        (ROOT / "chapters.json").write_text(
            json.dumps(self.chapters, ensure_ascii=False, indent=2), encoding="utf-8")
    def chapter(self, number, title):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.chapters.append({"number": number, "title": title, "start": round(self.time, 2)})
        
        # 1. Creamos los textos
        eyebrow = label("Estructura de datos: Filtro de bloom", 14, MUTED)
        num = label(number, 18, TEAL)
        heading = label(title, 34, max_width=12.4)
        
        # 2. Agrupamos el "eyebrow" y el "heading" verticalmente
        # El buff=0.15 controla el espacio entre "Estructura de datos" y el título principal
        header_group = VGroup(eyebrow, heading).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # 3. Movemos todo el grupo a la esquina superior izquierda
        # buff=0.3 es la distancia desde el borde de la pantalla. Redúcelo si lo quieres aún más arriba.
        header_group.to_corner(UL, buff=0.3)
        
        # 4. Posicionamos el número en la esquina superior derecha
        num.to_corner(UR, buff=0.3)
        
        # 5. La línea (rule) la colocamos justo debajo del grupo de textos
        # En lugar de coordenadas fijas, usamos next_to
        rule = Line(LEFT, RIGHT, color=STROKE, stroke_width=1)
        rule.width = 12.9 # Ancho fijo para que abarque toda la pantalla (ajusta si es necesario)
        rule.next_to(header_group, DOWN, buff=0.2) # Se coloca 0.2 unidades debajo del título
        
        # 6. El footer se queda abajo
        footer = label("C++ ejecuta las operaciones  ·  Manim representa el registro real", 13, MUTED)
        footer.to_edge(DOWN, buff=0.3) # to_edge(DOWN) es más seguro que coordenadas fijas
        
        # 7. Animación
        self.play(
            FadeIn(eyebrow), 
            FadeIn(num), 
            FadeIn(heading), 
            Create(rule), 
            FadeIn(footer), 
            run_time=0.65
        )
    def note(self, first, second="", color=TEAL):
        box = panel(12.65, 1.28, [0, -2.55, 0], color)
        a = label(first, 24, INK, 11.9).move_to([0, -2.30, 0])
        b = label(second, 20, MUTED, 11.9).move_to([0, -2.82, 0])
        group = VGroup(box, a, b)
        self.play(FadeIn(group, shift=UP * 0.1), run_time=0.45)
        return group

    def board(self, values, y=-0.50):
        self.cells, self.digits = [], []
        group = VGroup()
        for i, value in enumerate(values):
            p = np.array([(i - 5.5) * 0.99, y, 0.0])
            cell = RoundedRectangle(width=0.84, height=0.86, corner_radius=0.1,
                                    stroke_color=TEAL if value else STROKE,
                                    stroke_width=2, fill_color=TEAL if value else PANEL,
                                    fill_opacity=0.15 if value else 1).move_to(p)
            digit = label(value, 30, TEAL if value else MUTED).move_to(p)
            index = label(i, 17, MUTED).move_to(p + DOWN * 0.72)
            self.cells.append(cell)
            self.digits.append(digit)
            group.add(cell, digit, index)
        self.play(LaggedStart(*[FadeIn(m) for m in group], lag_ratio=0.012), run_time=0.75)
        return group

    def introduction(self):
        self.chapter("01", "¿Está este elemento en el conjunto?")
        title = label("FILTRO DE BLOOM", 52, TEAL).move_to([0, 1.7, 0])
        sub = label("Una estructura probabilística para consultar pertenencia", 25, MUTED)
        sub.move_to([0, 0.88, 0])
        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(sub), run_time=1.1)
        cards = VGroup()
        for x, color, a, b in [(-3.25, TEAL, "DEFINITIVAMENTE NO", "Podemos descartar el elemento."),
                                (3.25, AMBER, "POSIBLEMENTE SÍ", "Hay que confirmar en el conjunto real.")]:
            box = panel(6.05, 1.50, [x, -0.45, 0], color)
            t = label(a, 23, color, 5.6).move_to([x, -0.18, 0])
            d = label(b, 19, MUTED, 5.6).move_to([x, -0.75, 0])
            cards.add(VGroup(box, t, d))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.3), run_time=1.2)
        self.note("TDA: conjunto con consulta aproximada de pertenencia.",
                  "Ahorra memoria; admite falsos positivos. No recupera los elementos.")
        self.wait(11)

    def hash_explanation(self):
        self.chapter("02", "Los ingredientes: bits y funciones hash")
        a = label("m = 12 bits", 29, TEAL).move_to([-3.9, 2.05, 0])
        b = label("k = 2 funciones hash", 29, PURPLE).move_to([3.1, 2.05, 0])
        self.play(FadeIn(a), FadeIn(b), run_time=0.5)
        self.board(self.events["empty"]["before"])
        formulas = VGroup(
            label("h1(x) = x mod 12", 28, TEAL).move_to([-3.25, 0.98, 0]),
            label("h2(x) = (⌊x / 12⌋ + 3) mod 12", 25, PURPLE, 6.3).move_to([3.0, 0.98, 0]))
        self.play(FadeIn(formulas), run_time=0.6)
        self.note("mod es el residuo de la división; ⌊x / 12⌋ es la división entera.",
                  "Hashes sencillos para enseñar. En producción se busca buena distribución.")
        self.wait(12)

    def operation(self, tag, number, title, intro, conclusion, hold):
        e = self.events[tag]
        self.chapter(number, title)
        board = self.board(e["before"])
        x, positions = e["x"], e["hashes"]
        action = f'{e["op"]}({x})'
        tokenbox = panel(3.6, 0.65, [0, 2.1, 0], TEAL if e["op"] == "insert" else AMBER)
        token = label(action, 26).move_to(tokenbox)
        self.play(FadeIn(tokenbox), FadeIn(token), run_time=0.45)
        note = self.note(intro, "Observa los índices debajo de cada casilla.")
        self.wait(2.4)
        hashcards = []
        for j, (p, col, xpos) in enumerate(zip(positions, [TEAL, PURPLE], [-3.1, 3.1])):
            expr = (f"{x} mod 12 = {p}" if j == 0
                    else f"({x // 12} + 3) mod 12 = {p}")
            card = panel(4.9, 0.68, [xpos, 1.07, 0], col)
            text = label(f"h{j+1}:  {expr}", 23, col, 4.5).move_to(card)
            g = VGroup(card, text)
            hashcards.append(g)
            self.play(FadeIn(g), run_time=0.5)
        self.wait(1.8)
        for j, p in enumerate(positions):
            col = [TEAL, PURPLE][j]
            arrow = Arrow(hashcards[j].get_bottom(), self.cells[p].get_top() + UP * 0.03,
                          buff=0.04, color=col, stroke_width=4,
                          max_tip_length_to_length_ratio=0.13)
            self.play(GrowArrow(arrow), self.cells[p].animate.set_stroke(col, width=4), run_time=0.8)
            if e["op"] == "insert":
                newdigit = label(e["after"][p], 30, TEAL).move_to(self.digits[p])
                self.play(Transform(self.digits[p], newdigit),
                          self.cells[p].animate.set_fill(TEAL, opacity=0.15), run_time=0.55)
            else:
                self.play(Indicate(self.digits[p], color=col, scale_factor=1.35), run_time=0.7)
            self.wait(0.7)
            self.play(FadeOut(arrow), self.cells[p].animate.set_stroke(
                TEAL if e["after"][p] else STROKE, width=2), run_time=0.3)
            # Consulta real con cortocircuito: no lee el segundo bit si ya vio 0.
            if e["op"] == "contains" and not e["before"][p]:
                break
        self.play(FadeOut(note), run_time=0.25)
        if e["op"] == "insert":
            status, color = "INSERCIÓN COMPLETADA", TEAL
        else:
            status = "true  ·  POSIBLEMENTE ESTÁ" if e["result"] else "false  ·  DEFINITIVAMENTE NO ESTÁ"
            color = AMBER if e["result"] else TEAL
        result = label(status, 26, color).move_to([0, -1.60, 0])
        self.play(FadeIn(result), run_time=0.5)
        if tag == "false_positive":
            truth = "Referencia externa: solo insertamos {5, 17}. El 15 no pertenece."
            self.note(conclusion, truth, AMBER)
        elif tag == "empty":
            self.note(conclusion, "El segundo bit ya no necesita leerse: contains devuelve false.")
        else:
            self.note(conclusion, "Los bits cambian al insertar; una consulta no modifica el filtro.")
        self.wait(hold)

    def deletion_explanation(self):
        self.chapter("10", "¿Por qué no hay remove(x) en el filtro básico?")
        state = self.events["duplicate"]["after"]
        self.board(state)
        a, b = self.events["insert5"], self.events["insert17"]
        shared = sorted(set(a["hashes"]) & set(b["hashes"]))
        t1 = label(f'5 marca {a["hashes"][0]} y {a["hashes"][1]}', 28, TEAL).move_to([-3.3, 1.9, 0])
        t2 = label(f'17 marca {b["hashes"][0]} y {b["hashes"][1]}', 28, PURPLE).move_to([3.3, 1.9, 0])
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.5)
        arrows = VGroup()
        for p in shared:
            arrows.add(Arrow(t1.get_bottom(), self.cells[p].get_top(), color=TEAL, buff=0.1),
                       Arrow(t2.get_bottom(), self.cells[p].get_top(), color=PURPLE, buff=0.1))
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)
        self.note(f'El bit {shared[0]} pertenece a las marcas de ambos elementos.',
                  f'Si se borrara para quitar 5, contains(17) podría dar false.', RED)
        warn = label("Un borrado individual puede crear falsos negativos.", 25, RED)
        warn.move_to([0, -1.6, 0])
        self.play(FadeIn(warn), run_time=0.5)
        self.wait(11)

    def clear_explanation(self):
        self.chapter("11", "clear() sí puede reiniciar todo el filtro")
        e = self.events["clear"]
        self.board(e["before"])
        self.note("clear() descarta todas las marcas, de todos los elementos.",
                  "Es un reinicio completo; no elimina un elemento individual.")
        self.wait(3)
        animations = []
        for p, value in enumerate(e["after"]):
            if e["before"][p] != value:
                animations += [Transform(self.digits[p], label(value, 30, MUTED).move_to(self.digits[p])),
                               self.cells[p].animate.set_stroke(STROKE).set_fill(PANEL, opacity=1)]
        self.play(*animations, run_time=1.6)
        after = self.events["after_clear"]
        result = label(f'contains({after["x"]}) → {str(after["result"]).lower()}', 30, TEAL)
        result.move_to([0, 1.3, 0])
        self.play(FadeIn(result), run_time=0.6)
        self.wait(6)

    def application(self):
        self.chapter("12", "¿Para qué sirve en la práctica?")
        q = panel(3.4, 0.8, [-4.45, 0.9, 0])
        f = panel(3.4, 0.8, [0, 0.9, 0], TEAL)
        qt = label("Buscar un registro", 23).move_to(q)
        ft = label("Filtro de Bloom", 23, TEAL).move_to(f)
        link = Arrow(q.get_right(), f.get_left(), color=MUTED, buff=0.08)
        self.play(FadeIn(q), FadeIn(qt), FadeIn(f), FadeIn(ft), GrowArrow(link), run_time=1)
        upper = panel(3.5, 1.05, [4.5, 1.7, 0], TEAL)
        lower = panel(3.5, 1.05, [4.5, -0.2, 0], AMBER)
        u = VGroup(label("false", 25, TEAL).move_to([4.5, 1.91, 0]),
                   label("Evita la búsqueda", 21).move_to([4.5, 1.48, 0]))
        l = VGroup(label("true", 25, AMBER).move_to([4.5, 0.03, 0]),
                   label("Consulta la base de datos", 18).move_to([4.5, -0.42, 0]))
        a1 = Arrow(f.get_right(), upper.get_left(), color=TEAL, buff=0.08)
        a2 = Arrow(f.get_right(), lower.get_left(), color=AMBER, buff=0.08)
        self.play(FadeIn(upper), FadeIn(u), GrowArrow(a1), run_time=0.8)
        self.play(FadeIn(lower), FadeIn(l), GrowArrow(a2), run_time=0.8)
        self.note("El filtro descarta ausencias antes de una consulta costosa.",
                  "Para confirmar un sí, se consulta una fuente que guarda los datos reales.")
        self.wait(10)

    def complexity(self):
        self.chapter("13", "Costo y límites de la estructura")
        rows = [("insert(x)", "O(k)", "Marca k posiciones."),
                ("contains(x)", "O(k) en el peor caso", "Revisa hasta k bits; puede salir antes."),
                ("Memoria", "O(m) bits", "En C++: bits empaquetados en bytes."),
                ("clear()", "O(m)", "Reinicia el almacenamiento.")]
        for i, (op, cost, desc) in enumerate(rows):
            y = 1.93 - i * 0.83
            box = panel(12.5, 0.7, [0, y, 0])
            a = label(op, 24, TEAL).move_to([-4.65, y, 0])
            b = label(cost, 22, AMBER, 3.5).move_to([-0.95, y, 0])
            c = label(desc, 19, MUTED, 5.3).move_to([3.65, y, 0])
            self.play(FadeIn(VGroup(box, a, b, c)), run_time=0.45)
        self.note("Aquí k = 2 y las claves son enteros de tamaño fijo: O(1).",
                  "Con cadenas, calcular los hashes también cuesta según su longitud.")
        limit = label("Más ocupación puede aumentar los falsos positivos.", 22, PURPLE)
        limit.move_to([0, -1.55, 0])
        self.play(FadeIn(limit), run_time=0.4)
        self.wait(13)

    def ending(self):
        self.chapter("14", "Qué debes recordar")
        facts = ["1. Guarda bits, no los elementos completos.",
                 "2. Un 0 permite descartar; todos 1 solo sugieren presencia.",
                 "3. Admite falsos positivos, sin falsos negativos en uso correcto.",
                 "4. insert y contains son sus operaciones principales."]
        for i, fact in enumerate(facts):
            t = label(fact, 27, INK, 12.2)
            t.move_to([-6.1 + t.width / 2, 1.8 - i * 0.78, 0])
            self.play(FadeIn(t, shift=RIGHT * 0.1), run_time=0.55)
        self.note("Poca memoria y consultas rápidas, a cambio de posibles falsos positivos.",
                  "Demostración reproducible: implementación C++ + animación Manim.")
        self.wait(9)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=1)