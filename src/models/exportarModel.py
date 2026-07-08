from importlib.resources import path

import pandas as pd
import os
import customtkinter as ctk

from resource_utils import ensure_directory, user_data_path

from models.arredondamentoModel import ArredondamentoModel
from models.abaDadosModel import AbaDadosModel
from models.abaResultadosModel import AbaResultadosModel, montar_titulo_coluna
from models.abaConcentracoesModel import AbaConcentracoesModel


from resource_utils import ensure_directory, user_data_path

class ExportarModel:

    def __init__(self):
        self.arredondamento = ArredondamentoModel()
        self.aba_dados = AbaDadosModel()
        self.aba_resultados = AbaResultadosModel()
        self.aba_concentracoes = AbaConcentracoesModel()

    def _normalizar_valores_para_excel(self, df):
        """Converte valores que parecem numéricos para tipos numéricos reais antes de gravar no Excel."""
        if df is None or df.empty:
            return df

        df_export = df.copy()

        for coluna in df_export.columns:
            serie = df_export[coluna]

            if not pd.api.types.is_object_dtype(serie) and not pd.api.types.is_string_dtype(serie):
                continue

            valores_normalizados = []
            for valor in serie:
                if pd.isna(valor):
                    valores_normalizados.append(valor)
                    continue

                if valor in ["", None]:
                    valores_normalizados.append(valor)
                    continue

                if isinstance(valor, str):
                    texto = valor.strip()
                    if texto in ["-", "--", "—", "NaN", "nan", "None", "none"]:
                        valores_normalizados.append(valor)
                        continue

                    try:
                        valores_normalizados.append(float(texto))
                    except ValueError:
                        valores_normalizados.append(valor)
                else:
                    valores_normalizados.append(valor)

            df_export[coluna] = valores_normalizados

        return df_export

    def _buscar_ld_para_elemento(self, ld_resultado, nome_padrao, elemento):
        if not ld_resultado:
            return None

        if not isinstance(ld_resultado, dict):
            return None

        valor_padrao = ld_resultado.get(nome_padrao, {}).get(elemento, "")
        if valor_padrao not in ["", None]:
            return valor_padrao

        for chave, dados in ld_resultado.items():
            if chave == nome_padrao:
                continue

            if isinstance(dados, dict):
                valor_fallback = dados.get(elemento, "")
                if valor_fallback not in ["", None]:
                    return valor_fallback

        return None

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
        caminho_arquivo=None,
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
        print("[DEBUG] nome_padrao para exportação:", nome_padrao)
        print("[DEBUG] chaves_ld_resultado:", list(ld_resultado.keys()) if ld_resultado else [])

        # --- Aba "Dados" ---
        df_dados = self.aba_dados.montar(
            arquivos, areas_normalizadas, erros_normalizados, fatores_normalizacao
        )

        # --- Aba "Resultados" ---
        df_analise, elementos_ordenados, contagem_elementos = self.aba_resultados.montar(
            concentracoes, erros_propagados, unidade_padrao
        )

        # --- Aba "Concentrações" ---
        df_concentracoes = self.aba_concentracoes.montar(df_analise)

        #print("\n========== DF_CONCENTRACOES ==========")
        #print(df_concentracoes.to_string())

        #df_analise.to_excel("DEBUG_RESULTADOS.xlsx")
        #df_concentracoes.to_excel("DEBUG_CONCENTRACOES.xlsx")

<<<<<<< HEAD
=======
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
            elementos_ordenados = sorted(elementos_encontrados, key=lambda x: (x[0], x[1]))  # ordena por símbolo e energia)
            contagem_elementos = Counter(elemento for elemento, energia in elementos_ordenados)
            
            colunas = []
            for elemento, energia in elementos_ordenados:
                unidade = unidade_padrao.get(elemento, "")
                possui_duplicata = contagem_elementos[elemento] > 1
                nome_coluna = self.montar_titulo_coluna(elemento, energia, unidade, possui_duplicata)

                colunas.append((nome_coluna, "C"))
                colunas.append((nome_coluna, "Erro"))

            linhas = {}
            for nome_amostra, elementos in analise.items():
                linha = {}
                for elemento in elementos_ordenados:
                    unidade = unidade_padrao.get(elemento[0], "")
                    possui_duplicata = contagem_elementos[elemento[0]] > 1
                    nome_coluna = self.montar_titulo_coluna(elemento[0], elemento[1], unidade, possui_duplicata)
                                                      
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

                                    #nome_coluna = f"{elemento[0]} ({elemento[1]:.3f} keV)"

                                    linha[(nome_coluna, c_col)] = valor_str
                                    linha[(nome_coluna, e_col)] = erro_str

                                else:
                                    linha[(nome_coluna, c_col)] = valor_fmt
                                    linha[(nome_coluna, e_col)] = erro_fmt
                            else:
                                valor_fmt = round(valor_num)  # 👈 arredondamento simples
                                linha[(nome_coluna, c_col)] = valor_fmt
                                linha[(nome_coluna, e_col)] = ""

                        except Exception:
                            linha[(nome_coluna, c_col)] = valor
                            linha[(nome_coluna, e_col)] = erro

                linhas[nome_amostra] = linha

            df_analise = pd.DataFrame.from_dict(linhas, orient="index")
            df_analise = df_analise.reindex(columns=pd.MultiIndex.from_tuples(colunas))
            df_analise.index = list(linhas.keys())

            df_analise = df_analise.replace(r'^\s*$', '-', regex=True).fillna('-')

        else:
            df_analise = pd.DataFrame()
        
        # --- Nova aba: só concentrações (já formatadas) ---

        df_concentracoes = df_analise.xs("C", axis=1, level=1)
        df_concentracoes.columns.name = None

        df_concentracoes = df_concentracoes.replace(r'^\s*$', '-', regex=True).fillna('-')
        
>>>>>>> origin
        # Se o usuário não escolheu um local para salvar, salva em um diretório gravável pelo usuário
        if not caminho_arquivo:
            pasta_saida = ensure_directory(user_data_path("exports"))
            caminho_arquivo = os.path.join(pasta_saida, "amostras.xlsx")

        def _salvar_excel(path):

            df_dados_excel = self._normalizar_valores_para_excel(df_dados)
            df_concentracoes_excel = self._normalizar_valores_para_excel(df_concentracoes)
            df_analise_excel = self._normalizar_valores_para_excel(df_analise)

            with pd.ExcelWriter(
                path,
                engine="xlsxwriter",
            ) as writer:

                df_dados_excel.to_excel(writer, sheet_name="Dados", index=False, header=False)

                df_concentracoes_excel.to_excel(
                    writer,
                    sheet_name="Concentrações",
                    index=True,
                    index_label="Amostra"
                )

                df_analise_excel.to_excel(
                    writer,
                    sheet_name="Resultados",
                    index=True,
                    header=False,
                    startrow=2
                )

                worksheet = writer.sheets["Resultados"]

                # Cabeçalho linha 0
                worksheet.write(0, 0, "")

                # Cabeçalho linha 1
                worksheet.write(1, 0, "LD")

                # Cabeçalho linha 2
                worksheet.write(2, 0, "")

                col = 1

                for elemento, energia in elementos_ordenados:

                    unidade = unidade_padrao.get(elemento, "")
                    possui_duplicata = contagem_elementos[elemento] > 1
                    titulo = montar_titulo_coluna(elemento, energia, unidade, possui_duplicata)

                    # Linha 0 -> nome do elemento + unidade
                    worksheet.merge_range(
                        0,
                        col,
                        0,
                        col + 1,
                        titulo
                    )

                    # Busca LD
                    ld = "-"

                    if ld_resultado:
                        ld_bruto = self._buscar_ld_para_elemento(ld_resultado, nome_padrao, elemento)

                        if ld_bruto not in ["", None]:
                            ld = self.arredondamento.formatar_ld(ld_bruto)

                    # Linha 1 -> LD
                    worksheet.merge_range(
                        1,
                        col,
                        1,
                        col + 1,
                        ld
                    )

                    # Linha 2 -> C / Erro
                    worksheet.write(2, col, "C")
                    worksheet.write(2, col + 1, "Erro")

                    col += 2

        try:
            _salvar_excel(caminho_arquivo)
        except PermissionError:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta_saida = ensure_directory(user_data_path("exports"))
            caminho_arquivo = os.path.join(pasta_saida, f"amostras_{timestamp}.xlsx")
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
