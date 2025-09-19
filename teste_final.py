#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final corrigido
"""

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def teste_final():
    print("🔍 TESTE FINAL DE CONEXÃO")
    print("=" * 40)
    
    try:
        # Configurar credenciais
        scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(
            "automacao-planilhas-472615-e62bc76ce2a2.json", 
            scopes=scope
        )
        
        # Testar Google Drive API
        print("📊 Testando Google Drive API...")
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Buscar planilhas (sem campos problemáticos)
        print("🔍 Buscando planilhas...")
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            fields="files(id, name, owners)",
            pageSize=20
        ).execute()
        
        files = results.get('files', [])
        print(f"📋 Encontradas {len(files)} planilhas:")
        
        planilha_encontrada = False
        
        for file in files:
            print(f"   - {file['name']}")
            print(f"     ID: {file['id']}")
            
            # Verificar proprietários
            if 'owners' in file:
                for owner in file['owners']:
                    print(f"     Proprietário: {owner.get('emailAddress', 'N/A')}")
            
            # Verificar se é a planilha que estamos procurando
            nome_arquivo = file['name'].lower()
            if 'makino' in nome_arquivo or 'cobrança' in nome_arquivo or 'cobranca' in nome_arquivo:
                print(f"     🎯 ESTA PARECE SER A PLANILHA CORRETA!")
                planilha_encontrada = True
                
                # Tentar abrir com gspread
                print(f"     🔗 Tentando abrir com gspread...")
                try:
                    gc = gspread.authorize(creds)
                    planilha = gc.open_by_key(file['id'])
                    print(f"     ✅ Sucesso! Planilha: {planilha.title}")
                    
                    # Listar abas
                    abas = planilha.worksheets()
                    print(f"     📊 Abas: {[aba.title for aba in abas]}")
                    
                    # Verificar se tem a aba "Pedidos"
                    aba_pedidos = None
                    for aba in abas:
                        if aba.title.lower() == 'pedidos':
                            aba_pedidos = aba
                            break
                    
                    if aba_pedidos:
                        print(f"     ✅ Aba 'Pedidos' encontrada!")
                        
                        # Verificar cabeçalhos
                        try:
                            cabecalhos = aba_pedidos.row_values(1)
                            print(f"     📋 Cabeçalhos: {cabecalhos}")
                        except:
                            print(f"     ⚠️ Não foi possível ler cabeçalhos")
                    else:
                        print(f"     ⚠️ Aba 'Pedidos' não encontrada")
                    
                    return file['id'], planilha.title
                    
                except Exception as e:
                    print(f"     ❌ Erro ao abrir: {str(e)}")
        
        if not planilha_encontrada and len(files) > 0:
            print(f"\n💡 Planilhas encontradas, mas nenhuma parece ser a correta.")
            print(f"   Procuramos por: 'makino', 'cobrança', 'cobranca'")
        
        if len(files) == 0:
            print("❌ Nenhuma planilha encontrada!")
            print("\n🔧 DIAGNÓSTICO:")
            print("   - As APIs estão funcionando")
            print("   - A conta de serviço está autenticada")
            print("   - Mas não consegue ver nenhuma planilha")
            print("\n💡 POSSÍVEIS CAUSAS:")
            print("   1. A planilha não foi compartilhada com a conta de serviço")
            print("   2. O compartilhamento ainda não foi efetivado (aguarde alguns minutos)")
            print("   3. A conta de serviço não tem permissão para listar arquivos")
            print("\n🎯 SOLUÇÃO:")
            print("   1. Vá para a planilha no Google Sheets")
            print("   2. Clique em 'Compartilhar'")
            print("   3. Adicione: robo-planilha-python@automacao-planilhas-472615.iam.gserviceaccount.com")
            print("   4. Defina como 'Editor'")
            print("   5. Aguarde 2-3 minutos")
            print("   6. Execute este teste novamente")
        
        return None, None
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None, None

if __name__ == "__main__":
    planilha_id, nome = teste_final()
    if planilha_id:
        print(f"\n🎉 SUCESSO!")
        print(f"   Planilha: {nome}")
        print(f"   ID: {planilha_id}")
    else:
        print(f"\n⚠️ Planilha não encontrada ou não acessível")
