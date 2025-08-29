from tkinter.filedialog import askopenfilename, askopenfilenames

#__________________________________________________________________________________________________________________
#importações dos txt do winxas
arquivo_padrao = askopenfilename(title="Selecione o arquivo.txt que deseja utilizar como PADRÃO!", filetypes=[("Arquivos de texto", "*.txt")])
arquivos = askopenfilenames(title="Selecione os seus dados.", filetypes=[("Arquivos de texto", "*.txt")])
#_____________________________________________________________________________________________________________________
c_padrao = {"Ca": 2022, "Fe":137, "Cu": 12.8, "K": 17762, "Mg": 2061, "Mn": 32.6, "P":5250, "Zn": 35.9}
area_padrao = {}    #dicionário onde serão armazenados as áreas do documento que você escolher como padrão
padrao_elemento = {}    #banco de dados de padrão, ainda não finalizado
elementos = {
    12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar",
    19: "K", 20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn",
    26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 31: "Ga", 32: "Ge",
    33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",
    40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd",
    47: "Ag", 48: "Cd", 49: "In", 50: "Sn", 51: "Sb", 52: "Te", 53: "I",
    54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho",
    68: "Er", 69: "Tm", 70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W",
    75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg", 81: "Tl",
    82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra",
    89: "Ac", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu"
}
#____________________________________________________________________________________________________________________
#documentos é um dicionario que armazena dicionarios, isto é: Documentos[0] = "documento1": bloco de notas
documentos = {}
concentracoes = {}    #dicionário onde serão armazenados as concentrações

for i, arquivo in enumerate(arquivos, start=1):
    #armazena caminho no dicionário documentos
    documentos[f"documento{i}"] = {"caminho": arquivo}

    #extrai nome da amostra para usar no dicionário de concentrações
    nome_amostra = arquivo.split("/")[-1].replace(".txt", "")
    concentracoes[f"concentracao{i}"] = {nome_amostra: {}}


#_____________________________________________________________________________________________________________________

#aqui, ele pega o conteudo que vai ser o documento de texto pulando as 5 linhas iniciais e o lê linha por linha, tirando espaços e formatando, basicamente
for doc in documentos.values():  # doc é o dicionário interno
    with open(doc["caminho"], "r", encoding="utf-8") as f:
        conteudo = f.readlines()[5:]
    # Cada linha vira uma lista de floats
    doc["linhas"] = [ [float(x.strip()) for x in linha.split(",")] for linha in conteudo ]

#__________________________________________________________________________
#import do padrão
with open(arquivo_padrao, "r") as p:
    for line in p:
        line = line.strip()
        if line and line[0].isdigit():
            valores = [v.strip() for v in line.split(",")]
            try:
                z = int(valores[0])
                area = float(valores[2])
                elemento = elementos.get(z, "-")
                area_padrao[elemento] = area
                
            except:
                continue
#_________________________________________________________________________________________________________________________
# NORMALIZAÇÃO
# pega a área de Ar (18) para normalizar todas as áreas
area_ar_padrao = area_padrao.get("Ar", None)

#dicionario para guardar os fatores de normalização
fatores_normalizacao = {}

#calcula o fator para cada amostra (baseado no ar)
for i, (doc_nome, info) in enumerate(documentos.items(), start=1):
    nome_amostra = list(concentracoes[f"concentracao{i}"].keys())[0]
    
    # Encontra a área de Ar (18) na amostra
    area_ar_amostra = None
    for linha in info["linhas"]:
        if linha[0] == 18:  # número atômico do Ar
            area_ar_amostra = linha[2]  # área líquida medida para Ar
            break
    
    if area_ar_amostra and area_ar_padrao:
        fatores_normalizacao[nome_amostra] = area_ar_padrao / area_ar_amostra
        
        # Normaliza todas as áreas na amostra
        #for linha in info["linhas"]:
           # linha[2] *= fator  # normaliza a área líquida medida



#import dos dados + cálculo
for i, (doc_nome, info) in enumerate(documentos.items(), start=1):
    nome_amostra = list(concentracoes[f"concentracao{i}"].keys())[0]
    fator = fatores_normalizacao.get(nome_amostra, 1)  # usa 1 se não houver fator (sem normalização)
    
    for linha in info["linhas"]:
        num = linha[0]           # número do elemento
        area_net = linha[2]      # área líquida medida
        elemento = elementos[num]
        
        #aplica normalização na área antes do cálculo
        area_net_normalizada = area_net * fator

        # Calcula concentração apenas se o elemento estiver nos padrões
        if elemento in c_padrao and elemento in area_padrao:
            conc = (area_net_normalizada * c_padrao[elemento]) / area_padrao[elemento]
            concentracoes[f"concentracao{i}"][nome_amostra][elemento] = conc




#_________________________________________________________________________________________________________________________
# Exemplo de print final
for chave, dados in concentracoes.items():
    print(f"--- {chave} ---")
    for amostra, valores in dados.items():
        print(f"{amostra}: {valores}")
        pass

  







    
        
 
            
