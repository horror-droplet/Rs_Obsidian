#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度源泉徴収票解析スクリプト
"""

import pdfplumber
import re

def extract_gensen_data():
    """2023年源泉徴収票からデータを抽出"""
    pdf_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理/給与/2023/2023_源泉徴収.pdf'
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        print("📄 2023年源泉徴収票データ")
        print("="*50)
        
        # テキストの最初の部分を表示
        lines = text.split('\n')[:20]
        for i, line in enumerate(lines):
            if line.strip():
                print(f"{i+1:2d}: {line.strip()}")
        
        # 支払金額を抽出
        payment_patterns = [
            r'支払金額.*?(\d{1,3}(?:,\d{3})*)',
            r'(\d{1,3}(?:,\d{3})*)\s*円.*支払',
        ]
        
        for pattern in payment_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    amount = int(match.replace(',', ''))
                    if 7000000 <= amount <= 12000000:  # 妥当な年収範囲
                        print(f"\n💰 支払金額（年収）: ¥{amount:,}")
                        return amount
                except:
                    continue
        
        print("\n❌ 支払金額の抽出に失敗しました")
        return None
        
    except Exception as e:
        print(f"源泉徴収票読み取りエラー: {e}")
        return None

if __name__ == "__main__":
    extract_gensen_data()