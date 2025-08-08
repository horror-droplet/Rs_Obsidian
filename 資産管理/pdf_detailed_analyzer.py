#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
給与明細PDF詳細項目解析スクリプト
早出残業手当などの具体的項目を抽出
"""

import os
import glob
import re
from pathlib import Path
import PyPDF2
import pdfplumber

def extract_detailed_salary_items(pdf_path):
    """給与明細から詳細項目を抽出"""
    filename = os.path.basename(pdf_path)
    
    # 両方の方法でテキスト抽出
    text_pypdf2 = ""
    text_pdfplumber = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text_pypdf2 += page.extract_text()
    except Exception as e:
        print(f"PyPDF2エラー: {e}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pdfplumber += page_text + "\n"
    except Exception as e:
        print(f"pdfplumberエラー: {e}")
    
    # より詳細な分析のため両方のテキストを使用
    combined_text = text_pypdf2 + "\n" + text_pdfplumber
    
    # デバッグ情報を最小限に抑制
    # print(f"\n{'='*60}")
    # print(f"ファイル: {filename}")
    # print(f"{'='*60}")
    
    # 早出残業関連のキーワードパターン
    overtime_patterns = [
        r'早出.*?(\d+(?:,\d+)*)',
        r'残業.*?(\d+(?:,\d+)*)',
        r'時間外.*?(\d+(?:,\d+)*)',
        r'超過.*?(\d+(?:,\d+)*)',
        r'深夜.*?(\d+(?:,\d+)*)',
        r'休日.*?(\d+(?:,\d+)*)',
        r'割増.*?(\d+(?:,\d+)*)'
    ]
    
    # 文字化けパターンも考慮した検索
    garbled_patterns = [
        r'[^\w\s]{2,}(\d+(?:,\d+)*)',  # 文字化け文字の後の数値
        r'(\d+(?:,\d+)*)[^\w\s]{2,}',  # 数値の後の文字化け文字
    ]
    
    found_items = []
    
    # 行ごとに分析
    lines = combined_text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # 数値を含む行を検出
        if re.search(r'\d+(?:,\d+)*', line):
            # 前後の行も含めて分析
            context_lines = []
            for j in range(max(0, i-2), min(len(lines), i+3)):
                context_lines.append(lines[j].strip())
            
            context = ' '.join(context_lines)
            
            # パターンマッチング
            for pattern in overtime_patterns:
                matches = re.findall(pattern, context)
                if matches:
                    found_items.append({
                        'pattern': pattern,
                        'matches': matches,
                        'context': context[:100],
                        'line_number': i
                    })
            
            # print(f"行 {i:3d}: {line[:80]}...")
    
    # 数値のリストを抽出
    all_numbers = re.findall(r'\d{1,3}(?:,\d{3})+|\d{4,}', combined_text)
    unique_numbers = sorted(list(set([int(n.replace(',', '')) for n in all_numbers if int(n.replace(',', '')) >= 1000])), reverse=True)
    
    # 詳細出力を抑制
    # print(f"\n抽出された数値（上位20個）:")
    # for i, num in enumerate(unique_numbers[:20]):
    #     print(f"{i+1:2d}. ¥{num:,}")
    # 
    # print(f"\n検出されたパターン:")
    # for item in found_items:
    #     print(f"パターン: {item['pattern']}")
    #     print(f"マッチ: {item['matches']}")
    #     print(f"コンテキスト: {item['context']}")
    #     print(f"行番号: {item['line_number']}")
    #     print("-" * 40)
    
    # テーブル抽出も試行（出力は抑制）
    # try:
    #     with pdfplumber.open(pdf_path) as pdf:
    #         for page_num, page in enumerate(pdf.pages):
    #             tables = page.extract_tables()
    #             if tables:
    #                 print(f"\nページ {page_num + 1} のテーブル:")
    #                 for table_num, table in enumerate(tables):
    #                     print(f"テーブル {table_num + 1}:")
    #                     for row_num, row in enumerate(table[:10]):  # 最初の10行まで
    #                         if row and any(cell for cell in row if cell and cell.strip()):
    #                             print(f"  行{row_num}: {[cell.strip() if cell else '' for cell in row]}")
    #                     if len(table) > 10:
    #                         print(f"  ... (他 {len(table) - 10} 行)")
    #                     print()
    # except Exception as e:
    #     print(f"テーブル抽出エラー: {e}")
    
    return {
        'filename': filename,
        'numbers': unique_numbers,
        'patterns': found_items,
        'raw_text_length': len(combined_text)
    }

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理/給与/2024'
    
    # 給与PDFファイルを分析（特別一時金を除く通常給与のみ）
    pdf_files = [f for f in glob.glob(os.path.join(base_path, '*給与.pdf')) if '特別一時金' not in f]
    pdf_files.sort()
    
    print("早出残業手当等の詳細項目解析を開始...")
    
    # 全ての給与ファイルを分析
    overtime_data = []
    
    for pdf_file in pdf_files:
        result = extract_detailed_salary_items(pdf_file)
        
        # 早出残業手当と時間を抽出
        overtime_amount = None
        overtime_hours = None
        year_month = None
        
        # ファイル名から年月を抽出
        match = re.search(r'(2024-\d{2})', result['filename'])
        if match:
            year_month = match.group(1)
        
        # 早出残業手当の金額を抽出（テーブルデータから確実に取得）
        for pattern_result in result['patterns']:
            if '早出' in pattern_result['pattern']:
                for match_val in pattern_result['matches']:
                    if match_val not in ['26', '27', '28', '29', '30', '31', '32', '0']:  # 時間データを除外
                        try:
                            amount = int(match_val.replace(',', ''))
                            if 80000 <= amount <= 150000:  # 早出残業手当の妥当な範囲
                                overtime_amount = amount
                                break
                        except:
                            continue
                if overtime_amount:
                    break
        
        # 早出残業時間を抽出（より詳細なパターンマッチング）
        time_pattern = r'早出残業時間\s+(\d+\.?\d*)'
        # 時間抽出用のテキスト処理
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text_for_time = ""
                for page in reader.pages:
                    text_for_time += page.extract_text()
                    
            for line in text_for_time.split('\n'):
                if '早出残業時間' in line:
                    match = re.search(time_pattern, line)
                    if match:
                        try:
                            hours = float(match.group(1))
                            if 20 <= hours <= 35:  # 妥当な早出残業時間範囲
                                overtime_hours = hours
                                break
                        except:
                            continue
        except:
            pass
        
        # バックアップとして従来の方法も試行
        if not overtime_hours:
            for pattern_result in result['patterns']:
                if '早出' in pattern_result['pattern']:
                    for match_val in pattern_result['matches']:
                        if match_val in ['26', '27', '28', '29', '30']:  # 時間データ
                            try:
                                hours = float(match_val)
                                if 20 <= hours <= 35:
                                    overtime_hours = hours
                                    break
                            except:
                                continue
                    if overtime_hours:
                        break
        
        # デバッグ情報を簡潔に表示
        print(f"📊 {result['filename']}: ", end="")
        if overtime_amount and overtime_hours and year_month:
            hourly_rate = overtime_amount / overtime_hours
            print(f"早出残業手当 ¥{overtime_amount:,} ({overtime_hours}時間, ¥{hourly_rate:,.0f}/時間)")
            overtime_data.append({
                'year_month': year_month,
                'filename': result['filename'],
                'overtime_amount': overtime_amount,
                'overtime_hours': overtime_hours,
                'hourly_rate': hourly_rate
            })
        else:
            print("データ抽出失敗")
    
    # 結果を整理して表示
    print(f"\n📋 2024年 早出残業手当 完全データ（{len(overtime_data)}ヶ月分）")
    print("="*70)
    print(f"{'月':<8} {'早出残業手当':<12} {'時間':<8} {'時間単価':<10}")
    print("-"*70)
    
    total_amount = 0
    total_hours = 0
    
    for data in sorted(overtime_data, key=lambda x: x['year_month']):
        print(f"{data['year_month']:<8} ¥{data['overtime_amount']:,>10} {data['overtime_hours']:>6.2f}時間 ¥{data['hourly_rate']:>8,.0f}")
        total_amount += data['overtime_amount']
        total_hours += data['overtime_hours']
    
    if overtime_data:
        avg_rate = total_amount / total_hours
        print("-"*70)
        print(f"{'合計':<8} ¥{total_amount:,>10} {total_hours:>6.1f}時間 ¥{avg_rate:>8,.0f}")
        print(f"\n💡 年間早出残業代総額: ¥{total_amount:,}")
        print(f"💡 平均月間早出残業時間: {total_hours/len(overtime_data):.1f}時間")
        print(f"💡 平均時間単価: ¥{avg_rate:,.0f}/時間")
    
    return overtime_data

if __name__ == "__main__":
    main()