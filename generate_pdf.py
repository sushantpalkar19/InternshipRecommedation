#!/usr/bin/env python3
"""Convert PRD markdown to a professional PDF using fpdf2."""

from fpdf import FPDF
import re
import os

class PRD_PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return  # Skip header on title page
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, 'PRD - Internship Recommendation System (PS25034)', align='L')
        self.cell(0, 8, f'Page {self.page_no()}', align='R', new_x="LMARGIN", new_y="NEXT")
        self.line(10, 18, 200, 18)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Smart India Hackathon 2025 | Developed by Sushant & Nirbhay', align='C')

    def chapter_title(self, num, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(30, 60, 120)
        self.ln(4)
        self.cell(0, 10, f'{num}. {title}', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def subsection_title(self, title):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(70, 70, 70)
        self.ln(1)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=15):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 5.5, '-')
        self.multi_cell(0, 5.5, f' {text}')
        self.ln(1)

    def table_header(self, cols, widths):
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 8, col, border=1, fill=True, align='C')
        self.ln()

    def table_row(self, cols, widths, fill=False):
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(40, 40, 40)
        if fill:
            self.set_fill_color(240, 245, 255)
        else:
            self.set_fill_color(255, 255, 255)
        
        # Calculate max height needed
        max_lines = 1
        for i, col in enumerate(cols):
            lines = self.multi_cell(widths[i], 5, col, dry_run=True, output="LINES")
            if len(lines) > max_lines:
                max_lines = len(lines)
        
        row_height = max(8, max_lines * 5)
        
        # Check if we need a new page
        if self.get_y() + row_height > 270:
            self.add_page()
        
        y_start = self.get_y()
        x_start = self.get_x()
        
        for i, col in enumerate(cols):
            x = x_start + sum(widths[:i])
            self.set_xy(x, y_start)
            self.cell(widths[i], row_height, '', border=1, fill=fill)
            self.set_xy(x + 1, y_start + 1)
            self.multi_cell(widths[i] - 2, 5, col)
        
        self.set_xy(x_start, y_start + row_height)


def parse_markdown(md_path):
    """Parse markdown file and return structured content."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def build_pdf(md_content, output_path):
    pdf = PRD_PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # ============ TITLE PAGE ============
    pdf.add_page()
    pdf.ln(40)
    
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 15, 'Product Requirements', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Document', align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'Internship Recommendation System', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'PS25034', align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(15)
    pdf.set_draw_color(30, 60, 120)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)
    info_lines = [
        ('Version', '1.0'),
        ('Date', 'August 21, 2026'),
        ('Authors', 'Sushant Palkar, Nirbhay Moholkar'),
        ('Program', 'Smart India Hackathon 2025'),
        ('Status', 'Draft'),
    ]
    for label, value in info_lines:
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(50, 8, label + ':', align='R')
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 8, f'  {value}', new_x="LMARGIN", new_y="NEXT")
    
    # ============ TABLE OF CONTENTS ============
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 12, 'Table of Contents', new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(30, 60, 120)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    toc_items = [
        '1. Executive Summary',
        '2. Problem Statement',
        '3. Goals & Objectives',
        '4. User Personas',
        '5. Current System Architecture',
        '6. Known Issues & Bugs',
        '7. Functional Requirements',
        '8. Non-Functional Requirements',
        '9. Data Requirements',
        '10. Model Architecture & Evaluation',
        '11. UI/UX Improvements',
        '12. Testing Strategy',
        '13. Improvement Roadmap',
        '14. Success Metrics',
        '15. Appendix',
    ]
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(40, 40, 40)
    for item in toc_items:
        pdf.cell(0, 8, item, new_x="LMARGIN", new_y="NEXT")
    
    # ============ SECTION 1: Executive Summary ============
    pdf.add_page()
    pdf.chapter_title('1', 'Executive Summary')
    pdf.body_text(
        'The Internship Recommendation System is a machine-learning-powered web application '
        'that matches students with the most relevant internship opportunities based on their '
        'skills and interests. Built using TF-IDF, CountVectorizer, and Word2Vec models, the '
        'system uses cosine similarity to rank and recommend internships from a dataset of '
        '500+ records.'
    )
    pdf.body_text(
        'This PRD outlines the current state of the product, identifies gaps and improvement '
        'areas, and provides a roadmap for future development.'
    )
    
    # ============ SECTION 2: Problem Statement ============
    pdf.chapter_title('2', 'Problem Statement')
    pdf.body_text('Students face significant challenges when searching for internships:')
    
    problems = [
        'Information Overload: Hundreds of listings across platforms make manual filtering tedious.',
        'Skill Mismatch: Students apply to roles that don\'t align with their expertise.',
        'Discovery Gap: Relevant opportunities are often missed due to poor keyword matching.',
        'No Personalization: Existing platforms rarely offer intelligent, skill-based matching.',
    ]
    for p in problems:
        pdf.bullet(p)
    
    pdf.ln(2)
    pdf.subsection_title('Target Users')
    pdf.body_text('Students (undergraduate/postgraduate) seeking internships aligned with their technical skills.')
    
    # ============ SECTION 3: Goals & Objectives ============
    pdf.chapter_title('3', 'Goals & Objectives')
    
    pdf.subsection_title('3.1 Primary Goals')
    cols = ['#', 'Goal', 'Success Metric']
    widths = [10, 100, 80]
    pdf.table_header(cols, widths)
    goals_primary = [
        ('G1', 'Match students to relevant internships based on skills', '>80% user satisfaction'),
        ('G2', 'Provide a fast, intuitive interface', '<3 second response time'),
        ('G3', 'Compare multiple ML approaches', 'Three models with quality trade-offs'),
    ]
    for i, row in enumerate(goals_primary):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    pdf.ln(4)
    pdf.subsection_title('3.2 Secondary Goals')
    pdf.table_header(cols, widths)
    goals_secondary = [
        ('G4', 'Enable filtering by location, mode, duration', 'Filter works end-to-end'),
        ('G5', 'Scale to 5,000+ internship records', 'No performance degradation'),
        ('G6', 'Integrate real-time data from external APIs', 'At least one live API'),
    ]
    for i, row in enumerate(goals_secondary):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 4: User Personas ============
    pdf.add_page()
    pdf.chapter_title('4', 'User Personas')
    
    pdf.subsection_title('Persona 1: CS Student (Primary)')
    pdf.bullet('Age: 20-24')
    pdf.bullet('Goal: Find a Python/Data Science internship')
    pdf.bullet('Pain Point: Manually scanning 100+ listings; keyword search returns irrelevant results')
    pdf.bullet('Usage: Enters skills, selects TF-IDF model, reviews top 10 matches')
    
    pdf.ln(2)
    pdf.subsection_title('Persona 2: Career Counselor (Secondary)')
    pdf.bullet('Age: 30-50')
    pdf.bullet('Goal: Help multiple students find internships')
    pdf.bullet('Pain Point: No bulk recommendation tool')
    pdf.bullet('Usage: Compares models, evaluates recommendation quality')
    
    # ============ SECTION 5: Architecture ============
    pdf.add_page()
    pdf.chapter_title('5', 'Current System Architecture')
    
    pdf.body_text('Architecture Flow:')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(40, 40, 40)
    arch_lines = [
        '┌─────────────────────────────────────────────┐',
        '│              Streamlit Frontend              │',
        '│   ┌─────────┐  ┌──────────┐  ┌───────────┐ │',
        '│   │  Input   │  │  Model   │  │  Results  │ │',
        '│   │  Skills  │->│ Selector │->│  Display  │ │',
        '│   └─────────┘  └──────────┘  └───────────┘ │',
        '└───────────────────┬─────────────────────────┘',
        '                    │',
        '        ┌───────────┼───────────┐',
        '        v           v           v',
        '  ┌──────────┐ ┌──────────┐ ┌──────────┐',
        '  │  TF-IDF  │ │  CountV  │ │ Word2Vec │',
        '  │  Model   │ │  Model   │ │  Model   │',
        '  └────┬─────┘ └────┬─────┘ └────┬─────┘',
        '       └────────────┼────────────┘',
        '                    v',
        '            ┌──────────────┐',
        '            │   data.csv   │',
        '            │  (500 rows)  │',
        '            └──────────────┘',
    ]
    for line in arch_lines:
        pdf.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.subsection_title('Tech Stack')
    cols = ['Layer', 'Technology']
    widths = [60, 130]
    pdf.table_header(cols, widths)
    tech = [
        ('Frontend', 'Streamlit (Python)'),
        ('ML Models', 'scikit-learn, gensim'),
        ('Data', 'Pandas, CSV'),
        ('Computation', 'NumPy'),
    ]
    for i, row in enumerate(tech):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 6: Known Issues ============
    pdf.add_page()
    pdf.chapter_title('6', 'Known Issues & Bugs')
    
    pdf.subsection_title('6.1 Critical Bugs')
    cols = ['ID', 'Issue', 'Impact']
    widths = [18, 100, 72]
    pdf.table_header(cols, widths)
    bugs_crit = [
        ('BUG-1', 'Path bug: pd.read_csv("data.csv") at module level uses CWD. Models in models/ expect data.csv at root.', 'App crashes on import'),
        ('BUG-2', 'Stipend double-wrapping: app.py prepends "Rupee" to values already formatted in CSV.', 'Display shows double Rupee symbol'),
        ('BUG-3', 'Similarity Score hidden: Models return score but app.py filters it out.', 'Users cannot see match confidence'),
    ]
    for i, row in enumerate(bugs_crit):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    pdf.ln(4)
    pdf.subsection_title('6.2 Medium Priority Issues')
    cols2 = ['ID', 'Issue', 'Impact']
    pdf.table_header(cols2, widths)
    bugs_med = [
        ('MED-1', 'Module-level side effects: CSV loading + vectorizer fitting on import', 'Slow startup'),
        ('MED-2', 'No @st.cache_resource: Models re-fitted on every rerun', 'Poor performance'),
        ('MED-3', 'Word2Vec trained on 500 rows: Tiny corpus', 'Weak embeddings'),
        ('MED-4', 'Empty data/ directory; data.csv at project root', 'Confusing structure'),
        ('MED-5', 'No input validation beyond empty check', 'Garbage in, garbage out'),
    ]
    for i, row in enumerate(bugs_med):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 7: Functional Requirements ============
    pdf.add_page()
    pdf.chapter_title('7', 'Functional Requirements')
    
    pdf.subsection_title('7.1 Current Features (Implemented)')
    cols = ['ID', 'Feature', 'Status']
    widths = [18, 120, 52]
    pdf.table_header(cols, widths)
    features_now = [
        ('F-1', 'Skill-based internship recommendation', 'Implemented'),
        ('F-2', 'Three ML model selection', 'Implemented'),
        ('F-3', 'Streamlit web UI with sidebar', 'Implemented'),
        ('F-4', 'Top-N results display', 'Implemented'),
        ('F-5', 'Basic input validation (empty check)', 'Implemented'),
    ]
    for i, row in enumerate(features_now):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    pdf.ln(4)
    pdf.subsection_title('7.2 Proposed Improvements')
    cols2 = ['ID', 'Feature', 'Priority', 'Effort']
    widths2 = [14, 95, 40, 41]
    pdf.table_header(cols2, widths2)
    features_new = [
        ('F-6', 'Fix path bug in model files', 'P0', '1 hr'),
        ('F-7', 'Show Similarity Score in results', 'P0', '30 min'),
        ('F-8', 'Fix stipend formatting', 'P0', '30 min'),
        ('F-9', 'Add @st.cache_resource for caching', 'P1', '2 hrs'),
        ('F-10', 'Lazy-load models', 'P1', '2 hrs'),
        ('F-11', 'Add filter panel (location, mode, etc.)', 'P1', '4 hrs'),
        ('F-12', 'Use pre-trained Word2Vec', 'P1', '3 hrs'),
        ('F-13', 'Add skill autocomplete', 'P2', '4 hrs'),
        ('F-14', 'Model comparison view', 'P2', '5 hrs'),
        ('F-15', 'User authentication & profiles', 'P2', '8 hrs'),
        ('F-16', 'Internshala / LinkedIn API integration', 'P3', '12 hrs'),
        ('F-17', 'Export results to CSV/PDF', 'P2', '3 hrs'),
        ('F-18', 'BERT / Sentence Transformers model', 'P3', '8 hrs'),
        ('F-19', 'Feedback mechanism', 'P2', '5 hrs'),
        ('F-20', 'Analytics dashboard', 'P3', '8 hrs'),
    ]
    for i, row in enumerate(features_new):
        pdf.table_row(row, widths2, fill=(i % 2 == 0))
    
    # ============ SECTION 8: Non-Functional Requirements ============
    pdf.add_page()
    pdf.chapter_title('8', 'Non-Functional Requirements')
    
    cols = ['Category', 'Requirement', 'Target']
    widths = [40, 90, 60]
    pdf.table_header(cols, widths)
    nfr = [
        ('Performance', 'Recommendation latency', '< 2 seconds'),
        ('Performance', 'Page load time', '< 3 seconds'),
        ('Scalability', 'Dataset size support', '5,000+ records'),
        ('Usability', 'Mobile responsiveness', 'Responsive via Streamlit'),
        ('Accessibility', 'Screen reader support', 'ARIA labels'),
        ('Reliability', 'Graceful error handling', 'No unhandled exceptions'),
        ('Security', 'Input sanitization', 'No XSS via skill input'),
        ('Maintainability', 'Code modularity', 'Separate layers'),
        ('Testing', 'Unit test coverage', '> 70% for model logic'),
    ]
    for i, row in enumerate(nfr):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 9: Data Requirements ============
    pdf.add_page()
    pdf.chapter_title('9', 'Data Requirements')
    
    pdf.subsection_title('9.1 Current Dataset Schema')
    cols = ['Column', 'Type', 'Description', 'Example']
    widths = [35, 20, 70, 65]
    pdf.table_header(cols, widths)
    schema = [
        ('Internship_ID', 'int', 'Unique identifier', '1'),
        ('Title', 'str', 'Job title', '"AI Research Intern"'),
        ('Skills', 'str', 'Comma-separated skills', '"Python, ML, Pandas"'),
        ('Location', 'str', 'City name', '"Delhi"'),
        ('Duration', 'str', 'Time period', '"3 Months"'),
        ('Stipend', 'str', 'Monthly pay', '"Rupee 15,000"'),
        ('Mode', 'str', 'Work mode', '"Remote"'),
    ]
    for i, row in enumerate(schema):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    pdf.ln(4)
    pdf.subsection_title('9.2 Data Quality Concerns')
    data_issues = [
        'Skill-title mismatch: Many records have skills that don\'t match the title.',
        'Synthetic data: All 500 records are generated, not real.',
        'No skill taxonomy: Skills are free-text without normalization.',
        'Missing values: Some stipend fields are "Unpaid" or empty.',
    ]
    for issue in data_issues:
        pdf.bullet(issue)
    
    pdf.ln(2)
    pdf.subsection_title('9.3 Recommended Data Improvements')
    data_improvements = [
        'Add a skill taxonomy for normalization.',
        'Source real data from Internshala API or similar.',
        'Add skill categories (Programming, Framework, Tool, Soft Skill).',
        'Include company name and application URL.',
        'Add posting date and application deadline.',
    ]
    for imp in data_improvements:
        pdf.bullet(imp)
    
    # ============ SECTION 10: Model Architecture ============
    pdf.add_page()
    pdf.chapter_title('10', 'Model Architecture & Evaluation')
    
    pdf.subsection_title('10.1 TF-IDF (Recommended Baseline)')
    pdf.bullet('Approach: Vectorize skills using TF-IDF, compute cosine similarity')
    pdf.bullet('Strengths: Weighted keyword matching, handles rare skills well')
    pdf.bullet('Weakness: No semantic understanding')
    pdf.bullet('Improvement: Add n-gram support (bigrams for "Machine Learning")')
    
    pdf.ln(2)
    pdf.subsection_title('10.2 CountVectorizer (Baseline)')
    pdf.bullet('Approach: Binary/count frequency matching')
    pdf.bullet('Strengths: Simple, fast')
    pdf.bullet('Weakness: No weighting - common skills dominate')
    pdf.bullet('Improvement: Only useful as a comparison baseline')
    
    pdf.ln(2)
    pdf.subsection_title('10.3 Word2Vec (Semantic Model)')
    pdf.bullet('Approach: Train Word2Vec on skill corpus, average word vectors')
    pdf.bullet('Strengths: Captures semantic relationships')
    pdf.bullet('Weakness: Trained on tiny corpus (500 rows); embeddings are poor')
    pdf.bullet('Improvement: Use pre-trained Google News Word2Vec or Sentence Transformers')
    
    pdf.ln(2)
    pdf.subsection_title('10.4 Recommended Model Enhancements')
    cols = ['Model', 'Enhancement', 'Expected Impact']
    widths = [35, 80, 75]
    pdf.table_header(cols, widths)
    enhancements = [
        ('TF-IDF', 'Add bigram support', '+5% accuracy for compound skills'),
        ('TF-IDF', 'Custom stop words (remove "intern")', 'Better signal-to-noise'),
        ('Word2Vec', 'Pre-trained vectors', 'Significant quality boost'),
        ('New', 'BERT / Sentence Transformers', 'Best semantic understanding'),
        ('New', 'Hybrid (TF-IDF + Semantic)', 'Best of both worlds'),
    ]
    for i, row in enumerate(enhancements):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 11: UI/UX ============
    pdf.add_page()
    pdf.chapter_title('11', 'UI/UX Improvements')
    
    pdf.subsection_title('11.1 Current UI Flow')
    pdf.body_text('Landing Page -> Enter Skills -> Select Model -> Click Button -> View Results Table')
    
    pdf.subsection_title('11.2 Proposed Enhancements')
    cols = ['Enhancement', 'Description', 'Priority']
    widths = [45, 110, 35]
    pdf.table_header(cols, widths)
    ui_enhancements = [
        ('Skill Autocomplete', 'Dropdown with available skills from dataset', 'P1'),
        ('Filter Panel', 'Location, Duration, Mode, Stipend range filters', 'P1'),
        ('Model Comparison', 'Side-by-side results from 2-3 models', 'P2'),
        ('Match Explanation', 'Show which skills matched and why', 'P2'),
        ('Export Button', 'Download results as CSV or PDF', 'P2'),
        ('Rating System', 'Users rate recommendation quality (1-5)', 'P2'),
        ('Dark Mode', 'Toggle for dark/light theme', 'P3'),
        ('Responsive Cards', 'Card-based layout instead of table', 'P3'),
    ]
    for i, row in enumerate(ui_enhancements):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 12: Testing ============
    pdf.add_page()
    pdf.chapter_title('12', 'Testing Strategy')
    
    pdf.subsection_title('12.1 Unit Tests')
    pdf.bullet('recommend_tfidf(): Returns correct columns, handles empty input, respects top_n')
    pdf.bullet('recommend_countvec(): Same as above')
    pdf.bullet('recommend_word2vec(): Same + handles unknown skills gracefully')
    pdf.bullet('get_vector(): Returns zero vector for unknown words')
    
    pdf.ln(2)
    pdf.subsection_title('12.2 Integration Tests')
    pdf.bullet('End-to-end: Input skills -> model selection -> results displayed')
    pdf.bullet('Path resolution: Models correctly find data.csv from any CWD')
    
    pdf.ln(2)
    pdf.subsection_title('12.3 Performance Tests')
    pdf.bullet('Benchmark recommendation latency for 500, 1000, 5000 records')
    pdf.bullet('Memory usage profiling')
    
    # ============ SECTION 13: Roadmap ============
    pdf.add_page()
    pdf.chapter_title('13', 'Improvement Roadmap')
    
    pdf.subsection_title('Phase 1: Fix & Harden (Week 1)')
    phase1 = [
        'Fix path bug in all model files (BUG-1)',
        'Fix stipend double-wrapping (BUG-2)',
        'Show Similarity Score in results (BUG-3)',
        'Add @st.cache_resource for model caching',
        'Lazy-load models (remove module-level side effects)',
        'Add proper error handling',
    ]
    for item in phase1:
        pdf.bullet(item)
    
    pdf.ln(2)
    pdf.subsection_title('Phase 2: Enhance UX (Week 2)')
    phase2 = [
        'Add filter panel (location, mode, duration, stipend)',
        'Add skill autocomplete from dataset',
        'Add model comparison view',
        'Add export to CSV',
        'Improve README with proper markdown tables',
    ]
    for item in phase2:
        pdf.bullet(item)
    
    pdf.ln(2)
    pdf.subsection_title('Phase 3: Improve ML Quality (Week 3)')
    phase3 = [
        'Integrate pre-trained Word2Vec or Sentence Transformers',
        'Add skill normalization / taxonomy',
        'Add bigram support to TF-IDF',
        'Create proper train/test split for evaluation',
        'Document precision/recall metrics for each model',
    ]
    for item in phase3:
        pdf.bullet(item)
    
    pdf.ln(2)
    pdf.subsection_title('Phase 4: Scale & Integrate (Week 4+)')
    phase4 = [
        'Integrate Internshala / LinkedIn API for real data',
        'Add user authentication',
        'Add feedback mechanism',
        'Build analytics dashboard',
        'Deploy to cloud (AWS/GCP)',
    ]
    for item in phase4:
        pdf.bullet(item)
    
    # ============ SECTION 14: Success Metrics ============
    pdf.add_page()
    pdf.chapter_title('14', 'Success Metrics')
    
    cols = ['Metric', 'Current', 'Target']
    widths = [85, 50, 55]
    pdf.table_header(cols, widths)
    metrics = [
        ('Recommendation accuracy (user survey)', 'Unknown', '> 80%'),
        ('Response time', 'Unknown', '< 2s'),
        ('Dataset size', '500 records', '5,000+'),
        ('Models available', '3', '5+'),
        ('User satisfaction (NPS)', 'Unknown', '> 7/10'),
        ('Bug count (Critical)', '3', '0'),
        ('Test coverage', '0%', '> 70%'),
    ]
    for i, row in enumerate(metrics):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ SECTION 15: Appendix ============
    pdf.ln(8)
    pdf.chapter_title('15', 'Appendix')
    
    pdf.subsection_title('A. Proposed File Structure (After Fixes)')
    pdf.set_font('Courier', '', 8)
    pdf.set_text_color(40, 40, 40)
    structure = [
        'SIH25034_Internship_Recommendation/',
        '  app.py                    # Streamlit main app',
        '  requirements.txt          # Dependencies',
        '  PRD.md                    # This document',
        '  README.md                 # Documentation',
        '  data/',
        '    internships.csv         # Cleaned dataset',
        '  models/',
        '    __init__.py',
        '    base.py                 # Shared model logic',
        '    model_tfidf.py          # TF-IDF model',
        '    model_countvec.py       # CountVectorizer model',
        '    model_word2vec.py       # Word2Vec model',
        '  tests/',
        '    test_models.py          # Model unit tests',
        '    test_app.py             # Integration tests',
        '  utils/',
        '    preprocessing.py        # Skill normalization',
        '    data_loader.py          # Cached data loading',
    ]
    for line in structure:
        pdf.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 10)
    pdf.subsection_title('B. Dependency List')
    cols = ['Package', 'Purpose']
    widths = [50, 140]
    pdf.table_header(cols, widths)
    deps = [
        ('streamlit', 'Web UI'),
        ('pandas', 'Data manipulation'),
        ('scikit-learn', 'TF-IDF, CountVec, cosine similarity'),
        ('gensim', 'Word2Vec'),
        ('numpy', 'Numerical computation'),
        ('pytest', 'Testing (proposed)'),
        ('requests', 'API integration (proposed)'),
    ]
    for i, row in enumerate(deps):
        pdf.table_row(row, widths, fill=(i % 2 == 0))
    
    # ============ BACK COVER ============
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 10, 'Smart India Hackathon 2025', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'Problem Statement ID: PS25034', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, '"Connecting skills with opportunities - intelligently."', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, 'Developed by: Sushant Palkar & Nirbhay Moholkar', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Save
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == '__main__':
    md_path = os.path.join(os.path.dirname(__file__), 'PRD_Internship_Recommendation_System.md')
    output_path = os.path.join(os.path.dirname(__file__), 'PRD_Internship_Recommendation_System.pdf')
    
    md_content = parse_markdown(md_path)
    build_pdf(md_content, output_path)
