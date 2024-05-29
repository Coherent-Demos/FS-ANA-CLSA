import streamlit as st
import requests
import json
import pandas as pd
import datetime
import time
import os

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

st.set_page_config(layout="wide")

# @st.cache_data
def definedCombination(inputdata):
    if 'DCloading' in st.session_state:
      DCloading.warning("Running Simulations")    

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "Base_Inputs": inputdata,
            "CompanyName": selectedCompany
          }
       },
        "request_meta": {
          "call_purpose": "CLSA FE",
          "source_system": "SPARK",
          "service_category": ""
        }
      })

    # st.json(payload)

    url = "https://excel.uat.jp.coherent.global/clsa/api/v3/folders/Aggregate%20Models/services/Output%20Analysis%20-%20by%20Company/execute"
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'clsa',
       'x-synthetic-key': '3ca9da18-31fa-4a82-a9ba-44130dff5c6a'
    }
    # }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    if 'DCloading' in st.session_state:
      DCloading.success("API call successful")
    return response

def discoveryAPI(selectedCompany):  

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "Company": selectedCompany
          }
       },
        "request_meta": {
          "call_purpose": "CLSA FE",
          "source_system": "SPARK",
          "service_category": ""
        }
      })

    url = "https://excel.uat.jp.coherent.global/clsa/api/v3/folders/Aggregate%20Models/services/Analysis%20-%20CLSA%20Spark%20Services/execute"
    headers = {
       'Content-Type': 'application/json',
       'x-tenant-name': 'clsa',
       'x-synthetic-key': '3ca9da18-31fa-4a82-a9ba-44130dff5c6a'
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    return response

def generate_comb_chart(data, value_pairs, title):
    if 'Analyst Prediction' in value_pairs and value_pairs['Analyst Prediction'] is not None:
        value_pairs['Analyst Prediction'] = round(value_pairs['Analyst Prediction'], 3)

    # Check for None values in value_pairs
    if any(value is None for value in value_pairs.values()):
        # Create an empty chart with a message
        fig = go.Figure()
        fig.add_annotation(x=0.5, y=0.5, text='No Data Available', showarrow=False, xref='paper', yref='paper', font=dict(size=12))
        fig.update_layout(xaxis={'visible': False}, yaxis={'visible': False}, title=title + " Distribution", showlegend=False)
        return fig
    
    # Continue with the original function if no None values are found
    df = pd.DataFrame(data)
    fig = go.Figure()

    # Adding bar chart for the historical data
    fig.add_trace(go.Bar(x=df['Historical'], y=df['Count'], name='Original Data', marker_color='#000662'))

    # Add Min-Max range as a filled area (this should be added first)
    min_value = value_pairs['Min']
    max_value = value_pairs['Max']
    fig.add_shape(type='rect', x0=min_value, x1=max_value, y0=df['Count'].min(), y1=df['Count'].max(), fillcolor='#FEF151', opacity=0.35, line_width=0)

    # Add line for "Analyst Prediction" as a shape
    if 'Analyst Prediction' in value_pairs:
        value = value_pairs['Analyst Prediction']
        fig.add_shape(type='line', x0=value, x1=value, y0=df['Count'].min(), y1=df['Count'].max(), line=dict(color='#5E75EC', width=4))

    # Add lines for each value pair except "Analyst Prediction"
    for label, value in value_pairs.items():
        if label != "Analyst Prediction":
            fig.add_trace(go.Scatter(x=[value, value], y=[df['Count'].min(), df['Count'].max()], mode='lines', opacity=0.3, line=dict(color='#FEF151', width=1), name=f"{label}: {value}"))

    # Add line for "Analyst Prediction" to ensure it appears in the legend
    if 'Analyst Prediction' in value_pairs:
        value = value_pairs['Analyst Prediction']
        fig.add_trace(go.Scatter(x=[value, value], y=[df['Count'].min(), df['Count'].max()], mode='lines', line=dict(color='#5E75EC', width=4), name=f"Analyst Prediction: {value}"))

    # Update layout
    fig.update_layout(
        title={
            'text': "<br />" + title + " Distribution",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis={
            'title': {
                'text': title,
                'font': {'color': 'black', 'size': 14, 'family': 'Source Sans Pro, sans-serif'},
            },
            'tickfont': {'color': '#a0a0a0', 'size': 12, 'family': 'Source Sans Pro, sans-serif'},
            'tickformat': ',.0%'  # Add percentage sign to x-axis labels
        },
        yaxis={
            'title': {
                'text':  "<br />" + 'Frequency',
                'font': {'color': 'black', 'size': 14, 'family': 'Source Sans Pro, sans-serif'}
            },
            'tickfont': {'color': '#a0a0a0', 'size': 12, 'family': 'Source Sans Pro, sans-serif'},
            'dtick': 1  # Ensure only whole numbers are shown
        },
        legend={
            'orientation': "h",  # Horizontal orientation
            'x': 0.5,
            'xanchor': 'center',
            'y': -0.2,
            'yanchor': 'top'
        },
        plot_bgcolor='#fafafa',
        paper_bgcolor='#fafafa',
        margin=dict(t=80, l=40, b=32, r=100),
        height=600
    )

    return fig

def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / stddev) ** 2)

def generate_comb_chart_best_fit(data, value_pairs, title):
    # Create a DataFrame
    df = pd.DataFrame(data)

    # Set the font family
    plt.rcParams["font.family"] = ["Arial"]

    # Create a scatter plot using Matplotlib
    fig, ax = plt.subplots()

    # Scatter plot with smaller dots and custom color
    ax.scatter(df["Historical"], df["Count"], color='#a0a0a0', label="Original Data", s=30)

    # Fit the model to the data
    params, covariance = curve_fit(gaussian, df["Historical"], df["Count"], p0=[1, np.mean(df["Historical"]), 1])
    amplitude, mean, stddev = params

    # Create x values for the fitted curve
    x_fit = np.linspace(min(df["Historical"]), max(df["Historical"]), 100)

    # Generate the fitted curve using the fitted parameters
    y_fit = gaussian(x_fit, amplitude, mean, stddev)

    # Plot the fitted curve as a best-fit line with blue color
    ax.plot(x_fit, y_fit, color='blue', linestyle='-', linewidth=2, label="Best-Fit Line")

    # Plot the new value pairs as vertical lines
    for label, value in value_pairs.items():
        line_color = 'red' if label == "Analyst Prediction" else '#f4d35e'
        line_width = 1
        ax.axvline(x=value, color=line_color, linestyle='-', linewidth=line_width, label=f"{label}: {value}")

    # Fill the area below the best-fit line with blue color
    ax.fill_between(x_fit, y_fit, color='blue', alpha=0.2, label="Area Below Best-Fit Line")

    # Plot the min-max range area
    min_value = value_pairs["Min"]
    max_value = value_pairs["Max"]
    ax.fill_betweenx(y=[ax.get_ylim()[0], ax.get_ylim()[1]], x1=min_value, x2=max_value, color='#f4d35e', alpha=0.5, label="Min-Max Range")

    # Customize the chart
    ax.set_xlabel(title)
    ax.set_ylabel("Count")
    ax.set_title(title + " Distribution")

    # Add a legend
    ax.legend()

    return fig

def multiply_and_convert_to_json(input_df):
    # Create a copy of the input DataFrame
    modified_df = input_df.copy()

    for column in modified_df.columns[1:]:  # Start from the second column
      # trim " %" from the end of the string
      modified_df[column] = modified_df[column].str.rstrip(" %")
      modified_df[column] = pd.to_numeric(modified_df[column], errors='coerce', downcast='integer') / 100

    # Convert the DataFrame to JSON format
    json_data = modified_df.to_json(orient='records')

    return json_data

def string_check(value):
    # Check if the value is a string
    if isinstance(value, str):
        try:
            # Convert the string to an integer
            value = int(value)
        except ValueError:
            # Handle the case where the string cannot be converted to an integer
            return 0

    # If value is an int or has been successfully converted to int, return it
    return value

def detect_currency_or_percentage(value):
    return "$" if " ($)" in value else "%" if " (%)" in value else ""


#Start of UI
image_path = "coherent-clsa-logo.svg"
st.image(image_path, caption="", width=280)

st.text("‎") 
st.write("## Equity Analytics")
st.write("Input your financial assumptions and instantly receive analysis on key financial metrics for a broad range of companies. Our advanced models transform your inputs into valuable outputs, helping you make informed investment decisions.")

#initialize data
json_data = [
  {
    "INPUTS": "INPUT 1",
    "Historical 1 SD": 1.5033853094776,
    "CURR - BASE": 0.24,
    "CURR - MIN": -1.2633853094776,
    "CURR - MAX": 1.7433853094776,
    "NEXT - BASE": 0.12,
    "NEXT - MIN": -1.3833853094776,
    "NEXT - MAX": 1.6233853094776
  },
  {
    "INPUTS": "INPUT 2",
    "Historical 1 SD": 3.15565794909837,
    "CURR - BASE": 0.51,
    "CURR - MIN": -2.64565794909837,
    "CURR - MAX": 3.66565794909837,
    "NEXT - BASE": 0.23,
    "NEXT - MIN": -2.92565794909837,
    "NEXT - MAX": 3.38565794909837
  },
  {
    "INPUTS": "INPUT 3",
    "Historical 1 SD": 4.07886347775884,
    "CURR - BASE": 1.15,
    "CURR - MIN": -2.92886347775884,
    "CURR - MAX": 5.22886347775884,
    "NEXT - BASE": 0.1,
    "NEXT - MIN": -3.97886347775884,
    "NEXT - MAX": 4.17886347775884
  },
  {
    "INPUTS": "INPUT 4",
    "Historical 1 SD": 8.21102123851926,
    "CURR - BASE": 0.7,
    "CURR - MIN": -7.51102123851926,
    "CURR - MAX": 8.91102123851926,
    "NEXT - BASE": 0.25,
    "NEXT - MIN": -7.96102123851926,
    "NEXT - MAX": 8.46102123851926
  }
]
Spark_outputs = {"gm_htable":[{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0},{"Historical":0,"Count":0}],"listOfOutputs":[{"DS OUTPUTS":"net_profit_margin"},{"DS OUTPUTS":"revenue_growth"},{"DS OUTPUTS":"target_multiple"},{"DS OUTPUTS":"target_price"}],"minmaxtable":[{"Metric":"Analys Prediction","Revenue Growth":350.540556197299,"Net Profit Margin":12.0240055813407,"Gross Margin":"","Target multiple":16.8226055718116,"Target Price upside":91.2929594181175},{"Metric":"Min (Simulation)","Revenue Growth":-3.3931025420385,"Net Profit Margin":-838.675349051121,"Gross Margin":-838.675349051121,"Target multiple":-838.675349051121,"Target Price upside":-3.3931025420385},{"Metric":"Max (Simulation)","Revenue Growth":5.1129808598092,"Net Profit Margin":1089.80887713455,"Gross Margin":1089.80887713455,"Target multiple":127.252380327068,"Target Price upside":5.1129808598092}],"npm_htable":[{"Historical":-110,"Count":0},{"Historical":-104,"Count":2},{"Historical":-98,"Count":1},{"Historical":-92,"Count":0},{"Historical":-86,"Count":0},{"Historical":-80,"Count":0},{"Historical":-74,"Count":0},{"Historical":-68,"Count":0},{"Historical":-62,"Count":0},{"Historical":-56,"Count":0},{"Historical":-50,"Count":0},{"Historical":-44,"Count":1},{"Historical":-38,"Count":0},{"Historical":-32,"Count":2},{"Historical":-26,"Count":0},{"Historical":-20,"Count":0},{"Historical":-14,"Count":0},{"Historical":-8,"Count":2},{"Historical":-2,"Count":1},{"Historical":4,"Count":5},{"Historical":10,"Count":8},{"Historical":16,"Count":13},{"Historical":22,"Count":5},{"Historical":28,"Count":0},{"Historical":34,"Count":0},{"Historical":40,"Count":0}],"rg_htable":[{"Historical":-79,"Count":1},{"Historical":-58,"Count":1},{"Historical":-37,"Count":3},{"Historical":-16,"Count":11},{"Historical":5,"Count":17},{"Historical":26,"Count":1},{"Historical":47,"Count":2},{"Historical":68,"Count":2},{"Historical":89,"Count":0},{"Historical":110,"Count":0},{"Historical":131,"Count":0},{"Historical":152,"Count":0},{"Historical":173,"Count":0},{"Historical":194,"Count":0},{"Historical":215,"Count":0},{"Historical":236,"Count":0},{"Historical":257,"Count":0},{"Historical":278,"Count":0},{"Historical":299,"Count":0},{"Historical":320,"Count":0},{"Historical":341,"Count":1},{"Historical":362,"Count":0},{"Historical":383,"Count":0},{"Historical":404,"Count":0}],"Simualtions":256,"TM_htable":[{"Historical":8,"Count":997},{"Historical":62,"Count":17},{"Historical":116,"Count":18},{"Historical":170,"Count":0},{"Historical":224,"Count":0},{"Historical":278,"Count":0},{"Historical":332,"Count":0},{"Historical":386,"Count":0},{"Historical":440,"Count":2},{"Historical":494,"Count":1},{"Historical":548,"Count":2},{"Historical":602,"Count":0},{"Historical":656,"Count":0},{"Historical":710,"Count":0},{"Historical":764,"Count":0}],"TPU_htable":[{"Historical":-58,"Count":275},{"Historical":-37,"Count":181},{"Historical":-16,"Count":106},{"Historical":5,"Count":132},{"Historical":26,"Count":286},{"Historical":47,"Count":230},{"Historical":68,"Count":118},{"Historical":89,"Count":78},{"Historical":110,"Count":48},{"Historical":131,"Count":14},{"Historical":152,"Count":1},{"Historical":173,"Count":0}],"Gross Margin":0,"Net Margin":3.77899625339069,"Revenue Growth":0.179666874434118,"Target Multilple":9.79730203448272,"Target Price":0.859706677248583,"Target Price (Upside)":0}
discoveryData = {"listOfCompanies":[{"List of Companies":"MGM China","Logo":"https://www.amk-international.com/partners/mgm.png"},{"List of Companies":"PICC","Logo":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/People%27s_Insurance_Company_of_China_logo.svg/1280px-People%27s_Insurance_Company_of_China_logo.svg.png"},{"List of Companies":"Sungrow","Logo":"https://companieslogo.com/img/orig/300274.SZ_BIG-11a258e5.png?t=1685244307"},{"List of Companies":"Yum China","Logo":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdaHylMHKhNNBUxWlWOiKp3WoDgb7KyupjgyqJElki0g&s"},{"List of Companies":"CSL","Logo":"https://toppng.com/uploads/preview/csl-vector-logo-download-11573949412sjfa8yj7kq.png"},{"List of Companies":"CIMB","Logo":"https://originallyus.sg/wp-content/uploads/2022/01/CIMB-Logo.png"},{"List of Companies":"Grab","Logo":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTb4y-nlez45Pk3DsBPWlkt7482eXyrQgyyHcARP5TEBg&s"},{"List of Companies":"MediaTek","Logo":"https://w7.pngwing.com/pngs/893/931/png-transparent-logo-mediatek-brand-product-design-label-ces-2018-monitor-text-label-rectangle-thumbnail.png"}],"listOfRegions":[{"List of Regions":"China","Icon":"🇨🇳"},{"List of Regions":"Korea","Icon":"🇰🇷"},{"List of Regions":"Australia","Icon":"🇦🇺"},{"List of Regions":"Malaysia","Icon":"🇲🇾"},{"List of Regions":"Singapore","Icon":"🇸🇬"},{"List of Regions":"Taiwan","Icon":"🇹🇼"}],"listOfSectors":[{"List of Sectors":"Gaming","Icon":"🎮"},{"List of Sectors":"F&B","Icon":"🍽️"},{"List of Sectors":"Healthcare","Icon":"🚑"},{"List of Sectors":"Banks","Icon":"🏦"},{"List of Sectors":"Transport","Icon":"🚌"},{"List of Sectors":"Tech","Icon":"🤖"}],"Model_Inputs":[{"Model Inputs":"Kfc Cogs Growth","CURR":0.31,"NEXT":0.31,"HISTORICAL 1SD":0.0621},{"Model Inputs":"Kfc Same Store Sales Growth","CURR":0.05,"NEXT":0.01,"HISTORICAL 1SD":0.0142},{"Model Inputs":"Pizzahut Cogs Growth","CURR":0.31,"NEXT":0.31,"HISTORICAL 1SD":0.0604},{"Model Inputs":"Pizzahut Same Store Sales Growth","CURR":0.07,"NEXT":0.02,"HISTORICAL 1SD":0.0177}],"Model_Mapping":[{"INPUTS":"FY0_KFC_COGS_growth","OUTPUTS":"Gross_Margin"},{"INPUTS":"FY0_KFC_same_store_sales_growth","OUTPUTS":"Net_profit_margin"},{"INPUTS":"FY0_Pizzahut_COGS_growth","OUTPUTS":"Revenue_growth"},{"INPUTS":"FY0_Pizzahut_same_store_sales_growth","OUTPUTS":"target_multiple"},{"INPUTS":"FY1_KFC_COGS_growth","OUTPUTS":"targetprice_upside"},{"INPUTS":"FY1_KFC_same_store_sales_growth","OUTPUTS":"historicaldata"},{"INPUTS":"FY1_Pizzahut_COGS_growth","OUTPUTS":""},{"INPUTS":"FY1_Pizzahut_same_store_sales_growth","OUTPUTS":""}],"Model_Outputs":[{"Model Outputs":"Gross Margin"},{"Model Outputs":"Net Profit Margin"},{"Model Outputs":"Revenue Growth"},{"Model Outputs":"Target Multiple"},{"Model Outputs":"Targetprice Upside"},{"Model Outputs":"Historicaldata"}],"Region":"China","Sector":"F&B","Input Frequency":"FY","Spark Service":"Company models/Yum China_080223-v4","Logo URL":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdaHylMHKhNNBUxWlWOiKp3WoDgb7KyupjgyqJElki0g&s","No of Companies":8,"No of Regions":6,"No of Sectors":6}
DCerrors = []
companyOptions = ["", 'MGM China', 'PICC', 'Sungrow', 'Yum China', 'CSL', 'CIMB', 'Grab']
update_data = discoveryData.get("Model_Inputs")

with st.expander("Spark Service (Model)"):
  st.markdown('[https://spark.uat.jp.coherent.global/clsa/products/Aggregate%20Models/Output%20Analysis%20-%20by%20Company/apiTester/test](https://spark.uat.jp.coherent.global/clsa/products/Aggregate%20Models/Output%20Analysis%20-%20by%20Company/apiTester/test)')

st.write("  ")
response = discoveryAPI("")
discoveryData = response.json()['response_data']['outputs']
list_of_companies_data = discoveryData.get("listOfCompanies")

if list_of_companies_data:
  companyOptions = [""] + [item["List of Companies"] for item in list_of_companies_data]
colcompany01, colcompany02, colcompany03 = st.columns([1, 1, 1])
with colcompany01:  
  selectedCompany = st.selectbox("Select an Equity Stock", companyOptions)
with colcompany02:
  st.write("  ")
with colcompany03:
  st.write("  ")

if selectedCompany != "":

  with st.expander("", expanded=True):
    col30, col31, col32, col33, col34 = st.columns([0.1,1.5,1,1,1])
    with col30:
      st.write("  ")
    with col31:
      LOGO_placeholder = st.container()
    with col32:  
      COMPANY_placeholder = st.container()
    with col33:
      REGION_placeholder = st.container()
    with col34:
      SECTOR_placeholder = st.container()

    # Call discoveryAPI
    response = discoveryAPI(selectedCompany)
    # Parse the JSON response
    discoveryData = response.json()['response_data']['outputs']
    update_data = discoveryData.get("Model_Inputs")

    Local_Image = "pages/" + selectedCompany + ".svg"
    LOGO_url = Local_Image

    with LOGO_placeholder:
      LOGO_placeholder.image(LOGO_url, caption="", width=200)
    with COMPANY_placeholder:
      st.markdown("<div class='custom-metric-label'>Company</div><div class='custom-metric-value'>" + selectedCompany + "</div>", unsafe_allow_html=True)
    with REGION_placeholder:  
      st.markdown("<div class='custom-metric-label'>Region</div><div class='custom-metric-value'>" + discoveryData.get("Region") + "</div>", unsafe_allow_html=True)
    with SECTOR_placeholder:  
      st.markdown("<div class='custom-metric-label'>Sector</div><div class='custom-metric-value'>" + discoveryData.get("Sector") + "</div>", unsafe_allow_html=True)

    st.write("  ")

  with st.form("DC Form"):
    Go = True
    ERRORBOX = st.empty()
    DCLoading = st.empty()

    st.write("Choose your assumption range")
    inputTableContainer = st.container()
    st.caption("Default values for the input cells have been derived using the base assumption that min & max values are within +1 and -1 Standard Deviations")
    DCbutton_clickedContainer = st.container()

  st.write("  ")
  st.write("  ")

  ResultsContainer = st.container()

  with inputTableContainer:

    for i in range(len(json_data)):

      unit = detect_currency_or_percentage(update_data[i]["Model Inputs"])
      unit_dollar = "$" if unit == "$" else ""
      unit_percent = "%" if unit == "%" else ""
      json_data[i]["INPUTS"] = update_data[i]["Model Inputs"].replace(" (%)", "").replace(" ($)", "")

      json_data[i]["CURR - MIN"] = f"{unit_dollar} {json_data[i]['CURR - BASE'] - json_data[i]['Historical 1 SD']:.2f} {unit_percent}"
      json_data[i]["CURR - MAX"] = f"{unit_dollar} {json_data[i]['CURR - BASE'] + json_data[i]['Historical 1 SD']:.2f} {unit_percent}"
      json_data[i]["NEXT - MIN"] = f"{unit_dollar} {json_data[i]['NEXT - BASE'] - json_data[i]['Historical 1 SD']:.2f} {unit_percent}"
      json_data[i]["NEXT - MAX"] = f"{unit_dollar} {json_data[i]['NEXT - BASE'] + json_data[i]['Historical 1 SD']:.2f} {unit_percent}"

      json_data[i]['Historical 1 SD'] = f"{unit_dollar} {update_data[i]['HISTORICAL 1SD']:.2f} {unit_percent}"
      json_data[i]['CURR - BASE'] = f"{unit_dollar} {update_data[i]['CURR']:.2f} {unit_percent}"
      json_data[i]['NEXT - BASE'] = f"{unit_dollar} {update_data[i]['NEXT']:.2f} {unit_percent}"

    def highlight_col(x):
      r = 'background-color: #fafafa; color: #909090'
      df1 = pd.DataFrame('', index=x.index, columns=x.columns)
      df1.loc[:, :] = r
      return df1  

    # Create a DataFrame from JSON data
    df = pd.DataFrame(json_data)
    all_numeric_columns = df.select_dtypes(include=[float, int]).columns

    columns_to_exclude = []
    numeric_columns = [col for col in all_numeric_columns if col not in columns_to_exclude]

    df[numeric_columns] = df[numeric_columns] * 100

    inputTable = st.data_editor(
      df.style.apply(highlight_col, axis=None),
      use_container_width=True,
      hide_index=True,
      column_config={
        "INPUTS": st.column_config.Column("INPUTS", disabled=True),
        "Historical 1 SD": st.column_config.Column("Historical 1 SD", disabled=True),
        "CURR - BASE": st.column_config.Column("CURR - BASE", disabled=True),
        "NEXT - BASE": st.column_config.Column("NEXT - BASE", disabled=True),
        "CURR - MIN": st.column_config.Column("CURR - MIN"),
        "CURR -  MAX": st.column_config.Column("CURR -  MAX"),
        "NEXT - MIN": st.column_config.Column("NEXT - MIN"),
        "NEXT - MAX": st.column_config.Column("NEXT - MAX")
      }
    )

  with DCbutton_clickedContainer:
    DCbutton_clicked = st.form_submit_button("Simulate")
    if DCbutton_clicked: 
      apiInput = multiply_and_convert_to_json(inputTable)
      apiInput_dict = json.loads(apiInput)
      DCalldata = definedCombination(apiInput_dict)
      processingTime = DCalldata.json()['response_meta']['process_time']
      Spark_outputs = DCalldata.json()['response_data']['outputs']
      DCerrors = DCalldata.json()['response_data']['errors']

      with ResultsContainer:
        colresults01, colresults02 = st.columns([1, 1])
        with colresults01:
          st.write(selectedCompany + " Results")
        with colresults02: 
          st.markdown(f"<p style='text-align: right;'>Processing Time: {processingTime} ms</p>", unsafe_allow_html=True)

        col01, col02 = st.columns([1,1])
        
        with col01:
          with st.expander("", expanded=True):
            RG_METRIC_placeholder = st.empty()
        with col02:
          with st.expander("", expanded=True):
            NIG_METRIC_placeholder = st.empty()
          
        TM_CHART_placeholder = st.empty()
        RG_CHART_placeholder = st.empty() 
        NIG_CHART_placeholder = st.empty()
        NPM_CHART_placeholder = st.empty()

        # Chart value averages 
        if isinstance(Spark_outputs["Revenue Growth (%)"], int) or isinstance(Spark_outputs["Revenue Growth (%)"], float):
          RG_AVG = round(Spark_outputs["Revenue Growth (%)"] * 100, 2)
        else: 
          RG_AVG = 0
        RG_METRIC_placeholder.metric(label='Revenue Growth (%)', value=f"{RG_AVG}%" if RG_AVG != 0 else "N/A") 

        if isinstance(Spark_outputs["Net Income Growth (%)"], int) or isinstance(Spark_outputs["Net Income Growth (%)"], float):
          NIG_AVG = round(Spark_outputs["Net Income Growth (%)"] * 100, 2)
        else: 
          NIG_AVG = 0
        NIG_METRIC_placeholder.metric(label="Net Income Growth (%)", value=f"{NIG_AVG}%" if NIG_AVG != 0 else "N/A")
        
        #generate line chart of results
        if not DCerrors:
          data_rg = pd.DataFrame(Spark_outputs["rg_htable"])
          value_pairs_rg = {
            "Min": round(string_check(Spark_outputs["minmaxtable"][1]["Revenue Growth (%)"]), 1),
            "Max": round(string_check(Spark_outputs["minmaxtable"][2]["Revenue Growth (%)"]), 1),
            "Analyst Prediction": Spark_outputs["minmaxtable"][0]["Revenue Growth (%)"]
          }
          chart_fig = generate_comb_chart(data_rg, value_pairs_rg, "Revenue Growth")
          RG_CHART_placeholder.plotly_chart(chart_fig, use_container_width=True)

          data_nig = pd.DataFrame(Spark_outputs["npm_htable"])
          value_pairs_nig = {
            "Min": round(string_check(Spark_outputs["minmaxtable"][1]["Net Income Growth (%)"]), 2),
            "Max": round(string_check(Spark_outputs["minmaxtable"][2]["Net Income Growth (%)"]), 2),
            "Analyst Prediction": Spark_outputs["minmaxtable"][0]["Net Income Growth (%)"]
          }
          chart_fig = generate_comb_chart(data_nig, value_pairs_nig, "Net Income Growth (%)")
          NIG_CHART_placeholder.plotly_chart(chart_fig, use_container_width=True)

          # Function to format values safely
          def safe_format(value):
              try:
                  # If the value is zero or can be converted to a float, format it.
                  return "{:,.2f}".format(float(value))
              except (TypeError, ValueError):
                  # If there is an error during formatting, return a default string
                  return "N/A"

          initState = False
        else:
          error_messages = [error["message"] for error in DCerrors]
          if error_messages:
              ERRORBOX.error("\n ".join(error_messages))
  
# Add the style tag to change button color to blue
st.markdown("""
<style>
    .stButton button { /* Adjust the class name according to your button's class */
        background-color: #6700F6 !important;
        color: white !important;
    }
            
    .stPlotlyChart  {
      border: 1px solid #dcdcdc;
      border-radius: 8px;
      box-sizing: border-box;
      overflow: hidden;
    }   

    a {
            color: #6700F6!important;
    }          
  
    .custom-metric-label {
        font-size: 14px;      
    }
            
    .custom-metric-value {
      font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

