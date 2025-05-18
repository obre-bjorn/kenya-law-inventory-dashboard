import streamlit as st
import pandas as pd
import plotly.express as px

from sheetgetter import getDataFromExcelSheets

def generateDashboard():
    all_data = getDataFromExcelSheets('inventory-report.xlsx')  
    
    #Sidebar filter
    person = st.sidebar.selectbox("Select Person", all_data["Person"].unique())
    
    filtered = all_data[all_data["Person"] == person]
    
    filtered = filtered.sort_values("Month")
    filtered.set_index("Month", inplace=True)

    # Optional: create Month_Label for tooltips if needed
    filtered["Month_Label"] = filtered.index.strftime("%b-%y")
    
    
    st.title(f"Perfomance Dashboard for {person}")
    
    st.subheader("Target vs Actual")
    
    
    melted = pd.melt(
        filtered,
        id_vars="Month_Label",
        value_vars=["Target", "Actual"],
        var_name="Metric",
        value_name="Value"
    )
    
    # Change bar colors
    color_map = {
    "Target": "rgba(0, 123, 255, 0.8)",   # Blue with transparency
    "Actual": "rgba(255, 99, 132, 0.8)"   # Red with transparency
    }

    # Plot
    fig = px.bar(
        melted,
        x="Month_Label",
        y="Value",
        color="Metric",
        color_discrete_map= color_map,
        barmode="overlay",  # 'group' shows side-by-side, 'overlay' allows full overlap
        title="Target vs Actual"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cases",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
    

    
    st.markdown("---")
    st.markdown("### 📈Performance (%) Chart")

    
    filtered["Results"] = filtered["Results"] * 100
# Plotly interactive line chart (from previous message)
    fig = px.line(
        filtered,
        x="Month_Label",
        y="Results",
        title="Performance (%) Over Time",
        markers=True,
        labels={"Results": "Performance (%)", "Month_Label": "Month"}
    )

    fig.update_traces(line=dict(color="green", width=2), marker=dict(size=6))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Performance (%)",
        xaxis_tickangle=-45,
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
    

generateDashboard()