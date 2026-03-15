from flask import Flask, request, jsonify
from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)


load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
index_name = "class12-english"

# Connect to the existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name, 
    embedding=embeddings
)

# Set up the retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize the Google Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5,
    max_output_tokens=512
)

# Create the QA Chain with a default prompt template
default_prompt_template = """Use the following context to answer the question. If you don't know the answer, say so.

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(default_prompt_template)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)   

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the QA API. Use the /predict endpoint to get answers."})


@app.route('/predict', methods=['POST'])
def query():
    """Process query and return QA response."""
    try:
        # Handle JSON and form data
        if request.is_json:
            data = request.get_json()
            user_query = data.get('query')
        else:
            user_query = request.form.get('query')

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Execute the chain
        response = qa_chain.invoke({'query': user_query})

        # Extract the raw result from the chain
        raw_result = response["result"]
        source_docs = [doc.page_content for doc in response.get("source_documents", [])]

        # Clean markdown code blocks if present
        clean_result = raw_result.replace("```json", "").replace("```", "").strip()

        # Try to parse as JSON, fallback to string
        try:
            result_data = json.loads(clean_result)
        except json.JSONDecodeError:
            result_data = {"message": clean_result}

        return jsonify({
            "result": result_data,
            "success": True,
            "source_documents": source_docs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)