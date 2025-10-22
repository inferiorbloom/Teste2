import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui_config import janela
from padroes import arquivos
from calculos import concentracoes
import numpy as np

def config_graficos():
    config_graficos = ctk.CTkToplevel(janela)
    config_graficos.title("Configurar Gráficos")
    config_graficos.transient(janela)
    config_graficos.grab_set()

    # Centraliza na tela
    largura, altura = 1000, 800
    x = (config_graficos.winfo_screenwidth() // 2) - (largura // 2)
    y = (config_graficos.winfo_screenheight() // 2) - (altura // 2)
    config_graficos.geometry(f"{largura}x{altura}+{x}+{y}")

    # --- seleção da amostra ---
    selecione_amostra = ctk.CTkComboBox(
        config_graficos,
        values=[os.path.basename(arquivo).replace(".txt", "") for arquivo in arquivos]
    )
    selecione_amostra.grid(column=0, row=0, padx=10, pady=10)

    # --- slider ---
    slider_valor = ctk.CTkSlider(config_graficos, from_=1, to=20, number_of_steps=19)
    slider_valor.set(5)  # valor inicial
    slider_valor.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

    label_slider = ctk.CTkLabel(config_graficos, text="Traço: 5%")
    label_slider.grid(column=2, row=0, padx=10, pady=10)

    # --- frame para os gráficos ---
    frame_graficos = ctk.CTkFrame(config_graficos)
    frame_graficos.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="nsew")
    frame_graficos.grid_rowconfigure(0, weight=1)
    frame_graficos.grid_columnconfigure((0,1), weight=1)

    canvas_maioritario = None
    canvas_traco = None

    def atualizar_graficos(*args):
        nonlocal canvas_maioritario, canvas_traco
        amostra_selecionada = selecione_amostra.get()
        if not amostra_selecionada:
            return

        # --- busca a concentração ---
        concs = None
        for dados in concentracoes.values():
            if amostra_selecionada in dados:
                concs = dados[amostra_selecionada]
                break
        if concs is None:
            return

        elementos = list(concs.keys())
        valores = list(concs.values())

        # --- define limite do traço ---
        percentual = slider_valor.get()
        label_slider.configure(text=f"Traço: {percentual:.0f}%")
        soma_total = sum(valores)
        limite_traco = soma_total * (percentual / 100)

        # separa elementos maiores e traços
        elementos_traco = []
        valores_traco = []
        elementos_majoritarios = []
        valores_majoritarios = []

        soma_traco = 0
        for e, v in sorted(zip(elementos, valores), key=lambda x: x[1]):
            if soma_traco + v <= limite_traco:
                elementos_traco.append(e)
                valores_traco.append(v)
                soma_traco += v
            else:
                elementos_majoritarios.append(e)
                valores_majoritarios.append(v)

        # --- gráfico majoritário ---
        if canvas_maioritario:
            canvas_maioritario.get_tk_widget().destroy()
        fig1, ax1 = plt.subplots(figsize=(4, 4))

        ax1.pie(valores_majoritarios + [soma_traco],
                labels=elementos_majoritarios + ["Traço"],
                autopct='%1.1f%%', startangle=140)
        ax1.set_title(f"Gráfico Majoritário - {amostra_selecionada}")
        canvas_maioritario = FigureCanvasTkAgg(fig1, master=frame_graficos)
        canvas_maioritario.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # --- gráfico traço ---
        if canvas_traco:
            canvas_traco.get_tk_widget().destroy()
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        if valores_traco:
            ax2.pie(valores_traco, labels=elementos_traco, autopct='%1.1f%%', startangle=140)
        ax2.set_title(f"Gráfico Traço - até {percentual:.0f}%")
        canvas_traco = FigureCanvasTkAgg(fig2, master=frame_graficos)
        canvas_traco.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    # botao para mostrar
    botao_mostrar_grafico = ctk.CTkButton(config_graficos, text="Mostrar Gráficos", command=atualizar_graficos)
    botao_mostrar_grafico.grid(column=0, row=2, padx=10, pady=10)

    # vincula slider
    slider_valor.configure(command=lambda val: atualizar_graficos())