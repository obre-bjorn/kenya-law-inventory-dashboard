import streamlit as st
import pandas as pd
import plotly.express as px

from sheetgetter import getDataFromExcelSheets

def generateDashboard():
    st.set_page_config(layout="wide")

    # Load all data
    all_data = getDataFromExcelSheets('inventory-report.xlsx')

    # Ensure correct date format and sorting
    all_data['Month'] = pd.to_datetime(all_data['Month'], format='%b-%y')
    all_data = all_data.sort_values(['Person', 'Month'])
    
    

    # --- Annual Summary ---
    summary = all_data.groupby("Person").agg({
        "Carry": "sum",
        "Cases": "sum",
        "Actual": "sum"
    }).reset_index()

    summary["Fair_Target"] = summary["Carry"] + summary["Cases"]
    summary["Performance_%"] = (summary["Actual"] / summary["Fair_Target"]) * 100
    
    
    def grade(p):
        if p >= 70:
            return "✅ Met Expectation"
        else: 
            return "⚠️ Underperformed"
        

    summary["Status"] = summary["Performance_%"].apply(grade)

    # --- Dashboard Summary ---
    st.title("📊 Annual Performance Dashboard")

    passed = summary[summary["Status"] == "✅ Met Expectation"]
    underperformed = summary[summary["Status"] == "⚠️ Underperformed"]

    col1, col2 = st.columns(2)
    col1.metric("✅ Met Expectation", len(passed))
    col2.metric("⚠️ Underperformed", len(underperformed))
    
    
    st.markdown("---")

    # --- Filter by Category ---
    category = st.radio("Filter Category", ["✅ Met Expectation", "⚠️ Underperformed"])
    people_in_category = summary[summary["Status"] == category]["Person"].tolist()

    if not people_in_category:
        st.warning(f"No users in category: {category}")
        return

    # --- Full Summary Table List for all users  ---
    with st.expander("📋 View Full Annual Summary Table"):
        st.dataframe(summary[["Person", "Fair_Target", "Actual", "Performance_%", "Status"]])
    
    st.markdown("---")
    
    selected_person = st.selectbox("Select Person", sorted(people_in_category))

    # --- Filtered Person Data ---
    filtered = all_data[all_data["Person"] == selected_person].copy()
    filtered = filtered.sort_values("Month")
    filtered.set_index("Month", inplace=True)
    filtered["Month_Label"] = filtered.index.strftime("%b-%y")

    st.header(f"📌 Performance Dashboard for **{selected_person}**")
    
    

    
    
    
    quarter_summary = filtered.groupby("Fin_Quarter_Label").agg({
    "Actual": "sum",
    "Fair_Target": "sum"
    }).reset_index()

    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, divider,col2 = st.columns([1, 0.05, 1])
    
    
    #Quarterly Bar Chart
    with col1:
        st.subheader("📊 Quarterly Bar Chart")
        fig_bar = px.bar(
            quarter_summary,
            x="Fin_Quarter_Label",
            y=["Fair_Target", "Actual"],
            barmode="group",
            title="Quarterly Target vs Actual",
            color_discrete_map={"Fair_Target": "#007bff", "Actual": "#ff6384"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    #Divider for the columns    
    with divider:
        st.markdown("<div style='height:100%; width:5px; background-color:#ccc; margin: 0 auto;'></div>", unsafe_allow_html=True)

    #Quarterly Pie chart 
    with col2:
        st.subheader("🥧 Quarterly Pie Chart")
        fig_pie = px.pie(
            quarter_summary,
            names="Fin_Quarter_Label",
            values="Actual",
            title="Quarter-wise Contribution to Actual"
        )
        st.plotly_chart(fig_pie, use_container_width=True)





    # --- Target vs Actual ---
    st.subheader("🎯 Target vs Actual")
    melted = pd.melt(
        filtered,
        id_vars="Month_Label",
        value_vars=["Fair_Target", "Actual"],
        var_name="Metric",
        value_name="Value"
    )

    color_map = {
        "Fair_Target": "rgba(0, 123, 255, 0.9)",  # Blue
        "Actual": "rgba(255, 99, 132, 0.9)"  # Red
    }

    fig = px.bar(
        melted,
        x="Month_Label",
        y="Value",
        color="Metric",
        color_discrete_map=color_map,
        barmode="overlay",
        title="Monthly Target vs Actual"
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Cases", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


    # --- Performance Line Chart ---
    st.subheader("📈 Monthly Performance (%)")
    filtered["Results"] = filtered["Results"] * 100  # Scale to percent

    fig2 = px.line(
        filtered,
        x="Month_Label",
        y="Performance_%",
        title="Performance (%) Over Time",
        markers=True,
        labels={"Results": "Performance (%)", "Month_Label": "Month"}
    )
    fig2.update_traces(line=dict(color="green", width=2), marker=dict(size=6))
    fig2.update_layout(xaxis_tickangle=-45, hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

    

generateDashboard()
