import customtkinter as ctk
from PIL import Image
from padroes import selecionar_arquivo_padrao, selecionar_arquivos_amostras, escolher_padrao, gerenciar_padroes
from calculos import calcular_concentracoes
from exportar import exportar_para_excel
from graficos import config_graficos

# Carregando ícone
icone_pasta = ctk.CTkImage(light_image=Image.open("imagens/icones/pasta.png"), size=(20, 20))
icone_file = ctk.CTkImage(light_image=Image.open("imagens/icones/file.png"), size=(20, 20))
icone_excel = ctk.CTkImage(light_image=Image.open("imagens/icones/excel.png"), size=(20, 20))
icone_remover = ctk.CTkImage(light_image=Image.open("imagens/icones/remover.png"), size=(20, 20))
icone_padrao = ctk.CTkImage(light_image=Image.open("imagens/icones/padrao.png"), size=(20, 20))
icone_calcular = ctk.CTkImage(light_image=Image.open("imagens/icones/calcular.png"), size=(20, 20))
icone_adicionar = ctk.CTkImage(light_image=Image.open("imagens/icones/adicionar.png"), size=(20, 20))


# Janela principal
janela = ctk.CTk(fg_color="#1E1E1E")
janela.title("Cálculo de Concentrações")
janela.attributes("-topmost", False)
largura = 647
altura = 750
x = (janela.winfo_screenwidth() // 2) - (largura // 2)
y = (janela.winfo_screenheight() // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{x}+{y}")

#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame central com margem
frame = ctk.CTkFrame(janela, corner_radius=20)
frame.pack(expand=True, fill="both", padx=40, pady=40)
frame.grid_columnconfigure(0, weight=1, uniform="colunas")
frame.grid_columnconfigure(1, weight=1, uniform="colunas")
frame.grid_rowconfigure(3, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame de cima dentro do frame central
frame_cima = ctk.CTkFrame(frame, fg_color="transparent", border_color="#56A4D8", border_width=2, corner_radius=20)
frame_cima.grid(row=0, column=0, columnspan=2, stick="ew", padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Título
titulo = ctk.CTkLabel(frame_cima, text="Seleção de Dados", font=("Arial Black", 24))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
# Faz as colunas ocuparem espaço proporcional
frame_cima.grid_columnconfigure(0, weight=1)
frame_cima.grid_columnconfigure(1, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à esquerda dentro do frame cima ----------  Seleção de padrão
texto_orientacao = ctk.CTkLabel(frame_cima, text="Selecione Amostra Padrão", font=("Arial Black", 18), wraplength=200)
texto_orientacao.grid(column=0, row=1, padx=10, pady=10, sticky="n")
botao_selecionar_padrao = ctk.CTkButton(frame_cima, text="Selecionar Arquivo", command=selecionar_arquivo_padrao, image=icone_file, compound="left")
botao_selecionar_padrao.grid(column=0, row=2, padx=10, pady=10, sticky="n")
texto_arquivo_padrao = ctk.CTkLabel(frame_cima, text="")
texto_arquivo_padrao.grid(column=0, row=3, padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à direita dentro do frame cima ----------  Seleção de amostras
texto_orientacao2 = ctk.CTkLabel(frame_cima, text="Selecione Dados para Calcular", font=("Arial Black", 18), wraplength=200)
texto_orientacao2.grid(column=1, row=1, padx=10, pady=10, sticky="n")
botao_selecionar_amostras = ctk.CTkButton(frame_cima, text="Selecionar Arquivos", command=selecionar_arquivos_amostras, image=icone_pasta, compound="left")
botao_selecionar_amostras.grid(column=1, row=2, padx=10, pady=10, sticky="n")
texto_arquivos_amostras = ctk.CTkLabel(frame_cima, text="")
texto_arquivos_amostras.grid(column=1, row=3, padx=10, pady=10, sticky="n")

# Frame de cima dentro do frame central
frame_meio = ctk.CTkFrame(frame, fg_color="transparent", border_color="#D87878", border_width=2, corner_radius=20)
frame_meio.grid(row=2, column=0, columnspan=2, stick="ew", padx=10, pady=10)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Título
titulo = ctk.CTkLabel(frame_meio, text="Controle dos Padrões", font=("Arial Black", 24))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
# Faz as colunas ocuparem espaço proporcional
frame_meio.grid_columnconfigure(0, weight=1)
frame_meio.grid_columnconfigure(1, weight=1)
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à esquerda dentro do frame meio ----------  Gerenciar padrões
texto_orientacao7 = ctk.CTkLabel(frame_meio, text="Adicione e Remova Padrões", font=("Arial Black", 18), wraplength=200)
texto_orientacao7.grid(column=0, row=1, padx=40, pady=10, columnspan=1, sticky="n")
botao_gerenciar_padrao = ctk.CTkButton(frame_meio, text="Gerenciar Padrões", command=gerenciar_padroes)
botao_gerenciar_padrao.grid(column=0, row=2, padx=40, pady=10, sticky="n")
#_____________________________________________________________________________________________________________________________________________________________________________________
# Textos à direita dentro do frame meio ----------  Escolha de padrão
texto_orientacao4 = ctk.CTkLabel(frame_meio, text="Utilizar o Padrão de:", font=("Arial Black", 18), wraplength=200)
texto_orientacao4.grid(column=1, row=1, padx=40, pady=10, sticky="n")
botao_escolher_padrao = ctk.CTkButton(frame_meio, text="Escolher Padrão", command=escolher_padrao, image=icone_padrao, compound="left")
botao_escolher_padrao.grid(column=1, row=2, padx=40, pady=10, sticky="n")
texto_padraoselecionado = ctk.CTkLabel(frame_meio, text="Padrão escolhido: Nenhum")
texto_padraoselecionado.grid(column=1, row=3, padx=40, pady=10, sticky="n")

#frame inferior esquerdo dentro do frame central
frame_inferior_esquerda = ctk.CTkScrollableFrame(frame, fg_color="transparent", border_color="#DFD36B", border_width=2, corner_radius=20)
frame_inferior_esquerda.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
# Título
#titulo = ctk.CTkLabel(frame_inferior_esquerda, text="Opções Extras", font=("Arial Black", 18))
#titulo.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
# Faz as colunas ocuparem espaço proporcional
frame_inferior_esquerda.grid_columnconfigure(0, weight=1)

#Coisas dentro do frame inferior esquerdo
botao_config_graficos = ctk.CTkButton(frame_inferior_esquerda, text="Configurar Gráficos", command=config_graficos)
botao_config_graficos.grid(column=0, row=1, padx=10, pady=10)


#_____________________________________________________________________________________________________________________________________________________________________________________
# Frame inferior dentro do frame central
frame_inferior_direita = ctk.CTkFrame(frame, fg_color="transparent", border_color="#78D890", border_width=2, corner_radius=20)
frame_inferior_direita.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
# Título
titulo = ctk.CTkLabel(frame_inferior_direita, text="Calcular e Exportar", font=("Arial Black", 18))
titulo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
# Faz as colunas ocuparem espaço proporcional
frame_inferior_direita.grid_columnconfigure(0, weight=1)
#botão dentro do frame inferior direito
botao_calcular = ctk.CTkButton(frame_inferior_direita, text="Calcular Concentrações", state="disabled", command=calcular_concentracoes, image=icone_calcular, compound="left")
botao_calcular.grid(column=0, row=1, padx=10, pady=10)

# Botão de exportar dentro do frame inferior direito
botao_exportar = ctk.CTkButton(frame_inferior_direita, text="Exportar para Excel", state="disabled", command=exportar_para_excel, image=icone_excel, compound="left")
botao_exportar.grid(column=0, row=2, padx=10, pady=10)