#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF文字データ高精度抽出スクリプト
文字データが埋め込まれたPDFから早出残業手当を正確に抽出
"""

import os
import glob
import re
import pdfplumber
# import pandas as pd

def extract_text_precisely(pdf_path):
    """pdfplumberを使用して高精度でテキストを抽出"""
    text_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # テキスト抽出
                text = page.extract_text()
                if text:
                    text_data.append(text)
                
                # テーブル抽出も併用
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and any(cell for cell in row if cell):
                            # テーブルの行をテキストに変換
                            row_text = " | ".join([str(cell) if cell else "" for cell in row])
                            text_data.append(row_text)
    
    except Exception as e:
        print(f"PDF読み取りエラー ({pdf_path}): {e}")
        return ""
    
    return "\n".join(text_data)

def extract_overtime_data(text, filename):
    """テキストから早出残業手当の詳細を抽出"""
    data = {
        'filename': filename,
        'year_month': None,
        'overtime_allowance': None,
        'overtime_hours': None,
        'hourly_rate': None,
        'total_payment': None
    }
    
    # ファイル名から年月を抽出
    month_match = re.search(r'2024-(\d{2})', filename)
    if month_match:
        data['year_month'] = f"2024-{month_match.group(1)}"
    
    # 複数のパターンで早出残業手当を検索
    overtime_patterns = [
        r'早出残業手当\s*[|\s]*(\d{1,3}(?:,\d{3})*)',
        r'早出残業手当.*?(\d{1,3}(?:,\d{3})*)',
        r'早出.*?残業.*?(\d{1,3}(?:,\d{3})*)',
    ]
    
    for pattern in overtime_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                amount = int(match.replace(',', ''))
                if 50000 <= amount <= 200000:  # 妥当な範囲
                    data['overtime_allowance'] = amount
                    break
            except:
                continue
        if data['overtime_allowance']:
            break
    
    # 早出残業時間を抽出
    time_patterns = [
        r'早出残業時間\s*[|\s]*(\d+\.?\d*)',
        r'早出残業時間.*?(\d+\.?\d*)',
    ]
    
    for pattern in time_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                hours = float(match)
                if 15 <= hours <= 50:  # 妥当な範囲
                    data['overtime_hours'] = hours
                    break
            except:
                continue
        if data['overtime_hours']:
            break
    
    # 総支給額を抽出
    payment_patterns = [
        r'支給額合計\s*[|\s]*(\d{1,3}(?:,\d{3})*)',
        r'総支給.*?(\d{1,3}(?:,\d{3})*)',
    ]
    
    for pattern in payment_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                amount = int(match.replace(',', ''))
                if 400000 <= amount <= 1500000:  # 妥当な範囲
                    data['total_payment'] = amount
                    break
            except:
                continue
        if data['total_payment']:
            break
    
    # 時間単価を計算
    if data['overtime_allowance'] and data['overtime_hours']:
        data['hourly_rate'] = data['overtime_allowance'] / data['overtime_hours']
    
    return data

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理/給与/2024'
    
    # 通常給与ファイルのみ処理（特別一時金を除く）
    pdf_files = [f for f in glob.glob(os.path.join(base_path, '*.pdf')) 
                 if '給与' in f and '特別一時金' not in f and '源泉徴収' not in f]
    pdf_files.sort()
    
    print("🔍 高精度PDF文字データ抽出開始...")
    print("="*70)
    
    all_data = []
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        print(f"\n📄 処理中: {filename}")
        
        # テキスト抽出
        text = extract_text_precisely(pdf_file)
        
        if text:
            # 一部のテキストを表示（デバッグ用）
            preview_lines = text.split('\n')[:10]
            print("📝 抽出テキスト（最初の10行）:")
            for i, line in enumerate(preview_lines):
                if line.strip():
                    print(f"  {i+1:2d}: {line.strip()}")
            
            # 早出残業データを抽出
            data = extract_overtime_data(text, filename)
            all_data.append(data)
            
            # 結果表示
            print(f"📊 抽出結果:")
            print(f"  年月: {data['year_month']}")
            print(f"  総支給額: ¥{data['total_payment']:,}" if data['total_payment'] else "  総支給額: 抽出失敗")
            print(f"  早出残業手当: ¥{data['overtime_allowance']:,}" if data['overtime_allowance'] else "  早出残業手当: 抽出失敗")
            print(f"  早出残業時間: {data['overtime_hours']}時間" if data['overtime_hours'] else "  早出残業時間: 抽出失敗")
            print(f"  時間単価: ¥{data['hourly_rate']:,.0f}/時間" if data['hourly_rate'] else "  時間単価: 計算不可")
        else:
            print("❌ テキスト抽出失敗")
    
    # 成功したデータの集計
    successful_data = [d for d in all_data if d['overtime_allowance'] and d['overtime_hours']]
    
    print(f"\n📋 2024年 早出残業手当 集計結果")
    print("="*70)
    print(f"成功数: {len(successful_data)}/{len(all_data)} ファイル")
    
    if successful_data:
        print(f"\n{'月':<10} {'総支給額':<12} {'早出残業手当':<12} {'時間':<8} {'時間単価':<10}")
        print("-"*70)
        
        total_allowance = 0
        total_hours = 0
        
        for data in sorted(successful_data, key=lambda x: x['year_month'] or ''):
            total_allowance += data['overtime_allowance']
            total_hours += data['overtime_hours']
            
            print(f"{data['year_month']:<10} "
                  f"¥{data['total_payment']:,>10} " if data['total_payment'] else f"{'不明':<12} "
                  f"¥{data['overtime_allowance']:,>10} "
                  f"{data['overtime_hours']:>6.1f}時間 "
                  f"¥{data['hourly_rate']:>8,.0f}")
        
        print("-"*70)
        avg_rate = total_allowance / total_hours if total_hours > 0 else 0
        print(f"{'合計/平均':<10} {'':>12} ¥{total_allowance:,>10} {total_hours:>6.1f}時間 ¥{avg_rate:>8,.0f}")
        
        # 年間推定
        if len(successful_data) >= 3:
            monthly_avg = total_allowance / len(successful_data)
            annual_estimate = monthly_avg * 12
            print(f"\n💡 年間推定早出残業手当: ¥{annual_estimate:,.0f}")
            print(f"💡 月平均早出残業手当: ¥{monthly_avg:,.0f}")
            print(f"💡 平均時間単価: ¥{avg_rate:,.0f}")
    
    return all_data

if __name__ == "__main__":
    data = main()