#import all necessary libraries
from audioop import reverse
from enum import auto
from shutil import unregister_archive_format
from tkinter.tix import COLUMN
from turtle import color, title, width
import streamlit as st
import pandas as pand
import numpy as np
from datetime import datetime, timedelta , date
import gspread
from google.oauth2.service_account import Credentials
from gspread_pandas import Spread, Client
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import calendar
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests
from streamlit_folium import st_folium
import folium
import streamlit.components.v1 as components
import requests

from PIL import Image
import time
import base64
from win10toast import ToastNotifier
from millify import millify



#import chart libraries 
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from streamlit_echarts import st_echarts
from pyecharts.charts import Pie
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
#Consumer library
import re
import os
# from wordcloud import STOPWORDS, WordCloud
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob
from deta import Deta 

#configuring database NoSQL
deta=Deta(st.secrets["deta_key"])
parameter=deta.Base("parameter")
parameter2=deta.Base("parameter2")

#setting page configuration for streamlit
st.set_page_config(
page_title="D-Aggregate Technologies ®️",
page_icon="📉",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://d-aggregate.com/#',
'Report a bug': None,
'About': """We help organizations draw actionable insight from on-ground market data & build 
                datacentric solutions that drives informed decison and productivity."""
}
)
st.markdown("""<head>
<meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no">
</head>""",unsafe_allow_html=True)
#set the css styling sheet 
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#set the image
logo="DAggregate.png"

#set the Web title as D-Aggregate Technologies
st.markdown(f"""
            <div class="container">
                <a href="https://d-aggregate.com/#"><img class="logo-img"
                src="data:image/png;base64,{base64.b64encode(open(logo, "rb").read()).decode()}"></a>
                <h6 class="imghead-text"> <b>D-Aggregate Technologies -</b> (Real-Time Data Intelligence On Brand Performance 📈 📉 📊)</h6>
                </div>
""",unsafe_allow_html=True)

#create tab clicks for retail and consumer insights
tb1,tb2,tb3=st.columns([3,3,7])
tb1,tb2=st.tabs(["RETAIL INSIGHTS","CONSUMER INSIGHTS"])
toaster = ToastNotifier()
toaster.show_toast("Hi Welcome Here!", 
                    "You Can View Insight Better On Your Desktop/Laptop", duration=20, threaded=True)
#initializing gcp database service account and API endpoint
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('brandinsight-97ca5fe9e187.json', scopes=scope)
client = Client(scope=scope, creds=credentials)
#footer Note
def definitions():
                    st.markdown(f"""
                    <br>
                    <br>
                    <h5 class="terms"><u>DEFINITION OF TERMS</u></h5>
                    <div class="footnote">
                    <p><b>Market Share(ND)</b> : This indicate the Numeric Distribution of brand product[{Product}] across different stores. 
                                This helps businesses and multinational understand spread of their products in retail stores</p>
                    <p><b>Market Share(WD)</b> : This indicate the Weighted Distribution of brand product[{Product}] across different stores. 
                                This helps businesses and multinational understand depth/drop size of their products in retail stores</p>
                    <p><b>Fast Moving Brand</b> : This explains the level of offtakes of your brand product[{Product}] against competition across different stores. 
                                This helps businesses and multinational understand spread of their products in retail stores</p>
                    <p><b>Pricing Analysis</b> : This shows the average selling price(&#8358;) of your brand products variants[{Product}] in the stores. 
                                    This is estimated by calculating the average price across stores in {country}</p>
                    <p><b>Region(Urban/Rural)</b> : Urban areas are metropolitant area in a country with key basic amenities-(Urban areas comprise larger places and 
                    densely settled areas around them) & Rural areas comprise open country and settlements with fewer than 2,500 residents.</p>
                    </div>
                    <br>
                    <br>
                    <p class="checkus"><b>👉Would You Like To Have Exclusive Brands Data Intelligence 
                            Platform Like This?</b> <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                    <p style="font-size:16px; text-align:center; color:darkgreen;"> Copyright©️ D-AGGREGATE(2022) -All right reserved</p>
                    """,unsafe_allow_html=True)

def consumer_definitions():
                    st.write(f"""
                    <br>
                    <br>
                    <h5 class="terms"><u>DEFINITION OF TERMS</u></h5>
                    <div class="footnote">
                    <p><b>Tweets Subjectivity</b> : Subjectivity quantifies the amount of personal opinion and factual information contained in the text. 
                                The higher subjectivity means that the text contains personal opinion rather than factual information. </p>
                    <p><b>Tweets Potential Impact</b> : This defines the level of impressions tweets about {keyword}, the impact is calculated using Reach and Likes, 
                                thats is the potential number of followers by users and retweets</p>
                    <p><b>Tweets Potential Reach</b> : This explains the potential reach for all tweets about {keyword}, 
                                        that is the number of potential user followers who could possibly see the tweets.</p>
                    <p><b>Average Engagement Per Reach</b> : This explains the average Likes and Retweets Per UserFollowers, thats is the average engagement on tweets by userfollowers. This helps brand measure their campaign imapct, 
                    influence and versatility on social media</p>
                    <p><b>Sentiment Polarity</b> :Sentiment Analysis can help us decipher the mood and 
                    emotions of general public and gather insightful information regarding the context.</p>
                    </div>
                    <br>
                    <br>
                    <p class="checkus"><b>👉Would You Like To Have Exclusive Brands Data Intelligence 
                            Platform Like This?</b> <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                    <p style="font-size:16px; text-align:center; color:darkgreen;"> Copyright©️ D-AGGREGATE(2022) -All right reserved</p>
                    """,unsafe_allow_html=True)
@st.cache
def tweetembed(tweetURL):
    api="https://publish.twitter.com/oembed?url={}".format(tweetURL)
    response=requests.get(api)
    # res=response.json()
    res = response.json()["html"]
    return res
@st.cache
def db(name,table):
    dbtable=Spread(name,client=client)
    db_df=dbtable.sheet_to_df(index=False,sheet=table)
    return db_df

@st.cache
def load_lottie(url:str):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_url="https://assets4.lottiefiles.com/packages/lf20_8gmx5ktv.json"
lottie_insight=load_lottie(lottie_url)

@st.cache
def convert_df(input_df):
    return input_df.to_html(escape=False, justify="center", max_rows=20,index=False,col_space=25)
#Retail Insights
with tb1:
    st.markdown("""
    <br>
    <h5 class="select_params">Select Brand Category, Product & Country</h5>
    """,unsafe_allow_html=True)
    cat,gp,pd,gp,ctry,gp,region=st.columns([4,0.5,4,0.5,4,0.5,4])
    category=cat.selectbox("🔲Brand Category",["Personal & Home Care","Foods,Seasonings & Beverages",
                    "Alcoholic & Non-Alcoholic Drinks","Pharmaceuticals"])
    if category=='Personal & Home Care':
        Product=pd.selectbox("🛍️🛒Products",['Bathing Soap(Antiseptic & Frangrance)',
            'Baby Lotions','Body Lotions','Toothpaste','Diapers','Detergents/Dish Wash','Insecticides','Sanitary Pads'])
        country=ctry.selectbox("🌍Country",['Nigeria'])
        location=region.selectbox("🌄Region", ["Urban","Rural"])
        # st.markdown(f""" 
        #     <br>
        #     """,
        #     unsafe_allow_html=True)
        personal_care=st.button("EXPLORE INSIGHT")
        if personal_care and Product=="Bathing Soap(Antiseptic & Frangrance)" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=True, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                fragtbl=db(name="Antispetics_Fragrance",table="F_Market_Share")
                #creating market share metrics
                stores=millify(10000)
                st.markdown("""<h6 class="fragrance_title"><u>Fragrance Soaps</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3=st.columns(3)
                exp1,space1,exp2,space2,exp3=st.columns([5,1,5,1,5])
                #Fragrance Soap
                met1.metric(fragtbl["Products"].iloc[0],fragtbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{fragtbl["Products"].iloc[0]}</b><img class="img_metric" src="https://www.pngfind.com/pngs/m/75-757243_lux-soap-png-lux-soap-bar-png-transparent.png"> is availabe 
                in {millify(fragtbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(fragtbl["Products"].iloc[1],fragtbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{fragtbl["Products"].iloc[1]}</b><img class="img_metric" src="https://marketsng.fra1.digitaloceanspaces.com/images/CWdbKYN5jeduvmZkO77krd8WGBx1VZXYpdAFMBQ2.png"> is availabe 
                in {millify(fragtbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(fragtbl["Products"].iloc[2],fragtbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{fragtbl["Products"].iloc[2]}</b><img class="img_metric" src="https://shoponclick.ng/wp-content/uploads/2020/12/Joy-Beauty-Bar-Tender-.png"> is availabe 
                in {millify(fragtbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                #Antiseptics
                st.markdown("""<br>""",unsafe_allow_html=True)
                antiseptbl=db(name="Antispetics_Fragrance", table="A_Market_Share")
                st.markdown("""<h6 class="antiseptic_title"><u>Antispetic Soaps</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3,met4,met5,met6=st.columns(6)
                exp1,spc,exp2,spc,exp3,spc,exp4,spc,exp5,spc,exp6=st.columns([3,0.5,3,0.5,3,0.5,3,0.5,3,0.5,3])
                #antiseptic soap
                met1.metric(antiseptbl["Products"].iloc[0],antiseptbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[0]}</b><img class="img_metric" src="https://www.kindpng.com/picc/m/150-1503502_dettol-original-soap-png-transparent-png.png"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(antiseptbl["Products"].iloc[1],antiseptbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[1]}</b><img class="img_metric" src="https://marketsng.fra1.digitaloceanspaces.com/images/sxkrJnnYUH6VzUj1MLCF4oE1vHuRAwaOQXRxjNId.png"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(antiseptbl["Products"].iloc[2],antiseptbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[2]}</b><img class="img_metric" src="https://nextcashandcarry.com.ng/wp-content/uploads/2022/05/Anti-Bac.-Soap-70g-Original.png"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</b></i>""",unsafe_allow_html=True)
                met4.metric(antiseptbl["Products"].iloc[3],antiseptbl["%Store"].iloc[3])
                exp4.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[3]}</b><img class="img_metric" src="https://orangegroups.com/wp-content/uploads/2019/10/delta.png"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[3])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met5.metric(antiseptbl["Products"].iloc[4],antiseptbl["%Store"].iloc[4])
                exp5.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[4]}</b><img class="img_metric" src="https://premiercool.com.ng/wp-content/uploads/2019/08/Soap-ULTIMATE.png"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[4])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met6.metric(antiseptbl["Products"].iloc[5],antiseptbl["%Store"].iloc[5])
                exp6.markdown(f"""<p class="metric_explainer"><b>{antiseptbl["Products"].iloc[5]}</b><img class="img_metric" src="https://www.drogeria-vmd.com/imagegen.php?autoimage=1704765"> is availabe 
                in {millify(antiseptbl["Stores"].iloc[5])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                #explaining market share
                st.markdown("""
                <p class="checkus"><b>👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page?</b> <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                fragwt=db(name="Antispetics_Fragrance",table="F_Quantity")
                c = (
                Line()
                .add_xaxis(fragwt["Date"].tolist())
                .add_yaxis("Lux", fragwt["Lux Fragrance Soap"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Eva", fragwt["Eva Fragrance Soap"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Joy",fragwt["Joy Fragrance Soaps"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Fragrance Soaps Market Size",
                    subtitle="Frangrace Soaps Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                    )
                )
                    )
                
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                Antiseptwt=db(name="Antispetics_Fragrance",table="A_Quantity")
                d = (
                Line()
                .add_xaxis(Antiseptwt["Date"].tolist())
                .add_yaxis("Dettol", Antiseptwt["Dettol"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Extract", Antiseptwt["Extract"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("2Sure",Antiseptwt["2Sure"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Delta",Antiseptwt["Delta"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Premier Cool",Antiseptwt["Premier Cool"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Carex",Antiseptwt["Carex"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Antiseptic Soaps Market Size",
                    subtitle="Antiseptic Soaps Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1.5%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                    # xaxis_opts=opts.AxisOpts(grid_index=1),
                    # tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
                    
                
                st_pyecharts(d,height="350px", width="1120px")
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>Fragrance Soaps</u></h6>""",unsafe_allow_html=True)
                fragmv=db(name="Antispetics_Fragrance",table="F_Fast_moving")

                # fragfig = go.Figure(data=[go.Pie(labels=fragmv["Products"], values=fragmv["Purchase Frequency"], 
                # pull=[0, 0.1, 0],hole=0.1,textinfo="label+percent",insidetextorientation='radial',hoverinfo="label+percent+name")])
                # fragfig.update_layout(title="Sales Freq. By Brand Product"
                #  )
                # fragfig.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
                # fmv1.plotly_chart(fragfig)
                antisepmv=db(name="Antispetics_Fragrance",table="A_Fast_moving")
                # antisepfig = go.Figure(data=[go.Pie(labels=antisepmv["Products"], values=antisepmv["Purchase Frequency"], 
                # pull=[0,0,0,0.1, 0],hole=0.1,textinfo="label+percent",insidetextorientation='radial',hoverinfo="label+percent+name")])
                # antisepfig.update_layout(title="Sales Freq. By Brand products"
                #  )
                # antisepfig.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
                # fmv3.plotly_chart(antisepfig)
                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(fragmv["Products"],fragmv["Purchase Frequency"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Fragrance Soap In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                st.markdown("""<br>
                <h6 class="antiseptic_title"><u>Antiseptic Soaps</u></h6>""",unsafe_allow_html=True)               
                m2 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(antisepmv["Products"],antisepmv["Purchase Frequency"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Antiseptic Soap In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m2,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>Fragrance Soaps(&#8358;)</u></h6>""",unsafe_allow_html=True)
                fragprice=db(name="Antispetics_Fragrance",table="Fragrance Pricing")
                @st.cache
                def convert_df(input_df):
                    return input_df.to_html(escape=False, justify="center", max_rows=15,index=False,col_space=25)
                html = convert_df(fragprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                #antiseptic table
                antisepprice=db(name="Antispetics_Fragrance",table="Antiseptic Pricing")
                st.markdown("""<br>
                <h6 class="antiseptic_title"><u>Antiseptic Soaps(&#8358;)</u></h6>""",unsafe_allow_html=True) 
                html = convert_df(antisepprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/ant1.png","Assets_img/ant3.png","Assets_img/ant4.png","Assets_img/ant5.png"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy" >
                </div>
                """,unsafe_allow_html=True)
                 #call definition function
                definitions()
        elif personal_care and Product=="Baby Lotions" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=False, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                babytbl=db(name="Baby_Lotions",table="Market_shares")
                #creating market share metrics
                stores=10000
                st.markdown("""<h6 class="fragrance_title"><u>Baby Lotions</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3=st.columns(3)
                exp1,space1,exp2,space2,exp3=st.columns([5,1,5,1,5])
                
                met1.metric(babytbl["Products"].iloc[0],babytbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{babytbl["Products"].iloc[0]}</b><img class="img_metric" src="https://www.ebeosi.com.ng/public/uploads/products/photos/8U0bZ2IHgDMC2KdysG3quYqOi6kTGnoYTfUgMIpW.jpeg"> is availabe 
                in {millify(babytbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(babytbl["Products"].iloc[1],babytbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{babytbl["Products"].iloc[1]}</b><img class="img_metric" src="https://www.nbc.lk/storage/uploads/image/1_60c99fad47d0f.png/medium/1_60c99fad47d0f.png"> is availabe 
                in {millify(babytbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(babytbl["Products"].iloc[2],babytbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{babytbl["Products"].iloc[2]}</b><img class="img_metric" src="https://sambethelsuperstores.com/wp-content/uploads/2019/06/CUSSON-BABY-LOTION.jpg"> is availabe 
                in {millify(babytbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                #Antiseptics
                st.markdown("""<br>""",unsafe_allow_html=True)
               
                #explaining market share
                st.markdown("""
                <p class="checkus">👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page? <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                babywt=db(name="Baby_Lotions",table="Quantity")
                c = (
                Line()
                .add_xaxis(babywt["Date"].tolist())
                .add_yaxis("Pears", babywt["Pears Baby Lotion"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Panda", babywt["Panda Baby Lotion"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Cussons",babywt["Cusson Baby Lotion"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Baby Lotions Market Size",
                    subtitle="Baby Lotions Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%")
                    ,
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>Baby Lotions</u></h6>""",unsafe_allow_html=True)
                babymv=db(name="Baby_Lotions",table="Fast Moving")

                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(babymv["Products"],babymv["%Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Baby Lotions In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>Baby Lotions(&#8358;)</u></h6>""",unsafe_allow_html=True)
                babyprice=db(name="Baby_Lotions",table="Baby_Lotion_Prices")
                html = convert_df(babyprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/babyl1.jpg","Assets_img/babyl2.jpg","Assets_img/babyl3.jpg","Assets_img/babyl4.jpg"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy">
                </div>
                """,unsafe_allow_html=True)
                #call definition function
                definitions()
        elif personal_care and Product=="Body Lotions" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=False, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                bodytbl=db(name="Body Lotion",table="Market_share")
                #creating market share metrics
                stores=10000
                st.markdown("""<h6 class="fragrance_title"><u>Body Lotions</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3,met4=st.columns(4)
                exp1,space1,exp2,space2,exp3,space3,exp4=st.columns([5,1,5,1,5,1,5])
                
                met1.metric(bodytbl["Products"].iloc[0],bodytbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{bodytbl["Products"].iloc[0]}</b><img class="img_metric" src="https://venusforyou.com/wp-content/uploads/2016/05/nourishing-lotion.png"> is availabe 
                in {millify(bodytbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(bodytbl["Products"].iloc[1],bodytbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{bodytbl["Products"].iloc[1]}</b><img class="img_metric" src="https://jendolstores.com/wp-content/uploads/2021/02/unnamed.png"> is availabe 
                in {millify(bodytbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(bodytbl["Products"].iloc[2],bodytbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{bodytbl["Products"].iloc[2]}</b><img class="img_metric" src="https://w7.pngwing.com/pngs/393/554/png-transparent-nivea-nourishing-body-lotion-nivea-nourishing-body-lotion-factor-de-proteccion-solar-skin-whitening-la-india-cream-skin-whitening-body-wash.png"> is availabe 
                in {millify(bodytbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                met4.metric(bodytbl["Products"].iloc[3],bodytbl["%Store"].iloc[3])
                exp4.markdown(f"""<p class="metric_explainer"><b>{bodytbl["Products"].iloc[3]}</b><img class="img_metric" src="https://kao-h.assetsadobe3.com/is/image/content/dam/sites/kaousa/www-jergens-com/images/au/products/daily-moisturizers/JER_Ultra-Healing_Moisturiser%20Duo%20(400mL%20&%20650mL).png?fmt=png-alpha&wid=336"> is availabe 
                in {millify(bodytbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                #Antiseptics
                st.markdown("""<br>""",unsafe_allow_html=True)
               
                #explaining market share
                st.markdown("""
                <p class="checkus">👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page? <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                bodywt=db(name="Body Lotion",table="Quantity")
                c = (
                Line()
                .add_xaxis(bodywt["Date"].tolist())
                .add_yaxis("Venus", bodywt["Venus"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Nivea", bodywt["Nivea"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Jergens",bodywt["Jergens"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Caro White",bodywt["Caro White Body"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Body Lotions Market Size",
                    subtitle="Body Lotions Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>Body Lotions</u></h6>""",unsafe_allow_html=True)
                bodymv=db(name="Body Lotion",table="Fast_moving")

                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(bodymv["Products"],bodymv["% Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Baby Lotions In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>Body Lotions(&#8358;)</u></h6>""",unsafe_allow_html=True)
                bodyprice=db(name="Body Lotion",table="Body_lotion_prices")
                html = convert_df(bodyprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/babyl1.jpg","Assets_img/babyl2.jpg","Assets_img/babyl3.jpg","Assets_img/babyl4.jpg"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy">
                </div>
                """,unsafe_allow_html=True)
                #call definition function
                definitions()        
        elif personal_care and Product=="Toothpaste" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=False, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                pastetbl=db(name="ToothPaste",table="Market_share")
                #creating market share metrics
                stores=10000
                st.markdown("""<h6 class="fragrance_title"><u>ToothPaste</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3,met4,met5=st.columns(5)
                exp1,space1,exp2,space2,exp3,space3,exp4,space4,exp5=st.columns([5,1,5,1,5,1,5,1,5])
                
                met1.metric(pastetbl["Products"].iloc[0],pastetbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{pastetbl["Products"].iloc[0]}</b><img class="img_metric" src="
                https://th.bing.com/th/id/R.d0b30810bffb5d106b37e1c76c9ab653?rik=CS77kuS33parxg&pid=ImgRaw&r=0"> is availabe 
                in {millify(pastetbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(pastetbl["Products"].iloc[1],pastetbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{pastetbl["Products"].iloc[1]}</b><img class="img_metric" src="
                https://citinewsroom.com/wp-content/uploads/2020/08/Pepsodent-New-Pack-Tube.png"> is availabe 
                in {millify(pastetbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(pastetbl["Products"].iloc[2],pastetbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{pastetbl["Products"].iloc[2]}</b><img class="img_metric" src="https://olivertwiststore.com/wp-content/uploads/2020/06/oral-b-pro-health-toothpaste-40g.jpg"> is availabe 
                in {millify(pastetbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                met4.metric(pastetbl["Products"].iloc[3],pastetbl["%Store"].iloc[3])
                exp4.markdown(f"""<p class="metric_explainer"><b>{pastetbl["Products"].iloc[3]}</b><img class="img_metric" src="https://www.srssulit.com/wp-content/uploads/products/489-1.png"> is availabe 
                in {millify(pastetbl["Stores"].iloc[3])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                met5.metric(pastetbl["Products"].iloc[4],pastetbl["%Store"].iloc[4])
                exp5.markdown(f"""<p class="metric_explainer"><b>{pastetbl["Products"].iloc[4]}</b><img class="img_metric" src="https://th.bing.com/th/id/OIP.wOsO6iOayApbiW-1JtK-sAHaD9?pid=ImgDet&rs=1"> is availabe 
                in {millify(pastetbl["Stores"].iloc[4])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                #ToothPaste
                st.markdown("""<br>""",unsafe_allow_html=True)
               
                #explaining market share
                st.markdown("""
                <p class="checkus">👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page? <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                pastewt=db(name="ToothPaste",table="Quantity")
                c = (
                Line()
                .add_xaxis(pastewt["Date"].tolist())
                .add_yaxis("CloseUP", pastewt["Close UP"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Pepsodent", pastewt["Pepsodent"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Oral B",pastewt["Oral B"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Colgate",pastewt["Colgate"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Sensodyne",pastewt["Sensodyne"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="ToothPaste Market Size",
                    subtitle="ToothPaste Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>BToothPaste</u></h6>""",unsafe_allow_html=True)
                pastemv=db(name="ToothPaste",table="Fast_moving")

                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(pastemv["Products"],pastemv["% Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold ToothPaste In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>ToothPaste(&#8358;)</u></h6>""",unsafe_allow_html=True)
                pasteprice=db(name="ToothPaste",table="Tothpaste_Prices")
                html = convert_df(pasteprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/babyl1.jpg","Assets_img/babyl2.jpg","Assets_img/babyl3.jpg","Assets_img/babyl4.jpg"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy">
                </div>
                """,unsafe_allow_html=True)
                #call definition function
                definitions()        
        elif personal_care and Product=="Diapers" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=False, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                diapertbl=db(name="Baby_Diapers",table="Market_share")
                #creating market share metrics
                stores=10000
                st.markdown("""<h6 class="fragrance_title"><u>Baby Diapers</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3,met4=st.columns(4)
                exp1,space1,exp2,space2,exp3,space3,exp4=st.columns([5,1,5,1,5,1,5])
                
                met1.metric(diapertbl["Products"].iloc[0],diapertbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{diapertbl["Products"].iloc[0]}</b><img class="img_metric" src="
                https://www.huggies.com.ng/-/media/Project/HuggiesNG/Images/Products/Huggies-Nigeria-Images/resized-packshots/ProductArtboard-5.png?h=545&w=766"> is availabe 
                in {millify(diapertbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(diapertbl["Products"].iloc[1],diapertbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{diapertbl["Products"].iloc[1]}</b><img class="img_metric" src="
                https://th.bing.com/th/id/OIP.TbKNmk51q0jTr7caBScCUgHaHa?pid=ImgDet&w=500&h=500&rs=1"> is availabe 
                in {millify(diapertbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(diapertbl["Products"].iloc[2],diapertbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{diapertbl["Products"].iloc[2]}</b><img class="img_metric" src="https://th.bing.com/th/id/R.d0a0925df00dc04b3e9c53e0109a2ff1?rik=4QwRBGTytLdAAA&pid=ImgRaw&r=0"> is availabe 
                in {millify(diapertbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                met4.metric(diapertbl["Products"].iloc[3],diapertbl["%Store"].iloc[3])
                exp4.markdown(f"""<p class="metric_explainer"><b>{diapertbl["Products"].iloc[3]}</b><img class="img_metric" src="https://www.kisskidsdiapers.com/u_file/2106/products/05/9c8ba0cdc3.png.500x500.png"> is availabe 
                in {millify(diapertbl["Stores"].iloc[3])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>
                """,unsafe_allow_html=True)
                #ToothPaste
                st.markdown("""<br>""",unsafe_allow_html=True)
               
                #explaining market share
                st.markdown("""
                <p class="checkus">👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page? <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                diaperwt=db(name="Baby_Diapers",table="Quantity")
                c = (
                Line()
                .add_xaxis(diaperwt["Date"].tolist())
                .add_yaxis("Huggies", diaperwt["Huggies"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Molfix", diaperwt["Molfix"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Swaddlers",diaperwt["Swaddlers"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Kisskids",diaperwt["Kisskids"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="ToothPaste Market Size",
                    subtitle="ToothPaste Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>Baby Diapers</u></h6>""",unsafe_allow_html=True)
                diapermv=db(name="Baby_Diapers",table="Fast_moving")

                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(diapermv["Products"],diapermv["% Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Baby Diaper In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>Baby Diaper(&#8358;)</u></h6>""",unsafe_allow_html=True)
                diaperprice=db(name="Baby_Diapers",table="Price_state")
                html = convert_df(diaperprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/babyl1.jpg","Assets_img/babyl2.jpg","Assets_img/babyl3.jpg","Assets_img/babyl4.jpg"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy">
                </div>
                """,unsafe_allow_html=True)
                #call definition function
                definitions()        
        elif personal_care and Product=="Detergents/Dish Wash" and country=="Nigeria":
            with st.spinner(text=" Loading Retail Insight "), st_lottie_spinner(lottie_insight, speed=1,height=150, loop=True, key="loading_gif"):
                time.sleep(2)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brand Product Performance(Market Share/Numeric Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share across retail stores in <b>{country}</b> indicates the number of stores where your brands are available. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Diswash
                dishtbl=db(name="Detergent_DishWash",table="Dish_market")
                #creating market share metrics
                stores=millify(int(10000))
                st.markdown("""<h6 class="fragrance_title"><u>Dish Washes</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3=st.columns(3)
                exp1,space1,exp2,space2,exp3=st.columns([5,1,5,1,5])
                #Fragrance Soap
                met1.metric(dishtbl["Products"].iloc[0],dishtbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{dishtbl["Products"].iloc[0]}</b><img class="img_metric" src="https://cdn.shopify.com/s/files/1/0399/6136/2595/products/MamaLemonLiquidWash550ml.png?v=1610715287"> is availabe 
                in {millify(dishtbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(dishtbl["Products"].iloc[1],dishtbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"> <b>{dishtbl["Products"].iloc[1]}</b><img class="img_metric" src="https://sdistributionspzoo.com/wp-content/uploads/2021/08/SDWL-750ml-bottle-packshot.png.png"> is availabe 
                in {millify(dishtbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(dishtbl["Products"].iloc[2],dishtbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{dishtbl["Products"].iloc[2]}</b><img class="img_metric" src="https://be2sure.ng/wp-content/uploads/2021/12/2SURE_FAMILY-DISHWASH.jpg"> is availabe 
                in {millify(dishtbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                #Antiseptics
                st.markdown("""<br>""",unsafe_allow_html=True)
                dettbl=db(name="Detergent_DishWash", table="Det_market")
                st.markdown("""<h6 class="antiseptic_title"><u> Detergent Soaps</u></h6>""",unsafe_allow_html=True)
                met1,met2,met3,met4,met5,met6=st.columns(6)
                exp1,spc,exp2,spc,exp3,spc,exp4,spc,exp5,spc,exp6=st.columns([3,0.5,3,0.5,3,0.5,3,0.5,3,0.5,3])
                #antiseptic soap
                met1.metric(dettbl["Products"].iloc[0],dettbl["%Store"].iloc[0])
                exp1.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[0]}</b><img class="img_metric" src="https://w7.pngwing.com/pngs/163/54/png-transparent-ariel-laundry-detergent-persil-ariel-laundry-detergent-with-downy-cleaning-stain-detergent.png"> is availabe 
                in {millify(dettbl["Stores"].iloc[0])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met2.metric(dettbl["Products"].iloc[1],dettbl["%Store"].iloc[1])
                exp2.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[1]}</b><img class="img_metric" src="https://htsplus.ng/wp-content/uploads/2021/07/image_fe314d2e-5847-4dd9-8b75-e5b2743f9d77_512x512-removebg-preview.png"> is availabe 
                in {millify(dettbl["Stores"].iloc[1])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met3.metric(dettbl["Products"].iloc[2],dettbl["%Store"].iloc[2])
                exp3.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[2]}</b><img class="img_metric" src="https://shoponclick.ng/wp-content/uploads/2020/07/Omo-Washing-Powder-Detergent-2kg.png"> is availabe 
                in {millify(dettbl["Stores"].iloc[2])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</b></i>""",unsafe_allow_html=True)
                met4.metric(dettbl["Products"].iloc[3],dettbl["%Store"].iloc[3])
                exp4.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[3]}</b><img class="img_metric" src="https://cdn.shopify.com/s/files/1/0399/6136/2595/products/zipsmall.png?v=1632229417"> is availabe 
                in {millify(dettbl["Stores"].iloc[3])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met5.metric(dettbl["Products"].iloc[4],dettbl["%Store"].iloc[4])
                exp5.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[4]}</b><img class="img_metric" src="https://htsplus.ng/wp-content/uploads/2021/07/sunlight-1.png"> is availabe 
                in {millify(dettbl["Stores"].iloc[4])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                met6.metric(dettbl["Products"].iloc[5],dettbl["%Store"].iloc[5])
                exp6.markdown(f"""<p class="metric_explainer"><b>{dettbl["Products"].iloc[5]}</b><img class="img_metric" src="https://cdn.shopify.com/s/files/1/0399/6136/2595/products/soklin500g.png?v=1628759288"> is availabe 
                in {millify(dettbl["Stores"].iloc[5])}stores out of <b><u>{stores}</u></b> audited in 
                last <i>30days</i></p>""",unsafe_allow_html=True)
                #explaining market share
                st.markdown("""
                <p class="checkus"><b>👉Would You Like To Have Exclusive Brands Data Intelligence 
                Page?</b> <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>
                <br>""",unsafe_allow_html=True)
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Brands Product Performance(Market Size/Weighted Distribution) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> market share(the volume of your brand products) across retail stores in <b>{country}</b> indicates the depth of your products in stores. 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                #Fragrance
                dishwt=db(name="Detergent_DishWash",table="Dish_Quantity")
                c = (
                Line()
                .add_xaxis(dishwt["Date"].tolist())
                .add_yaxis("Mama Lemon", dishwt["Mama Lemon"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Sunlight", dishwt["Sunlight"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("2Sure",dishwt["2Sure"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Dish Washes Market Size",
                    subtitle="Dish Washes Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                    )
                )
                    )
                
                st_pyecharts(c,height="350px", width="1120px")
                #Antiseptics
                detwt=db(name="Detergent_DishWash",table="Det_Quantity")
                d = (
                Line()
                .add_xaxis(detwt["Date"].tolist())
                .add_yaxis("Ariel", detwt["Ariel"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Good Mama", detwt["Good Mama"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("OMO Detergent",detwt["OMO Detergent"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Zip",detwt["Zip"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Sunlight",detwt["Sunlight"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .add_yaxis("Klin",detwt["Klin"].tolist(), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Detergent Soap Market Size",
                    subtitle="Detergent Soap Volume In Trade"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1.5%", pos_top="5%"),
                    yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True)
                         )
                     )
                            )
                    # xaxis_opts=opts.AxisOpts(grid_index=1),
                    # tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
                    
                
                st_pyecharts(d,height="350px", width="1120px")
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Fast Moving Brands(Most Sold Brand) In Retail</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> most sold brand across stores in <b>{country}</b> indicates the frequency of purchase of each brands 
                These retail stores includes <i><u>neighbouhood retail stores</u>, <u>open market retail stores</u>, 
                <u>shopping malls(like shoprite etc)</u></i></p>
                <br> """,
                unsafe_allow_html=True)
                
                st.markdown("""<h6 class="fragrance_title"><u>Dish Washes</u></h6>""",unsafe_allow_html=True)
                dishmv=db(name="Detergent_DishWash",table="Dish_Fast_moving")

                # fragfig = go.Figure(data=[go.Pie(labels=fragmv["Products"], values=fragmv["Purchase Frequency"], 
                # pull=[0, 0.1, 0],hole=0.1,textinfo="label+percent",insidetextorientation='radial',hoverinfo="label+percent+name")])
                # fragfig.update_layout(title="Sales Freq. By Brand Product"
                #  )
                # fragfig.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
                # fmv1.plotly_chart(fragfig)
                detmv=db(name="Detergent_DishWash",table="Det_Fast_Moving")
                # antisepfig = go.Figure(data=[go.Pie(labels=antisepmv["Products"], values=antisepmv["Purchase Frequency"], 
                # pull=[0,0,0,0.1, 0],hole=0.1,textinfo="label+percent",insidetextorientation='radial',hoverinfo="label+percent+name")])
                # antisepfig.update_layout(title="Sales Freq. By Brand products"
                #  )
                # antisepfig.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
                # fmv3.plotly_chart(antisepfig)
                m1 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(dishmv["Products"],dishmv["%Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Dish Washes In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="0.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m1,height="350px")
                st.markdown("""<br>
                <h6 class="antiseptic_title"><u>Detergent Soaps</u></h6>""",unsafe_allow_html=True)               
                m2 = (
                    Pie()
                    .add("Sales Frequency By Brands products(%)",[list(f) for f in zip(detmv["Products"],detmv["%Frequency(Stores)"])])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Most Sold Detergent Soaps In Stores(%)"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_right="1.5%", pos_top="10%"))
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                        )
                st_pyecharts(m2,height="350px")
                #Price Table
                st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"> Price Analysis of Brand Products & Product Variants Across Retail Stores</h5>
                <p class="title_mktshare_explainer"><b>{Product}</b> price analsys across stores in <b>{country}</b> indicates the average price of 
                products across all stores in last <i>30days</i>. These prices are <b><u>UNIT PRICE(&#8358;)</u></b> of each product variant.
                </p>
                <br> """,
                unsafe_allow_html=True)
                #fragrance table
                st.markdown("""<h6 class="fragrance_title"><u>Dish Washes Prices(&#8358;)</u></h6>""",unsafe_allow_html=True)
                dishprice=db(name="Detergent_DishWash",table="Dish Wash Prices")
                @st.cache
                def convert_df(input_df):
                    return input_df.to_html(escape=False, justify="center", max_rows=15,index=False,col_space=25)
                html = convert_df(dishprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                #antiseptic table
                detprice=db(name="Detergent_DishWash",table="Detergents Prices")
                st.markdown("""<br>
                <h6 class="antiseptic_title"><u>Detergent Soap(&#8358;)</u></h6>""",unsafe_allow_html=True) 
                html = convert_df(detprice)
                st.markdown(f"""<table class="center">{html}</table>""",unsafe_allow_html=True)
                img1,img2,img3,img4="Assets_img/ant1.png","Assets_img/ant3.png","Assets_img/ant4.png","Assets_img/ant5.png"
                st.markdown(f"""
                        <div class="shelf_img_container">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img1, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img2, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img3, "rb").read()).decode()}" loading="lazy">
                <img class="shelf_img"
                src="data:image/png;base64,{base64.b64encode(open(img4, "rb").read()).decode()}" loading="lazy" >
                </div>
                """,unsafe_allow_html=True)
                 #call definition function
                definitions()






with tb2:
    st.markdown("""<p class="quote">Get Quick Insights On <u>Consumers Perceptions</u>, <u>Purchase Decision(Both Online and Offline)</u>,<u>Consumer Journey</u>,<u>Consumer Stickyness</u>,<u>Prefererence</u> 
    About Your Brand & <u><i>Competition Activities</i></u>...
    <img class="img_metric" src="https://www.iconpacks.net/icons/2/free-twitter-logo-icon-2429-thumb.png" 
    # loading="lazy"><img class="img_metric" src="https://flyclipart.com/thumb2/png-facebook-logo-transparent-facebook-logo-images-935854.png" 
    # loading="lazy"><img class="img_metric" src="https://batlab.web.unc.edu/wp-content/uploads/sites/10162/2019/06/instagram-png-instagram-png-logo-1455.png" 
    # loading="lazy"><img class="img_metric" src="https://toppng.com/uploads/preview/reddit-icon-reddit-logo-transparent-115628752708pqmsy4kgm.png" 
    # loading="lazy"></p>""",unsafe_allow_html=True)
    now=datetime.now()
    today=date.today()
    last_30= now - timedelta(days=30)
    brand1,br,brand2,br,brand3,br,brand4=st.columns([4,0.8,4,0.8,4,0.8,4])
    keyword=brand1.text_input("🛍️Kindly Input Your Brand Name or Campaign #Tag",
    placeholder="e.g Milo or #Family")
    location=brand2.text_input("🌐Please Input Your Target Location Name", 
    placeholder= "e.g Nigeria, Abuja Nigeria, UK")
    start_date=brand3.date_input("📅Select Your Prefered Start Period of Engagement")
    end_date=brand4.date_input("📅Select Your Prefered End Period of Engagement")
    start_time=datetime.now()
    end_time=datetime.now()
    if keyword !="" and location !="" and start_date != today:
        tweets=[]
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date} near:{location}").get_items()):
            if i>500:
                break
            tweets.append([tweet.url,
                                   tweet.date,
                                   tweet.id,
                                   tweet.content,
                                   tweet.likeCount,
                                   tweet.retweetCount,
                                   tweet.hashtags,
                                   tweet.replyCount,
                                   tweet.quoteCount,
                                   tweet.source,
                                   tweet.user.username,
                                   tweet.user.location,
                                   tweet.user.followersCount,
                                   tweet.coordinates])
        @st.cache(ttl=24*3600)
        def covert_df(tweets):
                # """st.cache helps cache the function to prevent it running every time people comes on platform"""   
            return tweets.to_csv().encode("utf-8")

        tweets=pand.DataFrame(tweets,columns=['Url',
                        'Datetime',
                        'Tweet Id',
                        'Tweet',
                        'Likes',
                        'Retweets',
                        'Hashtag',
                        'Replies',
                        'Quotes',
                        'Source',
                        'Username',
                        'Location',
                        'UserFollowers',
                        'Coordinates'])
        source=[text.split('>')[1].split('<')[0] for text in tweets.Source]
        tweets["Consumer Platform"]=source
        @st.cache(ttl=24*3600)
        def clean_tweet(tweet):
                # """clean tweets from unnecessary syntax"""
                tweet = re.sub('https://\\S+', '', tweet)
                tweet = re.sub('http://\\S+', '', tweet)
                tweet = re.sub('[^A-Za-z]+', ' ', tweet)
                return tweet
        tweets["clean_tweet"]=tweets["Tweet"].apply(clean_tweet)

        #subjectivity of tweets
        @st.cache(ttl=24*3600)
        def subjectivity(tweet):
                """using TextBlob for subjectivity of the tweets
            """
                return TextBlob(tweet).sentiment.subjectivity

        #polarity
        @st.cache(ttl=24*3600)
        def polarity(tweet):
                # """using same TextBlob to define polarity score"""
                return TextBlob(tweet).sentiment.polarity

        #polarity label
        @st.cache(ttl=24*3600)
        def pol_label(score):
                if score <0:
                    return "Negative"
                if score ==0:
                    return "Neutral"
                if score>0:
                    return "Positive"
        @st.cache(ttl=24*3600)
        def sub_label(score):
                if score>0:
                    return "Subjective"
                if score<=0:
                    return "Objective"
        tweets['Polarity'] = tweets['clean_tweet'].apply(polarity)
        tweets['Polarity Label'] = tweets['Polarity'].apply(pol_label)
        tweets['Subjectivity'] = tweets['clean_tweet'].apply(
                    subjectivity)
        tweets['Subjectivity Label'] = tweets['Subjectivity'].apply(
                    sub_label)
        tweets['Polarity Label Coded'] = tweets['Polarity Label'].map(
                    {'Negative': 0, 'Neutral': 1, 'Positive': 2})
        tweets['Subjectivity Label Coded'] = tweets['Subjectivity Label'].map(
                    {'Subjective': 0, 'Objective': 1})
        #generate coordinates
        tweets['Coordinates'] = tweets['Coordinates'].fillna(
                    'Coordinates(latitude=0.00000, longitude=0.00000)', inplace=False)
        coordinates = tweets['Coordinates']
        data = []
        coords = coordinates
        for coordinate_values in coords:
                cleaned_coord = [
                float(coord) for coord in re.findall(
                    r"\d+\.\d+", str(coordinate_values))]
                data.append(cleaned_coord)
        data = pand.DataFrame(data, columns=['Latitude', 'Longitude'])
        data['Latitude'] = data['Latitude'].astype(float)
        data['Longitude'] = data['Longitude'].astype(float)
        tweets['Latitude'] = data['Latitude']
        tweets['Longitude'] = data['Longitude']
        #write the wteets
        # tweets_10=tweets.head(10)
        # st.write(tweets_10)
        #tweets Analysis
        T_tweets=len(tweets)
        LikesI=tweets["Likes"].sum()
        impact=tweets['UserFollowers'].sum()+tweets['Retweets'].sum()+LikesI+0.5
        impactP=((int(impact)-LikesI)/impact)*100
        impactP=round(impactP,1)
        reach=tweets['UserFollowers'].sum()+0.5
        reachP=((reach-T_tweets)/reach)*100
        reachP=round(reachP,1)
        T_follower=reach/(LikesI+tweets['Retweets'].sum())
        T_follower=round(T_follower,0)
        ins1,brk,ins2=st.columns([2.5,0.1,8])
        ins1.markdown(f"""<h2 class="s_insight">{keyword} | {location}</h2>""",unsafe_allow_html=True)
        ins1.markdown(f"""<p><span style="color:#016969df;"><img class="img_metric" src="https://toppng.com/uploads/preview/twitter-logo-11549680523gyu1fhgduu.png" loading="lazy">
        Twitter</span> Insights({T_tweets}tweets📈) About <b><u>{keyword}</u></b> In <b><u>{location}</u></b> Between <b><u>{start_date}</u></b> And  <b><u>{end_date}</u></b>""",unsafe_allow_html=True)

        # ins2.markdown("""<p class="quote"> “More than 50% of innovation comes from the voice of the customer.” - <i>Lou Rossi</i>
        #                 “Listening is hearing the needs of the customer, 
        #             understanding those needs and making sure the company recognises the opportunity they present.” - 
        #             <i>Frank Eliason</i></p>
        #             """,unsafe_allow_html=True)
        ins1.metric("Tweets Potential Impact",millify(impact))
        ins1.metric("Tweets Potential Reach",millify(reach))
        ins1.metric("Avg. Engagement/Reach",millify(T_follower))
        Likesfig = px.line(tweets, x=tweets["Datetime"], y=tweets["Likes"],
                    color=tweets["Subjectivity Label"],
                    title='Engagement Trends On {} In {}'.format(keyword,location),
            labels={"value":"Tweet Engagement","variable":"Tweets Subjectivity"})
        Likesfig.update_xaxes(
            rangeslider_visible=True)
        Likesfig.update_xaxes(showline=True, linewidth=2, linecolor='grey')
        Likesfig.update_yaxes(showline=True, linewidth=2, linecolor='grey')
        brk.markdown("""<div class="vl"></div>""",unsafe_allow_html=True)
        ins2.plotly_chart(Likesfig, use_container_width=True)
        st.markdown("""<br>""",unsafe_allow_html=True)
        st.markdown("""<p class="checkus"><b>👉Would You Like To Have Exclusive Brands Data Intelligence 
                            Page?</b> <a href="https://d-aggregate.com/subscribe.php"> Kindly Upgrade Your Plan</a>👈</p>""",unsafe_allow_html=True)
        #render some tweets URL
        st.markdown(f""" 
                <br>
                <h5 class="title_mktshare"><img class="img_metric" src="https://toppng.com/uploads/preview/twitter-logo-11549680523gyu1fhgduu.png" loading="lazy">
                        Recent Tweets About {keyword} In {location}</h5>
                 """,unsafe_allow_html=True)
        emb1,emb2=st.columns(2)
        tweet_4=tweets.sample(5,replace=True)
        url1=tweet_4['Url'].iloc[0]
        url2=tweet_4['Url'].iloc[1]
        res1=tweetembed(url1)
        res2=tweetembed(url2)
        with emb1:
            components.html(res1,width=750, height=500)
        with emb2:
            components.html(res2,width=750, height=500)
        st.markdown("""<div class="hl"><hr></div>""",unsafe_allow_html=True)
        #sentiment analysis
        sent1,hole,sent2=st.columns([4,0.1,8])
        sent = px.pie(tweets, values=tweets["Polarity Label"].value_counts(), 
        names=tweets['Polarity Label'].value_counts().index,color=tweets['Polarity Label'].value_counts().index,
             title='Tweets Sentiments Analysis',color_discrete_map={
                "Positive": "Blue",
                "Negative": "Red",
                "Neutral": "goldenrod"
                })
            #  hover_data=['Likes'], labels={'Likes':'Tweets Likes'})
        sent.update_traces(textposition='inside', textinfo='percent+label')
        sent1.plotly_chart(sent, use_container_width=True)
        hole.markdown("""<div class="vl"></div>""",unsafe_allow_html=True)
        RTweets= px.bar(tweets, x="Location", y='Likes',
             hover_data=['Retweets', 'Replies'], color='UserFollowers',
             title="Which Location Are Users Mostly Engaging From? About {}".format(keyword),
             labels={'Retweets':'Retweets By Location'}, height=400)
        sent2.plotly_chart(RTweets,use_container_width=True)
        st.markdown("""<div class="hl"><hr></div>""",unsafe_allow_html=True)
        c = (
        WordCloud()
        .add("WordCloud",[list(f) for f in zip(tweets["clean_tweet"],tweets["UserFollowers"])], 
        word_size_range=[20, 300], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="Tweets WordCloud & Reach",pos_left="40%"))
        ) 
        st_pyecharts(c)
        st.markdown("""<div class="hl"><hr></div>""",unsafe_allow_html=True)
        
        Tmap = folium.Map(location=[tweets["Latitude"].mean(), 
                    tweets["Longitude"].mean()], zoom_start=3, control_scale=True)
        for index, location_info in tweets.iterrows():
            # if location_info["Latitude"]>0 and location_info["Longitude"]>0:
                folium.Marker([location_info["Latitude"], location_info["Longitude"]], 
                popup=location_info["Tweet"]).add_to(Tmap)
        # call to render Folium map in Streamlit
        inst,brk,maps=st.columns([5,0.1,5])
        with inst:
            st.markdown(f""" 
                <br>
                <h5 class="title_mktshare">🗯️Subjectivity Inference On Tweets Related to {keyword}</h5>
                 """,unsafe_allow_html=True)
            fig = px.pie(tweets, values=tweets["Subjectivity Label"].value_counts(), 
            names=tweets['Subjectivity Label'].value_counts().index,color=tweets['Subjectivity Label'].value_counts().index,
             title='Tweets Subjectivity Analysis',color_discrete_map={
                "Subjective": "goldenrod",
                "Objective": "Blue",
                })
            #  hover_data=['Likes'], labels={'Likes':'Tweets Likes'})
            fig.update_traces(textposition='inside', textinfo='percent+label')     
            st.plotly_chart(fig)
        brk.markdown("""<div class="vl"></div>""",unsafe_allow_html=True)
        with maps:
            st.markdown(f""" 
                <br>
                <h5 class="title_mktshare">🌍Spatial Insight Of Tweets About <b>{keyword}</b> From Different Locations</h5>
                 """,unsafe_allow_html=True)
            st_folium(Tmap, height=400,width=750)
        
        st.markdown("""<div class="hl"><hr></div>""",unsafe_allow_html=True)
        parameter.insert({"start_date": str(start_date), "keyword": str(keyword), "location": str(location),"enddate":str(end_date)})
        # emb1.write(f"""{components.html(res1,height=1500, width=1000)}""",unsafe_allow_html=True)
        with st.form("Comments"):
            comment=st.text_area("Kindly share your feedback",max_chars=500,
            placeholder="I love the insights, kindly help me upgrade my plan")
            submitted = st.form_submit_button("Submit feedback")
            if submitted:
                parameter2.insert({"comment": str(comment)})
        consumer_definitions()
    else:
        toaster.show_toast("Error", 
                    "Please fill all necessary inputs", duration=15, threaded=True)  
        
        

   # Every form must have a submit button.
            
            # db.put({"key": str(start_date), "keyword": str(keyword), "location": 
            #         str(location), "comment": str(comment), "enddate":str(end_date)})


    


        



    # sm1,sm2,sm3=st.columns(3)
    # sm1.markdown("""<p class="quote"> “More than 50% of innovation comes from the voice of the customer.” - <i>Lou Rossi</i>
    #                 </p>
    #                 <p class="quote"> “Listening is hearing the needs of the customer, 
    #                 understanding those needs and making sure the company recognises the opportunity they present.” - 
    #                 <i>Frank Eliason</i> </p>
    #                 """,unsafe_allow_html=True)
    # sm2.markdown("""<img class="social_media_img" src="https://365psd.com/images/previews/cce/20-popular-social-media-icons-psd-png-56137.png" 
    # loading="lazy">""",unsafe_allow_html=True)
                
                
                
                
                
                


            







