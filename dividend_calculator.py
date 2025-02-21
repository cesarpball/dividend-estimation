import yfinance as yf
from datetime import datetime, timedelta
import pytz
from collections import defaultdict
import pandas as pd
import calendar
import argparse
import json
import requests


def get_monthly_dividends(tickets, shares_owned):
    monthly_dividends = defaultdict(list)
    
    end_date = datetime.now(pytz.UTC)
    start_date = end_date - timedelta(days=365)
    
    for ticket, shares in shares_owned.items():
        try:
            stock = yf.Ticker(ticket)
            dividends = stock.dividends
            
            if not dividends.empty:
                dividends.index = dividends.index.tz_convert('UTC')
                recent_dividends = dividends[dividends.index >= start_date]
                
                for date, amount in recent_dividends.items():
                    payment_info = {
                        'ticket': ticket,
                        'shares': shares,
                        'amount_per_share': amount,
                        'total_amount': amount * shares,
                        'payment_date': date.strftime('%Y-%m-%d'),
                        'day_of_month': date.day
                    }
                    monthly_dividends[date.month].append(payment_info)
                    
        except Exception as e:
            print(f"Error processing {ticket}: {str(e)}")
            
    return monthly_dividends

def calculate_investment_costs(portfolio):
    investment_costs = {}
    for ticker, details in portfolio.items():
        if isinstance(details, dict):
            shares = details['shares']
            cost_per_share = details['cost_per_share']
            investment_costs[ticker] = shares * cost_per_share
        else:
            # Handle old format where details is just number of shares
            shares = details
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('regularMarketPrice', 0)
            investment_costs[ticker] = shares * current_price
    return investment_costs


def predict_next_payments(monthly_dividends):
    current_year = datetime.now().year
    next_payments = []
    
    for month, payments in monthly_dividends.items():
        for payment in payments:
            last_date = datetime.strptime(payment['payment_date'], '%Y-%m-%d')
            
            _, last_day = calendar.monthrange(current_year, month)
            payment_day = min(last_date.day, last_day)
            
            next_date = datetime(current_year, month, payment_day)
            if next_date < datetime.now():
                next_year = current_year + 1
                _, last_day = calendar.monthrange(next_year, month)
                payment_day = min(last_date.day, last_day)
                next_date = datetime(next_year, month, payment_day)
            
            next_payment = payment.copy()
            next_payment['predicted_date'] = next_date.strftime('%Y-%m-%d')
            next_payments.append(next_payment)
    
    return sorted(next_payments, key=lambda x: datetime.strptime(x['predicted_date'], '%Y-%m-%d'))

def get_usd_to_eur_rate():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    return data['rates']['EUR']

def calculate_dividend_taxes(amount_eur):
    tax_brackets = [
        (0, 6000, 0.19),
        (6000.01, 50000, 0.21),
        (50000.01, 200000, 0.23),
        (200000.01, 300000, 0.27),
        (300000.01, float('inf'), 0.28)
    ]
    
    total_tax = 0
    remaining_amount = amount_eur
    
    for lower, upper, rate in tax_brackets:
        if remaining_amount <= 0:
            break
            
        taxable_in_bracket = min(remaining_amount, upper - lower)
        if taxable_in_bracket > 0:
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket
            remaining_amount -= taxable_in_bracket
            
    return total_tax


def main():
    parser = argparse.ArgumentParser(description='Calculate dividend payments from a portfolio')
    parser.add_argument('--portfolio', type=str, required=True, help='Path to JSON file containing portfolio')
    args = parser.parse_args()
    
    eur_rate = get_usd_to_eur_rate()
    
    with open(args.portfolio, 'r') as f:
        portfolio = json.load(f)
    
    monthly_divs = get_monthly_dividends(portfolio.keys(), portfolio)
    next_payments = predict_next_payments(monthly_divs)
    
    print("\nDividend Payment Schedule:")
    print("-" * 90)
    print(f"{'Stock':<6} {'Payment Date':<12} {'Shares':<8} {'Per Share':<10} {'Total USD':<10} {'Total EUR':<10}")
    print("-" * 90)
    
    current_month = None
    yearly_totals_usd = defaultdict(float)
    yearly_totals_eur = defaultdict(float)
    
    for payment in next_payments:
        payment_date = datetime.strptime(payment['predicted_date'], '%Y-%m-%d')
        month_year = payment_date.strftime('%B %Y')
        year = payment_date.strftime('%Y')
        
        if month_year != current_month:
            print(f"\n{month_year}")
            print("-" * 90)
            current_month = month_year
        
        eur_amount = payment['total_amount'] * eur_rate
        print(f"{payment['ticket']:<6} {payment['predicted_date']:<12} {payment['shares']:<8} "
              f"${payment['amount_per_share']:<9.2f} ${payment['total_amount']:<9.2f} €{eur_amount:.2f}")
        
        yearly_totals_usd[year] += payment['total_amount']
        yearly_totals_eur[year] += eur_amount
    
    monthly_totals_usd = defaultdict(float)
    monthly_totals_eur = defaultdict(float)
    for payment in next_payments:
        month = datetime.strptime(payment['predicted_date'], '%Y-%m-%d').strftime('%B %Y')
        monthly_totals_usd[month] += payment['total_amount']
        monthly_totals_eur[month] += payment['total_amount'] * eur_rate
    
    print("\nMonthly Expected Totals:")
    print("-" * 40)
    for month, total_usd in monthly_totals_usd.items():
        total_eur = monthly_totals_eur[month]
        print(f"{month:<12} ${total_usd:.2f} | €{total_eur:.2f}")
        
    print("\nYearly Expected Totals:")
    print("-" * 40)
    for year, total_usd in yearly_totals_usd.items():
        total_eur = yearly_totals_eur[year]
        print(f"{year:<12} ${total_usd:.2f} | €{total_eur:.2f}")


    print("\nYearly Tax Calculations:")
    print("-" * 60)
    for year, total_eur in yearly_totals_eur.items():
        tax_amount = calculate_dividend_taxes(total_eur)
        net_amount = total_eur - tax_amount
        print(f"{year:<12} Gross: €{total_eur:.2f} | Tax: €{tax_amount:.2f} | Net: €{net_amount:.2f}")

    # investment_costs = calculate_investment_costs(portfolio)
    # total_investment_usd = sum(investment_costs.values())

    # total_investment_eur = total_investment_usd * eur_rate
    # # Get shares for dividend calculation
    # shares_owned = {ticker: details['shares'] if isinstance(details, dict) else details 
    #                for ticker, details in portfolio.items()}
    
    
    # print("\nInvestment Summary:")
    # print("-" * 90)
    # print(f"Total Investment: ${total_investment_usd:.2f} | €{total_investment_eur:.2f}")
    # print("-" * 90)
    
    # # Rest of your existing print statements...
    
    # print("\nMonthly Return on Investment:")
    # print("-" * 60)
    # for month, total_usd in monthly_totals_usd.items():
    #     total_eur = monthly_totals_eur[month]
    #     monthly_roi = (total_eur / total_investment_eur) * 100
    #     print(f"{month:<12} ROI: {monthly_roi:.2f}% | €{total_eur:.2f} / €{total_investment_eur:.2f}")
        
    # print("\nYearly Return on Investment:")
    # print("-" * 60)
    # for year, total_eur in yearly_totals_eur.items():
    #     yearly_roi = (total_eur / total_investment_eur) * 100
    #     print(f"{year:<12} ROI: {yearly_roi:.2f}% | €{total_eur:.2f} / €{total_investment_eur:.2f}")

if __name__ == "__main__":
    main()