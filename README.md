📡 Sistema de Inventário e Monitoramento de Computadores em Rede

Projeto desenvolvido para a disciplina de Redes de Computadores, com foco na construção de um sistema Cliente/Servidor capaz de realizar descoberta automática de hosts na LAN, coleta de métricas de hardware e sistema operacional, consolidação de dados no servidor e execução de ações remotas de forma segura.

🎯 Objetivo

Desenvolver um sistema cliente/servidor que permita:

Descoberta automática de computadores na rede local

Coleta periódica de informações de hardware e sistema

Consolidação e visualização dos dados no servidor

Execução de comandos administrativos remotos

Comunicação segura com criptografia ponta a ponta

🧩 Arquitetura do Sistema

O projeto segue o modelo Cliente/Servidor, utilizando sockets TCP e UDP com protocolo próprio.

Cliente: Executado nas máquinas monitoradas

Servidor: Responsável pela descoberta, coleta, consolidação, visualização e auditoria

A comunicação é protegida por criptografia híbrida:

RSA para troca segura de chaves

AES-GCM para comunicação de dados com confidencialidade e integridade

⚙️ Funcionalidades
🖥️ Coleta de Dados no Cliente

Quantidade de CPUs / núcleos

Memória RAM livre

Espaço em disco livre

Interfaces de rede (IP, status UP/DOWN, tipo)

Identificação do sistema operacional

🗄️ Servidor e Consolidação

Dashboard em terminal com lista de clientes

Identificação de clientes online e offline

Última atualização de cada cliente

Detalhamento completo de um cliente selecionado

Exportação de relatórios em CSV ou JSON

🕵️ Monitoramento de Status

Cliente é considerado offline após 30 segundos sem resposta

Atualização automática de status

🔐 Segurança

Comunicação criptografada ponta a ponta

Autenticação de clientes

Controle de acesso por tipo de comando

Auditoria no servidor com registro de:

Ação executada

Cliente envolvido

Data e hora

🖱️🎹 Funcionalidades Bônus

Controle remoto do mouse (movimento e clique)

Controle remoto do teclado

Essas ações são executadas apenas mediante autenticação e comunicação segura.

🛠️ Tecnologias Utilizadas

Python 3

Sockets TCP e UDP

Programação Orientada a Objetos

Bibliotecas criptográficas (RSA e AES-GCM)

JSON e CSV para serialização de dados

▶️ Como Executar
1️⃣ Iniciar o Servidor
python servidor.py
2️⃣ Iniciar o Cliente
python cliente.py

Os clientes serão descobertos automaticamente na rede local.

📊 Dashboard (Servidor)

No menu do servidor é possível:

Listar clientes conectados

Atualizar dados manualmente

Detalhar um cliente específico

Executar comandos remotos

Exportar relatórios
