import json
from openai import OpenAI


class RecipeGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def build_prompt(self, features, ingredient_scores):

        prompt = f"""
You are a scientific culinary reconstruction AI.

You are reconstructing a dish based on chemical and visual residue evidence.

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
4. Propose the most plausible dish category.
5. Generate a realistic modern recipe.
6. Explain the molecular reasoning clearly.
7. Provide a confidence score (0-100).

Return ONLY valid JSON:

{{
  "dish_name": "...",
  "dish_category": "...",
  "ingredients": [
    {{"name": "...", "quantity": "..."}}
  ],
  "cooking_steps": ["..."],
  "molecular_reasoning": "...",
  "confidence_score": 0
}}
"""
        return prompt

    def generate_recipe(self, features, ingredient_scores):

        prompt = self.build_prompt(features, ingredient_scores)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a molecular gastronomy reconstruction model."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        output_text = response.choices[0].message.content

        try:
            return json.loads(output_text)
        except:
            return {"error": "Invalid JSON", "raw_output": output_text}