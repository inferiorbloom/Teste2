import math
import os

class LimiteDeteccaoModel:

    def _buscar_valor_por_elemento(self, dados, nome_amostra, elemento):
        if not isinstance(dados, dict):
            return None

        amostra_dados = dados.get(nome_amostra)
        if not isinstance(amostra_dados, dict):
            return None

        if elemento in amostra_dados:
            return amostra_dados[elemento]

        for chave, valor in amostra_dados.items():
            if isinstance(chave, tuple) and chave and chave[0] == elemento:
                return valor

        return None

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

                limites_area[elemento] = 3 * math.sqrt(bg)

            limites[arquivo] = limites_area

        ld_resultado = {}
        for arquivo, elementos in limites.items():
            nome = os.path.basename(arquivo).replace(".pdf", "").strip()
            ld_resultado[nome] = {}

            for elemento, limite_area in elementos.items():

                area_norm = self._buscar_valor_por_elemento(areas_normalizadas, nome, elemento)
                conc = self._buscar_valor_por_elemento(concentracoes, nome, elemento)

                if area_norm not in [None, "", 0] and conc not in [None, "", 0]:
                    try:
                        conc_valor = float(conc)
                        area_norm_valor = float(area_norm)
                    except (TypeError, ValueError):
                        continue

                    ld = (conc_valor * limite_area) / area_norm_valor
                    ld_resultado[nome][elemento] = ld
        #print("areas normalizadas:", areas_normalizadas)
        #print("------------------------------")
        #print("Concentrações:", concentracoes)
        #print("------------------------------")
        #print("Limites de detecção calculados:", ld_resultado)
        #print("Backgrounds:", backgrounds)
        #print("Backgrounds:", arquivos_fullReport)
        #print("------------------------------")
        #print("Limites de detecção área:", limites[arquivo])
        #print(ld_resultado)
    
       
        return ld_resultado


    def reorganizar_concentracoes(self, concentracoes):

        concentracoes_novas = {}

        for bloco in concentracoes.values():

            for arquivo, elementos in bloco.items():

                concentracoes_novas[arquivo] = {}

                for elemento, valor in elementos.items():

                    concentracoes_novas[arquivo][elemento] = float(valor)

        return concentracoes_novas