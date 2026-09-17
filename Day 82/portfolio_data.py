"""
Day 82: Developer Portfolio Project Showcase & Data Models
Curated showcase of Python, Web Development, and Data Science projects.
"""

PROFILE = {
    "name": "Tirth Patel",
    "title": "Full-Stack Python Engineer & Data Scientist",
    "tagline": "Architecting resilient web applications, data science pipelines, and intelligent automation systems.",
    "location": "India",
    "github": "https://github.com/Tirth3929v",
    "skills": [
        {"name": "Python 3.12", "level": "Expert", "category": "Core"},
        {"name": "Flask & Jinja2", "level": "Advanced", "category": "Web"},
        {"name": "SQLAlchemy 2.0 ORM", "level": "Advanced", "category": "Database"},
        {"name": "Pandas & NumPy", "level": "Expert", "category": "Data Science"},
        {"name": "Scikit-Learn (ML)", "level": "Advanced", "category": "Machine Learning"},
        {"name": "Matplotlib & Seaborn", "level": "Advanced", "category": "Data Viz"},
        {"name": "Plotly Express", "level": "Advanced", "category": "Data Viz"},
        {"name": "RESTful API Design", "level": "Expert", "category": "Web"},
        {"name": "Git & Version Control", "level": "Expert", "category": "DevOps"},
        {"name": "HTML5 / CSS3 / Bootstrap", "level": "Advanced", "category": "Frontend"},
    ],
    "projects": [
        {
            "id": 1,
            "title": "Clean Blog with Relational DB & RBAC",
            "category": "Web & Architecture",
            "day": "Day 69",
            "description": "Production-grade blog engine featuring bidirectional One-to-Many ORM models, @admin_only decorator security, and threaded discussion comments.",
            "tech": ["Flask", "SQLAlchemy 2.0", "Flask-Login", "WTForms", "Bootstrap 5"],
            "github_path": "Day 69/main.py"
        },
        {
            "id": 2,
            "title": "Boston Housing Multivariable ML Predictor",
            "category": "Machine Learning",
            "day": "Day 80",
            "description": "Multivariable Ordinary Least Squares regression model predicting residential home valuations across 13 economic indicators with R² = 0.81.",
            "tech": ["Scikit-Learn", "Pandas", "NumPy", "Seaborn"],
            "github_path": "Day 80/main.py"
        },
        {
            "id": 3,
            "title": "Google Play Store Interactive Analytics Dashboard",
            "category": "Data Science",
            "day": "Day 75",
            "description": "Comprehensive exploratory data analytics dashboard featuring interactive 4D bubble plots, category download volumes, and revenue simulations.",
            "tech": ["Plotly Express", "Pandas", "HTML5"],
            "github_path": "Day 75/main.py"
        },
        {
            "id": 4,
            "title": "RESTful API Microservice Architecture",
            "category": "Web & Architecture",
            "day": "Day 66",
            "description": "Full-featured RESTful JSON microservice with complete HTTP verbs (GET, POST, PATCH, DELETE) and secret API key header authentication.",
            "tech": ["Flask", "SQLite", "REST API", "JSON"],
            "github_path": "Day 66/main.py"
        },
        {
            "id": 5,
            "title": "Dr. Semmelweis Clinical Hypothesis Testing",
            "category": "Data Science",
            "day": "Day 79",
            "description": "Longitudinal epidemiological study and Welch's two-sample t-test proving handwashing reduced maternal sepsis deaths by 75%+.",
            "tech": ["SciPy Stats", "Matplotlib", "Pandas"],
            "github_path": "Day 79/main.py"
        },
        {
            "id": 6,
            "title": "International Morse Code Audio Synthesizer",
            "category": "Automation & Tools",
            "day": "Day 81",
            "description": "Pure Python telecommunication encoder and 800Hz PCM sine wave audio generator without external dependencies.",
            "tech": ["Python", "PCM Audio", "Wave Binary", "Math"],
            "github_path": "Day 81/main.py"
        }
    ]
}
