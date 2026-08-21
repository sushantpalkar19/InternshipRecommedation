# Product Requirements Document (PRD)

## Internship Recommendation System — PS25034

**Smart India Hackathon 2025**

| Field              | Detail                                      |
|--------------------|---------------------------------------------|
| **Version**        | 1.0                                         |
| **Date**           | August 21, 2026                             |
| **Authors**        | Sushant Palkar, Nirbhay Moholkar            |
| **Problem ID**     | PS25034                                     |
| **Status**         | Draft                                       |

---

## 1. Executive Summary

The Internship Recommendation System is a machine-learning-powered web application that matches students with the most relevant internship opportunities based on their skills and interests. Built using TF-IDF, CountVectorizer, and Word2Vec models, the system uses cosine similarity to rank and recommend internships from a dataset of 500+ records.

This PRD outlines the current state of the product, identifies gaps and improvement areas, and provides a roadmap for future development.

---

## 2. Problem Statement

Students face significant challenges when searching for internships:

- **Information Overload**: Hundreds of listings across platforms make manual filtering tedious.
- **Skill Mismatch**: Students apply to roles that don't align with their expertise.
- **Discovery Gap**: Relevant opportunities are often missed due to poor keyword matching.
- **No Personalization**: Existing platforms rarely offer intelligent, skill-based matching.

**Target Users**: Students (undergraduate/postgraduate) seeking internships aligned with their technical skills.

---

## 3. Goals & Objectives

### 3.1 Primary Goals
| # | Goal | Success Metric |
|---|------|----------------|
| G1 | Match students to relevant internships based on skills | >80% user satisfaction with recommendations |
| G2 | Provide a fast, intuitive interface | <3 second response time |
| G3 | Compare multiple ML approaches | Three models with quality trade-offs documented |

### 3.2 Secondary Goals
| # | Goal | Success Metric |
|---|------|----------------|
| G4 | Enable filtering by location, mode, duration | Filter functionality works end-to-end |
| G5 | Scale to 5,000+ internship records | No performance degradation |
| G6 | Integrate real-time data from external APIs | At least one live API integrated |

---

## 4. User Personas

### Persona 1: CS Student (Primary)
- **Age**: 20–24
- **Goal**: Find a Python/Data Science internship
- **Pain Point**: Manually scanning 100+ listings; keyword search returns irrelevant results
- **Usage**: Enters skills, selects TF-IDF model, reviews top 10 matches

### Persona 2: Career Counselor (Secondary)
- **Age**: 30–50
- **Goal**: Help multiple students find internships
- **Pain Point**: No bulk recommendation tool
- **Usage**: Compares models, evaluates recommendation quality

---

## 5. Current System Architecture

```
┌─────────────────────────────────────────────┐
│              Streamlit Frontend              │
│   ┌─────────┐  ┌──────────┐  ┌───────────┐ │
│   │  Input   │  │  Model   │  │  Results  │ │
│   │  Skills  │→ │ Selector │→ │  Display  │ │
│   └─────────┘  └──────────┘  └───────────┘ │
└───────────────────┬─────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │  TF-IDF  │ │  CountV  │ │ Word2Vec │
  │  Model   │ │  Model   │ │  Model   │
  └────┬─────┘ └────┬─────┘ └────┬─────┘
       └────────────┼────────────┘
                    ▼
            ┌──────────────┐
            │   data.csv   │
            │  (500 rows)  │
            └──────────────┘
```

### 5.1 Tech Stack
| Layer        | Technology        |
|-------------|-------------------|
| Frontend    | Streamlit (Python)|
| ML Models   | scikit-learn, gensim |
| Data        | Pandas, CSV       |
| Computation | NumPy             |

---

## 6. Known Issues & Bugs (Current State)

### 6.1 Critical Bugs

| ID   | Issue | Impact | File |
|------|-------|--------|------|
| BUG-1 | **Path bug in model files**: `pd.read_csv("data.csv")` at module level uses CWD, not project root. Models live in `models/` but expect `data.csv` at root. | App crashes on import | `model_tfidf.py`, `model_countvec.py`, `model_word2vec.py` |
| BUG-2 | **Stipend double-wrapping**: `app.py` lambda prepends `₹` to values already formatted as `₹5,000` in CSV. | Display shows `₹₹5,000/month` | `app.py:78` |
| BUG-3 | **Similarity Score hidden**: Models return `Similarity_Score` but `app.py` filters it out. | Users can't see match confidence | `app.py:85` |

### 6.2 Medium Priority Issues

| ID   | Issue | Impact |
|------|-------|--------|
| MED-1 | Module-level side effects: CSV loading + vectorizer fitting on import | Slow startup, no lazy loading |
| MED-2 | No `@st.cache_resource`: Models re-fitted on every Streamlit rerun | Poor performance |
| MED-3 | Word2Vec trained on 500 rows: Tiny corpus produces weak embeddings | Semantic model underperforms TF-IDF |
| MED-4 | `data/` directory is empty; `data.csv` sits at project root | Confusing project structure |
| MED-5 | No input validation beyond empty check | Garbage input produces garbage output |
| MED-6 | README markdown tables render as plain text | Poor documentation rendering |

---

## 7. Functional Requirements

### 7.1 Current Features (Implemented)

| ID   | Feature | Status |
|------|---------|--------|
| F-1  | Skill-based internship recommendation | ✅ Implemented |
| F-2  | Three ML model selection (TF-IDF, CountVec, Word2Vec) | ✅ Implemented |
| F-3  | Streamlit web UI with sidebar | ✅ Implemented |
| F-4  | Top-N results display | ✅ Implemented |
| F-5  | Basic input validation (empty check) | ✅ Implemented |

### 7.2 Required Improvements (Proposed)

| ID   | Feature | Priority | Effort |
|------|---------|----------|--------|
| F-6  | Fix path bug in model files | P0 | 1 hr |
| F-7  | Show Similarity Score in results | P0 | 30 min |
| F-8  | Fix stipend formatting | P0 | 30 min |
| F-9  | Add `@st.cache_resource` for model caching | P1 | 2 hrs |
| F-10 | Lazy-load models (remove module-level side effects) | P1 | 2 hrs |
| F-11 | Add location/duration/mode/stipend filters | P1 | 4 hrs |
| F-12 | Use pre-trained Word2Vec (Google News vectors) | P1 | 3 hrs |
| F-13 | Add skill auto-suggestion/autocomplete | P2 | 4 hrs |
| F-14 | Add comparison view (side-by-side model output) | P2 | 5 hrs |
| F-15 | User authentication & profile saving | P2 | 8 hrs |
| F-16 | Integration with Internshala / LinkedIn API | P3 | 12 hrs |
| F-17 | Export results to CSV/PDF | P2 | 3 hrs |
| F-18 | BERT / Sentence Transformers model | P3 | 8 hrs |
| F-19 | Feedback mechanism (thumbs up/down) | P2 | 5 hrs |
| F-20 | Analytics dashboard (popular skills, match rates) | P3 | 8 hrs |

---

## 8. Non-Functional Requirements

| Category | Requirement | Target |
|----------|-------------|--------|
| **Performance** | Recommendation latency | < 2 seconds |
| **Performance** | Page load time | < 3 seconds |
| **Scalability** | Dataset size support | 5,000+ records |
| **Usability** | Mobile responsiveness | Responsive via Streamlit |
| **Accessibility** | Screen reader support | ARIA labels in Streamlit |
| **Reliability** | Graceful error handling | No unhandled exceptions |
| **Security** | Input sanitization | No XSS via skill input |
| **Maintainability** | Code modularity | Separate model, UI, and data layers |
| **Testing** | Unit test coverage | > 70% for model logic |

---

## 9. Data Requirements

### 9.1 Current Dataset Schema

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Internship_ID | int | Unique identifier | 1 |
| Title | str | Job title | "AI Research Intern" |
| Skills | str | Comma-separated skills | "Python, ML, Pandas" |
| Location | str | City name | "Delhi" |
| Duration | str | Time period | "3 Months" |
| Stipend | str | Monthly pay | "₹15,000" |
| Mode | str | Work mode | "Remote" |

### 9.2 Data Quality Concerns

- **Skill-title mismatch**: Many records have skills that don't match the internship title (e.g., "Backend Developer" with IoT skills).
- **Synthetic data**: All 500 records are generated, not sourced from real listings.
- **No skill taxonomy**: Skills are free-text without normalization (e.g., "ML" vs "Machine Learning").
- **Missing values**: Some stipend fields are "Unpaid" or empty.

### 9.3 Recommended Data Improvements

1. Add a **skill taxonomy** for normalization (e.g., "ML" → "Machine Learning")
2. Source **real data** from Internshala API or similar
3. Add **skill categories** (Programming, Framework, Tool, Soft Skill)
4. Include **company name** and **application URL**
5. Add **posting date** and **application deadline**

---

## 10. Model Architecture & Evaluation

### 10.1 TF-IDF (Recommended Baseline)
- **Approach**: Vectorize skills using TF-IDF, compute cosine similarity
- **Strengths**: Weighted keyword matching, handles rare skills well
- **Weakness**: No semantic understanding
- **Improvement**: Add n-gram support (bigrams for "Machine Learning")

### 10.2 CountVectorizer (Baseline)
- **Approach**: Binary/count frequency matching
- **Strengths**: Simple, fast
- **Weakness**: No weighting — common skills dominate
- **Improvement**: Only useful as a comparison baseline

### 10.3 Word2Vec (Semantic Model)
- **Approach**: Train Word2Vec on skill corpus, average word vectors
- **Strengths**: Captures semantic relationships
- **Weakness**: Trained on tiny corpus (500 rows); embeddings are poor
- **Improvement**: Use pre-trained Google News Word2Vec (300d) or switch to Sentence Transformers

### 10.4 Recommended Model Enhancements

| Model | Enhancement | Expected Impact |
|-------|-------------|-----------------|
| TF-IDF | Add bigram support | +5% accuracy for compound skills |
| TF-IDF | Custom stop words (remove "intern") | Better signal-to-noise |
| Word2Vec | Pre-trained vectors | Significant quality boost |
| New | BERT / Sentence Transformers | Best semantic understanding |
| New | Hybrid (TF-IDF + Semantic) | Best of both worlds |

---

## 11. UI/UX Improvements

### 11.1 Current UI Flow
```
Landing Page → Enter Skills → Select Model → Click Button → View Results Table
```

### 11.2 Proposed UI Enhancements

| Enhancement | Description | Priority |
|-------------|-------------|----------|
| **Skill Autocomplete** | Dropdown with available skills from dataset | P1 |
| **Filter Panel** | Location, Duration, Mode, Stipend range filters | P1 |
| **Model Comparison** | Side-by-side results from 2-3 models | P2 |
| **Match Explanation** | Show which skills matched and why | P2 |
| **Export Button** | Download results as CSV or PDF | P2 |
| **Rating System** | Users rate recommendation quality (1–5) | P2 |
| **Dark Mode** | Toggle for dark/light theme | P3 |
| **Responsive Cards** | Card-based layout instead of table | P3 |

### 11.3 Proposed Wireframe Flow
```
┌──────────────────────────────────────────────────────────┐
│  SIDEBAR              │           MAIN AREA              │
│                       │                                   │
│  [Model Selector]     │  🎓 Internship Recommender       │
│  ○ TF-IDF             │                                   │
│  ○ CountVec           │  Skills: [________________] 🔍   │
│  ○ Word2Vec           │                                   │
│                       │  Filters: [Location▾][Mode▾]     │
│  ─────────────        │                                   │
│  Filters:             │  ┌────────────────────────────┐  │
│  Location [All ▾]     │  │ 🏆 Top Matches (23 found)  │  │
│  Mode [All ▾]         │  │                              │  │
│  Duration [All ▾]     │  │  Title    │ Match │ Location │  │
│  Stipend [₹0-₹50k]   │  │  ─────────┼───────┼──────────│  │
│                       │  │  ML Intern│ 92%   │ Delhi    │  │
│  ─────────────        │  │  AI Res.. │ 87%   │ Remote   │  │
│  Available Skills:    │  │  Data An..│ 84%   │ Mumbai   │  │
│  □ Python             │  └────────────────────────────┘  │
│  □ Machine Learning   │                                   │
│  □ SQL                │  [Export CSV] [Export PDF]        │
└──────────────────────────────────────────────────────────┘
```

---

## 12. Testing Strategy

### 12.1 Unit Tests
| Test Area | Tests |
|-----------|-------|
| `recommend_tfidf()` | Returns correct columns, handles empty input, respects top_n |
| `recommend_countvec()` | Same as above |
| `recommend_word2vec()` | Same + handles unknown skills gracefully |
| `get_vector()` | Returns zero vector for unknown words |

### 12.2 Integration Tests
- End-to-end: Input skills → model selection → results displayed
- Path resolution: Models correctly find `data.csv` from any CWD

### 12.3 Performance Tests
- Benchmark recommendation latency for 500, 1000, 5000 records
- Memory usage profiling

---

## 13. Improvement Roadmap

### Phase 1: Fix & Harden (Week 1)
- [ ] Fix path bug in all model files (BUG-1)
- [ ] Fix stipend double-wrapping (BUG-2)
- [ ] Show Similarity Score in results (BUG-3)
- [ ] Add `@st.cache_resource` for model caching
- [ ] Lazy-load models (remove module-level side effects)
- [ ] Add proper error handling

### Phase 2: Enhance UX (Week 2)
- [ ] Add filter panel (location, mode, duration, stipend)
- [ ] Add skill autocomplete from dataset
- [ ] Add model comparison view
- [ ] Add export to CSV
- [ ] Improve README with proper markdown tables

### Phase 3: Improve ML Quality (Week 3)
- [ ] Integrate pre-trained Word2Vec or Sentence Transformers
- [ ] Add skill normalization / taxonomy
- [ ] Add bigram support to TF-IDF
- [ ] Create proper train/test split for evaluation
- [ ] Document precision/recall metrics for each model

### Phase 4: Scale & Integrate (Week 4+)
- [ ] Integrate Internshala / LinkedIn API for real data
- [ ] Add user authentication
- [ ] Add feedback mechanism
- [ ] Build analytics dashboard
- [ ] Deploy to cloud (AWS/GCP)

---

## 14. Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Recommendation accuracy (user survey) | Unknown | > 80% |
| Response time | Unknown | < 2s |
| Dataset size | 500 records | 5,000+ |
| Models available | 3 | 5+ |
| User satisfaction (NPS) | Unknown | > 7/10 |
| Bug count (Critical) | 3 | 0 |
| Test coverage | 0% | > 70% |

---

## 15. Appendix

### A. File Structure (Proposed After Fixes)
```
SIH25034_Internship_Recommendation/
├── app.py                    # Streamlit main app
├── requirements.txt          # Dependencies
├── PRD.md                    # This document
├── README.md                 # Documentation
├── data/
│   └── internships.csv       # Cleaned dataset
├── models/
│   ├── __init__.py
│   ├── base.py               # Shared model logic
│   ├── model_tfidf.py        # TF-IDF model
│   ├── model_countvec.py     # CountVectorizer model
│   └── model_word2vec.py     # Word2Vec model
├── tests/
│   ├── test_models.py        # Model unit tests
│   └── test_app.py           # Integration tests
└── utils/
    ├── preprocessing.py      # Skill normalization
    └── data_loader.py        # Cached data loading
```

### B. Dependency List
| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | latest | Web UI |
| pandas | latest | Data manipulation |
| scikit-learn | latest | TF-IDF, CountVec, cosine similarity |
| gensim | latest | Word2Vec |
| numpy | latest | Numerical computation |
| pytest | latest | Testing (proposed) |
| requests | latest | API integration (proposed) |

### C. References
- Smart India Hackathon 2025 — Problem Statement PS25034
- scikit-learn TF-IDF Documentation
- Gensim Word2Vec Documentation
- Streamlit Documentation

---

*Document prepared for Smart India Hackathon 2025 — PS25034*
*"Connecting skills with opportunities — intelligently."*
