import time
import pyupbit
import datetime

access = "cKs1FWkGOihld7ZiF9ovRV6Togj8xIEfZh3rwnW7"
secret = "A382X1qBzp7dz9TCunMzvvwhet9seQgXxzJtgxc2"

def get_target_price(ticker, k): #ticker = 어떤코인인지 그리고 K값을 넣어주게 되면 
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 시작시간 9:00
        end_time = start_time + datetime.timedelta(days=1) # 9시에서 1일을 더해준 값

        if start_time < now < end_time - datetime.timedelta(seconds=7200): # 마지막 시간에서 7200초(1시간)를 빼줌
            target_price = get_target_price("KRW-BTC", 0.5) #목표가격 설정
            ma15 = get_ma15("KRW-BTC")
            current_price = get_current_price("KRW-BTC") # 현재가격
            if target_price < current_price and ma15 < current_price: # 현재가격이 목표가 가격보다 크면
                krw = get_balance("KRW") # 내 잔고를 조회하고
                if krw > 5000: # 내 잔고가 5000원보다 클 경우
                    upbit.buy_market_order("KRW-BTC", krw*0.9995) # 수수료 0.05% 고려해서 구매
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
