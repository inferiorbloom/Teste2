import pandas as pd
import os
import customtkinter as ctk

class ExportarModel:
    def exportar_para_excel(self, lista_arquivos, resultados):
        arquivos = lista_arquivos
        #concentracoes = resultados
        print('CATAPIMBAS')

        # --- Exportação dos dados originais (sem mudar nada) ---
        todos_dados = []
        for arquivo in arquivos:
            nome_amostra = os.path.basename(arquivo).replace(".txt", "")
            todos_dados.append([nome_amostra, "", "", "", ""])
            #todos_dados.append(["Elemento", "Z", "Energia", "Área", "Erro"])
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()[5:]
                for linha in linhas:
                    valores = [v.strip() for v in linha.split(",")]
                    if len(valores) > 1:
                        try:
                            z = valores[0]
                            nome_elemento = elementos.get(int(z), "")
                        except:
                            nome_elemento = ""
                        dados_sem_ultima = valores[:-1]
                        linha_export = [nome_elemento] + dados_sem_ultima
                        todos_dados.append(linha_export)
            todos_dados.append(["", "", "", "", ""])

        df_dados = pd.DataFrame(todos_dados, columns=["Elemento", "Z", "Energia", "Área", "Erro"])
        #print(df_dados)

        # --- Exportação da análise (concentrações já calculadas) ---
        # Agora só usa o dicionário `concentracoes` que já foi gerado antes
        analise = {}
        for chave_conc, dados_amostras in resultados.items():
            for nome_amostra, elementos in dados_amostras.items():
                analise[nome_amostra] = elementos  # já tem os elementos e valores

        # Extrai todos os elementos detectados
        elementos_encontrados = sorted({
            elemento
            for valores in analise.values()
            for elemento in valores.keys()
        })

        # Cria DataFrame direto das concentrações
        df_analise = pd.DataFrame.from_dict(analise, orient="index", columns=elementos_encontrados)

        # Exporta para Excel com duas abas
        with pd.ExcelWriter("amostras.xlsx") as writer:
            df_dados.to_excel(writer, sheet_name="Dados", index=False)
            df_analise.to_excel(writer, sheet_name="Análise", index=True)
        #print("Exportação concluída!")
'''
        # Pop-up de confirmação
        exportado = ctk.CTkToplevel(master)
        exportado.title("Exportação Concluída")
        texto_exportado = ctk.CTkLabel(
            exportado,
            text="Arquivo exportado com sucesso como 'amostras.xlsx'! 50 Reais por exportação.",
            font=("Arial Black", 16), wraplength=400
        )
        exportado.transient(janela)  # Torna a janela filha da janela principal
        exportado.grab_set()  # Impede interação com a janela principal enquanto esta está aberta
        texto_exportado.pack(padx=20, pady=20)
        exportado.update_idletasks()
        largura = exportado.winfo_width()
        altura = exportado.winfo_height()
        x = (exportado.winfo_screenwidth() // 2) - (largura // 2)
        y = (exportado.winfo_screenheight() // 2) - (altura // 2)
        exportado.geometry(f"+{x}+{y}")
        #som_concluido()
'''
        
