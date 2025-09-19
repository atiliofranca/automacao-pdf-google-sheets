#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Orçamentos PDF - Versão Simples com Centralização Garantida
Permite selecionar um ou mais PDFs na mesma janela
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import re
import gspread
from google.oauth2.service_account import Credentials
import os

class ExtratorSimples:
    def __init__(self):
        self.credenciais_arquivo = "planilha-python-472618-f3c9ba25d174.json"
        self.planilha_nome = "Cobrança Makino Irrigação"
        self.aba_nome = "Pedidos"
        
    def centralizar_janela(self, root, largura=400, altura=200):
        """Centralizar janela de forma mais robusta"""
        # Forçar atualização
        root.update_idletasks()
        
        # Obter dimensões da tela
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        
        # Calcular posição central
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        
        # Aplicar geometria
        root.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Forçar atualização e centralização
        root.update()
        root.lift()
        root.focus_force()
        
        # Manter no topo temporariamente
        root.attributes('-topmost', True)
        root.after(300, lambda: root.attributes('-topmost', False))
        
        # Garantir que está visível
        root.deiconify()
        
    def selecionar_pdfs(self):
        """Selecionar PDFs com janela centralizada"""
        # Criar janela temporária para centralizar o diálogo
        temp_root = tk.Tk()
        temp_root.withdraw()
        
        # Configurar posição central
        largura_tela = temp_root.winfo_screenwidth()
        altura_tela = temp_root.winfo_screenheight()
        
        # Centralizar janela temporária
        x = (largura_tela - 400) // 2
        y = (altura_tela - 300) // 2
        temp_root.geometry(f"400x300+{x}+{y}")
        
        # Tornar visível brevemente para centralizar o diálogo
        temp_root.deiconify()
        temp_root.update()
        temp_root.withdraw()
        
        # Abrir diálogo de seleção
        caminhos_arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos PDF de orçamento",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
            parent=temp_root
        )
        
        temp_root.destroy()
        
        if not caminhos_arquivos:
            return []
        
        return list(caminhos_arquivos)
    
    def extrair_dados_pdf(self, caminho_pdf):
        """Extrair dados do PDF"""
        try:
            # Abrir o PDF
            doc = fitz.open(caminho_pdf)
            texto_completo = ""
            
            # Extrair texto de todas as páginas
            for pagina_num in range(len(doc)):
                pagina = doc.load_page(pagina_num)
                texto_completo += pagina.get_text() + "\n"
            
            doc.close()
            
            # Aplicar regex para extrair os dados
            dados = self._aplicar_regex(texto_completo)
            
            if dados:
                return dados
            else:
                return None
                
        except Exception as e:
            return None
    
    def _aplicar_regex(self, texto):
        """Aplicar expressões regulares para extrair dados"""
        dados = {}
        
        # Regex para Cliente
        padrao_cliente = r"Cliente:\s*(.+?)(?:\n|$)"
        match_cliente = re.search(padrao_cliente, texto, re.IGNORECASE | re.MULTILINE)
        if match_cliente:
            dados['CLIENTE'] = match_cliente.group(1).strip()
        
        # Regex para Número do Pedido
        padrao_pedido = r"PEDIDO\s*N[°ºo]\s*(\d+)"
        match_pedido = re.search(padrao_pedido, texto, re.IGNORECASE)
        if match_pedido:
            dados['NUMERO DO PEDIDO'] = match_pedido.group(1)
        
        # Regex para Data
        padrao_data = r"Data\s*Emiss[ãa]o:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
        match_data = re.search(padrao_data, texto, re.IGNORECASE)
        if match_data:
            dados['DATA'] = match_data.group(1)
        
        # Regex para Valor
        padrao_valor = r"TOTAL:\s*\n.*?Vendedor:.*?\n.*?\n\s*([\d.,]+)"
        match_valor = re.search(padrao_valor, texto, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        if match_valor:
            valor_str = match_valor.group(1).strip()
            valor_limpo = valor_str.replace('.', '').replace(',', '.')
            try:
                valor_float = float(valor_limpo)
                dados['VALOR'] = f"{valor_float:.2f}"
            except ValueError:
                dados['VALOR'] = valor_str
        
        # Verificar se todos os campos obrigatórios foram encontrados
        campos_obrigatorios = ['CLIENTE', 'NUMERO DO PEDIDO', 'DATA', 'VALOR']
        campos_encontrados = [campo for campo in campos_obrigatorios if campo in dados]
        
        if len(campos_encontrados) < len(campos_obrigatorios):
            return None
        
        return dados
    
    def inserir_dados_planilha(self, dados_list):
        """Inserir dados na planilha Google Sheets"""
        try:
            # Configurar credenciais
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credenciais_arquivo, 
                scopes=scope
            )
            
            # Conectar ao Google Sheets
            gc = gspread.authorize(creds)
            
            # Abrir a planilha
            planilha = gc.open(self.planilha_nome)
            aba = planilha.worksheet(self.aba_nome)
            
            # Preparar dados para inserção
            linhas_dados = []
            for dados in dados_list:
                linha_dados = [
                    dados.get('CLIENTE', ''),
                    dados.get('NUMERO DO PEDIDO', ''),
                    dados.get('DATA', ''),
                    dados.get('VALOR', ''),
                    ''  # RETIRADO POR - deixado em branco
                ]
                linhas_dados.append(linha_dados)
            
            # Inserir dados
            aba.append_rows(linhas_dados)
            
            return True
            
        except Exception as e:
            return False
    
    def mostrar_janela_sucesso(self, sucessos, total):
        """Mostrar janela de sucesso centralizada"""
        # Criar janela
        root = tk.Tk()
        root.title("Extração Concluída")
        root.resizable(False, False)
        
        # Configurar estilo
        root.configure(bg='#f0f0f0')
        
        # Configurar tamanho e centralizar
        largura = 400
        altura = 200
        self.centralizar_janela(root, largura, altura)
        
        # Ícone de sucesso
        icone_label = tk.Label(
            root,
            text="✅",
            font=("Arial", 48),
            bg='#f0f0f0',
            fg='#27ae60'
        )
        icone_label.pack(pady=20)
        
        # Mensagem principal
        if sucessos == total:
            mensagem = f"Extração concluída com sucesso!\n\n{sucessos} arquivo(s) processado(s)."
            cor = '#27ae60'
        else:
            mensagem = f"Extração concluída!\n\n{sucessos} de {total} arquivo(s) processado(s)."
            cor = '#f39c12'
        
        mensagem_label = tk.Label(
            root,
            text=mensagem,
            font=("Arial", 12),
            bg='#f0f0f0',
            fg=cor,
            justify='center'
        )
        mensagem_label.pack(pady=10)
        
        # Botão OK
        botao_ok = tk.Button(
            root,
            text="OK",
            font=("Arial", 10, "bold"),
            bg='#3498db',
            fg='white',
            width=10,
            height=2,
            command=root.destroy,
            relief='flat'
        )
        botao_ok.pack(pady=20)
        
        # Executar janela
        root.mainloop()
    
    def executar(self):
        """Executar o processo completo"""
        # Selecionar PDFs
        caminhos_pdfs = self.selecionar_pdfs()
        if not caminhos_pdfs:
            return
        
        # Processar cada PDF
        dados_validos = []
        sucessos = 0
        falhas = 0
        
        for caminho_pdf in caminhos_pdfs:
            dados = self.extrair_dados_pdf(caminho_pdf)
            
            if dados:
                dados_validos.append(dados)
                sucessos += 1
            else:
                falhas += 1
        
        # Inserir dados válidos na planilha
        if dados_validos:
            if self.inserir_dados_planilha(dados_validos):
                # Mostrar janela de sucesso
                self.mostrar_janela_sucesso(sucessos, len(caminhos_pdfs))
            else:
                # Mostrar janela de erro
                self.mostrar_janela_erro()
        else:
            # Mostrar janela de erro
            self.mostrar_janela_erro()
    
    def mostrar_janela_erro(self):
        """Mostrar janela de erro centralizada"""
        # Criar janela
        root = tk.Tk()
        root.title("Erro na Extração")
        root.resizable(False, False)
        
        # Configurar estilo
        root.configure(bg='#f0f0f0')
        
        # Configurar tamanho e centralizar
        largura = 400
        altura = 200
        self.centralizar_janela(root, largura, altura)
        
        # Ícone de erro
        icone_label = tk.Label(
            root,
            text="❌",
            font=("Arial", 48),
            bg='#f0f0f0',
            fg='#e74c3c'
        )
        icone_label.pack(pady=20)
        
        # Mensagem de erro
        mensagem_label = tk.Label(
            root,
            text="Erro na extração dos dados!\n\nNenhum arquivo foi processado com sucesso.",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#e74c3c',
            justify='center'
        )
        mensagem_label.pack(pady=10)
        
        # Botão OK
        botao_ok = tk.Button(
            root,
            text="OK",
            font=("Arial", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            width=10,
            height=2,
            command=root.destroy,
            relief='flat'
        )
        botao_ok.pack(pady=20)
        
        # Executar janela
        root.mainloop()

def main():
    """Função principal"""
    try:
        extrator = ExtratorSimples()
        extrator.executar()
    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro: {str(e)}")

if __name__ == "__main__":
    main()
