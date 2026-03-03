from image_analysis import ImageAnalyzer
from molecular_inference import MolecularInference

if __name__ == "__main__":
    image_path = "backend/images/image1.png"

    analyzer = ImageAnalyzer(image_path)
    features = analyzer.analyze()

    print("\n=== Extracted Features ===")
    for key, value in features.items():
        print(f"{key}: {value}")

    inference = MolecularInference(features)
    ingredient_scores = inference.infer()

    print("\n=== Ingredient Probabilities ===")
    for ingredient, score in ingredient_scores.items():
        print(f"{ingredient}: {score}")