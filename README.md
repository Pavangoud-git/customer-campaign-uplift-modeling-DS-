# Customer Campaign Uplift Modeling Using Machine Learning

## 📌 Project Overview

Customer Campaign Uplift Modeling is a machine learning project that estimates which customers are more likely to purchase because of a marketing campaign.

Unlike traditional prediction models, uplift modeling focuses on the incremental impact of a campaign to help businesses make smarter customer-targeting decisions.

## 🎯 Project Objectives

- Estimate the impact of email marketing on customer purchases.
- Implement S-Learner, T-Learner, and X-Learner approaches.
- Identify customers with higher estimated campaign uplift.
- Build an interactive application using Streamlit.
- Support data-driven marketing decisions.

## 📊 Dataset

**Hillstrom Email Marketing Dataset**

The original dataset contains approximately 64,000 customers divided into three randomized groups:

- Men's Email
- Women's Email
- No Email

The project focuses on comparing the Women's Email and No Email groups.

Dataset source: https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Random Forest
- Streamlit
- Joblib
- Google Colab

## ⚙️ Project Workflow

1. Dataset collection and exploration
2. Data cleaning and preprocessing
3. Exploratory Data Analysis (EDA)
4. Treatment and control group creation
5. Training, validation, and test splitting
6. S-Learner implementation
7. T-Learner implementation
8. X-Learner implementation
9. Customer uplift prediction
10. Customer targeting analysis
11. Model evaluation
12. Interactive Streamlit application

## 🧠 Machine Learning Models

**S-Learner:** Uses a single model with customer features and a treatment indicator.

**T-Learner:** Uses separate models for treatment and control groups.

**X-Learner:** Estimates treatment effects using imputed outcomes and additional effect models.

## 📈 Application Features

- Interactive customer information form
- Estimated customer uplift score
- Campaign conversion probability comparison
- Customer targeting insights
- Streamlit-based user interface

## 💼 Business Benefits

- Helps identify customers who may benefit from marketing campaigns.
- Supports more targeted email marketing.
- Can help reduce unnecessary campaign spending.
- Encourages data-driven marketing decisions.

## 🚀 How to Run the Project

1. Clone or download this repository.
2. Install the required libraries using `requirements.txt`.
3. Ensure the trained model file is available in the application folder.
4. Run the application:

```bash
streamlit run app.py
```

## ⚠️ Limitations

- Individual customer treatment effects cannot be directly observed.
- Uplift estimates are uncertain and may vary across samples.
- A positive uplift score does not guarantee a purchase.
- Results from historical data may not generalize to future campaigns.
- Real campaign profitability requires campaign costs and profit margins.

## 👨‍💻 Author

**Pavan Bheemagani**

Aspiring Data Scientist | Machine Learning Enthusiast

GitHub: https://github.com/Pavangoud-git

## 📌 Conclusion

This project demonstrates the practical application of causal machine learning and uplift modeling to customer targeting. It combines data analysis, machine learning, and an interactive application to explore how marketing campaigns can create incremental customer value.
