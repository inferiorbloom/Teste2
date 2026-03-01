import math


class LimiteDeteccaoModel:
    # Função para calcular as limite de deteccao
    def calcular_limite_deteccao(self, arquivos_fullReport, arquivo_padrao, c_padrao):

        lista_arquivo_padrao = arquivo_padrao

        c_padrao = c_padrao["elementos"]

        # Dicionário dos elementos químicos
        elementos = {
            12: "Mg",
            13: "Al",
            14: "Si",
            15: "P",
            16: "S",
            17: "Cl",
            18: "Ar",
            19: "K",
            20: "Ca",
            21: "Sc",
            22: "Ti",
            23: "V",
            24: "Cr",
            25: "Mn",
            26: "Fe",
            27: "Co",
            28: "Ni",
            29: "Cu",
            30: "Zn",
            31: "Ga",
            32: "Ge",
            33: "As",
            34: "Se",
            35: "Br",
            36: "Kr",
            37: "Rb",
            38: "Sr",
            39: "Y",
            40: "Zr",
            41: "Nb",
            42: "Mo",
            43: "Tc",
            44: "Ru",
            45: "Rh",
            46: "Pd",
            47: "Ag",
            48: "Cd",
            49: "In",
            50: "Sn",
            51: "Sb",
            52: "Te",
            53: "I",
            54: "Xe",
            55: "Cs",
            56: "Ba",
            57: "La",
            58: "Ce",
            59: "Pr",
            60: "Nd",
            61: "Pm",
            62: "Sm",
            63: "Eu",
            64: "Gd",
            65: "Tb",
            66: "Dy",
            67: "Ho",
            68: "Er",
            69: "Tm",
            70: "Yb",
            71: "Lu",
            72: "Hf",
            73: "Ta",
            74: "W",
            75: "Re",
            76: "Os",
            77: "Ir",
            78: "Pt",
            79: "Au",
            80: "Hg",
            81: "Tl",
            82: "Pb",
            83: "Bi",
            84: "Po",
            85: "At",
            86: "Rn",
            87: "Fr",
            88: "Ra",
            89: "Ac",
            90: "Th",
            91: "Pa",
            92: "U",
            93: "Np",
            94: "Pu",
        }

        area_padrao = {}
        # Lê área do padrão

        with open(lista_arquivo_padrao, "r", encoding="utf-8") as p:
            for line in p:
                line = line.strip()
                if line and line[0].isdigit():
                    valores = [v.strip() for v in line.split(",")]
                    try:
                        z = int(valores[0])
                        area = float(valores[2])
                        elemento = elementos.get(z, "-")
                        area_padrao[elemento] = area
                    except (ValueError, IndexError):
                        continue

        print(area_padrao)
        print(c_padrao)

        backgrounds = arquivos_fullReport
        limites_area = {}
        for elemento, bg in backgrounds.items():
            limites_area[elemento] = round(3 * math.sqrt(bg))
        return limites_area
