import streamlit as st
st.set_page_config(layout="wide")

#Start of UI
image_path = "coherent-clsa-logo.svg"
st.image(image_path, caption="", width=280)

st.text("‎")
st.title("CLSA Analytics Dashboard: Unlock the Power of Equity Research")
st.text("‎")

col1, col2 = st.columns([1, 1])

with col1:
  with st.expander("**Equity Analytics Models**", expanded=True):
    st.text("‎")
    st.subheader("Unlock Insights with Company Analytics")
    st.write("Input your financial assumptions and instantly receive analysis on key financial metrics for a broad range of companies. Our advanced models transform your inputs into valuable outputs, helping you make informed investment decisions.")
    st.text("‎")
    st.page_link("pages/Equity Analytics.py", label="Open Equity Analytics Model →", icon="1️⃣")

with col2:
  with st.expander("**Region Sector & Analytics Models**", expanded=True):
    st.text("‎")
    st.subheader("Discover Region Sector Analytics with Ease")
    st.write("Access our comprehensive database of Region Sector Analytics to compare and contrast companies across multiple sectors. Our tool provides a detailed analysis of each company’s valuation, enabling you to identify investment opportunities quickly.")
    st.text("‎")
    st.page_link("pages/Region And Sector Analytics.py", label="Open Region & Sector Analytics Model →", icon="2️⃣")
