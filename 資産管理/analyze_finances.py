#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024年家計収支・資産推移分析スクリプト
"""

import csv
import os
import glob
from datetime import datetime
from collections import defaultdict
import statistics

def read_csv_shift_jis(file_path):
    """Shift_JISでCSVファイルを読み込み"""
    data = []
    try:
        with open(file_path, 'r', encoding='shift_jis') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"エラー: {file_path} - {e}")
    return data

def analyze_income_expense(base_path):
    """収入・支出データの分析"""
    files = glob.glob(os.path.join(base_path, '収入・支出詳細_2024-*.csv'))
    files.sort()
    
    all_data = []
    monthly_summary = defaultdict(lambda: {'income': 0, 'expense': 0, 'net': 0})
    category_summary = defaultdict(int)
    
    for file in files:
        data = read_csv_shift_jis(file)
        all_data.extend(data)
        
        # 月を抽出
        month = os.path.basename(file).split('_')[1][:7]  # 2024-01形式
        
        for row in data:
            if row['計算対象'] == '1':  # 実際の取引のみ
                amount = int(row['金額（円）'])
                category = row['大項目']
                
                if amount > 0:
                    monthly_summary[month]['income'] += amount
                else:
                    monthly_summary[month]['expense'] += abs(amount)
                    category_summary[category] += abs(amount)
                
                monthly_summary[month]['net'] = monthly_summary[month]['income'] - monthly_summary[month]['expense']
    
    return all_data, monthly_summary, category_summary

def analyze_assets(base_path):
    """資産推移データの分析"""
    files = glob.glob(os.path.join(base_path, '資産推移_2024-*.csv'))
    files.sort()
    
    monthly_assets = {}
    asset_categories = ['預金・現金・暗号資産（円）', '株式(現物)（円）', '投資信託（円）', '年金（円）']
    
    for file in files:
        data = read_csv_shift_jis(file)
        month = os.path.basename(file).split('_')[1].split('.')[0]  # 2024-01形式
        
        if data:
            # 月末の資産額を取得
            last_record = data[-1]
            monthly_assets[month] = {
                'total': int(last_record['合計（円）']),
                'cash': int(last_record['預金・現金・暗号資産（円）']),
                'stocks': int(last_record['株式(現物)（円）']),
                'investment_trusts': int(last_record['投資信託（円）']),
                'pension': int(last_record['年金（円）']),
                'points': int(last_record['ポイント（円）'])
            }
    
    return monthly_assets

def format_currency(amount):
    """通貨フォーマット"""
    return f"¥{amount:,}"

def format_usd(amount):
    """USD通貨フォーマット"""
    return f"${amount:,.0f}"

def get_usd_jpy_rates():
    """2024年月別USD/JPY為替レートデータ"""
    return {
        '2024-01': 145.97,
        '2024-02': 149.51,
        '2024-03': 149.72,
        '2024-04': 153.84,
        '2024-05': 155.77,
        '2024-06': 157.98,
        '2024-07': 157.91,
        '2024-08': 146.33,
        '2024-09': 143.15,
        '2024-10': 149.67,
        '2024-11': 153.50,
        '2024-12': 153.80
    }

def generate_report(monthly_summary, category_summary, monthly_assets):
    """レポート生成"""
    
    print("=" * 60)
    print("           2024年 家計収支・資産推移レポート")
    print("=" * 60)
    
    # 年間収支サマリー
    total_income = sum(data['income'] for data in monthly_summary.values())
    total_expense = sum(data['expense'] for data in monthly_summary.values())
    net_income = total_income - total_expense
    
    print(f"\n📊 年間収支サマリー")
    print(f"総収入: {format_currency(total_income)}")
    print(f"総支出: {format_currency(total_expense)}")
    print(f"純収入: {format_currency(net_income)}")
    print(f"貯蓄率: {(net_income / total_income * 100):.1f}%")
    
    # USD換算での収支サマリー
    usd_rates = get_usd_jpy_rates()
    avg_rate = sum(usd_rates.values()) / len(usd_rates)
    
    print(f"\n💵 USD換算（年間平均レート: {avg_rate:.2f}円/USD）")
    print(f"総収入: {format_usd(total_income / avg_rate)}")
    print(f"総支出: {format_usd(total_expense / avg_rate)}")
    print(f"純収入: {format_usd(net_income / avg_rate)}")
    
    # 月別収支
    print(f"\n📅 月別収支")
    print(f"{'月':<10} {'収入':<12} {'支出':<12} {'収支':<12}")
    print("-" * 50)
    
    for month in sorted(monthly_summary.keys()):
        data = monthly_summary[month]
        print(f"{month:<10} {format_currency(data['income']):<12} {format_currency(data['expense']):<12} {format_currency(data['net']):<12}")
    
    # 支出カテゴリ別
    print(f"\n💰 支出カテゴリ別（上位10位）")
    sorted_categories = sorted(category_summary.items(), key=lambda x: x[1], reverse=True)
    for category, amount in sorted_categories[:10]:
        percentage = (amount / total_expense) * 100
        print(f"{category:<20} {format_currency(amount):<12} ({percentage:.1f}%)")
    
    # 資産推移
    if monthly_assets:
        print(f"\n🏦 月末資産推移")
        print(f"{'月':<10} {'総資産':<12} {'現金・預金':<12} {'投資':<12}")
        print("-" * 50)
        
        for month in sorted(monthly_assets.keys()):
            data = monthly_assets[month]
            investment_total = data['stocks'] + data['investment_trusts']
            print(f"{month:<10} {format_currency(data['total']):<12} {format_currency(data['cash']):<12} {format_currency(investment_total):<12}")
        
        # 資産増減
        months = sorted(monthly_assets.keys())
        if len(months) >= 2:
            start_assets = monthly_assets[months[0]]['total']
            end_assets = monthly_assets[months[-1]]['total']
            asset_change = end_assets - start_assets
            
            print(f"\n📈 年間資産増減")
            print(f"期初資産: {format_currency(start_assets)}")
            print(f"期末資産: {format_currency(end_assets)}")
            print(f"資産増減: {format_currency(asset_change)}")
            print(f"増減率: {(asset_change / start_assets * 100):.1f}%")
            
            # USD換算での資産分析
            usd_rates = get_usd_jpy_rates()
            start_rate = usd_rates[months[0]]
            end_rate = usd_rates[months[-1]]
            
            start_assets_usd = start_assets / start_rate
            end_assets_usd = end_assets / end_rate
            asset_change_usd = end_assets_usd - start_assets_usd
            
            print(f"\n💵 USD換算での資産増減")
            print(f"期初資産: {format_usd(start_assets_usd)} (レート: {start_rate:.2f}円/USD)")
            print(f"期末資産: {format_usd(end_assets_usd)} (レート: {end_rate:.2f}円/USD)")
            print(f"資産増減: {format_usd(asset_change_usd)}")
            print(f"USD増減率: {(asset_change_usd / start_assets_usd * 100):.1f}%")
            
            # 為替影響の分析
            end_assets_usd_constant = end_assets / start_rate  # 為替レート固定での期末資産
            forex_impact_usd = end_assets_usd - end_assets_usd_constant
            
            print(f"\n🔄 円安影響分析")
            print(f"為替変動による影響: {format_usd(forex_impact_usd)}")
            print(f"実質資産増加（為替除く）: {format_usd(end_assets_usd_constant - start_assets_usd)}")
            print(f"実質増減率（為替除く）: {((end_assets_usd_constant - start_assets_usd) / start_assets_usd * 100):.1f}%")
    
    # 投資ポートフォリオ
    if monthly_assets:
        latest_month = max(monthly_assets.keys())
        latest_data = monthly_assets[latest_month]
        
        print(f"\n🎯 投資ポートフォリオ（2024年12月末）")
        total_investment = latest_data['stocks'] + latest_data['investment_trusts']
        
        if total_investment > 0:
            stock_ratio = (latest_data['stocks'] / total_investment) * 100
            fund_ratio = (latest_data['investment_trusts'] / total_investment) * 100
            
            print(f"投資総額: {format_currency(total_investment)}")
            print(f"株式: {format_currency(latest_data['stocks'])} ({stock_ratio:.1f}%)")
            print(f"投資信託: {format_currency(latest_data['investment_trusts'])} ({fund_ratio:.1f}%)")
            
            # 総資産に占める投資比率
            investment_ratio = (total_investment / latest_data['total']) * 100
            print(f"総資産に占める投資比率: {investment_ratio:.1f}%")

def main():
    base_path = '/Users/ryohei/Desktop/RsObsidian_Github/資産管理/マネーフォワード情報/'
    
    print("データ分析中...")
    
    # 収入・支出データの分析
    all_data, monthly_summary, category_summary = analyze_income_expense(base_path)
    
    # 資産推移データの分析
    monthly_assets = analyze_assets(base_path)
    
    # レポート生成
    generate_report(monthly_summary, category_summary, monthly_assets)

if __name__ == "__main__":
    main()