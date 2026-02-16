import math


class LimiteDeteccaoModel:
    # Função para calcular as limite de deteccao
    def calcular_limite_deteccao(self, arquivos_fullReport):
        backgrounds = arquivos_fullReport
        limites_area = {}
        for elemento, bg in backgrounds.items():
            limites_area[elemento] = round(3 * math.sqrt(bg))
        return limites_area
