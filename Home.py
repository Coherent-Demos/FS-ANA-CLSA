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
        st.markdown('<a href="/Equity_Analytics" class="custom-link" target="_self">Open Equity Analytics Model →</a>', unsafe_allow_html=True)

with col2:
    with st.expander("**Region Sector & Analytics Models**", expanded=True):
        st.text("‎")
        st.subheader("Discover Region & Sector Analytics with Ease")
        st.write("Access our comprehensive database of region and sector analytics to compare and contrast companies across multiple sectors. Our tool provides a detailed analysis of each company’s valuation, enabling you to identify investment opportunities quickly.")
        st.text("‎")
        st.markdown('<a href="/Region_&_Sector_Analytics" class="custom-link" target="_self">Open Region & Sector Analytics Model →</a>', unsafe_allow_html=True)

# CSS to inject for styling links
style = """
<style>
    a.custom-link {
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
    a.custom-link:hover {
        background-color: #5e00d6; /* Darken bg by 5% */
        text-decoration: none; /* No underline on hover */
        color: white;
    }
</style>
"""
# Inject the style into the app
st.markdown(style, unsafe_allow_html=True)