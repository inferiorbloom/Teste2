import math
import os

class LimiteDeteccaoModel:

    def calcular_limite_deteccao(self, arquivos_fullReport, arquivo_padrao, c_padrao, areas_normalizadas, concentracoes):

      #  print("Será que os arquivos estão chegando corretamente?")
      #  print(areas_normalizadas)
       # print("=================================")

       # print("Será que as concentrações estão chegando corretamente?")
       # print(concentracoes)
       # print("=================================")

        # reorganiza as concentrações
        concentracoes = self.reorganizar_concentracoes(concentracoes)

        #print("Concentrações reorganizadas:")
        #print(concentracoes)
        #print("=================================")

        limites = {}

        for arquivo, backgrounds in arquivos_fullReport.items():

            limites_area = {}

            for elemento, bg in backgrounds.items():

                limites_area[elemento] = round(3 * math.sqrt(bg))

            limites[arquivo] = limites_area

        ld_resultado = {}
        for arquivo, elementos in limites.items():
            nome = os.path.basename(arquivo).replace(".pdf", "")
            ld_resultado[nome] = {}

            for elemento, limite_area in elementos.items():

                area_norm = areas_normalizadas.get(nome, {}).get(elemento)
                conc = concentracoes.get(nome, {}).get(elemento)

                if area_norm and conc:

                    ld = (conc * limite_area) / area_norm
                    ld_resultado[nome][elemento] = ld

        print(ld_resultado)
       
        return ld_resultado


    def reorganizar_concentracoes(self, concentracoes):

        concentracoes_novas = {}

        for bloco in concentracoes.values():

            for arquivo, elementos in bloco.items():

                concentracoes_novas[arquivo] = {}

                for elemento, valor in elementos.items():

                    concentracoes_novas[arquivo][elemento] = float(valor)

        return concentracoes_novas