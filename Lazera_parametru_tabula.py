import streamlit as st
import pandas as pd
import itertools

st.set_page_config(page_title="Laser Parameter Table Generator", layout="wide")
st.title("Fiber 20W Laser Parameter Table Generator")

# --- Sidebar: faila augšupielāde ---
st.sidebar.header("Augšupielādējiet CSV vai Excel failu")
uploaded_file = st.sidebar.file_uploader("Izvēlieties CSV vai Excel failu", type=["csv", "xlsx"])

# --- Nemainīgie parametri ---
LASER_POWER = 70
LASER_TYPE = "Fiber 20W"

if uploaded_file:
    try:
        # Nolasām failu
        if uploaded_file.name.endswith(".csv"):
            df_input = pd.read_csv(uploaded_file)
        else:
            df_input = pd.read_excel(uploaded_file)

        st.sidebar.success(f"Fails '{uploaded_file.name}' veiksmīgi nolasīts!")
        st.subheader("Ievades dati")
        st.dataframe(df_input)

        # Pārbauda, vai nepieciešamie kolonnu nosaukumi eksistē
        required_cols = ["start_angles", "angle_steps", "repeats", "speeds"]
        if not all(col in df_input.columns for col in required_cols):
            st.error(f"Failā jābūt šādām kolonnām: {required_cols}")
        else:
            # Pārvērš katru kolonnu par sarakstu
            start_angles = df_input["start_angles"].dropna().astype(int).tolist()
            angle_steps = df_input["angle_steps"].dropna().astype(int).tolist()
            repeats = df_input["repeats"].dropna().astype(int).tolist()
            speeds = df_input["speeds"].dropna().astype(int).tolist()

            # --- Izveido kombinācijas ---
            combinations = list(itertools.product(start_angles, angle_steps, repeats, speeds))

            # --- Sagatavo datus DataFrame ---
            data = []
            for comb in combinations:
                start_angle, angle_step, repeat, speed = comb
                row = {
                    "Jauda (%)": LASER_POWER,
                    "Lāzera tips": LASER_TYPE,
                    "Start angle (°)": start_angle,
                    "Angle step (°)": angle_step,
                    "Atkārtojumi": repeat,
                    "Ātrums (mm/s)": speed
                }
                data.append(row)

            df_output = pd.DataFrame(data)

            st.subheader("Ģenerētā tabula")
            st.dataframe(df_output)

            # --- Lejuplādējamais Excel fails ---
            output_file = "laser_fiber_20W_autotable.xlsx"
            df_output.to_excel(output_file, index=False)
            st.download_button(
                label="Lejuplādēt Excel",
                data=open(output_file, "rb").read(),
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Kļūda faila nolasīšanā: {e}")
else:
    st.info("Lūdzu augšupielādējiet CSV vai Excel failu, lai ģenerētu tabulu.")

print(df.head(10))
