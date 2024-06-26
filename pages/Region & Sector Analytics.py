import streamlit as st
import requests
import json
import pandas as pd
import datetime
import time

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

st.set_page_config(layout="wide")

# @st.cache_data
def definedCombination():
    if 'DCloading' in st.session_state:
      DCloading.warning("Running Simulations")    

    payload = json.dumps({
       "request_data": {
          "inputs": {
            "SECTOR": SectorInput.split(" ⠀ ")[1] if SectorInput != "ALL" else "ALL",
            "REGION": RegionInput.split(" ⠀ ")[1] if RegionInput != "ALL" else "ALL"
          }
       },
        "request_meta": {
          "call_purpose": "FE",
          "source_system": "SPARK",
          "service_category": ""
        }
      })

    # st.json(payload)

    url = "https://excel.uat.jp.coherent.global/clsa/api/v3/folders/Aggregate%20Models/services/Output%20Analysis%20-%20by%20Sector%20&%20Region/execute"
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

@st.cache_data
def discoveryAPI():  

    payload = json.dumps({
       "request_data": {
          "inputs": {}
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

#Start of UI
image_path = "coherent-clsa-logo.svg"
st.image(image_path, caption="", width=280)

st.write("## Region & Sector Analytics")
st.write("Access our comprehensive database of region and sector analytics to compare and contrast companies across multiple sectors. Our tool provides a detailed analysis of each company’s valuation, enabling you to identify investment opportunities quickly.")
st.text("‎") 

#initialize data
outputs = {"CompanyResults":[{"CompanyName":"MGM China","Region":"China","Sector":"Gaming","Simulations":256,"Gross Margin":0,"Net Margin":-0.181755533943624,"Revenue Growth":0.19509258296829,"Target Multilple":9.29849549401816,"Target Price":0.91295226285384,"Target Price (Upside)":0},{"CompanyName":"PICC","Region":"Korea","Sector":"F&B","Simulations":256,"Gross Margin":0.0268488180328546,"Net Margin":0.067738030217524,"Revenue Growth":0.083660118252909,"Target Multilple":1.1,"Target Price":12.2975599356256,"Target Price (Upside)":0},{"CompanyName":"Sungrow","Region":"Australia","Sector":"Healthcare","Simulations":256,"Gross Margin":0.702185551501273,"Net Margin":6.93832733065174,"Revenue Growth":0.260258180483239,"Target Multilple":16.0999999999999,"Target Price":111.6875,"Target Price (Upside)":0},{"CompanyName":"Yum China","Region":"China","Sector":"F&B","Simulations":256,"Gross Margin":63.7823130139502,"Net Margin":33.5897409027668,"Revenue Growth":22.3180426153228,"Target Multilple":0,"Target Price":0,"Target Price (Upside)":0.126950179110116},{"CompanyName":"CSL","Region":"Australia","Sector":"Healthcare","Simulations":256,"Gross Margin":0,"Net Margin":-0.0341486679423975,"Revenue Growth":0.218057636557498,"Target Multilple":20.2916895550052,"Target Price":0.968889597682799,"Target Price (Upside)":0},{"CompanyName":"CIMB","Region":"Malaysia","Sector":"Banks","Simulations":256,"Gross Margin":0.0209244090164282,"Net Margin":0.0679660630439283,"Revenue Growth":0.083660118252909,"Target Multilple":1.1,"Target Price":12.3035930377106,"Target Price (Upside)":0},{"CompanyName":"Grab","Region":"Singapore","Sector":"Transport","Simulations":256,"Gross Margin":0.591072183635433,"Net Margin":7.48244144706627,"Revenue Growth":0.422713744051762,"Target Multilple":16.0999999999999,"Target Price":120.4375,"Target Price (Upside)":0},{"CompanyName":"MediaTek","Region":"Taiwan","Sector":"Tech","Simulations":256,"Gross Margin":85.2715823577931,"Net Margin":50.8860013643354,"Revenue Growth":22.8733767223018,"Target Multilple":0,"Target Price":0,"Target Price (Upside)":-0.106953478506799}],"noOfCompanies_filtered":8}
DCerrors = []
discoveryData = {"listOfCompanies":[{"List of Companies":"MGM China"},{"List of Companies":"PICC"},{"List of Companies":"Sungrow"},{"List of Companies":"Yum China"},{"List of Companies":"CSL"},{"List of Companies":"CIMB"},{"List of Companies":"Grab"},{"List of Companies":"MediaTek"}],"listOfRegions":[{"List of Regions":"China"},{"List of Regions":"Korea"},{"List of Regions":"Australia"},{"List of Regions":"Malaysia"},{"List of Regions":"Singapore"},{"List of Regions":"Taiwan"}],"listOfSectors":[{"List of Sectors":"Gaming"},{"List of Sectors":"F&B"},{"List of Sectors":"Healthcare"},{"List of Sectors":"Banks"},{"List of Sectors":"Transport"},{"List of Sectors":"Tech"}],"Model_Inputs":[{"Model Inputs":"Mgmcotai Massdropgrowth","CURR":0.7,"NEXT":0.25},{"Model Inputs":"Mgmcotai Vipturnovergrowth","CURR":1.15,"NEXT":0.1},{"Model Inputs":"Mgmmacau Massdropgrowth","CURR":0.51,"NEXT":0.23},{"Model Inputs":"Mgmmacau Vipturnovergrowth","CURR":0.24,"NEXT":0.12}],"Model_Mapping":[{"INPUTS":"FQ0_MGMcotai_Massdropgrowth","OUTPUTS":"net_profit_margin"},{"INPUTS":"FQ0_MGMcotai_VIPturnovergrowth","OUTPUTS":"revenue_growth"},{"INPUTS":"FQ0_MGMmacau_Massdropgrowth","OUTPUTS":"target_multiple"},{"INPUTS":"FQ0_MGMmacau_VIPturnovergrowth","OUTPUTS":"target_price"},{"INPUTS":"FQ1_MGMcotai_Massdropgrowth","OUTPUTS":"historicaldata"},{"INPUTS":"FQ1_MGMcotai_VIPturnovergrowth","OUTPUTS":""},{"INPUTS":"FQ1_MGMmacau_Massdropgrowth","OUTPUTS":""},{"INPUTS":"FQ1_MGMmacau_VIPturnovergrowth","OUTPUTS":""}],"Model_Outputs":[{"Model Outputs":"Net Profit Margin"},{"Model Outputs":"Revenue Growth"},{"Model Outputs":"Target Multiple"},{"Model Outputs":"Target Price"},{"Model Outputs":"Historicaldata"}],"Region":"China","Sector":"Gaming","Input Frequency":"FQ","Spark Service":"Company models/MGM China Model_20240315","Logo URL":"https://www.google.com/search?sca_esv=aab80bd44fbfc9fb&sca_upv=1&rlz=1C1GCEA_enHK973HK973&sxsrf=ACQVn08ECl4eOVZxTmn_ulGXAKgx9BvaHg:1711350191071&q=mgm+china&tbm=isch&source=lnms&prmd=nivmsbtz&sa=X&ved=2ahUKEwjyl-ah7I6FAxWg0jQHHVSBBJ0Q0pQJegQIFhAB&biw=2560&bih=1225&dpr=0.75#imgrc=SxDwMHDDJOruCM","No of Companies":8,"No of Regions":6,"No of Sectors":6}
processingTime = 0

with st.expander("Spark Service (Model)", expanded=False):
  st.markdown('[https://spark.uat.jp.coherent.global/clsa/products/Aggregate%20Models/Output%20Analysis%20-%20by%20Sector%20&%20Region/apiTester/test](https://spark.uat.jp.coherent.global/clsa/products/Aggregate%20Models/Output%20Analysis%20-%20by%20Sector%20&%20Region/apiTester/test)')

#Call discoveryAPI
response = discoveryAPI()

# Parse the JSON response
discoveryData = response.json()['response_data']['outputs']
update_data = discoveryData.get("Model_Inputs")
   
with st.form("DC Form"):
  
  Go = True
  ERRORBOX = st.empty()
  DCLoading = st.empty()

  col01, col02, col03, col04 = st.columns([1, 1, 1, 1])
  with col01:
    list_of_sectors_data = discoveryData.get("listOfSectors")
    if list_of_sectors_data:
      SectorOptions = ["ALL"] + [f"{item.get('Icon', '')} ⠀ {item['List of Sectors']}" for item in list_of_sectors_data]
      SectorInput = st.selectbox("Sector", SectorOptions)

  with col02:
    list_of_regions_data = discoveryData.get("listOfRegions")
    if list_of_regions_data:
      RegionOptions = ["ALL"] + [f"{item.get('Icon', '')} ⠀ {item['List of Regions']}" for item in list_of_regions_data]
      RegionInput = st.selectbox("Region", RegionOptions)

  with col03:
    st.text("‎")

  with col04:
    st.text("‎")

  DCbutton_clicked = st.form_submit_button("Simulate")
if DCbutton_clicked:   
  DCalldata = definedCombination()
  processingTime = DCalldata.json()['response_meta']['process_time']
  outputs = DCalldata.json()['response_data']['outputs']
  DCerrors = DCalldata.json()['response_data']['errors']

  col01, col02 = st.columns([1, 1])
  with col01:
    st.write("Results")
  with col02: 
    st.markdown(f"<p style='text-align: right;'>Processing Time: {processingTime} ms</p>", unsafe_allow_html=True)
  with st.expander("", expanded=True):
    NumCompanies_Metric_placeholder = st.empty()
    st.text("‎")
    SummaryOfCompanies_Df_placeholder = st.empty()

    if outputs['noOfCompanies_filtered'] > 0:
      SectorInputSplit = SectorInput.split(" ⠀ ")[1] if SectorInput != "ALL" else ""
      RegionInputSplit = RegionInput.split(" ⠀ ")[1] if RegionInput != "ALL" else "ALL Regions"
      CompanyPS = "Equity Stocks" if outputs['noOfCompanies_filtered'] > 1 else "Equity Stock"
      NumCompanies_Metric_placeholder.markdown(
        "#### " + str(outputs['noOfCompanies_filtered']) + 
        " <u>" + SectorInputSplit + "</u> " + 
        CompanyPS + " in <u>" + 
        RegionInputSplit + "</u>", 
        unsafe_allow_html=True
      )

      SummaryOfCompanies_Df = pd.DataFrame(outputs['CompanyResults'])
      SummaryOfCompanies_Df = SummaryOfCompanies_Df.loc[:, ~SummaryOfCompanies_Df.columns.str.contains('Column')]
      
      # Create the mapping
      company_logos = {company["List of Companies"]: company["Logo"] for company in discoveryData["listOfCompanies"]}

      # Add the "Logo" column based on "List of Companies"
      SummaryOfCompanies_Df['Logo'] = SummaryOfCompanies_Df['CompanyName'].map(company_logos)

      # Make "Logo" the first column
      SummaryOfCompanies_Df.insert(0, 'Logo', SummaryOfCompanies_Df.pop('Logo'))
    
      all_numeric_columns = SummaryOfCompanies_Df.select_dtypes(include=[float, int]).columns
      SummaryOfCompanies_Df[all_numeric_columns] = SummaryOfCompanies_Df[all_numeric_columns].applymap('{:.2f}'.format)

      columns_to_format = ["Net Income Growth (%)", "Revenue Growth (%)"]

      for column in columns_to_format:
        # Convert the column to numeric type, errors='coerce' will turn non-convertible values into NaN
        SummaryOfCompanies_Df[column] = pd.to_numeric(SummaryOfCompanies_Df[column], errors='coerce')
        
        # Now apply the formatting, multiplying by 100 to convert to percentage, and formatting as string with '%' symbol
        SummaryOfCompanies_Df[column] = SummaryOfCompanies_Df[column].apply(lambda x: '{:.2f}%'.format(x * 100) if not pd.isnull(x) else x)

      SummaryOfCompanies_Df_placeholder.dataframe(
        SummaryOfCompanies_Df,
        use_container_width=True,
        hide_index=True,
        column_config={
          "Logo": st.column_config.ImageColumn("", width=200, help="Streamlit app preview screenshots"),
          "Simulations": st.column_config.TextColumn("Simulations"),
        }
      )
    else:
      st.write("No companies found")


# Add the style tag to change button color to blue
st.markdown("""
<style>
    .stButton button { /* Adjust the class name according to your button's class */
        background-color: #6700F6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)