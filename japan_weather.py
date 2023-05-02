import streamlit as st
import datetime
import pandas as pd
import numpy as np
import geopandas as gpd
import random
import matplotlib.pyplot as plt
import japanize_matplotlib
from japanmap import picture

#st.set_option('deprecation.showPyplotGlobalUse', False)
filename = "northavedata.csv"
n_avg_df = pd.read_csv(filename, index_col = 0)
n_avg_df = n_avg_df.T
n_avg_df = n_avg_df.rename({"札幌":"北海道",
                            "盛岡":"岩手","仙台":"宮城",
                            "つくば（館野）":"茨城","宇都宮":"栃木","横浜":"神奈川","さいたま":"埼玉","前橋":"群馬",
                            "甲府":"山梨","金沢":"石川","松本":"長野",
                            "名古屋":"愛知","津":"三重"})

filename = "southavedata.csv"
s_avg_df = pd.read_csv(filename, index_col = 0)
s_avg_df = s_avg_df.T
s_avg_df = s_avg_df.rename({"彦根":"滋賀", "神戸":"兵庫",
                            "松江":"島根",
                            "高松":"香川","松山":"愛媛",
                            "那覇":"沖縄"})

avg_df = pd.concat([n_avg_df, s_avg_df])

#df =df.rename({"Hokkaido":"北海道",
#                           "Aomori":"青森","Akita":"秋田", "Iwate":"岩手", "Miyagi":"宮城","Yamagata":"山形", "Fukushima":"福島",
#                           "Ibaraki":"茨城", "Tochigi":"栃木", "Gunma":"群馬", "Saitama":"埼玉", "Chiba":"千葉", "Tokyo":"東京", "Kanagawa":"神奈川",
#                           "Niigata":"新潟", "Toyama":"富山", "Ishikawa":"石川","Fukui":"福井", "Yamanashi":"山梨", "Nagano":"長野",
#                           "Gifu":"岐阜","Shizuoka":"静岡", "Aichi":"愛知", "Mie":"三重",
#                           "Shiga":"滋賀", "Kyoto":"京都", "Osaka":"大阪","Hyogo":"兵庫", "Nara":"奈良", "Wakayama":"和歌山",
#                           "Tottori":"鳥取","Shimane":"島根", "Okayama":"岡山", "Hiroshima":"広島", "Yamaguchi":"山口",
#                           "Kagawa":"香川", "Tokushima":"徳島","Ehime":"愛媛", "Kochi":"高知",
#                           "Fukuoka":"福岡", "Saga":"佐賀", "Nagasaki":"長崎", "Kumamoto":"熊本", "Oita":"大分", "Miyazaki":"宮崎", "Kagoshima":"鹿児島", "Okinawa":"沖縄"})

st.set_page_config(
    page_title = "平均気温表示",
)

if "page_id" not in st.session_state:
    st.session_state.page_id = -1
    st.session_state.df = avg_df

df_column = st.session_state.df.columns.values
df_column1 = pd.to_datetime(df_column)
df_year = df_column1.year.unique()
df_month = df_column1.month.unique()
df_day = df_column1.day.unique()
year_list_selector = st.sidebar.selectbox("年", df_year)
month_list_selector = st.sidebar.selectbox("月", df_month)
days_list_selector = st.sidebar.selectbox("日", df_day)
selector = str(year_list_selector) + "/" + str(month_list_selector) + "/" + str(days_list_selector)

df_day = st.session_state.df[selector]

cmap = plt.get_cmap('seismic')
norm = plt.Normalize(vmin=st.session_state.df.min().min(), vmax=st.session_state.df.max().max())
fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
fig = plt.figure(figsize=(4,4))
plt.colorbar(plt.cm.ScalarMappable(norm, cmap))
plt.imshow(picture(st.session_state.df[selector].apply(fcol)))
st.pyplot(fig)
