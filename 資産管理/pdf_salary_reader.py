#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
給与PDFファイル読み取りスクリプト
PyPDF2とpdfplumberを使用してPDFから給与情報を抽出
"""

import os
import glob
import re
from pathlib import Path
import PyPDF2
import pdfplumber

def extract_text_with_pypdf2(pdf_path):
    """PyPDF2を使用してPDFからテキストを抽出"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"PyPDF2エラー ({pdf_path}): {e}")
    return text

def extract_text_with_pdfplumber(pdf_path):
    """pdfplumberを使用してPDFからテキストを抽出"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumberエラー ({pdf_path}): {e}")
    return text

def extract_tables_with_pdfplumber(pdf_path):
    """pdfplumberを使用してPDFからテーブルを抽出"""
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
    except Exception as e:
        print(f"pdfplumberテーブル抽出エラー ({pdf_path}): {e}")
    return tables

def parse_salary_info(text, filename):
    """テキストから給与情報を抽出"""
    salary_info = {
        'filename': filename,
        'year_month': None,
        'basic_salary': None,
        'total_payment': None,
        'total_deduction': None,
        'net_payment': None,
        'bonus': None,
        'text_content': text
    }
    
    # ファイル名から年月を抽出
    match = re.search(r'(\d{4})-(\d{2})', filename)
    if match:
        salary_info['year_month'] = f"{match.group(1)}-{match.group(2)}"
    
    # 金額パターンを検索（カンマ区切りの数字）
    amount_pattern = r'[\d,]+円?|¥[\d,]+|[\d,]+¥'
    amounts = re.findall(amount_pattern, text)
    
    # 一般的な給与項目のキーワードを検索
    keywords = {
        '基本給': 'basic_salary',
        '総支給': 'total_payment',
        '支給額': 'total_payment',
        '控除額': 'total_deduction',
        '差引支給額': 'net_payment',
        '手取り': 'net_payment',
        '賞与': 'bonus',
        '特別一時金': 'bonus'
    }
    
    for keyword, field in keywords.items():
        pattern = rf'{keyword}.*?([¥]?[\d,]+)円?'
        match = re.search(pattern, text)
        if match:
            amount_str = match.group(1).replace('¥', '').replace(',', '').replace('円', '')
            try:
                salary_info[field] = int(amount_str)
            except ValueError:
                pass
    
    return salary_info

def analyze_salary_pdfs(base_path):
    """給与PDFファイルを分析"""
    salary_data = []
    
    # 2024年の給与PDFファイルを検索
    pdf_pattern = os.path.join(base_path, '給与', '2024', '*.pdf')
    pdf_files = glob.glob(pdf_pattern)
    pdf_files.sort()
    
    print(f"発見されたPDFファイル数: {len(pdf_files)}")
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        print(f"\n処理中: {filename}")
        
        # 両方の方法でテキスト抽出を試行
        text_pypdf2 = extract_text_with_pypdf2(pdf_file)
        text_pdfplumber = extract_text_with_pdfplumber(pdf_file)
        
        # より多くのテキストが抽出できた方を使用
        if len(text_pdfplumber) > len(text_pypdf2):
            text = text_pdfplumber
            method = "pdfplumber"
        else:
            text = text_pypdf2
            method = "PyPDF2"
        
        print(f"使用方法: {method}")
        print(f"抽出テキスト長: {len(text)} 文字")
        
        if text.strip():
            # テーブル抽出も試行
            tables = extract_tables_with_pdfplumber(pdf_file)
            if tables:
                print(f"抽出テーブル数: {len(tables)}")
            
            # 給与情報を解析
            salary_info = parse_salary_info(text, filename)
            salary_data.append(salary_info)
            
            # デバッグ用：抽出されたテキストの一部を表示
            preview = text[:500] if len(text) > 500 else text
            print(f"テキストプレビュー:\n{preview}...")
        else:
            print("テキストを抽出できませんでした")
    
    return salary_data

def generate_salary_report(salary_data):
    """給与データのレポートを生成"""
    print("\n" + "="*60)
    print("           2024年 給与データ分析レポート")
    print("="*60)
    
    monthly_salaries = []
    bonuses = []
    
    for data in salary_data:
        if data['filename']:
            if '特別一時金' in data['filename'] or 'bonus' in data['filename'].lower():
                bonuses.append(data)
            else:
                monthly_salaries.append(data)
    
    print(f"\n📊 ファイル概要")
    print(f"月給ファイル数: {len(monthly_salaries)}")
    print(f"賞与ファイル数: {len(bonuses)}")
    
    # 抽出できた金額情報を表示
    print(f"\n💰 抽出された給与情報")
    for data in salary_data:
        print(f"\nファイル: {data['filename']}")
        print(f"年月: {data.get('year_month', '不明')}")
        
        for field, label in [
            ('basic_salary', '基本給'),
            ('total_payment', '総支給額'),
            ('total_deduction', '控除額'),
            ('net_payment', '差引支給額'),
            ('bonus', '賞与額')
        ]:
            value = data.get(field)
            if value:
                print(f"{label}: ¥{value:,}")

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理'
    
    print("給与PDFファイルの分析を開始...")
    
    # 給与PDFファイルを分析
    salary_data = analyze_salary_pdfs(base_path)
    
    # レポート生成
    generate_salary_report(salary_data)
    
    return salary_data

if __name__ == "__main__":
    main()