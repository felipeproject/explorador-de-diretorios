# File Tree Viewer

O **File Tree Viewer** é uma ferramenta simples para visualizar a estrutura de diretórios e arquivos de uma pasta no formato de árvore. Além disso, permite personalizar pastas e extensões a serem ignoradas, tudo por meio de uma interface gráfica em Tkinter. As configurações são salvas em um arquivo `config.json`, garantindo persistência entre as execuções.

## Funcionalidades

- **Visualização de Diretórios**: Exibe a estrutura de arquivos e pastas de um diretório de forma hierárquica.
- **Ignorar Pastas e Extensões**: Personalize as pastas e extensões a serem ignoradas ao listar os arquivos.
- **Configuração Persistente**: As configurações (pastas e extensões ignoradas) são salvas em um arquivo `config.json`.
- **Interface Gráfica (GUI)**: Interface amigável criada com Tkinter para facilitar a navegação e personalização.
- **Cópia para a Área de Transferência**: Copie todos os itens listados na árvore de diretórios para a área de transferência.

## Instalação

Para usar o **File Tree Viewer**, é necessário ter o Python 3 e o pacote `tkinter` instalado. Para garantir que tudo esteja pronto, siga as instruções abaixo:

1. **Instale o Tkinter** (caso não tenha instalado):

    ```bash
    pip install tk
    ```

2. **Clone o Repositório**:

    ```bash
    git clone https://github.com/seu-usuario/file_tree_viewer.git
    cd file_tree_viewer
    ```

## Como Usar

1. **Escolha um Diretório**: Ao executar o programa, será aberta uma janela para você selecionar o diretório que deseja visualizar.
2. **Visualização da Árvore de Diretórios**: A estrutura do diretório será exibida na interface gráfica, com arquivos e pastas listados em forma de árvore.
3. **Configurações de Ignoração**: Adicione ou remova pastas e extensões ignoradas na interface gráfica. Essas configurações são armazenadas no arquivo `config.json`.
4. **Cópia para a Área de Transferência**: Clique no botão **"Copiar todos os itens para a área de transferência"** para copiar a lista de itens exibidos na árvore.
5. **Recarregar Configurações**: Se você modificar o arquivo `config.json` diretamente, pode recarregar as configurações pela interface gráfica.

## Estrutura do Arquivo JSON

O arquivo `config.json` armazena as configurações do programa. Ele possui dois campos principais:

- **pastas_ignoradas**: Lista de pastas a serem ignoradas.
- **extensoes_ignoradas**: Lista de extensões de arquivos a serem ignoradas.

Exemplo de arquivo `config.json`:

```json
{
    "pastas_ignoradas": ["temp", "node_modules", ".git"],
    "extensoes_ignoradas": [".git", ".env"]
}
