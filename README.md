# 🎲 Lottery ML Analyzer

I have created a Python and Streamlit application that analyses past historical lottery lotto draw data and generates ranked number combinations based on frequency analysis and recent draw activity.

This is my first ML project which is to demonstrates basic data analysis, feature engineering, and an interactive UI for exploring patterns in lottery data.

# 🚀 Features

- Load historical lottery draw data from CSV
- Clean and structure data using **pandas**
- Analyze number frequency across all draws
- Identify **hot numbers** from recent draws
- Identify **cold numbers** not seen recently
- Apply a **weighted ranking model**
- Generate **1 or 5 suggested number combinations**
- Visualize number distribution using **matplotlib**
- Interactive controls using **Streamlit**

---

# 🧠 How the Model Works

Each number receives a score using a simple weighted ranking model:


Where:

- **historical_frequency** = number appearances across all draws  
- **recent_frequency** = appearances in the most recent draws  
- **recent_weight** = user-adjustable weight for recent activity  

This approach prioritizes numbers that appear frequently historically and recently.

---

# ⚠️ Important Note

PLEASE NOTE: Lottery draws are designed to be random.

This is my first ML project, which should be viewed as a **data analysis and ranking experiment**, not a guaranteed prediction tool.

---

# 🖥️ Application Interface

I used the Streamlit app which allows users to adjust parameters such as:

- Number of recent draws to analyze
- Weight applied to recent numbers
- Size of the candidate pool used for generating combinations

The application then generates ranked number combinations based on those parameters.

---

# ▶️ Running the Application

1. Install dependencies

pip install -r requirements.txt

2. Run the Streamlit app

streamlit run app.py

---


# 📂 Project Structure

lottery-ml-analyzer
│
├── data
│ └── lottery_data.csv
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
