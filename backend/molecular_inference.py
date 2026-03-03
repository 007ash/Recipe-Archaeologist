class MolecularInference:
    def __init__(self, features):
        self.features = features
        self.scores = {}

    # Utility function
    def add_score(self, ingredient, value):
        if ingredient not in self.scores:
            self.scores[ingredient] = 0
        self.scores[ingredient] += value

    # ---------------------------
    # Rule-Based Scoring
    # ---------------------------
    def apply_color_rules(self):
        hue = self.features.get("dominant_hue", 0)
        mean_rgb = self.features.get("mean_rgb", [0, 0, 0])
        
        if hue < 15 or hue > 160:
            color = "dark-brown" if sum(mean_rgb) < 250 else "red-dominant"
        elif 15 <= hue <= 60:
            color = "dark-brown" if sum(mean_rgb) < 250 else "yellow-orange"
        else:
            color = "dark-brown" if sum(mean_rgb) < 250 else "yellow-orange"

        if color == "yellow-orange":
            self.add_score("turmeric", 0.6)
            self.add_score("red_chili_powder", 0.4)

        elif color == "red-dominant":
            self.add_score("red_chili_powder", 0.7)
            self.add_score("tomato_puree", 0.5)

        elif color == "dark-brown":
            self.add_score("caramelized_onion", 0.6)
            self.add_score("soy_sauce", 0.4)

    def apply_oil_rules(self):
        if self.features["oil_presence"]:
            self.add_score("refined_oil", 0.6)
            self.add_score("ghee", 0.5)

    def apply_texture_rules(self):
        texture = self.features["texture"]

        if texture == "grainy":
            self.add_score("ground_spices", 0.6)
            self.add_score("lentil_base", 0.5)

        elif texture == "semi-grainy":
            self.add_score("ground_spices", 0.4)

        elif texture == "smooth":
            self.add_score("cream", 0.5)
            self.add_score("yogurt", 0.5)

    # ---------------------------
    # Normalize Scores (0–1)
    # ---------------------------
    def normalize_scores(self):
        if not self.scores:
            return self.scores

        max_score = max(self.scores.values())

        for ingredient in self.scores:
            self.scores[ingredient] = round(
                self.scores[ingredient] / max_score, 2
            )

        return self.scores

    # ---------------------------
    # Full Inference Pipeline
    # ---------------------------
    def infer(self):
        self.apply_color_rules()
        self.apply_oil_rules()
        self.apply_texture_rules()

        return self.normalize_scores()