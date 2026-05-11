import yfinance as yf
import requests, os

def execute():
    # 1. 抓資料
    pe = float(requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?response=json").json()['data'][-1][2])
    tk = yf.Tickers('00631L.TW QLD TWD=X')
    p_tw = tk.tickers['00631L.TW'].fast_info['last_price']
    p_us = tk.tickers['QLD'].fast_info['last_price']
    fx = tk.tickers['TWD=X'].fast_info['last_price']
    
    # 2. 算股數 (預算 20 萬)
    amt = 100000 if pe > 28 else 200000
    s_tw = int((amt*0.7)//p_tw)
    s_us = int(((amt*0.3)/fx)//p_us)

    # 3. 強制寫入 index.html 讓網頁變動
    output = f"""
    <html><body style="background:#000;color:#7ee787;font-family:monospace;padding:20px;font-size:20px;">
    <h2>Alvan 執行指令</h2>
    <p>偵測 PE: {pe}</p>
    <p>模式: {'過熱減半' if pe > 28 else '常態投入'}</p>
    <hr>
    <p style="color:#fff;">✅ 00631L: {s_tw} 股</p>
    <p style="color:#fff;">✅ QLD: {s_us} 股</p>
    <p style="font-size:12px;color:#8b949e;">最後更新: 2026-05-12</p>
    </body></html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__": execute()
