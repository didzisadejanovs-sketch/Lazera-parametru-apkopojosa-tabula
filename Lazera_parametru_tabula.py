import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="Laser Parameter Table Generator", layout="wide")
st.title("Fiber 20W Laser Parameter Table Generator")

# --- Sidebar: file upload ---
st.sidebar.header("Upload CSV or Excel")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

# --- Fixed laser parameters ---
LASER_POWER = 70
LASER_TYPE = "Fiber 20W"

# Initialize df_output to None
df_output = None

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df_input = pd.read_csv(uploaded_file)
        else:
            df_input = pd.read_excel(uploaded_file)

        st.sidebar.success(f"File '{uploaded_file.name}' successfully loaded!")

        st.subheader("Input data")
        st.dataframe(df_input)

        # Required columns
        required_cols = ["start_angles", "angle_steps", "repeats", "speeds"]
        if not all(col in df_input.columns for col in required_cols):
            st.error(f"File must contain columns: {required_cols}")
        else:
            # Convert each column to a list of ints
            start_angles = df_input["start_angles"].dropna().astype(int).tolist()
            angle_steps = df_input["angle_steps"].dropna().astype(int).tolist()
            repeats = df_input["repeats"].dropna().astype(int).tolist()
            speeds = df_input["speeds"].dropna().astype(int).tolist()

            # Generate combinations
            combinations = list(itertools.product(start_angles, angle_steps, repeats, speeds))

            # Prepare DataFrame
            data = []
            for comb in combinations:
                start_angle, angle_step, repeat, speed = comb
                data.append({
                    "Jauda (%)": LASER_POWER,
                    "Lāzera tips": LASER_TYPE,
                    "Start angle (°)": start_angle,
                    "Angle step (°)": angle_step,
                    "Atkārtojumi": repeat,
                    "Ātrums (mm/s)": speed
                })

            df_output = pd.DataFrame(data)

            # Display preview
            st.subheader("Generated Laser Table Preview")
            st.dataframe(df_output.head(10))

            # Download button
            output_file = "laser_fiber_20W_autotable.xlsx"
            df_output.to_excel(output_file, index=False)
            st.download_button(
                label="Download Excel",
                data=open(output_file, "rb").read(),
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV or Excel file to generate the table.")
