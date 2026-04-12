import streamlit as st
import pandas as pd
import time

from src.oblivious_fetch import oblivious_fetch
from src.k_anonymity import evaluate_k_anonymity
from src.diff_privacy import calculate_sensitivity, apply_laplace_noise


# ==========================================
st.set_page_config(page_title="Adaptive Privacy Shield", page_icon="🛡️", layout="wide")

@st.cache_data
def load_data():
    #Load mock database
    try:
        return pd.read_csv("mock_hr_database.csv")
    except FileNotFoundError:
        st.error("Database not found! Please run `python data_generator.py` first.")
        st.stop()

df = load_data()

#side bar control
st.sidebar.title("Threat Assessment Controls")
st.sidebar.markdown("Configure the strictness of the Middle-Layer Proxy.")

# Slider for k-anonymity Threat Detection
k_threshold = st.sidebar.slider(
    "K-Anonymity Threshold (k)", 
    min_value=2, max_value=500, value=50, step=10,
    help="Minimum number of records required. If subset size < k, query is denied."
)

# Slider for differential Privacy - Noise Level
epsilon = st.sidebar.slider(
    "Privacy Budget (ε)", 
    min_value=0.1, max_value=5.0, value=1.0, step=0.1,
    help="Lower ε = More noise (Higher Privacy). Higher ε = Less noise (Higher Accuracy)."
)

st.sidebar.divider()
st.sidebar.info(" **Demo Tip:** Try querying 'Engineering' (Safe) vs 'Executive' (Threat).")

# ==========================================
# DASHBOARD HEADER
st.title("Adaptive Privacy Shield")
st.markdown("### A Middle-Layer Defense Mechanism for Big Data Queries")
st.write("This dashboard demonstrates a multi-tier defense architecture protecting a backend HR database from re-identification and access pattern attacks.")

# Create a layout with two columns
col1, col2 = st.columns([1, 2])


# interface build with cols
with col1:
    
    st.subheader("1. Client Interface")
    st.write("Submit an aggregate request to the database.")
    
    # Dropdown to select the target demographic
    target_dept = st.selectbox("Target Demographic (Department):", df['Department'].unique())
    
    # hardcoded 'AVERAGE Salary' for this demo
    # but the backend supports COUNT as well.
    st.text_input("Query Type:", value="AVERAGE(Salary)", disabled=True)
    
    execute_btn = st.button("Execute Secure Query", type="primary", use_container_width=True)
    
    
with col2:
    
    st.subheader("2. Middle-Layer Proxy Pipeline")
    
    if execute_btn:
        # OBLIVIOUS FETCH
        st.markdown("Stage 1: Oblivious Data Retrieval")
        
        #Get the Routed (APS) 
        route = time.time()
        with st.spinner("Fetching blocks from Storage Tier..."):
            
            time.sleep(1) 
            secure_subset, dummies_used = oblivious_fetch(df, target_dept, num_dummies=2)
            
        st.info(f"**Access Pattern Masked:** To hide the true target, the proxy simultaneously fetched dummy blocks for `{dummies_used[0]}` and `{dummies_used[1]}`.")
        
        #K-ANONYMITY CHECK
        st.markdown("Stage 2: Threat Assessment")
        is_safe, subset_size = evaluate_k_anonymity(secure_subset, k_threshold)
        
        #Get the standard (CPU)
        if not is_safe:
            # THREAT DETECTED: Halt execution
            st.error(f" **PRIVACY THREAT DETECTED:** The query isolated {subset_size} records, falling below the strict K-Anonymity threshold of {k_threshold}.")
            st.error(" **ACTION:** Access Denied. Query terminated to prevent re-identification attack.")
            failed_time = time.time() - route
            st.error(f" **FAILED QUERY TIME:** {failed_time} sec")
            st.stop()
        else:
            # SAFE
            st.success(f" **Safe Query:** Isolated {subset_size} records. Passed K-Anonymity check (k={k_threshold}).")

        #DIFFERENTIAL PRIVACY INJECTION
        st.markdown("Stage 3: Differential Privacy Injection")
        

        standard = time.time()
        # Calculate true value (Vulnerable)
        true_average = secure_subset['Salary'].mean()
        
        # Calculate Math
        with st.spinner("Calculating Sensitivity and Laplace Noise..."):
            time.sleep(1)
            # Assuming max salary is around 200k for sensitivity calculation
            sens = calculate_sensitivity('AVERAGE', subset_size, max_possible_value=200000)
            safe_noisy_average = apply_laplace_noise(true_average, sens, epsilon)
        
        st.success(f"Noise injected successfully. (Sensitivity: {sens:,.2f} | ε: {epsilon})")

        #FINAL OUTPUT TO USER
        st.markdown("---")
        st.markdown("Final Released Data (Client View)")

        #CPU vs Routed time
        standard_time = time.time() - standard
        routed_time = time.time() - route

        # Display
        colA, colB = st.columns(2)

        colA.metric(
            label="Standard Query Time (CPU)",
            value=f"{standard_time:.6f} sec"
        )

        colB.metric(
            label="APS Routed Time",
            value=f"{routed_time:.6f} sec"
        )

        st.write("Overhead (APS - Standard):", f"{routed_time - standard_time:.6f} sec")
        
        # Display the metrics side-by-side
        metric_col1, metric_col2 = st.columns(2)
        
        metric_col1.metric(
            label="Protected Released Average", 
            value=f"${safe_noisy_average:,.2f}"
        )
        
        
        # In the real world, the user never sees this.
        metric_col2.metric(
            label="[Admin Only] True Average", 
            value=f"${true_average:,.2f}", 
            delta=f"Noise Added: ${(safe_noisy_average - true_average):,.2f}", 
            delta_color="off"
        )
        
        #A visual chart comparing the true vs noisy value
        chart_data = pd.DataFrame({
            "Metric": ["True Average", "Noisy Average"],
            "Value": [true_average, safe_noisy_average]
        })
        st.bar_chart(chart_data.set_index("Metric"), color="#8e24aa")


# DATABASE PREVIEW 
with st.expander("View Raw Backend Database (Storage Tier Simulation)"):
    st.dataframe(df.head(100), use_container_width=True)