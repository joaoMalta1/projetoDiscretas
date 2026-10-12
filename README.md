# Circuito de Euler — INF1631, grupo D

O programa gera grafos simples não direcionados até encontrar um circuito de
Euler, constrói e valida o circuito encontrado e verifica a ocorrência de
circuitos em um segundo experimento com 1000 grafos. Os parâmetros oficiais
são **n = 10**, **p = 0,30** e **seed = 482**.

## Como executar

No PowerShell, dentro deste diretório, use Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe testes.py -v
.\.venv\Scripts\python.exe main.py
```

Os comandos chamam diretamente o Python da `.venv`; não é necessário ativá-la.
Se `py` não estiver disponível, use `python -m venv .venv` na primeira linha,
após confirmar que `python --version` indica Python 3.12.

O programa informa o grafo encontrado, seus graus, o circuito, o resultado da
validação e as estatísticas dos 1000 grafos. A última linha sobre a figura
informa o arquivo gerado: `grafo_euleriano.png` com `matplotlib` ou
`grafo_euleriano.svg` como alternativa vetorial. A análise dos grafos não
depende de bibliotecas externas.

Opções adicionais:

```powershell
.\.venv\Scripts\python.exe main.py --sem-figura
.\.venv\Scripts\python.exe main.py --repeticoes 100000 --sem-figura
```

`--sem-figura` executa apenas os experimentos. `--repeticoes K` altera somente
o tamanho do segundo experimento e exige um inteiro positivo. A execução
oficial usa 1000 grafos; a rodada maior é complementar. Os parâmetros do grupo
permanecem fixos.

## Arquivos

- `main.py`: geração, critérios de Euler, Hierholzer, validação, figura e
  experimentos.
- `testes.py`: quatro casos obrigatórios e testes adicionais.
- `RELATORIO.md`: implementação, resultados observados e análise.
- `grafo_euleriano.svg` e `grafo_euleriano.png`: visualizações do grafo
  encontrado. O PNG está incorporado ao relatório.
- `requirements.txt`: dependência da visualização com `matplotlib`.

A pasta `.venv` e os arquivos de `__pycache__` são locais à execução e não
precisam ser entregues.

O experimento 2 inicializa um novo gerador com a seed 482. Por isso, seus
primeiros grafos repetem a sequência da busca do experimento 1. Os valores
obtidos são reproduzíveis; os tempos medidos podem variar entre execuções.
