import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

def main():
    # Streamlit が対応している任意のオブジェクトを可視化する (ここでは文字列)
    st.write('Hello, World!')

#CSV読み込み
file_name = "11.csv"

#列名～取り個数取得
col_names = [ 'c{0:02d}'.format(i) for i in range(30) ]
df = pd.read_csv(file_name, sep=',', names=col_names,encoding="UTF8")
number_of_pieces_str = df["c00"][3]
number_of_pieces_int = int(number_of_pieces_str)

#測定情報解析
df_measure_amount = int(df.iloc[4]["c00"])
df_measure_amount_last_line = int((df_measure_amount / number_of_pieces_int ) + 5)
measure_amount_for_hist = int(df_measure_amount / 5)

#取り個数別条件分岐
df_product_data = df[5:df_measure_amount_last_line]
df_product_data.reset_index(drop=True,inplace=True)

if number_of_pieces_int == 1:
    df_N_product_data = df_product_data[["c03","c04"]]
    df_N_product_data_rename = df_N_product_data.rename(columns = {"c03":"1-T1","c04":"1-T2",})

elif number_of_pieces_int == 2:
    df_N_product_data = df_product_data[["c02","c03","c04","c05","c06"]]
    df_N_product_data_rename = df_N_product_data.rename(columns = {"c02":"Mea_hist","c03":"1-T1","c04":"1-T2","c05":"2-T1","c06":"2-T2"})
    df_N_product_data_allint = df_N_product_data_rename.astype({"1-T1":float})
    df_N_product_data_allint["thickness_1"] = np.where(df_N_product_data_allint['1-T1']>df_N_product_data_allint['1-T2'],df_N_product_data_allint['1-T1'], df_N_product_data_allint['1-T2'])
    df_N_product_data_allint["thickness_2"] = np.where(df_N_product_data_allint['2-T1']>df_N_product_data_allint['2-T2'],df_N_product_data_allint['2-T1'], df_N_product_data_allint['2-T2'])
    df_describe = df_N_product_data_allint.describe()
    df_show_data = df_N_product_data_allint[["thickness_1","thickness_2","Mea_hist"]]
    df_show_data.fillna({"Mea_hist": 0},inplace=True)
    print(df_show_data)


elif number_of_pieces_int == 3:
    df_N_product_data = df_product_data[["c03","c04","c05","c06","c07","c08"]]
    df_N_product_data_rename = df_N_product_data.rename(columns = {"c03":"1-T1","c04":"1-T2","c05":"2-T1","c06":"2-T2","c07":"3-T1","c08":"3-T2"})

elif number_of_pieces_int == 4:
    df_N_product_data = df_product_data[["c03","c04","c05","c06","c07","c08","c09","c10"]]
    df_N_product_data_rename = df_N_product_data.rename(columns = {"c03":"1-T1","c04":"1-T2","c05":"2-T1","c06":"2-T2","c07":"3-T1","c08":"3-T2","c09":"4-T1","c10":"4-T2"})

else :
    print("error")



fig1_line = px.line(data_frame = df_N_product_data_allint["thickness_1"], x=df_N_product_data_allint.index, y="thickness_1")
fig1_line.update_layout(title=dict(text='<b>1_Wall Thickness Line',
                             font=dict(size=20,
                                       color='grey'),
                             xref='paper', # container or paper
                             x=0.5,
                             y=1.0,
                             xanchor='center'
                            ),
                   )
fig2_line = px.line(data_frame = df_N_product_data_allint["thickness_2"], x=df_N_product_data_allint.index, y="thickness_2")
fig2_line.update_layout(title=dict(text='<b>2_Wall Thickness Line',
                             font=dict(size=20,
                                       color='grey'),
                             xref='paper', # container or paper
                             x=0.5,
                             y=1.0,
                             xanchor='center'
                            ),
                   )

fig1_hist = px.histogram(data_frame = df_N_product_data_allint.index, x=df_N_product_data_allint["thickness_1"],nbins=measure_amount_for_hist,histnorm='percent')
fig1_hist.update_layout(title=dict(text='<b>1_Wall Thickness Hist',
                             font=dict(size=26,
                                       color='grey'),
                             xref='paper', # container or paper
                             x=0.5,
                             y=1.0,
                             xanchor='center',
                            ),
                   )
fig2_hist = px.histogram(data_frame = df_N_product_data_allint.index, x=df_N_product_data_allint["thickness_2"],nbins=measure_amount_for_hist,histnorm='percent')
fig2_hist.update_layout(title=dict(text='<b>2_Wall Thickness Hist',
                             font=dict(size=26,
                                       color='grey'),
                             xref='paper', # container or paper
                             x=0.5,
                             y=1.0,
                             xanchor='center'
                            ),
                   )


#Data Table作成
st.dataframe(df_show_data,width=1000,height=500)


#Graph作成
vars_thickness = [var for var in df_N_product_data_allint.columns if var.startswith('thickness')]
vars_graph = ["Line","Histgram"]
#st.set_page_config(layout="wide")

# Layout (Sidebar)
st.markdown("## Settings")
st.sidebar.markdown("## Target Variables")
nikuatu_selected = st.sidebar.selectbox('Categorical Variables', vars_thickness)
graph_selected = st.sidebar.selectbox('Categorical Variables', vars_graph)

#fig_line1,fig1_hist = st.columns([2, 1])
if nikuatu_selected == "thickness_1":
    st.plotly_chart(fig1_line, use_container_width=True)
    st.plotly_chart(fig1_hist, use_container_width=True)

elif nikuatu_selected == "thickness_2":
    st.plotly_chart(fig2_line, use_container_width=True)
    st.plotly_chart(fig2_hist, use_container_width=True)

#st.plotly_chart(fig1_line, use_container_width=True)
#st.plotly_chart(fig1_hist, use_container_width=True)
#st.plotly_chart(fig2_line, use_container_width=True)
#st.plotly_chart(fig2_hist, use_container_width=True)


#df_N_product_data_allint.plot( y=["thickness_1"], ylim=[-5,5] ,figsize=(16,4), alpha=0.5)
#df_N_product_data_allint.plot( y=["thickness_2"], ylim=[-5,5] ,figsize=(16,4), alpha=0.5, color= "g")
#df_N_product_data_allint.plot( y=["thickness_1"], bins=100, alpha=0.5, figsize=(16,4), range=[-5,5], kind='hist')
#df_N_product_data_allint.plot( y=["thickness_2"], bins=100, alpha=0.5, figsize=(16,4), range=[-5,5], kind='hist', color= "g")
#df_N_product_data_allint.plot( y=["thickness_1","thickness_2"], bins=100, alpha=0.2, figsize=(16,4), range=[-5,5], kind='hist', color= ("r","g"))

#fig1 =px.line(data_frame = df_N_product_data_allint["thickness_1"], x=df_N_product_data_allint.index, y="thickness_1")
#fig2 =px.line(data_frame = df_N_product_data_allint["thickness_2"], x=df_N_product_data_allint.index, y="thickness_2")
#fig1.show()
#fig2.show()

if __name__ == '__main__':
    main()