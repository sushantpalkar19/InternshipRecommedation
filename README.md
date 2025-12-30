# 🎯 Internship Recommendation System (PS25034)

Welcome to **Internship Recommender** — a smart recommendation system designed to match students with the most suitable internships based on their skills and interests.  
Built as part of **Smart India Hackathon 2025**, this project demonstrates the use of **Machine Learning & NLP models** (TF-IDF, CountVectorizer, Word2Vec) for personalized recommendations.

---

## 🚀 Features

✅ Recommend internships based on user-inputted skills  
✅ Three ML models for comparison:
- **TF-IDF (Recommended)** – Smart keyword weighting  
- **CountVectorizer** – Simple baseline model  
- **Word2Vec** – Semantic understanding of skills  

✅ Clean and interactive **Streamlit** web interface  
✅ Local dataset of **500+ synthetic internship records**  
✅ Real-time similarity scoring using **cosine similarity**

---

## 🧩 Project Structure

SIH25034_Internship_Recommendation/
│
├── app.py                       # Streamlit main app (UI + logic)
├── data.csv                     # Internship dataset (500+ records)
├── requirements.txt             # Python dependencies
│
├── models/
│   ├── model_tfidf.py           # TF-IDF recommendation logic
│   ├── model_countvec.py        # CountVectorizer logic
│   └── model_word2vec.py        # Word2Vec logic
│
└── README.md                    # Project documentation

---

## ⚙️ Installation & Setup

### Step 1 — Clone Repository
```bash
git clone https://github.com/<your-username>/SIH25034_Internship_Recommendation.git
cd SIH25034_Internship_Recommendation

Step 2 — Create Virtual Environment
python -m venv .venv

Step 3 — Activate Virtual Environment
On Windows:
.venv\Scripts\activate

On macOS/Linux:
source .venv/bin/activate

Step 4 — Install Dependencies
pip install -r requirements.txt

Step 5 — Run App on Localhost
streamlit run app.py

Then open your browser at 👉 http://localhost:8501

📊 Models Overview
ModelTechniqueDescriptionBest ForTF-IDFWeighted Keyword MatchingPrioritizes unique skill termsAccurate keyword-based matchesCountVectorizerFrequency-basedSimple baseline matchingQuick comparisonsWord2VecSemantic EmbeddingUnderstands meaning and relationshipsContext-aware matching

📁 Dataset Information
File: data.csv
Columns:


Internship_ID — Unique internship identifier


Title — Internship title (e.g., Data Analyst Intern)


Skills — List of required skills


Location — Internship city


Duration — Internship period (e.g., 3 Months)


Stipend — Monthly pay or benefits


Mode — Work mode (Onsite, Remote, Hybrid)



🧠 Example Usage


Launch the app.


Enter skills like Python, Data Science, Machine Learning.


Select your preferred model from the sidebar.


View top recommended internships with title, location, stipend, and duration.



💡 Future Enhancements


Integration with real-world internship APIs (e.g., Internshala)


User authentication and dashboard


Advanced NLP models like BERT or Sentence Transformers


Personalized feedback system



🧑‍💻 Developers
NameRole :Sushant Palkar and Nirbhay Moholkar Developer & Model Integration Frontend (Streamlit UI) & Data Engineering

🏁 License
This project is licensed under the MIT License — you are free to use, modify, and distribute it with attribution.

🧩 Acknowledgment
Developed for Smart India Hackathon 2025
Problem Statement ID: PS25034 – AyurSutra: Internship Recommendation System

✨ “Connecting skills with opportunities — intelligently.”

---


