#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o Extrator de Orçamentos PDF
Testa as funcionalidades principais sem precisar de arquivo PDF real
"""

import os
import json
from extrator_orcamento import ExtratorOrcamento

def testar_credenciais():
    """Testar se as credenciais estão configuradas corretamente"""
    print("=== TESTE 1: Verificação de Credenciais ===")
    
    arquivo_credenciais = "automacao-planilhas-472615-e62bc76ce2a2.json"
    
    if not os.path.exists(arquivo_credenciais):
        print("❌ Arquivo de credenciais não encontrado!")
        return False
    
    try:
        with open(arquivo_credenciais, 'r') as f:
            creds = json.load(f)
        
        campos_necessarios = ['type', 'project_id', 'private_key', 'client_email']
        for campo in campos_necessarios:
            if campo not in creds:
                print(f"❌ Campo '{campo}' não encontrado nas credenciais!")
                return False
        
        print(f"✅ Credenciais válidas!")
        print(f"   Projeto: {creds['project_id']}")
        print(f"   Email: {creds['client_email']}")
        return True
        
    except json.JSONDecodeError:
        print("❌ Arquivo de credenciais inválido (JSON malformado)!")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar credenciais: {str(e)}")
        return False

def testar_regex():
    """Testar as expressões regulares com dados de exemplo"""
    print("\n=== TESTE 2: Teste das Expressões Regulares ===")
    
    # Texto de exemplo simulando um PDF de orçamento
    texto_exemplo = """
    ORÇAMENTO DE IRRIGAÇÃO
    
    Cliente: João Silva Agricultura Ltda
    Endereço: Rua das Flores, 123
    
    PEDIDO N° 12345
    
    Data Emissão: 15/12/2024
    
    Itens:
    - Sistema de irrigação por gotejamento
    - Mangueiras 16mm
    - Gotejadores
    
    TOTAL: R$ 1.500,00
    
    Obrigado pela preferência!
    """
    
    extrator = ExtratorOrcamento()
    dados = extrator._aplicar_regex(texto_exemplo)
    
    if dados:
        print("✅ Regex funcionando corretamente!")
        print("Dados extraídos:")
        for chave, valor in dados.items():
            print(f"   {chave}: {valor}")
        return True
    else:
        print("❌ Falha na extração de dados!")
        return False

def testar_conexao_google_sheets():
    """Testar conexão com Google Sheets (sem inserir dados)"""
    print("\n=== TESTE 3: Teste de Conexão com Google Sheets ===")
    
    try:
        from google.oauth2.service_account import Credentials
        import gspread
        
        # Configurar credenciais
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(
            "automacao-planilhas-472615-e62bc76ce2a2.json", 
            scopes=scope
        )
        
        # Conectar ao Google Sheets
        gc = gspread.authorize(creds)
        
        # Tentar abrir a planilha
        try:
            planilha = gc.open("Cobrança Makino Irrigação")
            print("✅ Planilha encontrada!")
            
            # Verificar se a aba existe
            try:
                aba = planilha.worksheet("Pedidos")
                print("✅ Aba 'Pedidos' encontrada!")
                
                # Verificar estrutura das colunas
                cabecalhos = aba.row_values(1)
                print(f"   Cabeçalhos encontrados: {cabecalhos}")
                
                return True
                
            except gspread.exceptions.WorksheetNotFound:
                print("❌ Aba 'Pedidos' não encontrada!")
                print("   Certifique-se de que a aba existe na planilha.")
                return False
                
        except gspread.exceptions.SpreadsheetNotFound:
            print("❌ Planilha 'Cobrança Makino Irrigação' não encontrada!")
            print("   Certifique-se de que a planilha existe e está compartilhada.")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

def testar_dependencias():
    """Testar se todas as dependências estão instaladas"""
    print("\n=== TESTE 4: Verificação de Dependências ===")
    
    dependencias = [
        ('tkinter', 'Interface gráfica'),
        ('fitz', 'PyMuPDF - Extração de PDF'),
        ('gspread', 'Google Sheets API'),
        ('google.oauth2.service_account', 'Autenticação Google'),
        ('re', 'Expressões regulares'),
        ('json', 'Processamento JSON')
    ]
    
    todas_ok = True
    
    for modulo, descricao in dependencias:
        try:
            if modulo == 'fitz':
                import fitz
            elif modulo == 'tkinter':
                import tkinter
            elif modulo == 'gspread':
                import gspread
            elif modulo == 'google.oauth2.service_account':
                from google.oauth2.service_account import Credentials
            elif modulo == 're':
                import re
            elif modulo == 'json':
                import json
            
            print(f"✅ {descricao}")
            
        except ImportError:
            print(f"❌ {descricao} - Módulo '{modulo}' não encontrado!")
            todas_ok = False
    
    return todas_ok

def main():
    """Executar todos os testes"""
    print("🧪 INICIANDO TESTES DO SISTEMA")
    print("=" * 50)
    
    testes = [
        ("Dependências", testar_dependencias),
        ("Credenciais", testar_credenciais),
        ("Expressões Regulares", testar_regex),
        ("Conexão Google Sheets", testar_conexao_google_sheets)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado no teste '{nome_teste}': {str(e)}")
            resultados.append((nome_teste, False))
    
    # Resumo dos testes
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    testes_ok = 0
    total_testes = len(resultados)
    
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste:<25} {status}")
        if resultado:
            testes_ok += 1
    
    print(f"\nResultado Final: {testes_ok}/{total_testes} testes passaram")
    
    if testes_ok == total_testes:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O sistema está pronto para uso.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima antes de usar o sistema.")
    
    return testes_ok == total_testes

if __name__ == "__main__":
    main()
