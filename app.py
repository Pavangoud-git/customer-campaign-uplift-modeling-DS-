

import streamlit as st
import pandas as pd
import joblib
import sklearn
from pathlib import Path

st.set_page_config(
    page_title="Customer Campaign Uplift",
    page_icon="📈",
    layout="centered"
)

SUPPORTED_SKLEARN_VERSION = "1.6.1"

if sklearn.__version__ != SUPPORTED_SKLEARN_VERSION:
    st.error(
        f"This model requires scikit-learn {SUPPORTED_SKLEARN_VERSION}, "
        f"but the current environment has {sklearn.__version__}."
    )
    st.info(
        "Stop this Streamlit server, then from the project folder run:\n\n"
        "`.\.venv\Scripts\python.exe -m streamlit run app.py`\n\n"
        "Or double-click `run_app.bat`. If this app is deployed, rebuild "
        "the deployment after updating `requirements.txt`."
    )
    st.stop()

# Load the saved uplift model
MODEL_PATH = Path(__file__).parent / "uplift_model_bundle.joblib"


@st.cache_resource
def load_model_artifact():
    return joblib.load(MODEL_PATH)


artifact = load_model_artifact()

model_name = artifact["selected_model_name"]
model_bundle = artifact["selected_model"]
category_options = artifact["category_options"]


def predict_customer_outcome(name, bundle, X):

    if name == "S-Learner":

        X_treated = X.copy()
        X_control = X.copy()

        X_treated["treatment"] = 1
        X_control["treatment"] = 0

        p1 = bundle["model"].predict_proba(X_treated)[:, 1]
        p0 = bundle["model"].predict_proba(X_control)[:, 1]

        return float(p1[0] - p0[0]), float(p0[0]), float(p1[0])

    elif name == "T-Learner":

        p1 = bundle["model_treated"].predict_proba(X)[:, 1]
        p0 = bundle["model_control"].predict_proba(X)[:, 1]

        return float(p1[0] - p0[0]), float(p0[0]), float(p1[0])

    elif name == "X-Learner":

        tau1 = bundle["tau_treated"].predict(X)
        tau0 = bundle["tau_control"].predict(X)

        p = bundle["propensity"]

        if "model_control" not in bundle:
            raise ValueError(
                "X-Learner bundle must include 'model_control' to estimate "
                "the no-campaign purchase probability."
            )

        control_probability = float(
            bundle["model_control"].predict_proba(X)[0, 1]
        )
        estimated_uplift = float((p * tau0 + (1 - p) * tau1)[0])
        treated_probability = min(
            max(control_probability + estimated_uplift, 0.0),
            1.0
        )
        uplift = treated_probability - control_probability

        return uplift, control_probability, treated_probability

    raise ValueError("Unknown model")


st.title("Customer Campaign Uplift Modeling")

st.write(
    "Enter customer information available before a campaign. "
    "The model estimates the incremental purchase probability "
    "associated with the women's email campaign."
)

st.caption(f"Selected model: {model_name}")

with st.form("customer_form"):

    recency = st.slider(
        "Months since last purchase",
        min_value=1,
        max_value=12,
        value=3
    )

    history = st.number_input(
        "Past-year spending ($)",
        min_value=0.0,
        max_value=10000.0,
        value=200.0,
        step=10.0
    )

    history_segment = st.selectbox(
        "Past-year spending category",
        options=category_options["history_segment"]
    )

    mens = st.selectbox(
        "Previously purchased men's merchandise?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    womens = st.selectbox(
        "Previously purchased women's merchandise?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    zip_code = st.selectbox(
        "Location category",
        options=category_options["zip_code"],
        format_func=lambda x: (
            "Suburban" if x.lower() == "surburban" else x
        )
    )

    newbie = st.selectbox(
        "New customer?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    channel = st.selectbox(
        "Previous shopping channel",
        options=category_options["channel"]
    )

    submitted = st.form_submit_button("Estimate Uplift")

if submitted:

    customer = pd.DataFrame([{
        "recency": recency,
        "history": history,
        "mens": mens,
        "womens": womens,
        "newbie": newbie,
        "history_segment": history_segment,
        "zip_code": zip_code,
        "channel": channel
    }])

    score, control_probability, treated_probability = predict_customer_outcome(
        model_name,
        model_bundle,
        customer
    )

    st.metric(
        "Estimated uplift",
        f"{score * 100:.1f}%"
    )
    st.caption(
        "Calculated as (campaign conversion probability - no-campaign "
        "conversion probability) x 100. This is an absolute difference in "
        "percentage points, not relative lift."
    )

    st.subheader("Estimated campaign uplift")
    chart = pd.DataFrame(
        {
            "Predicted conversion probability (0-1)": [
                control_probability,
                treated_probability
            ]
        },
        index=["No campaign", "Women's email campaign"]
    )
    st.bar_chart(chart)
    st.caption(
        "Bar values are probabilities from 0 to 1. The estimated uplift "
        "in percentage points is (campaign probability - no-campaign "
        "probability) x 100. For the X-Learner, the campaign probability "
        "is the control probability plus the estimated treatment effect, "
        "constrained to the valid 0-1 probability range."
    )

    if score > 0:
        st.success(
            "The model estimates a positive uplift for this customer."
        )
    else:
        st.warning(
            "The model does not estimate a positive uplift "
            "for this customer."
        )

    st.caption(
        "This is a model estimate, not a guarantee of individual "
        "behavior. Validate any targeting strategy experimentally."
    )