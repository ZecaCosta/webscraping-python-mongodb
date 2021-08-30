# Webscraping com Python e MongoDBCancel changes

## ⭐ Boas vindas ao repositório

Olá, seja muito bem-vindo ao repositório **webscraping-python-mongodb**.

Neste repositório você vai encontrar alguns detalhes de como foi desenvolvido um serviço em que foram usadas técnicas de raspagem de dados e armazenamento dos dados obtidos em um banco de dados.

Siga esse README para saber mais.
  
[![made-with-python](https://img.shields.io/badge/Feito%20com-Python-1f425f.svg)](https://www.python.org/) [![mongo](https://img.shields.io/badge/Banco%20de%20dados-MongoDB-116149.svg)](https://www.mongodb.com/pt-br) [![linux](https://img.shields.io/badge/SO-Linux-1f425f.svg)](https://www.linux.org/) <img  alt="License"  src="https://img.shields.io/badge/license-MIT-brightgreen">

<h4  align="left">🚧 Como poderá ser visto mais adiante, o desenvolvimento do serviço ainda está em construção... 🚧</h4>

<p  align="center">
<a  href="#-sobre-o-projeto">Sobre</a> |
<a  href="#-funcionalidades">Funcionalidades</a> |<a  href="#-como-executar-o-projeto">Como executar</a> |
<a  href="#-tecnologias">Tecnologias</a> |
<a  href="#-autor">Autor</a> |
<a  href="#user-content--licença">Licença</a>
</p>

## 💻 Sobre o projeto

Esse projeto tem como objetivo criar um serviço de webscraping (raspagem de dados) em Python para capturar uma lista de pessoas aprovadas em um vestibular (4.671 páginas de dados fictícios) disponibilizadas pelo site https://sample-university-site.herokuapp.com/.

Para persistência de dados o serviço utiliza o gerenciador de banco de dados NoSQL `MongoDB`. Todos os dados raspados do site (CPFs, nomes e scores) serão armazenadas em uma coleção chamada `candidates` do banco de dados `approved_candidates`, utilizando a função Python `create`, disponibilizada no módulo `database.py`.

Esse projeto foi realizado durante o período de estudos do módulo de CS do curso de desenvolvimento web da [Trybe](https://www.betrybe.com/), com objetivo de exercitar conhecimentos de Python aprendidos.

`Web scraping:` é uma coleta de dados da web, de sites, onde são usados scripts e programas para “raspar” informações destes sites e que poderão ser usadas para futuras análises.

## ⚙️ Funcionalidades

- [X] Raspagem de dados
- [X] Salvar dados no banco de dados
- [ ] Verificar validade dos CPF's
- [ ] Higienização dos dados
- [ ] Testes unitários com cobertura de pelo menos 90%
- [ ] Estrutura
- [ ] Criar funções para manipular os dados salvos
- [ ] Melhoria de performance

> Os itens não assinalados ainda deverão ser implementados. Outras funcionalidades ainda não previstas poderão ser necessárias para completar esse projeto.

## 🚀 Como executar o projeto

### Pré-requisitos

Este projeto foi feito usando um máquina com sistema operacional Linux, assim todos os procedimentos aqui tratados são para esse ambiente.

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas, caso necessário, clique nos links abaixo e siga as instruções de instalação:

-  [Git](https://git-scm.com)
-  [Python](https://python.org.br/instalacao-linux/)
-  [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/).

### 🎲 Rodando o serviço

#### Clonar e preparar ambiente

```bash
# Clone este repositório
- `git clone https://github.com/ZecaCosta/webscraping-python-mongodb.git`

# Entre na pasta do repositório que você acabou de clonar
- `cd webscraping-python-mongodb`

# Crie o ambiente virtual para o projeto
- `python3 -m venv .venv &&  source .venv/bin/activate`

# Instale as dependências
- `python3 -m pip install -r dev-requirements.txt`
``` 
**Nota:** O arquivo dev-requirements.txt contém todos as dependências que serão utilizadas no projeto.

📚 Se quiser saber mais sobre a instalação de dependências com `pip`, veja esse [artigo](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1).

#### Detalhes do código

1. No arquivo `scraper.py` estão implementadas as funções utilizadas para o funcionamento do serviço.

- A função `fetch`:
Recebe um URL, faz uma ma requisição HTTP `get` e retorna conteúdo HTML da resposta. Como poderá ser utilizada várias vezes em sucessão, respeita um Rate Limit de 1 requisição por segundo e caso a requisição não receba resposta em até 3 segundos, será abandonada.

- A função `scrape_url_approvals`:
Recebe o conteúdo HTML de uma página e retorna uma lista de urls de todos os candidatos aprovados desta página.

- A função `get_candidate_url`
Recebe link de cada candidato aprovado, junta com a url base e retorna a url completa do candidato aprovado.

- A função `scrape_next_page_url`:
Recebe o conteúdo HTML de uma página e retorna a url da próxima página.

- A função `is_valid_page`
Recebe url de uma página e retorna True se essa página existir, usando como base de comparação o conteúdo `"Invalid page."` existente apenas nas páginas que não têm novos candidatos aprovados.

- A função `scrape_details`:
Recebe conteúdo HTML da página de um canditado aprovado, bem como sua url e retorna um dicionário com seus dados ( cpf, nome e score).

- A função `get_all_data`:
Principal função do serviço, invoca as demais funções com o objetivo de salvar no banco de dados `TODOS` os canditados aprovados, para isso invoca a função `create` importada do módulo `database.py`.

**Nota:** O teste manual para essa função é mostrado abaixo, mas como são mais de 4.600 páginas válidas, considere a possibilidade de não realizá-lo
```python
python3 -i scraper.py
>>> get_all_data()
>>> exit()
```
**Nota:** Caso queira testar manualmente, em benefício do tempo, fica a sugestão de antes implementar uma alteração em que ao invés de começar da página 1, comece mais próximo do final, por exemplo, pela página 4.665.

```python
def  get_all_data():
    # url = BASE_URL
    url = "https://sample-university-  site.herokuapp.com/approvals/4665"
    url_approvals_list = []
    status = True
    while status:
        html_content = fetch(url)
        url_approvals =      scrape_url_approvals(html_content)
        url_approvals_list.extend(url_approvals)
        url = scrape_next_page_url(html_content)
        print(url) # para acompanhar o processo de troca de páginas
        status = is_valid_page(url)
    print("salvando no MongoDB...") # para acompanhar o armazenamento
    data = [
        scrape_details(fetch(url), url) for url in url_approvals_list
    ]
   create(data)
   return  "Dados foram salvos no MongoDB"
```
Agora ficará viável executar o teste manual.

```python
python3 -i scraper.py
>>> get_all_data()
>>> exit()
```
- A função `get_data`:
Tem o mesmo da função `get_all_data`, apenas ao invés de salvar todos os canditados aprovados, irá salvar uma quantidade de canditados recebidos por parâmetro.

Teste manual para, por exemplo, obter 5 candidatos aprovados:

```python
python3 -i scraper.py
>>> get_data(5)
>>> exit()
```
2. No arquivo `database.py`

Neste arquivo está a configuração de acesso ao MongoDB, previamente instalado. Os dados raspados serão armazenados numa collection chamada `candidates` do banco de dados `approved_candidates`. Também está implementada a função chamada `create`.

Com o servidor MongoDB rodando, qualquer outro módulo conseguirá acessá-lo sem problemas, basta importar e chamar função `create`.

Para rodar o servidor MonngoDB no Linux, use o comando:

`sudo service mongod start`

**Nota:** O mongoDB utilizará por padrão a porta 27017. Se já houver outro serviço utilizando esta porta, considere desativá-lo.

Para carregar o shell do Mongodb e verificar os documentos da collection candidates, use a sequência de comandos:

```bash
mongosh
> show dbs
> use approved_candidates
> show collections
> db.candidates.find()
> db.candidates.count()
> exit
```

## 🛠 Tecnologias

As seguintes ferramentas e bibliotecas foram usadas na construção do projeto:

-  [Python](https://python.org.br/)
-  [MongoDB](https://www.mongodb.com/pt-br)
-  [pymongo](https://pypi.org/project/pymongo/)
-  [parsel](https://pypi.org/project/parsel/).
-  [requests](https://pypi.org/project/requests/)
-  [python-decouple](https://pypi.org/project/python-decouple)

## 🦸 Autor

<span>Sou <b>Zeca Costa</b>, estudante de Desenvolvimento Web na Trybe</span>

[![Linkedin Badge](https://img.shields.io/badge/-Zeca%20Costa-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/https://www.linkedin.com/in/zecacosta//)](https://www.linkedin.com/in/zecacosta/) [![Gmail Badge](https://img.shields.io/badge/-jccostaso@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:jccostaso@gmail.com)](mailto:jccostaso@gmail.com)

## 📝 Licença

Este projeto esta sobe a licença [MIT](./LICENSE).
