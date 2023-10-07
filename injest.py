import json
import re
from bs4 import BeautifulSoup
import joblib
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

def yaml_corrector(yaml_string):
    decoded_yaml = yaml_string.replace('\\n', '\n')
    formatted_yaml = re.sub(r':\s+', ': ', decoded_yaml)
    return formatted_yaml

def get_plain_text(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    plain_text = soup.get_text()
    return plain_text

def create_vector_db(data):
    docs = []
    for k, v in data.items():
        d = Document(page_content=v['content'] + v['code'], metadata=dict(id_=k, yaml = v['code']))
        docs.append(d)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    joblib.dump(db, "jfrog_pipe_vector_db.pkl")

def parse_html(html_content):
    # Using BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Finding all <pre> tags
    pre_tags = soup.find_all('pre')

    parts = []
    start_index = 0

    for pre in pre_tags:
        end_index = html_content.find(str(pre), start_index) + len(str(pre))
        parts.append(html_content[start_index:end_index])
        start_index = end_index

    # Adding the content after the last <pre> tag (if any)
    if start_index < len(html_content):
        parts.append(html_content[start_index:])
    
    print(f"Total {len(parts)} parts are created.")
    # Storing the content and <pre> tag's body in the desired dictionary format
    answer = {}

    for idx, part in enumerate(parts, 1):
        part_soup = BeautifulSoup(part, 'html.parser')
        
        # Extracting <pre> tag's body
        pre_content = part_soup.pre.string if part_soup.pre else None
        
        # Removing the <pre> tag to get the remaining content
        if part_soup.pre:
            part_soup.pre.decompose()
        
        answer[idx] = {
            'content': str(part_soup).strip(),
            'code': pre_content
        }
    
    return answer

def main():
    with open("scrapped_data.json", 'r') as fp:
        scrapped_data = json.load(fp)

    html_list = [x['topic']['text'] for x in scrapped_data['topics']]
    html = " \n \n ".join(html_list)

    parsed_data = parse_html(html)

    parsed_data_cleaned = {}
    for k, v in parsed_data.items():
        try:
            parsed_data_cleaned[k] = {
                'content' : get_plain_text(v['content']),
                'code' : yaml_corrector(v['code'])
            }
        except Exception as e:
            print(f"Error occured for topic {k} with exception {e}")

    create_vector_db(parsed_data_cleaned)
    
main()