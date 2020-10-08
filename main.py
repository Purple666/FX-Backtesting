from PickleLoader import PickleLoader
from EmaCross import EmaCross
from ConstantRiskPortfolio import ConstantRiskPortfolio
from ExecutionHandlerSimulation import ExecutionHandlerSimulation
from Evaluation import Evaluation


def backtest():
    DIR = '/Data/fx10-20 1H.pkl'
    EMA_PERIODS = 24
    EMA_TP = 50
    EMA_SL = 50
    INIT_CAP = 10000
    RISK = 0.05

    data_loader = PickleLoader(DIR)
    strategy = EmaCross(data_loader, EMA_PERIODS, EMA_TP, EMA_SL)
    portfolio = ConstantRiskPortfolio(INIT_CAP, RISK)
    execution = ExecutionHandlerSimulation(data_loader)
    performance = Evaluation(data_loader, portfolio)

    while data_loader.continue_backtest:
        signals = strategy.compute()

        orders = portfolio.order(signals=signals)

        fills = execution.execute(orders=orders)

        portfolio.update(fills)

        performance.evaluate()

        data_loader.set()

    return


if __name__ == '__main__':
    backtest()