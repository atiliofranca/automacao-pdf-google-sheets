#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização simples
"""

import os
import sys

def main():
    print("🚀 Iniciando Extrator de Orçamentos PDF...")
    
    # Verificar se o arquivo existe
    if not os.path.exists("extrator_simples.py"):
        print("❌ Arquivo extrator_simples.py não encontrado!")
        input("Pressione Enter para sair...")
        return
    
    # Executar o extrator
    try:
        os.system("python extrator_simples.py")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
