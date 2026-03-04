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

            files = {"file": uploaded_file.getvalue()}

            response = requests.post(
                API_URL,
                files={"file": uploaded_file}
            )

            if response.status_code == 200:

                result = response.json()

                features = result["visual_features"]
                ingredients = result["ingredient_probabilities"]
                recipe = result["reconstructed_recipe"]

                st.success("Analysis Complete!")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Visual Features")
                    st.json(features)

                with col2:
                    st.subheader("Ingredient Probabilities")

                    df = pd.DataFrame(
                        list(ingredients.items()),
                        columns=["Ingredient", "Score"]
                    )

                    st.bar_chart(df.set_index("Ingredient"))

                st.subheader("Generated Recipe")

                st.write("### Dish Name")
                st.write(recipe.get("dish_name"))

                st.write("### Category")
                st.write(recipe.get("dish_category"))

                st.write("### Ingredients")

                for ing in recipe.get("ingredients", []):
                    st.write(f"- {ing['name']} : {ing['quantity']}")

                st.write("### Cooking Steps")

                for step in recipe.get("cooking_steps", []):
                    st.write(f"{step}")

                st.write("### Molecular Reasoning")
                st.write(recipe.get("molecular_reasoning"))

                st.write("### Confidence Score")
                st.write(recipe.get("confidence_score"))

            else:
                st.error("API Error")