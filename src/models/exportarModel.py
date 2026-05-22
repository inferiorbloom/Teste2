import pandas as pd
import os
import customtkinter as ctk
import math
import numpy as np


class ExportarModel:

    def formatar_valor_erro(self, valor, erro):
        if erro is None or erro == 0:
            return valor, erro
        
        ordem = math.floor(math.log10(abs(erro)))
        sig = 2
        if ordem < 0:
            casas = -(ordem - (sig - 1))
            #print("DEBUG ORDEM:", ordem, "CASAS DECIMAIS:", casas)
            erro_arred = np.round(erro, casas)
            valor_arred = np.round(valor, casas)
        elif ordem >= 0:
            
            erro_arred = np.round(erro)
            valor_arred = np.round(valor)

        
        return valor_arred, erro_arred


    def formatar_ld(self, ld):
        if ld is None or ld == "":
            return ld

        try:
            ld = float(ld)
        except:
            return ld

        if ld == 0:
            return 0

        ordem = math.floor(math.log10(abs(ld)))
        primeira = ld / (10 ** ordem)

        # mesma lógica do erro
        if primeira < 3:
            sig = 2
        else:
            sig = 1

        casas = -(ordem - (sig - 1))

        return round(ld, casas)


    def exportar_para_excel(
        self,
        lista_arquivos,
        concentracoes=None,
        areas_normalizadas=None,
        fatores_normalizacao=None,
        erros_normalizados=None,
        erros_propagados=None,
        ld_resultado=None,
        unidade_padrao=None,
        arquivo_padrao=None,
    ):
        arquivos = lista_arquivos or []
        concentracoes = concentracoes or {}
        areas_normalizadas = areas_normalizadas or {}
        fatores_normalizacao = fatores_normalizacao or {}
        erros_normalizados = erros_normalizados or {}
        erros_propagados = erros_propagados or {}
        ld_resultado = ld_resultado or {}
        unidade_padrao = unidade_padrao or {}
        arquivo_padrao = arquivo_padrao or ""
        nome_padrao = os.path.basename(arquivo_padrao).replace(".txt", "")

        print("-------------------------")
        print(arquivo_padrao)
        print("-------------------------")
        print(nome_padrao)
        print("-------------------------")
        print(ld_resultado)


        elementos = {
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

        # --- Exportação dos dados originais (sem mudar nada) ---
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
                            nome_elemento = elementos.get(z, "")
                        except Exception:
                            nome_elemento = ""

                        energia = float(valores[1]) if valores[1] else 0
                        area = float(valores[2]) if valores[2] else 0
                        erro = float(valores[3]) if valores[3] else 0

                        erro_percent = (erro / area) * 100 if area != 0 else 0

                        area_norm = areas_normalizadas.get(nome_amostra, {}).get(nome_elemento, "")
                        erro_norm = erros_normalizados.get(nome_amostra, {}).get(nome_elemento, "")

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

        df_dados = pd.DataFrame(todos_dados)


        # --- Exportação da análise (Resultados) ---
        analise = {}
        elementos_encontrados = set()

        for bloco in concentracoes.values():
            if isinstance(bloco, dict):
                for nome_amostra, valores in bloco.items():
                    analise.setdefault(nome_amostra, {})
                    for elemento, valor in valores.items():
                        elementos_encontrados.add(elemento)
                        analise[nome_amostra].setdefault(elemento, {})
                        analise[nome_amostra][elemento]["C"] = valor

        for bloco in erros_propagados.values():
            if isinstance(bloco, dict):
                for nome_amostra, amostra_valores in bloco.items():
                    analise.setdefault(nome_amostra, {})
                    for elemento, erro in amostra_valores.items():
                        elementos_encontrados.add(elemento)
                        analise[nome_amostra].setdefault(elemento, {})
                        analise[nome_amostra][elemento]["Erro"] = erro

        if analise:
            elementos_ordenados = [elementos[z] for z in elementos
                                   if elementos[z] in elementos_encontrados]
            colunas = []
            for elemento in elementos_ordenados:
                colunas.append((elemento, "C"))
                colunas.append((elemento, "Erro"))

            linhas = {}
            for nome_amostra, elementos in analise.items():
                linha = {}
                for elemento in elementos_ordenados:
                    c_col = "C"
                    e_col = "Erro"
                    valor = elementos.get(elemento, {}).get("C", "")
                    erro = elementos.get(elemento, {}).get("Erro", "")

                    if valor != "":
                        try:
                            #print("DEBUG VALOR BRUTO:", valor, "ERRO BRUTO:", erro)
                            valor_num = float(valor)
                            erro_existe = erro not in ["", None]

                            if erro_existe:
                                erro_num = float(erro)
                            else:
                                erro_num = None

                            # 🔥 Se não tem erro ou erro = 0 → NÃO arredonda
                            if erro_existe:
                                valor_fmt, erro_fmt = self.formatar_valor_erro(valor_num, erro_num)
                                if isinstance(valor_fmt, (int, float)) and isinstance(erro_fmt, (int, float)):

                                    if erro_fmt != 0:
                                        ordem = math.floor(math.log10(abs(erro_fmt)))
                                        primeira = erro_fmt / (10 ** ordem)
                                        sig = 2 if primeira < 3 else 1
                                        casas = max(0, -(ordem - (sig - 1)))
                                    else:
                                        casas = 0

                                    valor_str = f"{valor_fmt:.{casas}f}"
                                    erro_str = f"{erro_fmt:.{casas}f}"

                                    linha[(elemento, c_col)] = valor_str
                                    linha[(elemento, e_col)] = erro_str

                                else:
                                    linha[(elemento, c_col)] = valor_fmt
                                    linha[(elemento, e_col)] = erro_fmt
                            else:
                                valor_fmt = round(valor_num)  # 👈 arredondamento simples
                                linha[(elemento, c_col)] = valor_fmt
                                linha[(elemento, e_col)] = ""

                        except Exception:
                            linha[(elemento, c_col)] = valor
                            linha[(elemento, e_col)] = erro

                linhas[nome_amostra] = linha

            df_analise = pd.DataFrame.from_dict(linhas, orient="index")
            df_analise = df_analise.reindex(columns=pd.MultiIndex.from_tuples(colunas))


            df_analise.index = list(linhas.keys())

        else:
            df_analise = pd.DataFrame()
        
        # --- Nova aba: só concentrações (já formatadas) ---

        df_concentracoes = df_analise.xs("C", axis=1, level=1)
        df_concentracoes.columns.name = None

        os.makedirs("tabela-excel", exist_ok=True)
        caminho_arquivo = os.path.join("tabela-excel", "amostras.xlsx")

        def _salvar_excel(path):
            with pd.ExcelWriter(path) as writer:
                df_dados.to_excel(writer, sheet_name="Dados", index=False, header=False)

                df_concentracoes.to_excel(
                    writer,
                    sheet_name="Concentrações",
                    index=True,
                    index_label="Amostra"
                )

               # escreve dataframe sem cabeçalho
                df_analise.to_excel(
                    writer,
                    sheet_name="Resultados",
                    index=True,
                    header=False,
                    startrow=2
                )

                workbook = writer.book
                worksheet = writer.sheets["Resultados"]

                # escreve "LD" na primeira coluna
                worksheet.write(1, 0, "LD")

                col = 1

                for elemento in elementos_ordenados:

                    unidade = unidade_padrao.get(elemento, "")

                    if unidade:
                        titulo = f"{elemento} ({unidade})"
                    else:
                        titulo = elemento

                    # linha 0 -> elemento
                    worksheet.merge_range(0, col, 0, col + 1, titulo)

                    # linha 1 -> valor do LD
                    ld = ""
                    if ld_resultado:
                        ld_bruto = ld_resultado.get(nome_padrao, {}).get(elemento, "")
                        ld = self.formatar_ld(ld_bruto)

                    worksheet.merge_range(1, col, 1, col + 1, ld)

                    # linha 2 -> C / Erro
                    worksheet.write(2, col, "C")
                    worksheet.write(2, col + 1, "Erro")

                    col += 2
        
        try:
            _salvar_excel(caminho_arquivo)
        except PermissionError:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = os.path.join("tabela-excel", f"amostras_{timestamp}.xlsx")
            _salvar_excel(caminho_arquivo)



        print("Exportacao concluida!")
        self.mostrar_popup_sucesso(caminho_arquivo)


    def mostrar_popup_sucesso(self, caminho_arquivo):
        popup = ctk.CTkToplevel()
        popup.title("Exportação Concluída!")
        popup.geometry("400x200")

        label = ctk.CTkLabel(
            popup,
            text=f"Arquivo exportado com sucesso!\n\nSalvo em:\n{caminho_arquivo}",
            font=("Arial", 16),
            justify="center",
            wraplength=360,
        )
        label.pack(pady=20, padx=20)

        botao_ok = ctk.CTkButton(popup, text="Fechar", width=100, command=popup.destroy)
        botao_ok.pack(pady=10)

        popup.update_idletasks()
        w, h = popup.winfo_width() + 100, popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        popup.grab_set()
