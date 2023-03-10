from config_auth import IDENTIFIER_IQOPTION, PASSWORD_IQOPTION
from strategy.views.run_analysis import RunAnalysys


RUN = RunAnalysys(identifier=IDENTIFIER_IQOPTION, password=PASSWORD_IQOPTION)
RUN.connect_wss()
RUN.initiate_strategies()