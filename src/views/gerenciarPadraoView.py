import customtkinter as ctk
from PIL import Image
import json
from tkinter import messagebox

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Gerenciar_PadraoView(ctk.CTkFrame):
    def __init__(self, sidebar, frame, dynamic_frame, variaveis, padrao_view):
        super().__init__(sidebar)

        self.combobox_padroes = padrao_view
        
        self.variaveis = variaveis
        self.caminho_json = self.variaveis.path
        self.frame = frame
        self.dynamic_frame = dynamic_frame

        icone_gear = ctk.CTkImage(light_image=Image.open("imagens/icones/gear.png"), size=(20, 20))

        # Botão Gerenciar
        self.botao_gerenciar = ctk.CTkButton(
            #self.sidebar,
            self.frame,
            text="",
            image=icone_gear,
            width=40,
            height=30,
            corner_radius=8,
            font=("Arial Black", 12),
            fg_color="#213A57",
            #hover_color="#777777",
            command=self.janela_gerenciar
        )
        self.botao_gerenciar.pack(side="right", padx=(0, 20))

    def janela_gerenciar(self):

        # Carrega JSON do Variaveis
        try:
            # self.caminho_json **não é um caminho**, aqui tem erro (vou explicar abaixo)
            self.padroes = self.variaveis.padroes.copy()   
        except:
            self.padroes = {} # caso nao exista

        # cria a janela
        self.win = ctk.CTkToplevel()
        self.win.title("Gerenciar Padrões")
        self.win.geometry("1000x700")
        self.win.focus_force()
        self.win.grab_set()

        largura, altura = 1000, 700
        x = (self.win.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.win.winfo_screenheight() // 2) - (altura // 2)
        self.win.geometry(f"{largura}x{altura}+{x}+{y}")

        # ---------------------------
        #      LAYOUT PRINCIPAL
        # ---------------------------
        self.win.columnconfigure(0, weight=1)
        self.win.columnconfigure(1, weight=2)
        self.win.rowconfigure(0, weight=1)

        # LEFT SIDE – LISTA DE PADRÕES
        frame_lista = ctk.CTkFrame(self.win)
        frame_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame_lista.rowconfigure(1, weight=1)

        frame_lista.columnconfigure(0, weight=1)   # <-- centraliza
        frame_lista.rowconfigure(1, weight=1)

        ctk.CTkLabel(frame_lista, text="Padrões carregados", font=("Arial Black", 16)).grid(
            row=0, column=0, pady=10
        )

        self.lista_padroes = ctk.CTkTextbox(frame_lista, width=300)
        self.lista_padroes.grid(row=1, column=0, sticky="nsew", padx=5)

        # RIGHT SIDE – FORMULÁRIO PARA ADICIONAR
        frame_form = ctk.CTkFrame(self.win)
        frame_form.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Atualize os padrões", font=("Arial Black", 16)).pack(pady=10)

        bot_salvar = ctk.CTkButton(frame_form, text="Salvar Padrões", fg_color="#00992e",
                                   command=self.salvar_padroes)
        bot_salvar.pack(pady=20)

        # exibe lista inicial
        self.atualizar_lista_json()

    # ---------------------------
    #       ATUALIZAR LISTA
    # ---------------------------
    def atualizar_lista_json(self):
        self.lista_padroes.delete("1.0", "end")

        for padrao in self.padroes:
            self.lista_padroes.insert("end", f"{padrao['nome']}:\n")
            for elem, conc in padrao["elementos"].items():
                self.lista_padroes.insert("end", f"   {elem}: {conc}\n")
            self.lista_padroes.insert("end", "\n")

    # ---------------------------
    #       SALVAR JSON
    # ---------------------------
    def salvar_padroes(self):
        try:
            texto = self.lista_padroes.get("1.0", "end").strip()

            novos = []
            bloco = None

            # lista com símbolos válidos para detectar elementos
            simbolos_validos = {
                "Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn",
                "Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y",
                "Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I",
                "Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho",
                "Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl",
                "Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu"
            }

            for linha in texto.split("\n"):

                if not linha.strip():
                    continue

                # Se a linha tem ":" → pode ser padrão ou elemento
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    chave = chave.strip()

                    # É um elemento se estiver na lista de símbolos válidos
                    if chave in simbolos_validos and bloco is not None:
                        bloco["elementos"][chave] = float(valor.strip())
                        continue

                # Caso contrário → é o nome de um novo padrão
                nome = linha.replace(":", "").strip()
                bloco = {"nome": nome, "elementos": {}}
                novos.append(bloco)

            # Salvar JSON
            with open(self.caminho_json, "w", encoding="utf-8") as f:
                json.dump(novos, f, indent=4, ensure_ascii=False)

            self.variaveis.padroes = novos.copy()
            messagebox.showinfo("Sucesso", "Padrões atualizados!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar:\n{e}")       

        self.combobox_padroes.atualizar_lista(novos) #Atualiza a lista da combobox que mostra os padroes
