#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Orçamentos PDF para Google Sheets
Automação para extrair dados de PDFs de orçamento e inserir na planilha "Cobrança Makino Irrigação"
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import re
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import sys
import os

class ExtratorOrcamento:
    def __init__(self):
        self.credenciais_arquivo = "automacao-planilhas-472615-e62bc76ce2a2.json"
        self.planilha_nome = "Cobrança Makino Irrigação"
        self.aba_nome = "Pedidos"
        self.dados_extraidos = {}
        
    def selecionar_arquivo_pdf(self):
        """Etapa 1: Seleção de arquivo PDF usando interface gráfica"""
        print("=== ETAPA 1: Seleção de Arquivo ===")
        
        # Configurar a janela de diálogo
        root = tk.Tk()
        root.withdraw()  # Esconder a janela principal
        
        # Abrir diálogo para seleção de arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo PDF de orçamento",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        
        root.destroy()
        
        if not caminho_arquivo:
            print("Nenhum arquivo selecionado.")
            return None
            
        print(f"Arquivo selecionado: {caminho_arquivo}")
        return caminho_arquivo
    
    def extrair_dados_pdf(self, caminho_pdf):
        """Etapa 2: Extração de dados do PDF usando PyMuPDF e regex"""
        print("\n=== ETAPA 2: Extração de Dados do PDF ===")
        
        try:
            # Abrir o PDF
            doc = fitz.open(caminho_pdf)
            texto_completo = ""
            
            # Extrair texto de todas as páginas
            for pagina_num in range(len(doc)):
                pagina = doc.load_page(pagina_num)
                texto_completo += pagina.get_text() + "\n"
            
            doc.close()
            
            print("Texto extraído do PDF com sucesso.")
            print("Aplicando expressões regulares...")
            
            # Aplicar regex para extrair os dados
            dados = self._aplicar_regex(texto_completo)
            
            if dados:
                self.dados_extraidos = dados
                print("Dados extraídos com sucesso:")
                for chave, valor in dados.items():
                    print(f"  {chave}: {valor}")
                return dados
            else:
                print("Erro: Não foi possível extrair todos os dados necessários.")
                return None
                
        except Exception as e:
            print(f"Erro ao processar o PDF: {str(e)}")
            return None
    
    def _aplicar_regex(self, texto):
        """Aplicar expressões regulares para extrair dados específicos"""
        dados = {}
        
        # Regex para Cliente (procurar "Cliente:" e capturar a linha seguinte)
        padrao_cliente = r"Cliente:\s*(.+?)(?:\n|$)"
        match_cliente = re.search(padrao_cliente, texto, re.IGNORECASE | re.MULTILINE)
        if match_cliente:
            dados['CLIENTE'] = match_cliente.group(1).strip()
        
        # Regex para Número do Pedido (procurar "PEDIDO N°" e capturar os dígitos)
        padrao_pedido = r"PEDIDO\s*N[°ºo]\s*(\d+)"
        match_pedido = re.search(padrao_pedido, texto, re.IGNORECASE)
        if match_pedido:
            dados['NUMERO DO PEDIDO'] = match_pedido.group(1)
        
        # Regex para Data (procurar "Data Emissão:" e capturar a data)
        padrao_data = r"Data\s*Emiss[ãa]o:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
        match_data = re.search(padrao_data, texto, re.IGNORECASE)
        if match_data:
            dados['DATA'] = match_data.group(1)
        
        # Regex para Valor (procurar "TOTAL:" e capturar o valor numérico)
        padrao_valor = r"TOTAL:\s*R?\$?\s*([\d.,]+)"
        match_valor = re.search(padrao_valor, texto, re.IGNORECASE)
        if match_valor:
            # Limpar e formatar o valor
            valor_limpo = match_valor.group(1).replace('.', '').replace(',', '.')
            try:
                dados['VALOR'] = float(valor_limpo)
            except ValueError:
                dados['VALOR'] = match_valor.group(1)
        
        # Verificar se todos os campos obrigatórios foram encontrados
        campos_obrigatorios = ['CLIENTE', 'NUMERO DO PEDIDO', 'DATA', 'VALOR']
        campos_encontrados = [campo for campo in campos_obrigatorios if campo in dados]
        
        if len(campos_encontrados) < len(campos_obrigatorios):
            print(f"Campos encontrados: {campos_encontrados}")
            print(f"Campos faltando: {set(campos_obrigatorios) - set(campos_encontrados)}")
            return None
        
        return dados
    
    def atualizar_planilha(self, dados):
        """Etapa 3: Atualização da planilha Google Sheets"""
        print("\n=== ETAPA 3: Atualização da Planilha ===")
        
        try:
            # Verificar se o arquivo de credenciais existe
            if not os.path.exists(self.credenciais_arquivo):
                print(f"Erro: Arquivo de credenciais '{self.credenciais_arquivo}' não encontrado.")
                return False
            
            # Configurar credenciais
            print("Configurando credenciais do Google Sheets...")
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credenciais_arquivo, 
                scopes=scope
            )
            
            # Conectar ao Google Sheets
            print("Conectando ao Google Sheets...")
            gc = gspread.authorize(creds)
            
            # Abrir a planilha
            print(f"Abrindo planilha '{self.planilha_nome}'...")
            planilha = gc.open(self.planilha_nome)
            
            # Selecionar a aba
            print(f"Selecionando aba '{self.aba_nome}'...")
            aba = planilha.worksheet(self.aba_nome)
            
            # Preparar os dados para inserção
            linha_dados = [
                dados.get('CLIENTE', ''),
                dados.get('NUMERO DO PEDIDO', ''),
                dados.get('DATA', ''),
                dados.get('VALOR', ''),
                ''  # RETIRADO POR - deixado em branco conforme especificação
            ]
            
            # Inserir nova linha na planilha
            print("Inserindo nova linha na planilha...")
            aba.append_row(linha_dados)
            
            print("✅ Dados inseridos com sucesso na planilha!")
            return True
            
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Erro: Planilha '{self.planilha_nome}' não encontrada.")
            print("Certifique-se de que a planilha existe e está compartilhada com o email da conta de serviço.")
            return False
            
        except gspread.exceptions.WorksheetNotFound:
            print(f"Erro: Aba '{self.aba_nome}' não encontrada na planilha.")
            return False
            
        except Exception as e:
            print(f"Erro ao atualizar a planilha: {str(e)}")
            return False
    
    def executar_automacao(self):
        """Executar o processo completo de automação"""
        print("🤖 INICIANDO AUTOMAÇÃO - EXTRATOR DE ORÇAMENTOS PDF")
        print("=" * 60)
        
        # Etapa 1: Seleção de arquivo
        caminho_pdf = self.selecionar_arquivo_pdf()
        if not caminho_pdf:
            print("❌ Processo cancelado - nenhum arquivo selecionado.")
            return False
        
        # Etapa 2: Extração de dados
        dados = self.extrair_dados_pdf(caminho_pdf)
        if not dados:
            print("❌ Processo cancelado - falha na extração de dados.")
            return False
        
        # Etapa 3: Atualização da planilha
        sucesso = self.atualizar_planilha(dados)
        
        if sucesso:
            print("\n🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
            print("Os dados foram inseridos na planilha 'Cobrança Makino Irrigação'.")
        else:
            print("\n❌ AUTOMAÇÃO FALHOU!")
            print("Verifique os erros acima e tente novamente.")
        
        return sucesso

def main():
    """Função principal"""
    try:
        extrator = ExtratorOrcamento()
        extrator.executar_automacao()
    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()
