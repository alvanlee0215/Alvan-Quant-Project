import yfinance as yf
import json, os, requests

# 策略參數
BASE_BUDGET = 200000
VAULT_FILE = 'investment_vault.json'

def get_taiex_pe():
    try:
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?response=json"
        res = requests.get(url)
        data = res.json()
        return float(data['data'][-1][2]) # 抓取最新本益比
    except:
        return 29.25 # 失敗時的保守值

def execute():
    pe = get_taiex_pe()
    tickers = yf.Tickers('00631L.TW QLD TWD=X')
    p_tw = tickers.tickers['00631L.TW'].fast_info['last_price']
    p_us = tickers.tickers['QLD'].fast_info['last_price']
    fx = tickers.tickers['TWD=X'].fast_info['last_price']
    
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as f: vault = json.load(f)
    else:
        vault = {"season": 1, "war_chest": 0}

    # 邏輯判定
    amt = BASE_BUDGET * 0.5 if pe > 28 else (BASE_BUDGET + vault["war_chest"] if pe < 18 else BASE_BUDGET)
    if pe > 28: vault["war_chest"] += (BASE_BUDGET * 0.5)
    elif pe < 18: vault["war_chest"] = 0

    print(f"\n--- 第 {vault['season']}/24 季 ---")
    print(f"偵測 P/E: {pe} | 模式: {'過熱' if pe>28 else ('大跌' if pe<18 else '常態')}")
    print(f"✅ 00631L: {int((amt*0.7)//p_tw)} 股")
    print(f"✅ QLD: {int(((amt*0.3)/fx)//p_us)} 股")
    
    vault["season"] += 1
    with open(VAULT_FILE, 'w') as f: json.dump(vault, f, indent=4)

if __name__ == "__main__": execute()
