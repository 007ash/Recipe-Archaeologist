# 🏺 Recipe Archaeologist

*Uncover the culinary secrets hidden in food stains.*

**Recipe Archaeologist** is an AI-powered project that analyzes images of food spills, smudges, and stains to reverse-engineer the likely recipe that caused them. By combining computer vision-based molecular inference with the generative power of a Large Language Model (Google Gemini), the system deduces spectral signatures, oil presence, texture, and probable ingredients mathematically—and then reconstructs the full original dish.

## 🚀 Features

- **Forensic Image Analysis**: Uses OpenCV to extract key visual features such as mean RGB, dominant hue, color variance, edge density (texture), and oil presence.
- **Molecular Inference Engine**: Maps physical features into rule-based scoring systems to probabilistically determine base ingredients (e.g., turmeric, red chili, oil, cream).
- **Generative Reconstruction**: Utilizes Google's Gemini Flash model to interpret the forensic breakdown and produce multiple hypotheses for the original dish, complete with recipes and molecular reasoning.
- **Interactive UI**: A sleek Streamlit dashboard that visualizes the molecular breakdown and inferred recipes side-by-side.
- **Prototyping Notebook**: A complete, self-contained Jupyter Notebook for rapid testing and experimentation without spinning up the backend/frontend.

## 📁 Project Structure

```bash
📦 Recipe Achelogist
├── 📂 backend
│   ├── image_analysis.py       # OpenCV-based visual feature extraction
│   ├── molecular_inference.py  # Rule-based ingredient scoring
│   ├── llm_engine.py           # Gemini prompting and integration
│   ├── main.py                 # FastAPI server handling API endpoints
│   └── requirements.txt        # Backend dependencies
├── 📂 frontend
│   └── app.py                  # Streamlit web application
├── 📂 NoteBook
│   └── noteBook.ipynb          # Self-contained prototype combining all logic
└── 📜 README.md                # Project documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/007ash/recipe-archaeologist.git
cd recipe-archaeologist
```

### 2. Set Up the Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies (make sure to create a virtual environment, if preferred):
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If `requirements.txt` does not include all dependencies, ensure `fastapi`, `uvicorn`, `opencv-python`, `numpy`, `python-multipart`, and `google-genai` are installed.*
3. **Configure your API Key**: Update the `API_KEY` variable inside `main.py` with your active Gemini API key.
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend will now be running at `http://127.0.0.1:8000`.

### 3. Set Up the Frontend
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install Streamlit (if not already installed):
   ```bash
   pip install streamlit pandas requests
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   The interactive UI will open automatically in your browser.

### 4. Running the Jupyter Prototype
If you want to experiment locally without starting the API and Streamlit:
1. Navigate to the `NoteBook` folder.
2. Open `noteBook.ipynb` in Jupyter Notebook or JupyterLab.
3. Insert your Gemini `API_KEY` in the final cell and execute the notebook directly.

## 🧪 How It Works

1. **Upload**: A user uploads an image of a stain.
2. **Analysis**: The image is analyzed sequentially for dominant hues, saturation, variance, and texture.
3. **Inference**: The system uses heuristics (e.g., low saturation + high brightness variation = oil presence) to narrow down potential ingredients.
4. **Generation**: The data is packed into a dynamic prompt and sent to the LLM to output accurate, scientifically sound recipes formatted neatly in JSON.
5. **Display**: The Streamlit frontend parses this data, demonstrating raw inputs, probabilities, and the final deduced recipes.
