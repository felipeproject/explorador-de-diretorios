import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import json

# Função para carregar as configurações do arquivo JSON
def carregar_configuracoes():
    arquivo_config = 'config.json'
    
    if not os.path.exists(arquivo_config):
        return {
            "pastas_ignoradas": ["temp", "node_modules", ".git"],
            "extensoes_ignoradas": [".git", ".hj"]
        }
    
    with open(arquivo_config, 'r') as f:
        return json.load(f)

# Função para salvar as configurações no arquivo JSON
def salvar_configuracoes(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Carregar configurações iniciais
config = carregar_configuracoes()

def listar_diretorio_em_arvore(caminho, nivel=0, lista_itens=None):
    """
    Função recursiva para listar o conteúdo de um diretório em formato de árvore,
    ignorando pastas e arquivos especificados. Armazena os itens a serem exibidos
    em uma lista para exibição na UI.
    """
    try:
        # Listando os itens no diretório
        itens = os.listdir(caminho)
        for item in itens:
            caminho_item = os.path.join(caminho, item)

            # Ignorar se for uma pasta ou arquivo com nome/extension ignorados
            if any(item.lower() == ignorada for ignorada in config["pastas_ignoradas"]):
                continue
            if any(item.lower().endswith(ext) for ext in config["extensoes_ignoradas"]):
                continue

            # Adiciona o item à lista de itens para exibição
            indentacao = '│   ' * nivel
            simbolo = '├── ' if nivel < len(os.listdir(caminho)) - 1 else '└── '
            lista_itens.append(f"{indentacao}{simbolo}{item}")
            
            # Se for um diretório, recursivamente listamos o conteúdo
            if os.path.isdir(caminho_item):
                listar_diretorio_em_arvore(caminho_item, nivel + 1, lista_itens)
    except PermissionError:
        lista_itens.append('  ' * nivel + '|-- [Acesso negado]')
    except FileNotFoundError:
        lista_itens.append('  ' * nivel + '|-- [Diretório não encontrado]')

def escolher_diretorio():
    """
    Função para abrir uma janela de diálogo e selecionar um diretório.
    """
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    diretorio = filedialog.askdirectory(title="Escolha um diretório")
    return diretorio

def copiar_para_area_transferencia(root, todos_itens):
    """
    Função para copiar todos os itens para a área de transferência.
    """
    root.clipboard_clear()  # Limpa a área de transferência
    root.clipboard_append("\n".join(todos_itens))  # Adiciona todos os itens à área de transferência
    messagebox.showinfo("Sucesso", "Todos os itens copiados para a área de transferência!")

def criar_interface(diretorio):
    """
    Cria a interface gráfica para exibir a estrutura de arquivos e pastas.
    """
    def atualizar_configuracoes():
        """
        Função para recarregar as configurações e atualizar a interface.
        """
        global config
        config = carregar_configuracoes()
        lista_itens = []
        listar_diretorio_em_arvore(diretorio, lista_itens=lista_itens)

        # Limpa a caixa de texto e insere a lista atualizada
        text_widget.delete(1.0, tk.END)
        for item in lista_itens:
            text_widget.insert(tk.END, item + "\n")

    def adicionar_pastas_extensoes():
        """
        Função que abre um pop-up para adicionar pastas e extensões ignoradas.
        """
        def salvar_pastas_extensoes():
            """
            Função para salvar as pastas e extensões adicionadas pelo usuário.
            """
            # Obter o conteúdo das caixas de texto
            pastas = pasta_text.get("1.0", tk.END).strip().splitlines()
            extensoes = extensao_text.get("1.0", tk.END).strip().splitlines()

            # Atualizar pastas e extensões ignoradas
            config["pastas_ignoradas"] = [pasta.strip() for pasta in pastas if pasta.strip()]
            config["extensoes_ignoradas"] = [extensao.strip() for extensao in extensoes if extensao.strip()]

            # Salvar as configurações no arquivo JSON
            salvar_configuracoes(config)

            # Fechar o pop-up
            popup.destroy()

            # Atualizar a interface principal
            atualizar_configuracoes()

            messagebox.showinfo("Sucesso", "Pastas e extensões atualizadas com sucesso!")

        # Criar a janela pop-up
        popup = tk.Toplevel(root)
        popup.title("Adicionar/Editar Pastas e Extensões Ignoradas")

        # Criar os rótulos e caixas de texto para pastas e extensões
        tk.Label(popup, text="Pastas Ignoradas (uma por linha):").pack(padx=10, pady=5)
        pasta_text = tk.Text(popup, height=10, width=40)
        pasta_text.pack(padx=10, pady=5)
        
        # Preencher a caixa de texto com as pastas ignoradas atuais
        pasta_text.insert(tk.END, "\n".join(config["pastas_ignoradas"]) + "\n")

        tk.Label(popup, text="Extensões Ignoradas (uma por linha):").pack(padx=10, pady=5)
        extensao_text = tk.Text(popup, height=10, width=40)
        extensao_text.pack(padx=10, pady=5)

        # Preencher a caixa de texto com as extensões ignoradas atuais
        extensao_text.insert(tk.END, "\n".join(config["extensoes_ignoradas"]) + "\n")

        # Botão para salvar as entradas
        btn_salvar = tk.Button(popup, text="Salvar", command=salvar_pastas_extensoes)
        btn_salvar.pack(pady=10)

    root = tk.Tk()
    root.title("Explorador de Diretórios")

    # Lista de itens a serem exibidos
    lista_itens = []
    
    # Chama a função para listar o diretório
    listar_diretorio_em_arvore(diretorio, lista_itens=lista_itens)

    # Criação do widget de Text para exibir os itens
    text_widget = tk.Text(root, height=20, width=80)
    text_widget.pack(padx=10, pady=10)
    
    # Preenche a Text com os itens encontrados
    for item in lista_itens:
        text_widget.insert(tk.END, item + "\n")

    # Função para quando o usuário clicar no botão de copiar
    def on_copiar():
        if lista_itens:
            # Chama a função para copiar todos os itens
            copiar_para_area_transferencia(root, lista_itens)
        else:
            messagebox.showwarning("Aviso", "Nenhum item encontrado para copiar.")

    # Botão para copiar todos os itens
    btn_copiar = tk.Button(root, text="Copiar todos os itens para a área de transferência", command=on_copiar)
    btn_copiar.pack(pady=5)

    # Botão para recarregar as configurações
    btn_recarregar = tk.Button(root, text="Recarregar Configurações", command=atualizar_configuracoes)
    btn_recarregar.pack(pady=5)

    # Botão para abrir o pop-up de adicionar pastas e extensões
    btn_adicionar = tk.Button(root, text="Adicionar/Editar Pastas/Extensões Ignoradas", command=adicionar_pastas_extensoes)
    btn_adicionar.pack(pady=5)

    # Inicia o loop da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    diretorio = escolher_diretorio()  # Pede ao usuário escolher um diretório
    if diretorio:
        # Inicia a interface gráfica para o diretório escolhido
        criar_interface(diretorio)
    else:
        print("Nenhum diretório foi selecionado.")
