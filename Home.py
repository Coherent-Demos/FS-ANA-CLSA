import streamlit as st
st.set_page_config(layout="wide")

#Start of UI
image_path = "coherent-clsa-logo.svg"
st.image(image_path, caption="", width=280)

st.text("‎")
st.title("Equity Analytics Dashboard: Unlock the Power of Equity Research")
st.text("‎")

col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("**Equity Analytics Models**", expanded=True):
        st.text("‎")
        st.subheader("Unlock Insights with Company Analytics")
        st.write("Input your financial assumptions and instantly receive analysis on key financial metrics for a broad range of companies. Our advanced models transform your inputs into valuable outputs, helping you make informed investment decisions.")
        st.text("‎")
        st.button("Open Equity Analytics Model →", on_click=lambda: st.experimental_rerun(), args=("pages/Equity Analytics.py",), kwargs={'label': "Open Equity Analytics Model →"})

with col2:
    with st.expander("**Region Sector & Analytics Models**", expanded=True):
        st.text("‎")
        st.subheader("Discover Region & Sector Analytics with Ease")
        st.write("Access our comprehensive database of region and sector analytics to compare and contrast companies across multiple sectors. Our tool provides a detailed analysis of each company’s valuation, enabling you to identify investment opportunities quickly.")
        st.text("‎")
        st.button("Open Region & Sector Analytics Model →", on_click=lambda: st.experimental_rerun(), args=("pages/Region & Sector Analytics.py",), kwargs={'label': "Open Region & Sector Analytics Model →"})

# CSS to inject
style = """
<style>
    .stButton>button {
        color: white;
        background-color: #6700F6;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #5e00d6; /* Darken bg by 5% */
        text-decoration: none; /* No underline on hover */
        color: white
    }
</style>
"""

st.markdown(style, unsafe_allow_html=True)