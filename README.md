# Sistema de Inventário e Monitoramento de Computadores em Rede

Projeto desenvolvido para a disciplina de **Redes de Computadores**, com o objetivo de implementar um sistema **cliente/servidor** capaz de realizar descoberta automática de computadores em uma rede local, coletar métricas de hardware e sistema operacional, consolidar essas informações em um servidor central e permitir ações remotas de forma segura.

---

## Objetivo

Desenvolver um sistema cliente/servidor que permita:

- Descoberta automática de clientes na rede local (LAN)
- Coleta periódica de informações de hardware e sistema operacional
- Consolidação e visualização dos dados no servidor
- Monitoramento de clientes online e offline
- Execução de comandos administrativos remotos
- Comunicação segura com criptografia ponta a ponta

---

## Arquitetura do Sistema

O sistema segue o modelo **Cliente/Servidor**, utilizando **sockets puros (TCP e UDP)** e um protocolo de comunicação próprio.

- **Cliente**: executado nas máquinas monitoradas, responsável pela coleta de dados e execução de comandos remotos
- **Servidor**: responsável pela descoberta dos clientes, consolidação das informações, visualização dos dados e auditoria

A comunicação segura é implementada por meio de criptografia híbrida:
- **RSA** para troca segura de chaves
- **AES-GCM** para transmissão de dados com confidencialidade e integridade

---

## Funcionalidades

### Coleta de Dados no Cliente
- Quantidade de processadores / núcleos
- Memória RAM livre
- Espaço em disco livre
- Interfaces de rede (IP, status UP/DOWN e tipo)
- Identificação do sistema operacional

### Servidor e Consolidação
- Dashboard em terminal com listagem dos clientes
- Exibição do sistema operacional, IP principal e última atualização
- Identificação de clientes online e offline
- Detalhamento completo de um cliente selecionado
- Exportação de relatórios em formato **CSV** ou **JSON**

### Monitoramento de Status
- Um cliente é considerado offline após 30 segundos sem resposta ao mecanismo de comunicação

---

## Segurança

- Comunicação criptografada ponta a ponta
- Autenticação dos clientes
- Controle de acesso por tipo de comando
- Auditoria no servidor com registro de ações executadas, cliente envolvido e data/hora

---

## Funcionalidades Bônus

- Controle remoto do mouse (movimento e clique)
- Controle remoto do teclado

As ações remotas são executadas apenas após autenticação e por meio de comunicação segura.

---

## Tecnologias Utilizadas

- Python 3
- Sockets TCP e UDP
- Programação Orientada a Objetos
- Criptografia RSA e AES-GCM
- JSON e CSV para serialização e exportação de dados
