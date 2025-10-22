import customtkinter as ctk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ConcentrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧪 Calculadora e Gráficos de Concentrações")
        self.geometry("1300x750")
        self.resizable(False, False)

        # --- VARIÁVEIS ---
        self.data_file = None
        self.standards = []
        self.graph_data = None

        # --- ABA PRINCIPAL COM GUIA ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Aba 1: Cálculo de concentração
        self.tab_calc = self.tabview.add("🔬 Cálculo de Concentrações")
        self.setup_calculation_tab(self.tab_calc)

        # Aba 2: Gráficos de Pizza
        self.tab_graph = self.tabview.add("📊 Gráficos de Pizza")
        self.setup_graph_tab(self.tab_graph)

    # ================================================================
    # 🧮 ABA DE CÁLCULO
    # ================================================================
    def setup_calculation_tab(self, parent):
        """Cria interface da aba de cálculo de concentração"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(frame, text="Cálculo de Concentrações", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Botões principais
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="📂 Carregar Dados", command=self.load_data).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="➕ Adicionar Padrão", command=self.add_standard).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="➖ Remover Padrão", command=self.remove_standard).grid(row=0, column=2, padx=10)
        ctk.CTkButton(btn_frame, text="🧮 Calcular", fg_color="#4CAF50", command=self.calculate).grid(row=0, column=3, padx=10)

        self.info_label = ctk.CTkLabel(frame, text="Nenhum arquivo carregado.", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.result_label = ctk.CTkLabel(frame, text="Resultado: -", font=("Arial", 18, "bold"))
        self.result_label.pack(pady=30)

    def load_data(self):
        """Carregar arquivo de dados"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.data_file = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
                self.info_label.configure(text=f"✅ Dados carregados: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar dados:\n{e}")

    def add_standard(self):
        """Adicionar padrão"""
        file_path = filedialog.askopenfilename(filetypes=[("txt", "*.txt"), ("Excel Files", "*.xlsx")])
        if file_path:
            self.standards.append(file_path)
            messagebox.showinfo("Padrão Adicionado", f"{file_path.split('/')[-1]} adicionado!")

    def remove_standard(self):
        """Remover padrão"""
        if self.standards:
            removed = self.standards.pop()
            messagebox.showinfo("Removido", f"Padrão removido: {removed.split('/')[-1]}")
        else:
            messagebox.showwarning("Aviso", "Nenhum padrão para remover!")

    def calculate(self):
        """Simulação de cálculo"""
        if self.data_file is None:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro!")
            return
        result = 3.42  # Valor fictício
        self.result_label.configure(text=f"Resultado: {result:.2f} mol/L")
        messagebox.showinfo("Cálculo concluído", "Cálculo de concentração realizado com sucesso!")

    # ================================================================
    # 📊 ABA DE GRÁFICO DE PIZZA
    # ================================================================
    def setup_graph_tab(self, parent):
        """Cria interface para gráficos de pizza"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(frame, text="Gerador de Gráficos de Pizza", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Área de controle
        control_frame = ctk.CTkFrame(frame)
        control_frame.pack(pady=10)

        ctk.CTkButton(control_frame, text="📂 Carregar Dados", command=self.load_graph_data).grid(row=0, column=0, padx=10)

        ctk.CTkLabel(control_frame, text="Coluna de Rótulos:").grid(row=1, column=0, padx=5, pady=5)
        self.label_col_entry = ctk.CTkEntry(control_frame, width=150)
        self.label_col_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(control_frame, text="Coluna de Valores:").grid(row=2, column=0, padx=5, pady=5)
        self.value_col_entry = ctk.CTkEntry(control_frame, width=150)
        self.value_col_entry.grid(row=2, column=1, padx=5, pady=5)

        # Controle de traço
        ctk.CTkLabel(control_frame, text="Estilo de Borda:").grid(row=3, column=0, padx=5, pady=5)
        self.edge_style = ctk.CTkOptionMenu(control_frame, values=["Nenhum", "Preto", "Branco", "Cinza"])
        self.edge_style.set("Preto")
        self.edge_style.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkButton(control_frame, text="🎨 Gerar Gráfico", fg_color="#3b82f6", command=self.plot_pie_chart).grid(row=4, column=0, columnspan=2, pady=20)

        # Área do gráfico
        self.graph_frame = ctk.CTkFrame(frame)
        self.graph_frame.pack(fill="both", expand=True, pady=10)

    def load_graph_data(self):
        """Carregar dados para o gráfico"""
        file_path = filedialog.askopenfilename(filetypes=[("txt", "*.txt"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.graph_data = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
                messagebox.showinfo("Sucesso", f"Dados carregados: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar dados:\n{e}")

    def plot_pie_chart(self):
        """Gera gráfico de pizza com base nos dados"""
        if self.graph_data is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo de dados primeiro!")
            return

        label_col = self.label_col_entry.get()
        value_col = self.value_col_entry.get()

        if label_col not in self.graph_data.columns or value_col not in self.graph_data.columns:
            messagebox.showerror("Erro", "Colunas inválidas! Verifique os nomes e tente novamente.")
            return

        labels = self.graph_data[label_col]
        values = self.graph_data[value_col]

        edge_color = {
            "Nenhum": None,
            "Preto": "black",
            "Branco": "white",
            "Cinza": "gray"
        }[self.edge_style.get()]

        # Criar gráfico
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90,
               wedgeprops={'edgecolor': edge_color, 'linewidth': 1.5})

        ax.axis("equal")
        ax.set_title("Distribuição de Dados", fontsize=14)

        # Limpar gráfico anterior
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Inserir gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    app = ConcentrationApp()
    app.mainloop()
