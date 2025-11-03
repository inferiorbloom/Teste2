import os
import json

class PadraoModel:
    def __init__(self):
        self.c_padrao = {}
'''
    def arquivos(self, lista_arquivo_padrao):
        """
        Recebe a lista de arquivos de padrão (geralmente um único arquivo .txt),
        e tenta carregar as concentrações do arquivo JSON de padrões.
        """
        # Garante que há pelo menos um arquivo selecionado
        if not lista_arquivo_padrao or not isinstance(lista_arquivo_padrao, list):
            print("Nenhum arquivo de padrão selecionado ou formato inválido.")
            return {}

        # Extrai o nome do arquivo padrão selecionado
        padrao_escolhido = os.path.basename(lista_arquivo_padrao[0])
        
        # Caminho do JSON de padrões
        path = r'padroes/padroes.json'
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                padroes = json.load(f)
                print(padroes)
                # Busca o padrão dentro do dicionário
                self.c_padrao = padroes.get(padrao_escolhido, {})
                print('aaaaaaaaaaaaaaaaaaaaa')
        else:
            print("Arquivo de padrões JSON não encontrado.")
            self.c_padrao = {}

        return self.c_padrao 
'''