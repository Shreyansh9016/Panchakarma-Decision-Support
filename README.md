<h1>Panchakarma Decision Support System</h1>

<p>
An evidence-based clinical decision support application for Panchakarma therapy
recommendations using Retrieval-Augmented Generation (RAG) over classical
Ayurveda texts.
</p>

<p>
The system analyzes patient details and symptoms to generate therapy suggestions
grounded in authoritative literature.
</p>

<hr>

<h2>Features</h2>

<ul>
  <li>Evidence-based recommendations using classical Ayurveda sources</li>
  <li>Retrieval-Augmented Generation (RAG) architecture</li>
  <li>FAISS vector database for semantic search</li>
  <li>Groq LLM integration for fast inference</li>
  <li>Explainable outputs with supporting passages</li>
  <li>Streamlit web interface</li>
</ul>

<hr>

<h2>How to Use the Application</h2>

<ol>
  <li>Enter patient information:
    <ul>
      <li>Age</li>
      <li>Gender</li>
      <li>Prakriti (Vata / Pitta / Kapha)</li>
      <li>Medical history</li>
      <li>Symptoms</li>
    </ul>
  </li>
  <li>Click <strong>Submit</strong></li>
  <li>Review the recommendation and supporting evidence</li>
</ol>

<hr>

<h1>Running the Application LOCALLY</h1>

<h2>Prerequisites</h2>

<ul>
  <li>Python 3.10 or later recommended</li>
  <li>Git installed</li>
</ul>

<h2>1. Clone the Repository</h2>

<pre><code>git clone https://github.com/YOUR_USERNAME/Panchakarma-Decision-Support.git
cd Panchakarma-Decision-Support
</code></pre>

<h2>2. Create Virtual Environment</h2>

<p><strong>Windows (CMD)</strong></p>

<pre><code>python -m venv rag_env
</code></pre>

<p><strong>macOS / Linux</strong></p>

<pre><code>python3 -m venv rag_env
</code></pre>

<h2>3. Activate Virtual Environment</h2>

<p><strong>Windows (CMD)</strong></p>

<pre><code>rag_env\Scripts\activate
</code></pre>

<p><strong>Windows (PowerShell)</strong></p>

<pre><code>rag_env\Scripts\Activate.ps1
</code></pre>

<p><strong>macOS / Linux</strong></p>

<pre><code>source rag_env/bin/activate
</code></pre>

<p>After activation, the terminal should display something like:</p>

<pre><code>(rag_env)
</code></pre>

<h2>4. Install Dependencies</h2>

<pre><code>pip install -r requirements.txt
</code></pre>

<h2>5. Add Groq API Key</h2>

<p>Create a file named <code>.env</code> in the project root:</p>

<pre><code>GROQ_API_KEY=your_api_key_here
</code></pre>

<h2>6. Run the Application</h2>

<pre><code>streamlit run app.py
</code></pre>

<p>The application will open in your browser.</p>

<h3>Notes (Local Run)</h3>

<ul>
  <li>The vector database is built automatically from the included PDFs</li>
  <li>First run may take several minutes</li>
  <li>Subsequent runs are much faster</li>
</ul>

<hr>

<h1>Running the Application ONLINE (Streamlit Cloud)</h1>

<h2>1. Open the deployed app link</h2>

<p>If the application is deployed, simply open the URL in your browser.</p>

<h2>2. Add API Key in Streamlit Secrets</h2>

<p>If required, go to:</p>

<p><strong>App → Settings → Secrets</strong></p>

<p>Add:</p>

<pre><code>GROQ_API_KEY = "your_api_key_here"
</code></pre>

<h2>3. Start the Application</h2>

<ul>
  <li>Streamlit Cloud puts inactive apps to sleep</li>
  <li>If the app has been idle, it may not start immediately</li>
  <li>A message or button may appear to wake the app</li>
  <li>Click it to start</li>
</ul>

<h3>Important — Initial Loading Time</h3>

<ul>
  <li>First startup may take <strong>1–3 minutes</strong></li>
  <li>The server environment is fresh</li>
  <li>The knowledge base may rebuild</li>
  <li>Embeddings are generated during initialization</li>
</ul>

<p>After initialization, the app runs normally.</p>

<hr>

<h2>Project Structure</h2>

<pre><code>Panchakarma-Decision-Support/
│
├── app.py                 # Streamlit application
├── build_db.py            # Builds FAISS vector database
├── rag_pipeline.py        # Retrieval + LLM pipeline
├── requirements.txt       # Dependencies
├── .env.example           # Example environment variables
├── .gitignore
│
├── data/
│   └── classical/         # Source PDFs used as knowledge base
│
└── vector_db/             # Generated database (not tracked)
</code></pre>

<hr>

<h2>Disclaimer</h2>

<p>
This system generates recommendations based on textual sources and is intended
for academic and educational purposes only.
</p>

<p>
<strong>It is NOT a substitute for professional medical advice,
diagnosis, or treatment.</strong>
</p>

<p>Always consult a qualified healthcare professional.</p>

<hr>

