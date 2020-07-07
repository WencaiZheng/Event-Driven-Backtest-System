# Declare the components with respective parameters
import queue
import time

import pandas as pd

import matplotlib.pyplot as plt
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import NaivePortfolio
from strategy import BuyAndHoldStrategy

events = queue.Queue()
start_date = "2018-01-01"
stock_list=list(pd.read_csv("./../sp500.csv").iloc[:5,0])

bars = HistoricCSVDataHandler(events, './../data', stock_list)
strategy = BuyAndHoldStrategy(bars, events)
port = NaivePortfolio(bars, events, start_date)
broker = SimulatedExecutionHandler(events)

while True:
    # Update the bars (specific backtest code, as opposed to live trading)
    if bars.continue_backtest:
        bars.update_bars()
    else:
        break
    # Handle the events
    while True:
        try:
            event = events.get(False)
        except queue.Empty:
            break
        else:
            if event is not None:
                if event.type == 'MARKET':
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type == 'SIGNAL':
                    port.update_signal(event)

                elif event.type == 'ORDER':
                    broker.execute_order(event)

                elif event.type == 'FILL':
                    port.update_fill(event)


    # 1-second heartbeat sample
    # time.sleep(1)

port.create_equity_curve_dataframe()
print(port.output_summary_stats())

port.equity_curve.to_csv("results/withHResult10Y.csv")