import pandas as pd
import os
import customtkinter as ctk

class ExportarModel:
    def exportar_para_excel(self, lista_arquivos, resultados):
        arquivos = lista_arquivos
        #concentracoes = resultados

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

        # Garante que o diretório exista
        os.makedirs("tabela-excel", exist_ok=True)

        caminho_arquivo = os.path.join("tabela-excel", "amostras.xlsx")
        
        # Exporta para Excel com duas abas
        with pd.ExcelWriter(caminho_arquivo) as writer:
            df_dados.to_excel(writer, sheet_name="Dados", index=False)
            df_analise.to_excel(writer, sheet_name="Análise", index=True)

        print("Exportacao concluida!")

        self.mostrar_popup_sucesso(caminho_arquivo)

    # --------------------------------------------
    # Pop-up de confirmação da exportação
    # --------------------------------------------
    def mostrar_popup_sucesso(self, caminho_arquivo):
        popup = ctk.CTkToplevel()
        popup.title("Exportação Concluída!")
        popup.geometry("400x200")

        label = ctk.CTkLabel(
            popup,
            text=f"Arquivo exportado com sucesso!\n\nSalvo em:\n{caminho_arquivo}",
            font=("Arial", 16),
            justify="center",
            wraplength=360
        )
        label.pack(pady=20, padx=20)

        botao_ok = ctk.CTkButton(
            popup,
            text="Fechar",
            width=100,
            command=popup.destroy
        )
        botao_ok.pack(pady=10)

        # Centraliza o pop-up na tela
        popup.update_idletasks()
        w, h = popup.winfo_width() + 100, popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        popup.grab_set()  # bloqueia interação com a janela principal
