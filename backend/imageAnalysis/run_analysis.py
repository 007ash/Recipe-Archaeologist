from image_analysis import ImageAnalyzer

if __name__ == "__main__":
    image_path = "backend/imageAnalysis/images/foodStain1.jpg"

    analyzer = ImageAnalyzer(image_path)
    features = analyzer.analyze()

    print("\n=== Extracted Features ===")
    for key, value in features.items():
        print(f"{key}: {value}")