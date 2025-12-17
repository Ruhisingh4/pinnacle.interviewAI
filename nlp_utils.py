# nlp_utils.py
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined fallback skills if resume extraction fails
DEFAULT_SKILLS = ["Python", "Java", "SQL", "Git", "Machine Learning"]

# Words to ignore
IGNORE_WORDS = {
    "Company", "University", "Education", "Experience", "Skills", "Student", "Internship", "Project"
}

def extract_skills(text):
    """
    Extract skills from resume text using spaCy NLP.
    Returns a list of up to 15 skills.
    """
    doc = nlp(text)
    skills = set()

    for token in doc:
        # Only nouns and proper nouns
        if token.pos_ in ["NOUN", "PROPN"]:
            word = token.text.strip()
            # Filter out short words, ignore words, and numeric tokens
            if len(word) > 2 and word.isalpha() and word not in IGNORE_WORDS:
                skills.add(word)

    # If extracted skills are too few, fallback to default skills
    if len(skills) < 5:
        skills = set(DEFAULT_SKILLS)

    # Return the first 15 unique skills
    return list(skills)[:15]
