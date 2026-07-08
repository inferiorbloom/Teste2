import os
import pandas as pd


class AbaDadosModel:
    """Monta o DataFrame usado na aba 'Dados' (dados brutos de cada amostra)."""

    ELEMENTOS = {
        13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
        21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni",
        29: "Cu", 30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr",
        37: "Rb", 38: "Sr", 39: "Y", 40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru",
        45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn", 51: "Sb", 52: "Te",
        53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
        61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er",
        69: "Tm", 70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os",
        77: "Ir", 78: "Pt", 79: "Au", 80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po",
        85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th", 91: "Pa", 92: "U",
        93: "Np", 94: "Pu",
    }

    def montar(self, arquivos, areas_normalizadas, erros_normalizados, fatores_normalizacao):
        """
        Recebe os arquivos de amostra + os dicionários já calculados em
        ConcentracaoModel e devolve o DataFrame pronto para a aba 'Dados'
        (sem cabeçalho, pois o cabeçalho já vai embutido nas linhas).
        """
        todos_dados = []

        for arquivo in arquivos:
            nome_amostra = os.path.basename(arquivo).replace(".txt", "")
            fator = fatores_normalizacao.get(nome_amostra, "")
            fator_formatado = ""
            if isinstance(fator, (int, float)):
                fator_formatado = round(fator, 2)
            else:
                try:
                    fator_formatado = round(float(fator), 2)
                except Exception:
                    fator_formatado = fator

            todos_dados.append([nome_amostra, "", "", "", "", "", "", "Normalização:", fator_formatado])
            todos_dados.append([
                "Elemento",
                "Z",
                "Energia (keV)",
                "Área (CPS)",
                "Erro (CPS)",
                "Erro (%)",
                "Área Normalizada (CPS)",
                "Erro Normalizado (CPS)"
            ])

            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()[5:]

                for linha in linhas:
                    valores = [v.strip() for v in linha.split(",")]
                    if len(valores) > 1:
                        try:
                            z = int(valores[0])
                            nome_elemento = self.ELEMENTOS.get(z, "")
                        except Exception:
                            nome_elemento = ""

                        energia = float(valores[1]) if valores[1] else 0
                        area = float(valores[2]) if valores[2] else 0
                        erro = float(valores[3]) if valores[3] else 0

                        erro_percent = (erro / area) * 100 if area != 0 else 0
                        chave = (nome_elemento, round(energia, 3))

                        area_norm = areas_normalizadas.get(nome_amostra, {}).get(chave, "")
                        erro_norm = erros_normalizados.get(nome_amostra, {}).get(chave, "")

                        if area_norm != "":
                            try:
                                area_norm = round(float(area_norm), 0)
                            except Exception:
                                pass

                        if erro_norm != "":
                            try:
                                erro_norm = round(float(erro_norm), 0)
                            except Exception:
                                pass

                        todos_dados.append([
                            nome_elemento,
                            z,
                            energia,
                            area,
                            erro,
                            round(erro_percent, 2),
                            area_norm,
                            erro_norm,
                        ])

            todos_dados.append(["", "", "", "", "", "", "", ""])

        return pd.DataFrame(todos_dados)
