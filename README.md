# Sistema de Reconhecimento Facial para Dispositivos Comuns: Prova de Conceito

Este projeto implementa um sistema de reconhecimento facial utilizando bibliotecas de visão computacional e inteligência artificial. Desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC), seu objetivo principal é atuar como uma **prova de conceito para a viabilidade do reconhecimento facial em tempo real utilizando hardware acessível e tecnologias presentes em dispositivos comuns**. O sistema demonstra o potencial da biometria facial como uma solução de **baixo custo** para identificação e autenticação, sem a necessidade de equipamentos especializados.

### Exemplos de Identificação

A seguir, são apresentadas imagens que ilustram a capacidade de identificação do sistema:

![Identificação da pessoa Rani](Rani_1.jpg)
*Figura 1: Exemplo de identificação facial para 'Rani'.*

![Identificação da pessoa Mantovani](Mantovani_1.jpg)
*Figura 2: Exemplo de identificação facial para 'Mantovani'.*

---

## 1. Requisitos do Sistema

Para rodar este projeto, você precisará de:

* **Sistema Operacional:** Windows 10 ou 11 (64 bits).
* **Python:** Versão **3.8.x** (neste projeto foi utilizada a versão 3.8.10).
* **Git:** Para clonar o repositório.
* **Webcam:** Um dispositivo de câmera funcional.
* **Espaço em Disco:** Mínimo de 5 GB livres.
* **Conexão com a Internet:** Necessária para baixar as dependências.

---

## 2. Configuração e Instalação

Siga estes passos para configurar e instalar o ambiente necessário.

### 2.1. Preparação Inicial

1.  **Instale o Python 3.8.10:**
    Baixe e instale o Python 3.8.10 (64 bits) do [site oficial do Python](https://www.python.org/downloads/release/python-3810/). **Importante:** Durante a instalação, **certifique-se de marcar a opção "Add Python 3.8 to PATH"**. Isso é crucial para que o sistema reconheça o Python.
    Você pode verificar a instalação abrindo o Prompt de Comando e digitando `python --version`, que deve retornar `Python 3.8.10`.

2.  **Clone o Repositório:**
    Abra o Prompt de Comando ou PowerShell, navegue até a pasta onde deseja salvar o projeto e clone o repositório:

    ```bash
    git clone [Projet-Final-Sistema-de-Reconhecimento-Facial]
    cd [Projet-Final-Sistema-de-Reconhecimento-Facial]
    ```

### 2.2. Configuração do Ambiente Virtual (`venv`)

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

1.  **Crie o `venv`:**
    No diretório raiz do projeto (onde está o `requirements.txt`):
    ```bash
    python -m venv venv
    ```
2.  **Ative o `venv`:**
    ```bash
    .\venv\Scripts\activate
    ```
    Você verá `(venv)` no início do seu prompt, indicando que o ambiente está ativo.

### 2.3. Instalação das Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. A instalação do **`dlib`** possui um passo específico e **crucial** devido à sua natureza compilada.

1.  **Instale o `dlib` (PASSO CRÍTICO):**
    A biblioteca `dlib` é um módulo Python para C++ e sua instalação direta via `pip` no Windows pode falhar sem as Build Tools do Visual Studio. Para evitar isso, usaremos uma versão pré-compilada (`.whl`).

    * **a. Baixe o arquivo `.whl`:**
        Baixe o arquivo `dlib-19.22.99-cp38-cp38-win_amd64.whl` de https://github.com/sachadee/Dlib/blob/main/dlib-19.22.99-cp38-cp38-win_amd64.whl. 
        
        Certifique-se de pegar a versão exata `19.22.99` para `cp38` (Python 3.8) e `win_amd64`.


    * **b. Instale o `.whl`:**
        **Com o `venv` ativo**, execute o comando, substituindo `C:\Caminho\Para\Seu\` pelo local onde você salvou o arquivo:
        ```bash
        pip install C:\Caminho\Para\Seu\dlib-19.22.99-cp38-cp38-win_amd64.whl
        ```

    * **c. Ajuste o `requirements.txt`:**
        **Depois de instalar o `.whl` do `dlib` com sucesso, comente a linha `dlib==19.22.99` no seu `requirements.txt` (adicione um `#` na frente).** Isso impede que o `pip` tente reinstalá-lo ou compilá-lo do PyPI.

2.  **Instale as Demais Dependências:**
    Com o `dlib` instalado, agora você pode instalar o resto das dependências do `requirements.txt` (certifique-se de que a linha do `dlib` está comentada!):
    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Estrutura do Projeto e Preparação de Dados

O projeto é organizado para facilitar a compreensão de suas funcionalidades e o tratamento dos dados.

* **`funcoes_principais.py`**: Este arquivo centraliza a implementação das diversas funções críticas do sistema, como detecção de faces, cálculo de embeddings faciais e comparação de faces. Cada função é cuidadosamente documentada para explicar seu propósito e uso.

* **`serializacao_banco_dados_LFW.py`**: Para otimizar o desempenho do sistema, especialmente no contexto de hardware acessível, este script é responsável por **serializar o banco de dados LFW (Labeled Faces in the Wild)**. Ele processa as imagens do LFW e as converte em um formato otimizado (geralmente um arquivo `.pkl` ou `.json` contendo embeddings faciais pré-calculados). Isso permite o carregamento rápido e eficiente dos dados durante a execução do sistema, evitando o reprocessamento de imagens a cada inicialização e reduzindo a carga computacional.

---

## 4. Execução do Sistema

Após a instalação bem-sucedida, você pode executar o sistema:

1.  **Ative o `venv`** (se ainda não estiver ativo).
2.  **Execute o script main.py** do projeto:
    ```bash
    python main.py
    ```

---

## 5. Solução de Problemas Comuns (Troubleshooting)

Esta seção aborda os erros mais frequentes e suas soluções.

### 5.1. Erros de Instalação

* **`Fatal error in launcher: Unable to create process using "..."` ou `O sistema não pode encontrar o arquivo especificado.`**
    * **Causa:** Geralmente ocorre após renomear a pasta do projeto, pois o `venv` mantém referências a caminhos antigos.
    * **Solução:** **Exclua completamente a pasta `venv`** dentro do seu projeto e, em seguida, **recrie-o e reinstale todas as dependências** seguindo os passos da Seção 2.2 e 2.3.

* **`ERROR: Could not find a version that satisfies the requirement dlib==19.22.99`**
    * **Causa:** Isso significa que o `pip` não encontrou essa versão específica do `dlib` pré-compilada no PyPI ou que o comando de instalação do `.whl` não foi usado ou executado corretamente.
    * **Solução:** Verifique se você **baixou o `.whl` exato** (`dlib-19.22.99-cp38-cp38-win_amd64.whl`) e se o **caminho no comando `pip install` está correto** (Seção 2.3.1.b). **Certifique-se de que o `venv` está ativo** ao rodar o comando.

* **`No module named` (`cv2`, `Pillow`, `face_recognition`)**
    * **Causa:** A biblioteca correspondente não foi instalada corretamente.
    * **Solução:** Confirme que seu `venv` está ativo e tente instalar o pacote individualmente, garantindo a versão correta se houver uma no `requirements.txt`:
        ```bash
        pip install opencv-python==4.6.0.66
        pip install Pillow==9.2.0
        pip install face_recognition==1.3.0
        ```
        *(Se `cmake` for um problema: `pip install cmake==3.17.2`)*

### 5.2. Problemas com a Webcam

* **Sistema não conecta à câmera ou tela preta:**
    * **Permissões do Windows:** Vá em `Configurações > Privacidade e Segurança > Câmera` e **ative o acesso à câmera** e a opção "Permitir que os aplicativos da área de trabalho acessem sua câmera".
    * **Conflito de Uso:** Certifique-se de que **nenhum outro aplicativo** (Zoom, Skype, navegador, etc.) esteja usando a webcam ao mesmo tempo.
    * **Índice da Câmera:** O código tenta `cv2.VideoCapture(0)` por padrão. Se você tiver várias câmeras ou uma virtual, o índice pode ser diferente. Se necessário, ajuste o índice da câmera no código (`1`, `2`, etc.).

---