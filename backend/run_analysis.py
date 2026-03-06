from image_analysis import ImageAnalyzer
from molecular_inference import MolecularInference
from llm_engine import RecipeGenerator

API_KEY = ""
if __name__ == "__main__":
    image_path = "backend/images/image1.png"

    # Step 1: Image analysis
    analyzer = ImageAnalyzer(image_path)
    features = analyzer.analyze()

    # Step 2: Molecular inference
    inference = MolecularInference(features)
    ingredient_scores = inference.infer()

    # Step 3: LLM reconstruction
    generator = RecipeGenerator(API_KEY)
    recipe = generator.generate_recipe(features, ingredient_scores)

    print("\nFINAL RECONSTRUCTED RECIPE -------")
    print(recipe)