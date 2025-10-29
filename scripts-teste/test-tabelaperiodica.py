import customtkinter as ctk

# Dados simplificados: número atômico, símbolo, nome e posição (linha, coluna)
# Apenas posições reais da tabela principal (sem lantanídeos e actinídeos)
ELEMENTS_LAYOUT = [
    (1,  "H",  "Hydrogen",      0, 0),
    (2,  "He", "Helium",        0, 17),
    (3,  "Li", "Lithium",       1, 0),
    (4,  "Be", "Beryllium",     1, 1),
    (5,  "B",  "Boron",         1, 12),
    (6,  "C",  "Carbon",        1, 13),
    (7,  "N",  "Nitrogen",      1, 14),
    (8,  "O",  "Oxygen",        1, 15),
    (9,  "F",  "Fluorine",      1, 16),
    (10, "Ne", "Neon",          1, 17),
    (11, "Na", "Sodium",        2, 0),
    (12, "Mg", "Magnesium",     2, 1),
    (13, "Al", "Aluminium",     2, 12),
    (14, "Si", "Silicon",       2, 13),
    (15, "P",  "Phosphorus",    2, 14),
    (16, "S",  "Sulfur",        2, 15),
    (17, "Cl", "Chlorine",      2, 16),
    (18, "Ar", "Argon",         2, 17),
    (19, "K",  "Potassium",     3, 0),
    (20, "Ca", "Calcium",       3, 1),
    (21, "Sc", "Scandium",      3, 2),
    (22, "Ti", "Titanium",      3, 3),
    (23, "V",  "Vanadium",      3, 4),
    (24, "Cr", "Chromium",      3, 5),
    (25, "Mn", "Manganese",     3, 6),
    (26, "Fe", "Iron",          3, 7),
    (27, "Co", "Cobalt",        3, 8),
    (28, "Ni", "Nickel",        3, 9),
    (29, "Cu", "Copper",        3, 10),
    (30, "Zn", "Zinc",          3, 11),
    (31, "Ga", "Gallium",       3, 12),
    (32, "Ge", "Germanium",     3, 13),
    (33, "As", "Arsenic",       3, 14),
    (34, "Se", "Selenium",      3, 15),
    (35, "Br", "Bromine",       3, 16),
    (36, "Kr", "Krypton",       3, 17),
    (37, "Rb", "Rubidium",      4, 0),
    (38, "Sr", "Strontium",     4, 1),
    (39, "Y",  "Yttrium",       4, 2),
    (40, "Zr", "Zirconium",     4, 3),
    (41, "Nb", "Niobium",       4, 4),
    (42, "Mo", "Molybdenum",    4, 5),
    (43, "Tc", "Technetium",    4, 6),
    (44, "Ru", "Ruthenium",     4, 7),
    (45, "Rh", "Rhodium",       4, 8),
    (46, "Pd", "Palladium",     4, 9),
    (47, "Ag", "Silver",        4, 10),
    (48, "Cd", "Cadmium",       4, 11),
    (49, "In", "Indium",        4, 12),
    (50, "Sn", "Tin",           4, 13),
    (51, "Sb", "Antimony",      4, 14),
    (52, "Te", "Tellurium",     4, 15),
    (53, "I",  "Iodine",        4, 16),
    (54, "Xe", "Xenon",         4, 17),
    (55, "Cs", "Cesium",        5, 0),
    (56, "Ba", "Barium",        5, 1),
    (72, "Hf", "Hafnium",       5, 3),
    (73, "Ta", "Tantalum",      5, 4),
    (74, "W",  "Tungsten",      5, 5),
    (75, "Re", "Rhenium",       5, 6),
    (76, "Os", "Osmium",        5, 7),
    (77, "Ir", "Iridium",       5, 8),
    (78, "Pt", "Platinum",      5, 9),
    (79, "Au", "Gold",          5, 10),
    (80, "Hg", "Mercury",       5, 11),
    (81, "Tl", "Thallium",      5, 12),
    (82, "Pb", "Lead",          5, 13),
    (83, "Bi", "Bismuth",       5, 14),
    (84, "Po", "Polonium",      5, 15),
    (85, "At", "Astatine",      5, 16),
    (86, "Rn", "Radon",         5, 17),
    (87, "Fr", "Francium",      6, 0),
    (88, "Ra", "Radium",        6, 1),
    (104,"Rf", "Rutherfordium", 6, 3),
    (105,"Db", "Dubnium",       6, 4),
    (106,"Sg", "Seaborgium",    6, 5),
    (107,"Bh", "Bohrium",       6, 6),
    (108,"Hs", "Hassium",       6, 7),
    (109,"Mt", "Meitnerium",    6, 8),
    (110,"Ds", "Darmstadtium",  6, 9),
    (111,"Rg", "Roentgenium",   6, 10),
    (112,"Cn", "Copernicium",   6, 11),
    (113,"Nh", "Nihonium",      6, 12),
    (114,"Fl", "Flerovium",     6, 13),
    (115,"Mc", "Moscovium",     6, 14),
    (116,"Lv", "Livermorium",   6, 15),
    (117,"Ts", "Tennessine",    6, 16),
    (118,"Og", "Oganesson",     6, 17),
]

# Lantanídeos e actinídeos (séries separadas)
LANTHANIDES = [
    (57,"La","Lanthanum"), (58,"Ce","Cerium"), (59,"Pr","Praseodymium"),
    (60,"Nd","Neodymium"), (61,"Pm","Promethium"), (62,"Sm","Samarium"),
    (63,"Eu","Europium"), (64,"Gd","Gadolinium"), (65,"Tb","Terbium"),
    (66,"Dy","Dysprosium"), (67,"Ho","Holmium"), (68,"Er","Erbium"),
    (69,"Tm","Thulium"), (70,"Yb","Ytterbium"), (71,"Lu","Lutetium")
]

ACTINIDES = [
    (89,"Ac","Actinium"), (90,"Th","Thorium"), (91,"Pa","Protactinium"),
    (92,"U","Uranium"), (93,"Np","Neptunium"), (94,"Pu","Plutonium"),
    (95,"Am","Americium"), (96,"Cm","Curium"), (97,"Bk","Berkelium"),
    (98,"Cf","Californium"), (99,"Es","Einsteinium"), (100,"Fm","Fermium"),
    (101,"Md","Mendelevium"), (102,"No","Nobelium"), (103,"Lr","Lawrencium")
]


class PeriodicTable(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Tabela Periódica - Disposição Clássica")
        self.geometry("1500x750")

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Área da tabela
        self.table = ctk.CTkFrame(main_frame)
        self.table.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Painel lateral
        self.info_frame = ctk.CTkFrame(main_frame, width=250)
        self.info_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Info widgets
        ctk.CTkLabel(self.info_frame, text="Detalhes do Elemento", font=("Arial", 16, "bold")).pack(pady=10)
        self.info_box = ctk.CTkTextbox(self.info_frame, width=230, height=100)
        self.info_box.pack(pady=10)

        ctk.CTkLabel(self.info_frame, text="Selecionados", font=("Arial", 14, "bold")).pack(pady=(10, 0))
        self.sel_box = ctk.CTkTextbox(self.info_frame, width=230, height=500)
        self.sel_box.pack(pady=10)

        self.buttons = {}
        self.selected = set()

        # Criar tabela principal
        for num, sym, name, row, col in ELEMENTS_LAYOUT:
            self.add_button(num, sym, name, row, col)

        # Lantanídeos e actinídeos
        self.add_series(LANTHANIDES, 8)
        self.add_series(ACTINIDES, 9)

        ctk.CTkLabel(self.table, text="Lantanídeos", font=("Arial", 12)).grid(row=7, column=2, columnspan=5, pady=(20, 0))
        ctk.CTkLabel(self.table, text="Actinídeos", font=("Arial", 12)).grid(row=8, column=2, columnspan=5, pady=(20, 0))

    def add_button(self, num, sym, name, row, col):
        btn = ctk.CTkButton(self.table, text=f"{sym}\n{num}", width=60, height=60,
                            fg_color="#1E90FF", hover_color="#4682B4",
                            command=lambda n=num, s=sym, nm=name: self.toggle_select(n, s, nm))
        btn.grid(row=row, column=col, padx=3, pady=3)
        self.buttons[num] = btn

    def add_series(self, series, row):
        for i, (num, sym, name) in enumerate(series):
            self.add_button(num, sym, name, row, i + 2)

    def toggle_select(self, num, sym, name):
        btn = self.buttons[num]
        if num in self.selected:
            self.selected.remove(num)
            btn.configure(fg_color="#1E90FF")
        else:
            self.selected.add(num)
            btn.configure(fg_color="#FFD700")

        # Atualiza info box
        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", "end")
        self.info_box.insert("end", f"Símbolo: {sym}\nNúmero atômico: {num}\nNome: {name}")
        self.info_box.configure(state="disabled")

        # Atualiza lista de selecionados
        self.sel_box.configure(state="normal")
        self.sel_box.delete("1.0", "end")
        for n in sorted(self.selected):
            s = next((e[1] for e in ELEMENTS_LAYOUT if e[0] == n), None)
            if not s:
                s = next((e[1] for e in LANTHANIDES + ACTINIDES if e[0] == n), "")
            self.sel_box.insert("end", f"{s} ({n})\n")
        self.sel_box.configure(state="disabled")


if __name__ == "__main__":
    app = PeriodicTable()
    app.mainloop()
