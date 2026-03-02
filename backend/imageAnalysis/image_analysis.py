import cv2
import numpy as np


class ImageAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.image_rgb = None
        self.gray = None
        self.hsv = None

    # ---------------------------------
    # Load Image
    # ---------------------------------
    def load_image(self):
        self.image = cv2.imread(self.image_path)

        if self.image is None:
            raise ValueError("Image not found. Check file path.")

        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

    # ---------------------------------
    # Mean Color (RGB)
    # ---------------------------------
    def extract_mean_color(self):
        return np.mean(self.image_rgb, axis=(0, 1))

    # ---------------------------------
    # Color Variance
    # ---------------------------------
    def extract_color_variance(self):
        return np.var(self.image_rgb, axis=(0, 1))

    # ---------------------------------
    # Dominant Hue (HSV Space)
    # ---------------------------------
    def extract_dominant_hue(self):
        hue_channel = self.hsv[:, :, 0]
        return int(np.mean(hue_channel))

    # ---------------------------------
    # Oil Detection (Improved Logic)
    # ---------------------------------
    def detect_oil_presence(self):
        """
        Oil tends to:
        - Lower saturation (washed-out look)
        - Increase brightness variation
        - Create smooth gradients
        """

        saturation = self.hsv[:, :, 1]
        value = self.hsv[:, :, 2]

        mean_saturation = np.mean(saturation)
        std_brightness = np.std(value)

        # Heuristic logic:
        oil_score = 0

        if mean_saturation < 80:
            oil_score += 1

        if std_brightness > 35:
            oil_score += 1

        oil_present = oil_score >= 1

        return oil_present, float(mean_saturation), float(std_brightness)

    # ---------------------------------
    # Edge Density (Texture Indicator)
    # ---------------------------------
    def analyze_texture(self):
        edges = cv2.Canny(self.gray, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size

        if edge_density < 0.02:
            texture = "smooth"
        elif edge_density < 0.05:
            texture = "semi-grainy"
        else:
            texture = "grainy"

        return texture, float(edge_density)

    # ---------------------------------
    # Stain Area Ratio
    # ---------------------------------
    def calculate_stain_area_ratio(self):
        """
        Detect stain area using thresholding.
        """
        _, thresh = cv2.threshold(self.gray, 200, 255, cv2.THRESH_BINARY_INV)
        stain_pixels = np.sum(thresh > 0)
        total_pixels = thresh.size

        area_ratio = stain_pixels / total_pixels
        return float(area_ratio)

    # ---------------------------------
    # Spread Metric (Contour Analysis)
    # ---------------------------------
    def calculate_spread_metric(self):
        """
        Measures how wide the stain spreads.
        """
        _, thresh = cv2.threshold(self.gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return 0.0

        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)

        if perimeter == 0:
            return 0.0

        spread_metric = area / perimeter
        return float(spread_metric)

    # ---------------------------------
    # Full Analysis
    # ---------------------------------
    def analyze(self):
        self.load_image()

        mean_color = self.extract_mean_color()
        color_variance = self.extract_color_variance()
        dominant_hue = self.extract_dominant_hue()

        oil_presence, mean_saturation, std_brightness = self.detect_oil_presence()
        texture, edge_density = self.analyze_texture()

        stain_area_ratio = self.calculate_stain_area_ratio()
        spread_metric = self.calculate_spread_metric()

        features = {
            "mean_rgb": mean_color.tolist(),
            "color_variance": color_variance.tolist(),
            "dominant_hue": dominant_hue,
            "oil_presence": oil_presence,
            "mean_saturation": mean_saturation,
            "brightness_std": std_brightness,
            "edge_density": edge_density,
            "texture": texture,
            "stain_area_ratio": stain_area_ratio,
            "spread_metric": spread_metric
        }

        return features

"""

| Feature          | Why It Matters               |
| ---------------- | ---------------------------- |
| mean_rgb         | Base pigment clue            |
| color_variance   | Mixed vs uniform spice       |
| dominant_hue     | Better color interpretation  |
| oil_presence     | Fat detection (multi-factor) |
| mean_saturation  | Washed vs vivid spice        |
| brightness_std   | Diffusion indicator          |
| edge_density     | Texture/granularity          |
| stain_area_ratio | Thick vs watery dish         |
| spread_metric    | Oil-heavy radial spread      |

  """