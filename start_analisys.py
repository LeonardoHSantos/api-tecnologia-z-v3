# from config_auth import IDENTIFIER_IQOPTION, PASSWORD_IQOPTION
from strategy.views.run_analysis import RunAnalysys


# RUN = RunAnalysys(identifier=IDENTIFIER_IQOPTION, password=PASSWORD_IQOPTION)
# RUN.connect_wss()
# # RUN.get_candles_check_alternative(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
# # RUN.initiate_strategies()

# list_active_name = ""
# timeframe = 60*5
# amount = 1000
# tzone = "America/Sao Paulo"
# list_support_resistence = [60*15, 60*60, 60*(60*4)]
# amount_sup = 10
# active_name = "EURJPY"




# dataframes = RUN.get_candles_alternative(
#         active_name=active_name,
#         timeframe=timeframe,
#         amount=amount,
#         tzone=tzone,
#         tt_loop=10)

# import pandas as pd
# lista_df = []
# for df in dataframes:
#     lista_df.append(df[0])

# print(len(lista_df))
# df_all = pd.concat(lista_df)
# df_all = df_all.sort_values(by='from',ascending=True)
# df_unique = df_all.drop_duplicates(subset='from', keep='first')
# print(df_all)
# print(df_unique)
# # df_base.to_excel("base.xlsx")





