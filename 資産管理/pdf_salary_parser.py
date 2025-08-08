#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
給与PDFファイル詳細解析スクリプト
文字化けしたテキストからでも数値パターンを抽出
"""

import os
import glob
import re
from pathlib import Path
import PyPDF2
import pdfplumber

def extract_numbers_from_garbled_text(text, filename):
    """文字化けしたテキストから数値パターンを抽出"""
    salary_info = {
        'filename': filename,
        'year_month': None,
        'extracted_numbers': [],
        'probable_salary': None,
        'probable_bonus': None,
        'total_payment': None,
        'net_payment': None
    }
    
    # ファイル名から年月を抽出
    match = re.search(r'(\d{4})-(\d{2})', filename)
    if match:
        salary_info['year_month'] = f"{match.group(1)}-{match.group(2)}"
    
    # 数値パターンを抽出（3桁以上のカンマ区切り数値）
    number_patterns = [
        r'\b\d{1,3}(?:,\d{3})+\b',  # カンマ区切り数値
        r'\b\d{6,}\b',              # 6桁以上の数値
        r'\b[1-9]\d{2,5}\b'         # 3-6桁の数値
    ]
    
    all_numbers = []
    for pattern in number_patterns:
        numbers = re.findall(pattern, text)
        for num_str in numbers:
            try:
                # カンマを除去して数値に変換
                num = int(num_str.replace(',', ''))
                if 100000 <= num <= 10000000:  # 10万円〜1000万円の範囲
                    all_numbers.append(num)
            except ValueError:
                continue
    
    # 重複を除去してソート
    unique_numbers = sorted(list(set(all_numbers)), reverse=True)
    salary_info['extracted_numbers'] = unique_numbers
    
    # ファイル種別による推定
    if 'ボーナス' in filename or '特別一時金' in filename:
        # ボーナスファイルの場合
        if unique_numbers:
            salary_info['probable_bonus'] = unique_numbers[0]  # 最大値をボーナス額と推定
            if len(unique_numbers) > 1:
                salary_info['net_payment'] = unique_numbers[1]  # 2番目を手取りと推定
    else:
        # 通常給与ファイルの場合
        if unique_numbers:
            # 50万円以下の最大値を給与額と推定
            salary_candidates = [n for n in unique_numbers if n <= 1000000]
            if salary_candidates:
                salary_info['probable_salary'] = salary_candidates[0]
            
            # 手取り額を推定（給与額の70-85%程度）
            if salary_info['probable_salary']:
                expected_net = salary_info['probable_salary'] * 0.75
                net_candidates = [n for n in unique_numbers 
                                if expected_net * 0.8 <= n <= expected_net * 1.1]
                if net_candidates:
                    salary_info['net_payment'] = net_candidates[0]
    
    return salary_info

def analyze_salary_structure(salary_data):
    """給与構造を分析"""
    monthly_data = []
    bonus_data = []
    
    for data in salary_data:
        if 'ボーナス' in data['filename'] or '特別一時金' in data['filename']:
            bonus_data.append(data)
        elif '給与' in data['filename']:
            monthly_data.append(data)
    
    # 月給データを分析
    monthly_salaries = []
    monthly_net = []
    
    for data in monthly_data:
        if data['probable_salary']:
            monthly_salaries.append(data['probable_salary'])
        if data['net_payment']:
            monthly_net.append(data['net_payment'])
    
    # ボーナスデータを分析
    total_bonus = 0
    for data in bonus_data:
        if data['probable_bonus']:
            total_bonus += data['probable_bonus']
    
    return {
        'monthly_salaries': monthly_salaries,
        'monthly_net': monthly_net,
        'total_bonus': total_bonus,
        'avg_monthly_salary': sum(monthly_salaries) / len(monthly_salaries) if monthly_salaries else 0,
        'avg_monthly_net': sum(monthly_net) / len(monthly_net) if monthly_net else 0
    }

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理'
    
    # 2024年の給与PDFファイルを検索
    pdf_pattern = os.path.join(base_path, '給与', '2024', '*.pdf')
    pdf_files = glob.glob(pdf_pattern)
    pdf_files.sort()
    
    print("="*60)
    print("        2024年 給与PDF詳細解析レポート")
    print("="*60)
    
    salary_data = []
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        
        # テキスト抽出
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"エラー ({filename}): {e}")
            continue
        
        # 数値解析
        salary_info = extract_numbers_from_garbled_text(text, filename)
        salary_data.append(salary_info)
        
        print(f"\n📄 {filename}")
        print(f"年月: {salary_info['year_month']}")
        print(f"抽出数値: {salary_info['extracted_numbers'][:5]}...")  # 上位5個まで表示
        
        if salary_info['probable_salary']:
            print(f"推定給与額: ¥{salary_info['probable_salary']:,}")
        if salary_info['probable_bonus']:
            print(f"推定ボーナス額: ¥{salary_info['probable_bonus']:,}")
        if salary_info['net_payment']:
            print(f"推定手取り額: ¥{salary_info['net_payment']:,}")
    
    # 全体分析
    analysis = analyze_salary_structure(salary_data)
    
    print(f"\n📊 給与構造分析")
    print(f"月給データ数: {len(analysis['monthly_salaries'])}")
    if analysis['avg_monthly_salary']:
        print(f"平均月給（総支給）: ¥{analysis['avg_monthly_salary']:,.0f}")
    if analysis['avg_monthly_net']:
        print(f"平均月給（手取り）: ¥{analysis['avg_monthly_net']:,.0f}")
    if analysis['total_bonus']:
        print(f"年間ボーナス総額: ¥{analysis['total_bonus']:,}")
    
    annual_salary = analysis['avg_monthly_salary'] * 12 + analysis['total_bonus'] if analysis['avg_monthly_salary'] else 0
    if annual_salary:
        print(f"推定年収: ¥{annual_salary:,.0f}")
    
    return salary_data, analysis

if __name__ == "__main__":
    main()