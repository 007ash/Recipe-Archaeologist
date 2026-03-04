import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from image_analysis import ImageAnalyzer
from molecular_inference import MolecularInference
from llm_engine import RecipeGenerator


API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Recipe Archaeologist API")


# -----------------------------
# CORS (allow frontend access)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Recipe Archaeologist API is running"}


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    if API_KEY is None:
        raise HTTPException(
            status_code=500,
            detail="API_KEY environment variable not set"
        )

    try:
        # -----------------------------
        # Save uploaded image
        # -----------------------------
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # Step 1: Image Analysis
        # -----------------------------
        analyzer = ImageAnalyzer(file_path)
        features = analyzer.analyze()

        # -----------------------------
        # Step 2: Molecular Inference
        # -----------------------------
        inference = MolecularInference(features)
        ingredient_scores = inference.infer()

        # -----------------------------
        # Step 3: LLM Recipe Generation
        # -----------------------------
        generator = RecipeGenerator(API_KEY)
        recipe_output = generator.generate_recipe(features, ingredient_scores)

        # -----------------------------
        # Return Full Pipeline Output
        # -----------------------------
        return {
            "visual_features": features,
            "ingredient_probabilities": ingredient_scores,
            "reconstructed_recipe": recipe_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Optional cleanup
        if os.path.exists(file_path):
            os.remove(file_path)