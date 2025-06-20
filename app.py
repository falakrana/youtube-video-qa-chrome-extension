import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

# Initialize components that can be reused across requests
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables=["context", "question"],
)

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

# Store vector stores in memory (for demo purposes)
# In production, consider using a proper cache or database
vector_stores = {}

def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        return transcript
    except TranscriptsDisabled:
        return None

def setup_chain_for_video(video_id):
    if video_id in vector_stores:
        return vector_stores[video_id]['chain']
    
    transcript = get_video_transcript(video_id)
    if not transcript:
        return None
    
    chunks = splitter.create_documents([transcript])
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    })
    
    chain = parallel_chain | prompt | llm | StrOutputParser()
    
    # Cache the chain and vector store
    vector_stores[video_id] = {
        'chain': chain,
        'vector_store': vector_store
    }
    
    return chain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    video_id = data.get('video_id')
    question = data.get('question')
    
    if not video_id or not question:
        return jsonify({'error': 'Missing video_id or question'}), 400
    
    chain = setup_chain_for_video(video_id)
    if not chain:
        return jsonify({'error': 'Could not retrieve transcript for this video'}), 400
    
    try:
        answer = chain.invoke(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)