import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Definir pastas e extensões a serem ignoradas
PASTAS_IGNORADAS = {'temp', '.git'}
EXTENSOES_IGNORADAS = {'.git', '.hj'}

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
            if any(item.lower() == ignorada for ignorada in PASTAS_IGNORADAS):
                continue
            if any(item.lower().endswith(ext) for ext in EXTENSOES_IGNORADAS):
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

    # Inicia o loop da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    diretorio = escolher_diretorio()  # Pede ao usuário escolher um diretório
    if diretorio:
        # Inicia a interface gráfica para o diretório escolhido
        criar_interface(diretorio)
    else:
        print("Nenhum diretório foi selecionado.")
