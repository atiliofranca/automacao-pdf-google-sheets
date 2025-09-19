# 🤖 Extrator de Orçamentos PDF para Google Sheets

Este sistema automatiza a extração de dados de PDFs de orçamento e os insere na planilha **"Cobrança Makino Irrigação"** do Google Sheets.

## 📋 Funcionalidades

- **Seleção de Arquivo**: Interface gráfica para selecionar arquivos PDF
- **Extração de Dados**: Extração automática de dados usando expressões regulares
- **Integração Google Sheets**: Inserção automática dos dados na planilha

## 📊 Dados Extraídos

O sistema extrai os seguintes dados dos PDFs:

| Campo | Descrição | Localização no PDF |
|-------|-----------|-------------------|
| **CLIENTE** | Nome do cliente | Campo "Cliente:" |
| **NUMERO DO PEDIDO** | Número do pedido | Campo "PEDIDO N°" |
| **DATA** | Data de emissão | Campo "Data Emissão:" |
| **VALOR** | Valor total | Campo "TOTAL:" |
| **RETIRADO POR** | Deixado em branco | - |

## 🛠️ Instalação

### 1. Pré-requisitos

- Python 3.7 ou superior
- Conta Google com acesso ao Google Sheets
- Planilha "Cobrança Makino Irrigação" criada no Google Sheets

### 2. Configurar Ambiente Virtual (Recomendado)

#### Opção A: Scripts Automáticos (Windows)
```bash
# Criar ambiente virtual
python -m venv venv

# Instalar dependências automaticamente
instalar_dependencias.bat

# Ativar ambiente virtual
ativar_ambiente.bat
```

#### Opção B: Comandos Manuais
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Verificar Instalação

```bash
# Executar testes do sistema
python teste_sistema.py
```

### 4. Configurar Credenciais

O arquivo `automacao-planilhas-472615-e62bc76ce2a2.json` já está configurado com as credenciais da conta de serviço.

**IMPORTANTE**: Certifique-se de que a planilha "Cobrança Makino Irrigação" está compartilhada com o email:
`robo-planilha-python@automacao-planilhas-472615.iam.gserviceaccount.com`

## 🚀 Como Usar

### Executar o Sistema

**IMPORTANTE**: Sempre ative o ambiente virtual antes de executar!

#### Opção 1: Script de Inicialização (Mais Fácil)
```bash
# Windows - Duplo clique no arquivo ou execute:
iniciar.bat

# Ou execute diretamente:
python iniciar.py
```

#### Opção 2: Execução Direta
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar o extrator simples
python extrator_simples.py
```

#### Opção 3: Versão Original (Um PDF)
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar versão original
python extrator_orcamento.py
```

### Processo de Execução

#### Versão Simples (Recomendada):
1. **Seleção de PDFs**: Uma janela será aberta para selecionar um ou mais arquivos PDF
2. **Processamento**: O sistema processa todos os arquivos automaticamente
3. **Janela de Sucesso**: Uma pequena janela centralizada mostra o resultado
4. **Inserção**: Os dados são inseridos na planilha Google Sheets

#### Versão Original:
1. **Seleção de Arquivo**: Uma janela será aberta para selecionar o arquivo PDF
2. **Extração**: O sistema extrai automaticamente os dados do PDF
3. **Inserção**: Os dados são inseridos na planilha Google Sheets

### Exemplo de Uso

```
🤖 INICIANDO AUTOMAÇÃO - EXTRATOR DE ORÇAMENTOS PDF
============================================================
=== ETAPA 1: Seleção de Arquivo ===
Arquivo selecionado: C:\Users\Usuario\Documents\orcamento_123.pdf

=== ETAPA 2: Extração de Dados do PDF ===
Texto extraído do PDF com sucesso.
Aplicando expressões regulares...
Dados extraídos com sucesso:
  CLIENTE: João Silva
  NUMERO DO PEDIDO: 12345
  DATA: 15/12/2024
  VALOR: 1500.00

=== ETAPA 3: Atualização da Planilha ===
Configurando credenciais do Google Sheets...
Conectando ao Google Sheets...
Abrindo planilha 'Cobrança Makino Irrigação'...
Selecionando aba 'Pedidos'...
Inserindo nova linha na planilha...
✅ Dados inseridos com sucesso na planilha!

🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!
Os dados foram inseridos na planilha 'Cobrança Makino Irrigação'.
```

## 📁 Estrutura do Projeto

```
├── extrator_simples.py           # Script principal (múltiplos PDFs)
├── extrator_orcamento.py         # Script original (um PDF)
├── iniciar.py                    # Script de inicialização
├── iniciar.bat                   # Script de inicialização (Windows)
├── teste_sistema.py              # Script de testes
├── requirements.txt               # Dependências Python
├── README.md                     # Documentação
├── venv/                         # Ambiente virtual Python
└── planilha-python-472618-f3c9ba25d174.json  # Credenciais Google
```

## 🔧 Configuração da Planilha

### Estrutura da Aba "Pedidos"

A aba "Pedidos" deve ter as seguintes colunas (na ordem):

| Coluna | Descrição |
|--------|-----------|
| A | CLIENTE |
| B | NUMERO DO PEDIDO |
| C | DATA |
| D | VALOR |
| E | RETIRADO POR |

## 🐛 Solução de Problemas

### Erro: "Planilha não encontrada"
- Verifique se a planilha "Cobrança Makino Irrigação" existe
- Confirme se está compartilhada com o email da conta de serviço

### Erro: "Aba não encontrada"
- Verifique se a aba "Pedidos" existe na planilha
- Confirme se o nome está exatamente como especificado

### Erro: "Dados não extraídos"
- Verifique se o PDF contém os campos necessários
- Confirme se o formato dos dados está correto no PDF

### Erro de Credenciais
- Verifique se o arquivo JSON de credenciais está presente
- Confirme se as credenciais estão válidas

## 📝 Padrões de Dados Suportados

### Formato de Data
- DD/MM/AAAA
- DD-MM-AAAA

### Formato de Valor
- R$ 1.500,00
- R$1.500,00
- 1500.00
- 1.500,00

### Formato de Pedido
- PEDIDO N° 12345
- PEDIDO Nº 12345
- PEDIDO No 12345

## 🔒 Segurança

- As credenciais são armazenadas localmente
- A conexão com Google Sheets usa autenticação segura
- Nenhum dado é transmitido para terceiros

## 📞 Suporte

Para problemas ou dúvidas, verifique:
1. Se todas as dependências estão instaladas
2. Se a planilha está configurada corretamente
3. Se o formato do PDF está conforme esperado

## 🆕 Versão

- **Versão**: 1.0
- **Data**: Dezembro 2024
- **Compatibilidade**: Python 3.7+
