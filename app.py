import streamlit as st
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=5):
    """Fetches Google search results using requests (alternative method)."""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            link = g.find('a')['href']
            search_results.append(link)
        return search_results[:num_results]
    return []

def get_political_leaning(name):
    """Analyzes political leaning using Google search results."""
    keywords = ["Republican", "Democrat", "Conservative", "Liberal", "Right-wing", "Left-wing", "Pro-life", "Pro-choice"]
    scores = {"Republican": 1, "Conservative": 1, "Right-wing": 1, "Pro-life": 1,
              "Democrat": -1, "Liberal": -1, "Left-wing": -1, "Pro-choice": -1}

    total_score = 0
    confidence = 0
    searched_terms = []
    
    for keyword in keywords:
        query = f"{name} {keyword}"
        searched_terms.append(query)
        results = google_search(query, num_results=5)
        match_count = sum(1 for result in results if keyword.lower() in result.lower())
        total_score += match_count * scores[keyword]
        confidence += match_count

    if confidence > 0:
        leaning = total_score / confidence
    else:
        leaning = 0

    if leaning > 0.5:
        result = "Moderate Right"
    elif leaning > 1.5:
        result = "Far Right"
    elif leaning < -0.5:
        result = "Moderate Left"
    elif leaning < -1.5:
        result = "Far Left"
    else:
        result = "Center/Undetermined"

    return result, confidence, searched_terms

# Streamlit UI
st.title("Political Leaning Detector")
st.write("Enter a name or organization to analyze their political leaning based on Google search results.")

user_input = st.text_input("Enter a name or company")

if user_input:
    leaning, confidence, terms = get_political_leaning(user_input)
    st.subheader(f"Estimated Leaning: {leaning}")
    st.write(f"Confidence Score: {confidence}")
    st.write("Searched Google terms:")
    st.write(terms)
