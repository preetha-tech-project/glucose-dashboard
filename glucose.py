# 📦 Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 🌱 App title
st.title("🌿 Sweat Glucose Dashboard")
st.write("Upload your CSV file to see glucose trends, alerts, and stats.")

# 📂 Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # ✅ Read data
    df = pd.read_csv(uploaded_file)

    # Show data preview
    st.subheader("📋 Data Preview")
    st.write(df.head())

    # Detect people columns (assumes first column is time)
    people = df.columns[1:]
    time_points = df.iloc[:, 0]

    # 📊 Static matplotlib plot
    st.subheader("🪄 Static Plot (Matplotlib)")
    plt.figure(figsize=(10, 5))
    for person in people:
        plt.plot(time_points, df[person], label=person, linewidth=1)
    plt.xlabel("Time (hours)")
    plt.ylabel("Sweat Glucose Level (mg/dL)")
    plt.title("Simulated Sweat Glucose Levels Over Time")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # 🌈 Interactive plot (Plotly)
    st.subheader("🌈 Interactive Plot (Plotly)")
    fig = go.Figure()
    for person in people:
        fig.add_trace(go.Scatter(x=time_points, y=df[person], mode='lines', name=person))
    fig.update_layout(
        xaxis_title='Time (hours)',
        yaxis_title='Sweat Glucose Level (mg/dL)',
        template='plotly_dark',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    # 🚨 Alerts
    st.subheader("🚨 Alerts (High Glucose > 120 mg/dL)")
    for person in people:
        max_val = np.max(df[person])
        if max_val > 120:
            st.warning(f"⚠️ {person}: glucose exceeded 120 mg/dL (max: {max_val:.1f})")
        else:
            st.success(f"✅ {person}: glucose stayed normal (max: {max_val:.1f})")

    # 📊 Statistical summary
    st.subheader("📊 Statistical Summary")
    summary = {}
    for person in people:
        summary[person] = {
            'Mean': np.mean(df[person]),
            'Max': np.max(df[person]),
            'Min': np.min(df[person]),
            'Std Dev': np.std(df[person])
        }
    df_summary = pd.DataFrame(summary).T
    st.table(df_summary)

    # 💾 Download processed data
    st.subheader("⬇️ Download Processed Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='processed_glucose_data.csv',
        mime='text/csv',
    )
else:
    st.info("👆 Please upload a CSV file to see the dashboard.")

