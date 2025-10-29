import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd

# Configuração inicial da aparência
ctk.set_appearance_mode("dark")  # "light" também é possível
ctk.set_default_color_theme("blue")


class ConcentrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧪 Calculadora de Concentrações")
        self.geometry("1200x700")
        self.resizable(True, True)

        # --- VARIÁVEIS ---
        self.data_file = None
        self.standard_file = None
        self.standards = []

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="Menu", font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(self.sidebar, text="📂 Carregar Dados", command=self.load_data).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self.sidebar, text="🧾 Selecionar Padrão", command=self.load_standard).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self.sidebar, text="⚙️ Gerenciar Padrões", command=self.open_standard_manager).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self.sidebar, text="🧮 Calcular Concentração", fg_color="#4CAF50", command=self.calculate).pack(pady=20, fill="x", padx=20)
        ctk.CTkButton(self.sidebar, text="Sair", fg_color="red", command=self.quit).pack(side="bottom", pady=20, fill="x", padx=20)

        # --- MAIN AREA ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Calculadora de Concentrações", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # Informações carregadas
        self.info_label = ctk.CTkLabel(self.main_frame, text="Nenhum arquivo carregado ainda.", font=("Arial", 16))
        self.info_label.pack(pady=10)

        # Área dos resultados
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True, pady=10)

        self.result_label = ctk.CTkLabel(self.result_frame, text="Resultado: -", font=("Arial", 18))
        self.result_label.pack(pady=30)

    # --- FUNÇÕES PRINCIPAIS ---

    def load_data(self):
        """Seleciona arquivo de dados experimentais"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.data_file = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
                self.info_label.configure(text=f"✅ Dados carregados: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar dados:\n{e}")

    def load_standard(self):
        """Seleciona arquivo com dados de padrão"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.standard_file = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
                messagebox.showinfo("Sucesso", f"Padrão carregado: {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar padrão:\n{e}")

    def open_standard_manager(self):
        """Janela para adicionar, remover e selecionar padrões"""
        manager = ctk.CTkToplevel(self)
        manager.title("Gerenciar Padrões")
        manager.geometry("500x500")

        ctk.CTkLabel(manager, text="Gerenciador de Padrões", font=("Arial", 20, "bold")).pack(pady=20)

        # Lista de padrões
        self.standard_listbox = ctk.CTkTextbox(manager, width=400, height=200)
        self.standard_listbox.pack(pady=10)
        self.refresh_standard_list()

        # Botões
        btn_frame = ctk.CTkFrame(manager)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="➕ Adicionar", command=self.add_standard).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="➖ Remover", command=self.remove_standard).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar", command=self.refresh_standard_list).grid(row=0, column=2, padx=10)

    def add_standard(self):
        """Adiciona um padrão à lista"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            self.standards.append(file_path)
            self.refresh_standard_list()

    def remove_standard(self):
        """Remove o último padrão"""
        if self.standards:
            removed = self.standards.pop()
            messagebox.showinfo("Removido", f"Padrão removido: {removed.split('/')[-1]}")
            self.refresh_standard_list()
        else:
            messagebox.showwarning("Aviso", "Nenhum padrão para remover!")

    def refresh_standard_list(self):
        """Atualiza a listagem de padrões"""
        if hasattr(self, "standard_listbox"):
            self.standard_listbox.delete("1.0", "end")
            if self.standards:
                for i, path in enumerate(self.standards):
                    self.standard_listbox.insert("end", f"{i+1}. {path.split('/')[-1]}\n")
            else:
                self.standard_listbox.insert("end", "Nenhum padrão carregado.\n")

    def calculate(self):
        """Simulação de cálculo de concentração"""
        if self.data_file is None or not self.standards:
            messagebox.showwarning("Aviso", "Carregue dados e padrões antes de calcular!")
            return
        # Aqui você pode implementar o cálculo real
        result_value = 3.42  # exemplo fictício
        self.result_label.configure(text=f"Resultado: {result_value:.2f} mol/L")
        messagebox.showinfo("Cálculo Concluído", "Cálculo de concentração realizado com sucesso!")


if __name__ == "__main__":
    app = ConcentrationApp()
    app.mainloop()
