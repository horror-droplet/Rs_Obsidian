#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023年度PDF文字データ高精度抽出スクリプト
文字データが埋め込まれたPDFから早出残業手当を正確に抽出
"""

import os
import glob
import re
import pdfplumber

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
    month_match = re.search(r'2023-(\d{2})', filename)
    if month_match:
        data['year_month'] = f"2023-{month_match.group(1)}"
    
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

def extract_bonus_data(text, filename):
    """特別一時金データを抽出"""
    data = {
        'filename': filename,
        'year_month': None,
        'bonus_amount': None,
        'net_bonus': None
    }
    
    # ファイル名から年月を抽出
    month_match = re.search(r'2023-(\d{2})', filename)
    if month_match:
        data['year_month'] = f"2023-{month_match.group(1)}"
    
    # 特別一時金の総支給額を抽出
    bonus_patterns = [
        r'支給額合計\s*[|\s]*(\d{1,3}(?:,\d{3})*)',
        r'総支給.*?(\d{1,3}(?:,\d{3})*)',
    ]
    
    for pattern in bonus_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                amount = int(match.replace(',', ''))
                if 500000 <= amount <= 2000000:  # ボーナスの妥当な範囲
                    data['bonus_amount'] = amount
                    break
            except:
                continue
        if data['bonus_amount']:
            break
    
    # 差引支給額（手取り）を抽出
    net_patterns = [
        r'差引支給額\s*[|\s]*(\d{1,3}(?:,\d{3})*)',
    ]
    
    for pattern in net_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                amount = int(match.replace(',', ''))
                if 400000 <= amount <= 1800000:  # 手取りボーナスの妥当な範囲
                    data['net_bonus'] = amount
                    break
            except:
                continue
        if data['net_bonus']:
            break
    
    return data

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理/給与/2023'
    
    # 通常給与ファイルのみ処理（特別一時金を除く）
    salary_files = [f for f in glob.glob(os.path.join(base_path, '*.pdf')) 
                   if '給与' in f and '特別一時金' not in f and '源泉徴収' not in f]
    salary_files.sort()
    
    # 特別一時金ファイル
    bonus_files = [f for f in glob.glob(os.path.join(base_path, '*特別一時金*.pdf'))]
    bonus_files.sort()
    
    print("🔍 2023年度 高精度PDF文字データ抽出開始...")
    print("="*70)
    
    all_salary_data = []
    all_bonus_data = []
    
    # 給与データの処理
    print("\n📊 月次給与データの処理")
    print("-"*50)
    
    for pdf_file in salary_files:
        filename = os.path.basename(pdf_file)
        print(f"\n📄 処理中: {filename}")
        
        # テキスト抽出
        text = extract_text_precisely(pdf_file)
        
        if text:
            # 早出残業データを抽出
            data = extract_overtime_data(text, filename)
            all_salary_data.append(data)
            
            # 結果表示
            print(f"📊 抽出結果:")
            print(f"  年月: {data['year_month']}")
            print(f"  総支給額: ¥{data['total_payment']:,}" if data['total_payment'] else "  総支給額: 抽出失敗")
            print(f"  早出残業手当: ¥{data['overtime_allowance']:,}" if data['overtime_allowance'] else "  早出残業手当: 抽出失敗")
            print(f"  早出残業時間: {data['overtime_hours']}時間" if data['overtime_hours'] else "  早出残業時間: 抽出失敗")
            print(f"  時間単価: ¥{data['hourly_rate']:,.0f}/時間" if data['hourly_rate'] else "  時間単価: 計算不可")
        else:
            print("❌ テキスト抽出失敗")
    
    # 特別一時金データの処理
    print(f"\n💰 特別一時金データの処理")
    print("-"*50)
    
    for pdf_file in bonus_files:
        filename = os.path.basename(pdf_file)
        print(f"\n📄 処理中: {filename}")
        
        # テキスト抽出
        text = extract_text_precisely(pdf_file)
        
        if text:
            # ボーナスデータを抽出
            data = extract_bonus_data(text, filename)
            all_bonus_data.append(data)
            
            # 結果表示
            print(f"📊 抽出結果:")
            print(f"  年月: {data['year_month']}")
            print(f"  特別一時金総額: ¥{data['bonus_amount']:,}" if data['bonus_amount'] else "  特別一時金総額: 抽出失敗")
            print(f"  手取り額: ¥{data['net_bonus']:,}" if data['net_bonus'] else "  手取り額: 抽出失敗")
        else:
            print("❌ テキスト抽出失敗")
    
    # 成功したデータの集計
    successful_salary_data = [d for d in all_salary_data if d['overtime_allowance'] and d['overtime_hours']]
    successful_bonus_data = [d for d in all_bonus_data if d['bonus_amount']]
    
    print(f"\n📋 2023年 給与・残業手当 集計結果")
    print("="*70)
    print(f"給与データ成功数: {len(successful_salary_data)}/{len(all_salary_data)} ファイル")
    print(f"ボーナスデータ成功数: {len(successful_bonus_data)}/{len(all_bonus_data)} ファイル")
    
    if successful_salary_data:
        print(f"\n【月次給与・早出残業手当】")
        print(f"{'月':<10} {'総支給額':<12} {'早出残業手当':<12} {'時間':<8} {'時間単価':<10}")
        print("-"*70)
        
        total_allowance = 0
        total_hours = 0
        total_payment = 0
        
        for data in sorted(successful_salary_data, key=lambda x: x['year_month'] or ''):
            total_allowance += data['overtime_allowance']
            total_hours += data['overtime_hours']
            if data['total_payment']:
                total_payment += data['total_payment']
            
            print(f"{data['year_month']:<10} "
                  f"¥{data['total_payment']:,>10} " if data['total_payment'] else f"{'不明':<12} "
                  f"¥{data['overtime_allowance']:,>10} "
                  f"{data['overtime_hours']:>6.1f}時間 "
                  f"¥{data['hourly_rate']:>8,.0f}")
        
        print("-"*70)
        avg_rate = total_allowance / total_hours if total_hours > 0 else 0
        print(f"{'合計/平均':<10} ¥{total_payment:,>10} ¥{total_allowance:,>10} {total_hours:>6.1f}時間 ¥{avg_rate:>8,.0f}")
        
        # 月平均計算
        monthly_avg_allowance = total_allowance / len(successful_salary_data) if successful_salary_data else 0
        monthly_avg_hours = total_hours / len(successful_salary_data) if successful_salary_data else 0
        
        print(f"\n💡 月次給与統計:")
        print(f"💡 年間早出残業手当総額: ¥{total_allowance:,.0f}")
        print(f"💡 月平均早出残業手当: ¥{monthly_avg_allowance:,.0f}")
        print(f"💡 月平均早出残業時間: {monthly_avg_hours:.1f}時間")
        print(f"💡 平均時間単価: ¥{avg_rate:,.0f}")
    
    if successful_bonus_data:
        print(f"\n【特別一時金（ボーナス）】")
        print(f"{'月':<10} {'総支給額':<15} {'手取り額':<15}")
        print("-"*50)
        
        total_bonus = 0
        total_net_bonus = 0
        
        for data in sorted(successful_bonus_data, key=lambda x: x['year_month'] or ''):
            total_bonus += data['bonus_amount'] if data['bonus_amount'] else 0
            total_net_bonus += data['net_bonus'] if data['net_bonus'] else 0
            
            print(f"{data['year_month']:<10} "
                  f"¥{data['bonus_amount']:,>13} " if data['bonus_amount'] else f"{'不明':<15} "
                  f"¥{data['net_bonus']:,>13}" if data['net_bonus'] else f"{'不明':<15}")
        
        print("-"*50)
        print(f"{'合計':<10} ¥{total_bonus:,>13} ¥{total_net_bonus:,>13}")
        
        print(f"\n💡 ボーナス統計:")
        print(f"💡 年間ボーナス総額: ¥{total_bonus:,.0f}")
        print(f"💡 年間ボーナス手取り: ¥{total_net_bonus:,.0f}")
        print(f"💡 ボーナス控除率: {((total_bonus - total_net_bonus) / total_bonus * 100):.1f}%" if total_bonus > 0 else "💡 ボーナス控除率: 計算不可")
    
    # 年間合計
    if successful_salary_data or successful_bonus_data:
        annual_salary_total = total_payment if successful_salary_data else 0
        annual_bonus_total = total_bonus if successful_bonus_data else 0
        annual_total = annual_salary_total + annual_bonus_total
        
        print(f"\n🎯 2023年度 年間収入総計")
        print("="*50)
        print(f"月次給与総計: ¥{annual_salary_total:,}")
        print(f"ボーナス総計: ¥{annual_bonus_total:,}")
        print(f"年収総計: ¥{annual_total:,}")
        
        if successful_salary_data:
            overtime_ratio = (total_allowance / annual_total * 100) if annual_total > 0 else 0
            print(f"早出残業手当比率: {overtime_ratio:.1f}%")
    
    return {
        'salary_data': successful_salary_data,
        'bonus_data': successful_bonus_data
    }

if __name__ == "__main__":
    data = main()