<div align="center">
  <h1>Sistemas Operacionais - Algoritmos Clássicos</h1>
  <p>Repositório criado para fins educacionais contendo implementações base dos principais algoritmos estudados na disciplina de Sistemas Operacionais.</p>
</div>

<br/>

<div align="center">
  <h3>Tecnologias Utilizadas</h3>
  <br>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" alt="Python" width="55" height="55" style="margin-right: 25px;" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original.svg" alt="Go" width="55" height="55" />
</div>

<br/>

## Sobre o Projeto

Este repositório tem como objetivo documentar e disponibilizar códigos essenciais para o estudo dos princípios fundamentais que regem os sistemas operacionais modernos. Os algoritmos aqui desenvolvidos abordam diversas partes críticas do funcionamento estrutural de um S.O., passando pelo escalonamento de processos, gerenciamento de memória, controle de entrada e saída (I/O) e sistemas de arquivos.

A grande maioria das lógicas e simulações foi desenvolvida em **Python**, devido à sua sintaxe de alto nível que facilita a compreensão pura dos algoritmos. O módulo direcionado a concorrência e processos leves foi implementado em **Go** (Golang), explorando a capacidade nativa e eficiente da linguagem para o tratamento de múltiplos fluxos de execução e sincronização.

---

## Estrutura do Repositório

O repositório está subdividido e organizado em módulos temáticos:

### Gerenciamento de Memória (`memory_management/`)
Algoritmos responsáveis por definir como o sistema operacional administra o espaço disponível na memória principal.
* **`first_fit.py`**: Implementa a política de alocação de memória First-Fit, que percorre a memória buscando o primeiro slot livre de tamanho suficiente para abrigar um processo.
* **`pagination.py`**: Simulador de memória paginada, expondo o conceito de divisão de memória física em quadros (frames) e memória lógica em páginas.

### Escalonamento de Processos (`preemptive_simulator/`)
Módulo responsável por ditar as regras e ordens de chegada na CPU, simulando a concorrência em sistemas multitarefa.
* **`priority/priority.py`**: Simulador de escalonador preemptivo baseado em tabela de prioridades definidas.
* **`round_robin/robin.py`**: Algoritmo preemptivo Round Robin, que faz a alternância equitativa de tempo (quantum) da CPU entre os processos aptos.

### Sistemas de Arquivos (`file_system/`)
* **`alocacao_contigua.py`**: Demonstra a estratégia primária de alocação contígua de arquivos no disco lógico, evidenciando fenômenos como a fragmentação externa espacial.

### Gerenciamento de Entrada e Saída (`io_management/`)
* **`disk_io_simulator.py`**: Simula requisições de disco rígido (leitura e escrita), comutando as operações de hardware lentas de I/O na fila de processamento.

### Concorrência e Threads (`threads/`)
* **`main.go`**: Utiliza programação em Go para demonstrar o controle manual de threads (goroutines), evidenciando a paralelização de tarefas com múltiplos núcleos sem a ocorrência de condições de corrida.

### Segurança (`security/`)
* **`security_breaker.py`**: Script voltado a evidenciar pontos de vulnerabilidades básicas dentro da estruturação lógica do sistema operacional.

---

## Requisitos e Como Executar

### Pré-requisitos
Para rodar os algoritmos deste repositório sem problemas, é necessário ter instalado as soluções em sua máquina local:
* Interpretador **Python 3.8** ou superior.
* Compilador **Go 1.20** ou superior.

### Instruções

Para visualizar o comportamento dos simuladores elaborados em Python, navegue pelo terminal até a pasta específica do módulo de seu interesse e utilize o interpretador:

```bash
cd memory_management
python first_fit.py
```

Para a execução e testes do laboratório focado em Goroutines e paralelismo estruturado em Golang:

```bash
cd threads
go run main.go
```

---

## Autor

Desenvolvido por [Emanuel Rodrigues](https://github.com/emanuelrodrigues2005).

---

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE) - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
