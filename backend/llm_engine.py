import json
from google import genai
from google.genai import types

class RecipeGenerator:
    def __init__(self, api_key):
        # The new SDK uses a centralized Client
        self.client = genai.Client(api_key=api_key)
        # Using Gemini 2.0 Flash (latest recommended for speed/JSON)
        self.model_id = "gemini-2.5-flash-lite"

    def build_prompt(self, features, ingredient_scores):
        # Prompt logic remains the same
        return f"""
You are a scientific culinary reconstruction AI.
You are reconstructing dishes based on chemical and visual residue evidence.

--- VISUAL FEATURES ---
Mean RGB: {features.get('mean_rgb')}
Color Variance: {features.get('color_variance')}
Dominant Hue (HSV scale): {features.get('dominant_hue')}
Mean Saturation: {features.get('mean_saturation')}
Oil Presence: {features.get('oil_presence')}
Brightness Std: {features.get('brightness_std')}
Edge Density: {features.get('edge_density')}
Texture Classification: {features.get('texture')}
Stain Area Ratio: {features.get('stain_area_ratio')}
Spread Metric: {features.get('spread_metric')}

--- INFERRED INGREDIENT SCORES ---
{json.dumps(ingredient_scores, indent=2)}

--- TASKS ---
1. Interpret what the hue, saturation, and brightness imply chemically.
2. Interpret what oil presence and spread imply about fat content.
3. Interpret what edge density and texture imply about solid particles.
4. Propose the TOP 3 most plausible dish categories.
5. Generate a realistic modern recipe for each dish.
6. Explain the molecular reasoning clearly.
7. Assign a confidence score (0-100) for each hypothesis.

Return ONLY valid JSON using this structure:

{
  "hypotheses": [
    {
      "dish_name": "string",
      "dish_category": "string",
      "ingredients": [
        {"name": "string", "quantity": "string"}
      ],
      "cooking_steps": ["string"],
      "molecular_reasoning": "string",
      "confidence_score": number
    }
  ]
}
"""

    def generate_recipe(self, features, ingredient_scores):
        prompt = self.build_prompt(features, ingredient_scores)

        try:
            # New syntax: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    # Force valid JSON output
                    response_mime_type="application/json",
                    temperature=0.6,
                    # System instruction is now passed in the config
                    system_instruction="You are a molecular gastronomy reconstruction model."
                )
            )
            output_text = response.text
        except Exception as e:
            print(f"\n[Error] Gemini API Call Failed: {e}")
            output_text = json.dumps({
                "error": "API Error", 
                "dish_name": "Unknown", 
                "molecular_reasoning": str(e)
            })

        try:
            return json.loads(output_text)
        except Exception:
            return {"error": "Invalid JSON", "raw_output": output_text}