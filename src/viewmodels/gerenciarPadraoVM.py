from views.gerenciarPadraoView import Gerenciar_PadraoView

class Gerenciar_PadraoVM:
    def __init__(self, dynamic_frame, sidebar, callback_voltar_inicio, frame):
        self.dynamic_frame = dynamic_frame
        self.sidebar = sidebar
        self.callback_voltar_inicio = callback_voltar_inicio
        self.gerenciar_view = Gerenciar_PadraoView(self.sidebar, frame, dynamic_frame)
        self.frame = frame

        self.gerenciar_frame = None
        self.gerenciar_visible = False

    def botao_gerenciar(self):
        # Cria e exibe o painel de gerenciamento
        self.gerenciar_view.botao_gerenciar.pack(pady=5)
        #self.gerenciar_view.botao_gerenciar.grid(row=0, column=1, sticky="w", padx=10)
        self.gerenciar_view.botao_gerenciar.configure(command=self.toggle_gerenciar)
        
    # -------------------------------------------
    # Toggle do painel "Gerenciar Padrões"
    # -------------------------------------------
    def toggle_gerenciar(self):
        if self.gerenciar_visible:
            self._hide_gerenciar()
        else:
            self._show_gerenciador()

    def _show_gerenciador(self):
        """Abre o painel de gerenciamento de padrões na área principal"""
        #self.gerenciar_view.texto_gerenciar.pack(side="right", padx=(0, 20))
        # Limpa o conteúdo atual da área principal
        self.gerenciar_visible = True        
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def _hide_gerenciar(self):
        if self.gerenciar_frame:
            self.gerenciar_frame.destroy()
            self.gerenciar_frame = None
        self.gerenciar_visible = False
        # Volta para a tela principal
        self.callback_voltar_inicio()
