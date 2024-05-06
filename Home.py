import streamlit as st


#Start of UI
image_path = "coherent-clsa-logo.png"
st.image(image_path, caption="")

st.title("CLSA Analytics Dashboard: Unlock the Power of Equity Research")

st.header("Company Equity Analytics Models", divider='blue')
st.subheader("Unlock Insights with Company Analytics")
st.write("Input your financial assumptions and instantly receive analysis on key financial metrics for a broad range of companies. Our advanced models transform your inputs into valuable outputs, helping you make informed investment decisions.")

st.page_link("pages/Equity Analytics.py", label="Equity Analytics Model", icon="1️⃣")

st.header("Region & Sector Valuation Analytics", divider='blue')
st.subheader("Explore Markets with Region & Sector Analytics")
st.write("Select a region and sector to access detailed reports on all companies within our expansive portfolio. Our tool simplifies your research process by providing CLSA’s expert analyses, enabling you to spot market opportunities swiftly.")

st.page_link("pages/Company Valuations.py", label="Company Valuations Model", icon="2️⃣")