import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="Recipe Archaeologist", layout="wide")

st.title("🏺 Recipe Archaeologist")
st.write("Generate a recipe from a food stain image using AI")

uploaded_file = st.file_uploader(
    "Upload a food stain image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Stain"):

        with st.spinner("Analyzing stain..."):

            response = requests.post(
                API_URL,
                files={"file": uploaded_file}
            )

            if response.status_code == 200:

                result = response.json()

                features = result["visual_features"]
                ingredients = result["ingredient_probabilities"]
                recipe_data = result["reconstructed_recipe"]

                st.success("Analysis Complete!")

                col1, col2 = st.columns(2)

                # -----------------------------
                # Visual Features
                # -----------------------------
                with col1:
                    st.subheader("🔬 Visual Features")
                    st.json(features)

                # -----------------------------
                # Ingredient Probabilities
                # -----------------------------
                with col2:
                    st.subheader("🧪 Ingredient Probabilities")

                    df = pd.DataFrame(
                        list(ingredients.items()),
                        columns=["Ingredient", "Score"]
                    )

                    st.bar_chart(df.set_index("Ingredient"))

                st.divider()

                st.subheader("🍲 Possible Recipe Reconstructions")

                hypotheses = recipe_data.get("hypotheses", [])

                if len(hypotheses) == 0:
                    st.warning("No recipe hypotheses returned")

                for i, h in enumerate(hypotheses):

                    st.divider()

                    st.write(f"## Hypothesis {i+1}: {h['dish_name']}")

                    st.write("**Category:**", h["dish_category"])
                    st.write("**Confidence:**", h["confidence_score"], "%")

                    st.write("### Ingredients")
                    for ing in h["ingredients"]:
                        st.write(f"- {ing['name']} : {ing['quantity']}")

                    st.write("### Cooking Steps")
                    for step in h["cooking_steps"]:
                        st.write(f"- {step}")

                    st.write("### Molecular Reasoning")
                    st.write(h["molecular_reasoning"])

                # -----------------------------
                # Explainability Panel
                # -----------------------------
                with st.expander("🔍 AI Reasoning Details"):
                    st.write("Visual Features")
                    st.json(features)

                    st.write("Ingredient Probabilities")
                    st.json(ingredients)

            else:
                st.error("API Error")