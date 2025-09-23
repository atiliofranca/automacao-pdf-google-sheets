# 🤖 Extrator de Orçamentos PDF para Google Sheets - Makino Irrigação

Sistema automatizado para extração de dados de PDFs de orçamento e inserção automática na planilha **"Cobrança Makino Irrigação"** do Google Sheets.

## ✨ Funcionalidades Principais

- 🔍 **Detecção Automática de Tipos**: Identifica automaticamente diferentes formatos de PDF
- 📄 **Seleção Múltipla**: Processa vários arquivos PDF simultaneamente
- 🎨 **Interface Gráfica**: Janelas centralizadas e amigáveis
- 💰 **Formatação de Moeda**: Valores em formato brasileiro (R$ 1.500,00)
- 📊 **Integração Google Sheets**: Inserção automática na planilha
- ✅ **Feedback Visual**: Mensagens de sucesso/erro personalizadas

## 📊 Dados Extraídos

O sistema extrai automaticamente os seguintes dados dos PDFs:

| Campo                      | Descrição       | Localização no PDF                  |
| -------------------------- | ----------------- | ------------------------------------- |
| **CLIENTE**          | Nome do cliente   | Campo "Cliente:"                      |
| **NUMERO DO PEDIDO** | Número do pedido | Campo "PEDIDO N°"                    |
| **DATA**             | Data de emissão  | Campo "Data Emissão:"                |
| **VALOR**            | Valor total       | Campo "TOTAL:" (formato: R$ 1.500,00) |
| **RETIRADO POR**     | Deixado em branco | -                                     |

## 🎯 Tipos de PDF Suportados

### Tipo 1: Formato Simples (exemplo1.pdf)

- Cliente na linha seguinte a "Cliente:"
- Formato de valor simples após "TOTAL:"

### Tipo 2: Formato Detalhado (exemplo2.pdf)

- Campo "Fantasia:" após "Cliente:"
- Valor após "VALOR BRUTO:" dentro de "TOTAL:"

## 🚀 Como Usar

### Opção 1: Executável Portável (Recomendado)

1. **Baixe** a pasta `Extrator_Orcamentos_Makino` completa
2. **Execute** o arquivo `Extrator_Orcamentos_Makino.exe`
3. **Selecione** os arquivos PDF que deseja processar
4. **Aguarde** a mensagem de sucesso

### Opção 2: Execução via Python

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar o extrator
python extrator_simples.py
```

## 🛠️ Instalação para Desenvolvimento

### Pré-requisitos

- Python 3.7 ou superior
- Conta Google com acesso ao Google Sheets
- Planilha "Cobrança Makino Irrigação" criada no Google Sheets

### Configuração do Ambiente

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

### Configurar Credenciais

O arquivo `planilha-python-472618-f3c9ba25d174.json` contém as credenciais da conta de serviço.

**IMPORTANTE**: A planilha "Cobrança Makino Irrigação" deve estar compartilhada com:
`robo-planilha-python@automacao-planilhas-472615.iam.gserviceaccount.com`

## 📁 Estrutura do Projeto

```
├── extrator_simples.py                    # Script principal
├── extrator_simples.spec                 # Configuração PyInstaller
├── gerar_executavel.bat                  # Script para gerar executável
├── requirements.txt                      # Dependências Python
├── README.md                            # Documentação principal
├── INSTRUÇÕES_EXECUTÁVEL.md             # Guia para gerar executável
├── ícone.ico                           # Ícone da aplicação
├── exemplo1.pdf                        # PDF tipo 1 (formato simples)
├── exemplo2.pdf                        # PDF tipo 2 (formato detalhado)
├── planilha-python-472618-f3c9ba25d174.json  # Credenciais Google
└── venv/                               # Ambiente virtual Python
```

## 🔧 Configuração da Planilha Google Sheets

### Estrutura da Aba "Pedidos"

A aba "Pedidos" deve ter as seguintes colunas (na ordem):

| Coluna | Descrição      |
| ------ | ---------------- |
| A      | CLIENTE          |
| B      | NUMERO DO PEDIDO |
| C      | DATA             |
| D      | VALOR            |
| E      | RETIRADO POR     |

### Compartilhamento da Planilha

1. Abra a planilha "Cobrança Makino Irrigação"
2. Clique em "Compartilhar"
3. Adicione o email: `robo-planilha-python@automacao-planilhas-472615.iam.gserviceaccount.com`
4. Defina permissão como "Editor"

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

## 🐛 Solução de Problemas

### Erro: "Planilha não encontrada"

- ✅ Verifique se a planilha "Cobrança Makino Irrigação" existe
- ✅ Confirme se está compartilhada com o email da conta de serviço

### Erro: "Aba não encontrada"

- ✅ Verifique se a aba "Pedidos" existe na planilha
- ✅ Confirme se o nome está exatamente como especificado

### Erro: "Dados não extraídos"

- ✅ Verifique se o PDF contém os campos necessários
- ✅ Confirme se o formato dos dados está correto no PDF

### Erro de Credenciais

- ✅ Verifique se o arquivo JSON de credenciais está presente
- ✅ Confirme se as credenciais estão válidas

### Erro de Antivírus (Executável)

- ✅ Adicione exceção no antivírus para o executável
- ✅ Desative temporariamente o antivírus durante o uso

## 🔒 Segurança

- ✅ As credenciais são armazenadas localmente
- ✅ A conexão com Google Sheets usa autenticação segura
- ✅ Nenhum dado é transmitido para terceiros
- ✅ Processamento local dos PDFs

## 📊 Exemplo de Execução

```
🤖 INICIANDO AUTOMAÇÃO - EXTRATOR DE ORÇAMENTOS PDF
============================================================
=== ETAPA 1: Seleção de Arquivo ===
Arquivo selecionado: C:\Users\Usuario\Documents\orcamento_123.pdf

=== ETAPA 2: Extração de Dados do PDF ===
Texto extraído do PDF com sucesso.
Detectando tipo de arquivo...
Tipo detectado: tipo1
Aplicando expressões regulares...
Dados extraídos com sucesso:
  CLIENTE: João Silva
  NUMERO DO PEDIDO: 12345
  DATA: 15/12/2024
  VALOR: R$ 1.500,00

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

## 🆕 Versão

- **Data**: Setembro 2025
- **Compatibilidade**: Python 3.7+
- **Plataforma**: Windows (executável portável)

## 📞 Suporte

Para problemas ou dúvidas:

1. ✅ Verifique se todas as dependências estão instaladas
2. ✅ Confirme se a planilha está configurada corretamente
3. ✅ Verifique se o formato do PDF está conforme esperado
4. ✅ Consulte a seção "Solução de Problemas" acima

---

**Desenvolvido para Makino Irrigação** 🌱
