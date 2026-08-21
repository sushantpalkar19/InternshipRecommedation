# 🎯 Internship Recommendation System (PS25034)

Welcome to **Internship Recommender** — an advanced recommendation system designed to match students with the most suitable internships based on their skills, preferences, and interests.  
Built as part of **Smart India Hackathon 2025**, this project demonstrates the use of **Machine Learning & NLP models** with evaluation-driven recommendations.

---

## 🚀 Features

✅ **Smart Skill Matching** - Recommend internships based on user-inputted skills with normalization  
✅ **Multiple ML Models** - Three recommendation models for comparison:
- **TF-IDF (Recommended)** – Smart keyword weighting  
- **CountVectorizer** – Simple baseline model  
- **Word2Vec** – Semantic understanding of skills  

✅ **Preference-Aware Ranking** - Weighted scoring considering:
- Skill relevance (70%)
- User preferences (20%)
- Internship quality/freshness (10%)

✅ **Advanced Filters** - Filter by location, work mode, domain, duration, and stipend  
✅ **Explainable Recommendations** - See why each internship was recommended with matched/missing skills  
✅ **Professional UI** - Modern card-based interface with detailed internship information  
✅ **Evaluation Metrics** - Precision@K, Recall@K, NDCG@K, MRR, Coverage, and Zero-result rate  
✅ **Clean Dataset** - 200+ realistic internship records with proper title-skill mappings  

---

## 🧩 Project Structure

SIH25034_Internship_Recommendation/
│
├── app.py                       # Streamlit main app (UI + logic)
├── requirements.txt             # Python dependencies
│
├── data/
│   ├── raw/
│   │   └── internships_raw.csv  # Original dataset backup
│   ├── processed/
│   │   └── internships_clean.csv # Cleaned dataset (200 records)
│   └── evaluation/
│       ├── evaluation_dataset.csv # Labelled evaluation data
│       ├── ground_truth.json      # Ground truth for evaluation
│       └── model_comparison.csv   # Model performance comparison
│
├── src/
│   ├── data_loader.py           # Centralized data loading
│   ├── preprocessing.py         # Skill normalization
│   ├── ranking.py               # Weighted ranking system
│   ├── explanations.py          # Recommendation explanations
│   └── evaluation.py            # Evaluation metrics
│
├── models/
│   ├── model_tfidf.py           # TF-IDF recommendation logic
│   ├── model_countvec.py        # CountVectorizer logic
│   └── model_word2vec.py        # Word2Vec logic
│
├── scripts/
│   ├── generate_clean_dataset.py    # Generate realistic dataset
│   ├── generate_evaluation_dataset.py # Create evaluation data
│   └── evaluate.py                  # Run model evaluation
│
└── README.md                    # Project documentation

---

## ⚙️ Installation & Setup

### Step 1 — Clone Repository
```bash
git clone https://github.com/<your-username>/SIH25034_Internship_Recommendation.git
cd SIH25034_Internship_Recommendation
```

### Step 2 — Create Virtual Environment
```bash
python -m venv .venv
```

### Step 3 — Activate Virtual Environment
**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Generate Dataset
```bash
python scripts/generate_clean_dataset.py
python scripts/generate_evaluation_dataset.py
```

### Step 6 — Run App on Localhost
```bash
streamlit run app.py
```

Then open your browser at 👉 http://localhost:8501

---

## 📊 Models Overview

| Model | Technique | Description | Best For |
|-------|-----------|-------------|----------|
| TF-IDF | Weighted Keyword Matching | Prioritizes unique skill terms | Accurate keyword-based matches |
| CountVectorizer | Frequency-based | Simple baseline matching | Quick comparisons |
| Word2Vec | Semantic Embedding | Understands meaning and relationships | Context-aware matching |

---

## 📁 Dataset Information

**File:** `data/processed/internships_clean.csv`

**Columns:**
- **Internship_ID** — Unique internship identifier
- **Title** — Internship title (e.g., Data Analyst Intern)
- **Company** — Company name
- **Description** — Detailed internship description
- **Skills** — List of required skills (normalized)
- **Location** — Internship city
- **Duration** — Internship period (e.g., 3 Months)
- **Stipend** — Monthly pay or benefits
- **Mode** — Work mode (Onsite, Remote, Hybrid)
- **Domain** — Technical domain (e.g., Data Science, Web Development)
- **Eligibility** — Required education
- **Experience_Level** — Required experience level
- **Application_URL** — Application link
- **Posted_Date** — Posting date
- **Deadline** — Application deadline
- **Status** — Open/Closed status

---

## 🧠 Example Usage

1. **Launch the app** using `streamlit run app.py`
2. **Enter your skills** like "Python, Data Science, Machine Learning"
3. **Set your preferences** using the sidebar filters
4. **Click "Get Recommendations"** to view top internships
5. **View explanations** by expanding "Why recommended?" sections

---

## 📈 Evaluation Results

The system has been evaluated using the following metrics:

- **Precision@K** - How many top-K recommendations are relevant
- **Recall@K** - How many relevant internships were retrieved
- **NDCG@K** - Ranking quality measurement
- **MRR** - Mean Reciprocal Rank
- **Coverage** - Catalog coverage percentage
- **Zero-result Rate** - Frequency of empty results

To run evaluation:
```bash
python scripts/evaluate.py
```

---

## 💡 Architecture

### Recommendation Pipeline

```
User Skills/Profile
        ↓
Skill Normalization
        ↓
Candidate Profile Representation
        ↓
Semantic Similarity (TF-IDF/CountVec/Word2Vec)
        ↓
Preference Filtering
        ↓
Weighted Ranking (70% Skills + 20% Preferences + 10% Quality)
        ↓
Top-K Recommendations
        ↓
Explainability Layer
        ↓
UI (Card-based Display)
```

---

## 🔧 Advanced Features

### Skill Normalization
The system automatically normalizes skills using aliases:
- `ml` → `Machine Learning`
- `ai` → `Artificial Intelligence`
- `reactjs` → `React`
- `nodejs` → `Node.js`
- And many more...

### Weighted Ranking
Configure ranking weights in the sidebar:
- **Skill Weight** (default: 0.70)
- **Preference Weight** (default: 0.20)
- **Quality Weight** (default: 0.10)

### Filters
- **Location** - Pune, Mumbai, Bangalore, Remote, etc.
- **Work Mode** - Remote, Hybrid, In-Office
- **Domain** - Data Science, Web Development, Cloud, etc.
- **Duration** - 1 Month, 3 Months, 6 Months, etc.
- **Stipend** - Min/Max stipend range

---

## 🧑‍💻 Developers

**Name:** Sushant Palkar and Nirbhay Moholkar  
**Role:** Full-stack development, ML integration, and data engineering

---

## 🏁 License

This project is licensed under the MIT License — you are free to use, modify, and distribute it with attribution.

---

## 🧩 Acknowledgment

Developed for **Smart India Hackathon 2025**  
Problem Statement ID: PS25034 – AyurSutra: Internship Recommendation System

✨ “Connecting skills with opportunities — intelligently.”

---

## 📝 Future Enhancements

- [ ] Integration with real-world internship APIs (e.g., Internshala)
- [ ] User authentication and profile management
- [ ] Advanced NLP models (Sentence Transformers, BERT)
- [ ] Resume parsing and skill extraction
- [ ] Personalized feedback and learning
- [ ] Mobile application
- [ ] Recruiter-side matching system


