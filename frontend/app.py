import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/analyze"

# --- Page Config ---
st.set_page_config(
    page_title="Recipe Archaeologist", 
    page_icon="🏺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.title("🏺 Recipe Archaeologist")
st.markdown("### *Uncover the culinary secrets hidden in food stains.*")
st.write("Upload an image of a food spill or stain, and our AI will analyze its molecular and visual properties to reverse-engineer the likely recipe.")
st.divider()

# --- File Uploader ---
col_upload, col_preview = st.columns([1, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload a food stain image",
        type=["jpg", "png", "jpeg"],
        help="Make sure the stain is well-lit and in focus!"
    )

if uploaded_file is not None:
    with col_preview:
        st.image(uploaded_file, caption="Target Stain for Analysis", use_column_width=True)

    if st.button("🔍 Analyze Stain", type="primary", use_container_width=True):
        
        with st.spinner("Analyzing spectral signatures and molecular properties..."):
            try:
                # --- API Call ---
                response = requests.post(
                    API_URL,
                    files={"file": uploaded_file.getvalue()}
                )

                if response.status_code == 200:
                    result = response.json()

                    features = result.get("visual_features", {})
                    ingredients = result.get("ingredient_probabilities", {})
                    recipe_data = result.get("reconstructed_recipe", {})
                    hypotheses = recipe_data.get("hypotheses", [])

                    st.success("Analysis Complete!")
                    st.divider()

                    # --- Section 1: Data & Analytics ---
                    st.header("🔬 Forensic Breakdown")
                    col_feat, col_ing = st.columns([1, 1])

                    with col_feat:
                        st.subheader("Visual & Molecular Features")
                        # Displaying key features as nice metrics
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Dominant Hue", f"{features.get('dominant_hue', 0)}°")
                        m2.metric("Texture", str(features.get('texture', 'N/A')).title())
                        m3.metric("Oil Presence", "Detected" if features.get('oil_presence') else "None")
                        
                        st.markdown("**Raw Data Payload:**")
                        st.json(features, expanded=False)

                    with col_ing:
                        st.subheader("Ingredient Probabilities")
                        if ingredients:
                            # Convert to DataFrame, sort for better visualization
                            df = pd.DataFrame(
                                list(ingredients.items()),
                                columns=["Ingredient", "Probability"]
                            ).sort_values(by="Probability", ascending=True)
                            
                            # Clean up ingredient names for display
                            df["Ingredient"] = df["Ingredient"].str.replace("_", " ").str.title()
                            
                            st.bar_chart(df.set_index("Ingredient"), horizontal=True)

                    st.divider()

                    # --- Section 2: Reconstructed Recipes ---
                    st.header("📜 Reconstructed Hypotheses")
                    st.write("Based on the forensic breakdown, here are the most likely dishes that caused this stain:")

                    if hypotheses:
                        # Create dynamic tabs based on the number of hypotheses
                        tab_names = [f"Option {i+1}: {h['dish_name']} ({h['confidence_score']}%)" for i, h in enumerate(hypotheses)]
                        tabs = st.tabs(tab_names)

                        for index, tab in enumerate(tabs):
                            with tab:
                                h = hypotheses[index]
                                
                                st.markdown(f"## {h.get('dish_name')}")
                                st.caption(f"**Category:** {h.get('dish_category')}")
                                
                                # Confidence Score Progress Bar
                                conf_score = h.get('confidence_score', 0)
                                st.progress(conf_score / 100.0, text=f"**Confidence Match:** {conf_score}%")
                                
                                st.markdown("---")
                                
                                col_recipe, col_reason = st.columns([1, 1])
                                
                                with col_recipe:
                                    st.subheader("🛒 Ingredients")
                                    for ing in h.get("ingredients", []):
                                        st.markdown(f"- **{ing['quantity']}** {ing['name']}")
                                        
                                    st.subheader("🍳 Cooking Steps")
                                    for i, step in enumerate(h.get("cooking_steps", [])):
                                        st.markdown(f"**{i+1}.** {step}")

                                with col_reason:
                                    st.subheader("🧠 AI Reasoning")
                                    st.info(h.get("molecular_reasoning", "No reasoning provided."))
                                    
                    else:
                        st.warning("No recipe hypotheses were returned from the API.")

                else:
                    st.error(f"API Error: Received status code {response.status_code}")
                    st.write(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Error: Could not connect to the backend. Is your API running on port 8000?")



