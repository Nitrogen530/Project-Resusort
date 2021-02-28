import pdfplumber
import nltk
import re
import subprocess
import requests
import os

# before you run please install the above packages

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

'''SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'English',
    'Optimization',
    'Research',
    'Statistical Analysis'
]'''

educational_institutes_keywrds = [
    'school',
    'college',
    'university',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
]


SKILLS_DB = []
print("\n")
print("Enter the skills below or press q to quit")
while True:
    skill = str(input("> "))
    if skill.lower() == 'q':
        break
    else:
        SKILLS_DB.append(skill.lower())

print("Skill Database: ", SKILLS_DB)


def extract_text_from_pdf(pdffileloc):
    with pdfplumber.open(str(pdffileloc)) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    return text

"""

************************IMPORTANT************************

"""
# the below method requires subscription
# I am broke af so I'm not using the below method
# GO TO THE FOLLOWING WEBISITE AND CREATE A FREE ACCOUNT
# IN THE SEARCH BAR search for 'SKILLS API' (NOTE: its skills not skill)
# https://promptapi.com/marketplace

'''
def skill_exists(skill):
    url = f'https://api.promptapi.com/skills?q={skill}&count=1'
    headers = {
        "apikey": "YOUR API KEY"
    }
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    if response.status_code == 200:
        return len(result) > 0 and result[0].lower() == skill.lower()
    raise Exception(result.get('message'))



def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if skill_exists(token.lower()):
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if skill_exists(ngram.lower()):
            found_skills.add(ngram)

    return found_skills
'''


def extract_names(txt):  # not so accurate though
    person_names = []

    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))

    return person_names


def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)

    if phone:
        number = ''.join(phone[0])

        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None


def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_education(input_text):  # not so accurate though
    organizations = []

    # first get all the organization names using nltk
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == ('ORGANIZATION' or 'FACILITY'):
                organizations.append(' '.join(c[0] for c in chunk.leaves()))

    # we search for each bigram and trigram for reserved words
    # (college, university etc...)
    education = set()
    # print(organizations)
    for org in organizations:
        for word in educational_institutes_keywrds:
            if org.lower().find(word) >= 0:
                education.add(org)

    return education


def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(
        map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)

    return found_skills

# location of all resumes, change accordingly
common_path = "E:/Full Stack Dev/Resusort/code/"
listOfFiles = [f for f in os.listdir(common_path) if os.path.isfile(f)]

if __name__ == '__main__':
    print("\n")
    print("\t\t\t\t\t\t\tDetails of Candidate")
    counter = 1
    for resumes in listOfFiles:

        if resumes.endswith(".pdf") or resumes.endswith(".docx"):
            print("Candidate ", counter)
            current_res = common_path + str(resumes)
            text = extract_text_from_pdf(current_res)
            names = extract_names(text)
            phone_number = extract_phone_number(text)
            emails = extract_emails(text)
            skills = extract_skills(text)
            education_information = extract_education(text)

            if names:
                print("Name: ", names[0])
            if phone_number:
                print("Phone Number: ", phone_number)
            if emails:
                print("Email Address: ", emails[0])
            if skills:
                print("Skills: ", skills)
            if education_information:
                print("Educational Details: ", education_information)
            counter += 1

            margin = (len(skills) / len(SKILLS_DB)) * 100
            if margin >= 70:
                print(f"\t\tCurrent candidate {resumes} selected")
            print(round(margin, 2))
            print("\n")
