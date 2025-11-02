import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------
# MAIN APP WINDOW
# ----------------------------------------
root = tk.Tk()
root.title("🏥 Health Data Analysis Dashboard")
root.geometry("1300x750")
root.configure(bg="#eef3f7")

df = None  # global dataframe

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------
def load_csv():
    global df

    file_path = filedialog.askopenfilename(
        title="Select Health Data CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        try:
            df = pd.read_csv(file_path)

            # ✅ Validation for required columns
            required_columns = ["Patient_ID", "Age", "Gender",
                                "Blood_Pressure", "Cholesterol", "Heart_Rate", "BMI"]
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror(
                    "Invalid CSV Format",
                    "CSV must contain these columns:\nPatient_ID, Age, Gender, Blood_Pressure, Cholesterol, Heart_Rate, BMI"
                )
                df = None
                return

            df.dropna(inplace=True)
            df["BMI"] = df["BMI"].astype(float)

            messagebox.showinfo("Success ✅", "CSV loaded successfully!")

            patient_ids = df["Patient_ID"].unique()
            patient_menu["values"] = patient_ids
            patient_menu.current(0)
            show_patient_data()  # display 1st patient automatically

        except Exception as e:
            messagebox.showerror("Error loading CSV", str(e))


def show_patient_data(*args):
    """Show single patient details similar to Streamlit metric cards."""
    if df is None:
        return

    selected = patient_var.get()
    patient_data = df[df["Patient_ID"] == selected].iloc[0]

    age_label.config(text=f"Age: {patient_data['Age']} years")
    gender_label.config(text=f"Gender: {patient_data['Gender']}")
    bmi_label.config(text=f"BMI: {patient_data['BMI']}")

    bp_label.config(text=f"Blood Pressure: {patient_data['Blood_Pressure']} mmHg")
    chol_label.config(text=f"Cholesterol: {patient_data['Cholesterol']} mg/dL")
    hr_label.config(text=f"Heart Rate: {patient_data['Heart_Rate']} bpm")


def plot_charts():
    """Generate three matplotlib charts just like Streamlit."""
    if df is None:
        messagebox.showwarning("Upload CSV", "Please upload a CSV file first.")
        return

    fig, axs = plt.subplots(1, 3, figsize=(13, 4))

    # Histogram — Age Distribution
    axs[0].hist(df["Age"], bins=10, color="skyblue", edgecolor="black")
    axs[0].set_title("Age Distribution")
    axs[0].set_xlabel("Age")
    axs[0].set_ylabel("Count")

    # Bar Chart — Gender Distribution
    df["Gender"].value_counts().plot(kind="bar", color=["lightcoral", "lightgreen"], ax=axs[1])
    axs[1].set_title("Gender Distribution")
    axs[1].set_xlabel("Gender")
    axs[1].set_ylabel("Count")

    # Scatter — Age vs BP (Cholesterol-Colored)
    scatter = axs[2].scatter(df["Age"], df["Blood_Pressure"], s=90,
                             c=df["Cholesterol"], cmap="viridis")
    axs[2].set_title("Age vs Blood Pressure (Color = Cholesterol)")
    axs[2].set_xlabel("Age")
    axs[2].set_ylabel("Blood Pressure")
    plt.colorbar(scatter, ax=axs[2], label="Cholesterol Level")

    # Clear previous graph if exists
    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def show_insights():
    """Show NumPy insights: Avg BP, Cholesterol, BMI"""
    if df is None:
        return

    avg_bp = np.mean(df["Blood_Pressure"])
    avg_chol = np.mean(df["Cholesterol"])
    avg_bmi = np.mean(df["BMI"])

    insights_label.config(
        text=f"📈 Average Stats:\n\n"
             f"• Avg Blood Pressure: {avg_bp:.2f} mmHg\n"
             f"• Avg Cholesterol: {avg_chol:.2f} mg/dL\n"
             f"• Avg BMI: {avg_bmi:.2f}"
    )


# ----------------------------------------
# UI LAYOUT (STRUCTURE SIMILAR TO STREAMLIT)
# ----------------------------------------

# Header
header = tk.Label(root, text="🏥 Health Data Analysis Dashboard",
                  font=("Arial", 22, "bold"), bg="#eef3f7")
header.pack(pady=10)

upload_btn = tk.Button(root, text="📂 Upload CSV", command=load_csv,
                       bg="#4CAF50", fg="white", font=("Arial", 13), padx=12)
upload_btn.pack(pady=5)

# Patient selection dropdown
patient_var = tk.IntVar()
ttk.Label(root, text="Select Patient ID:", font=("Arial", 13),
          background="#eef3f7").pack()

patient_menu = ttk.Combobox(root, textvariable=patient_var, state="readonly")
patient_menu.pack()

patient_menu.bind("<<ComboboxSelected>>", show_patient_data)

# Patient Info
info_frame = tk.Frame(root, bg="white", pady=15)
info_frame.pack(fill="x", padx=10, pady=10)

age_label = tk.Label(info_frame, text="Age: --", font=("Arial", 12), bg="white")
gender_label = tk.Label(info_frame, text="Gender: --", font=("Arial", 12), bg="white")
bmi_label = tk.Label(info_frame, text="BMI: --", font=("Arial", 12), bg="white")

bp_label = tk.Label(info_frame, text="Blood Pressure: --", font=("Arial", 12), bg="white")
chol_label = tk.Label(info_frame, text="Cholesterol: --", font=("Arial", 12), bg="white")
hr_label = tk.Label(info_frame, text="Heart Rate: --", font=("Arial", 12), bg="white")

widgets = [age_label, gender_label, bmi_label, bp_label, chol_label, hr_label]
for w in widgets:
    w.pack(side="left", padx=18)

# Chart Frame
chart_frame = tk.Frame(root, bg="#eef3f7")
chart_frame.pack(fill="both", expand=True)

tk.Button(root, text="📊 Show Charts", command=plot_charts,
          bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=5)

insights_label = tk.Label(root, text="", bg="#eef3f7", font=("Arial", 13))
insights_label.pack(pady=10)

tk.Button(root, text="📈 Show Insights", command=show_insights,
          bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=5)

root.mainloop()




























