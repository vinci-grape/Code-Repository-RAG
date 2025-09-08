# 🚀 Code Repository RAG System

<div align="center">

![Code Repository RAG](https://img.shields.io/badge/Code%20Repository-RAG-blue?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange?style=for-the-badge&logo=chainlink)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-purple?style=for-the-badge&logo=microsoft)

**An intelligent RAG system for code repository analysis with dual granularity processing**

[📖 Documentation](#-documentation) • [🚀 Quick Start](#-quick-start) • [🔧 Configuration](#-configuration) • [📊 Performance](#-performance-analysis)

</div>

---

## ✨ Overview

Welcome to **Code Repository RAG System** - an advanced Retrieval-Augmented Generation system specifically designed for analyzing and understanding code repositories. Built with modern AI technologies, this system provides intelligent question-answering capabilities about codebases with support for both **file-level** and **chunk-level** processing granularities.

### 🎯 Key Highlights

- 🎨 **Dual Processing Modes**: Choose between file-level summaries or detailed chunk analysis
- 🧠 **Intelligent Caching**: Smart caching system for optimal performance
- 🔍 **Multi-language Support**: Python, JavaScript, Java, C++, and more
- ⚡ **Azure OpenAI Integration**: Powered by GPT models via Azure
- 📈 **Performance Optimized**: Advanced caching and incremental processing
- 🛠️ **Modular Architecture**: Easy to extend and customize

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Code Parser   │───▶│   Document      │───▶│   Vector Store   │
│   (Multi-lang)  │    │   Processing    │    │   (Chroma)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Granularity   │    │   Embedding     │    │   QA System     │
│   Selection     │───▶│   Generation    │───▶│   (Azure OpenAI)│
│ (File/Chunk)    │    │ (HuggingFace)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
Code-Repository-RAG/
├── 📄 main.py                 # 🚀 Main entry point
├── 📄 requirements.txt        # 📦 Python dependencies
├── 📄 .env                    # ⚙️ Environment configuration
├── 📄 README.md              # 📖 This documentation
│
├── 📁 processed_repos/       # 💾 Cache & vector stores
│   └── 📁 {repo_hash}/       # Repository-specific data
│       ├── 📁 chunk/         # Chunk granularity data
│       └── 📁 file/          # File granularity data
│
└── 📁 repos/                 # 📚 Example repositories
    └── 📁 youtube-dl/        # Sample codebase for testing
```

## 🔥 Key Features

### 🎨 Dual Granularity Processing

#### 📄 File-Level Granularity
- **🎯 Purpose**: High-level code understanding
- **⚡ Process**: LLM-generated summaries for each file
- **💡 Benefits**: Contextual overview, reduced noise
- **🔍 Use Cases**: Architecture analysis, feature mapping
- **💾 Storage**: Summary + original content

#### 🧩 Chunk-Level Granularity
- **🎯 Purpose**: Detailed code analysis
- **⚡ Process**: Intelligent text chunking
- **💡 Benefits**: Precise code sections, better accuracy
- **🔍 Use Cases**: Bug fixes, implementation details
- **💾 Storage**: Individual code chunks with metadata

### 🚀 Performance Features

#### ⚡ Smart Caching System
- **📁 Repository Caching**: Avoid reprocessing existing repos
- **📝 Summary Caching**: Cache LLM-generated summaries
- **🔍 Vector Store Persistence**: Save processed embeddings
- **🔄 Incremental Updates**: Process only new/modified files

#### 🎯 Intelligent File Processing
- **🌐 Multi-language Support**: Python, JS, Java, C++, etc.
- **🚫 Smart Filtering**: Exclude caches, logs, dependencies
- **📊 Progress Tracking**: Real-time processing status
- **🛡️ Error Resilience**: Graceful handling of corrupted files

### 🤖 AI Integration

#### 🔷 Azure OpenAI Integration
- **🎨 GPT Models**: Access to latest GPT models
- **🔐 Token Authentication**: Secure CloudGPT integration
- **⚙️ Configurable Parameters**: Temperature, max tokens
- **🌐 API Flexibility**: Multiple API versions support

#### 🧠 Embedding Models
- **🏆 High-Quality Embeddings**: Sentence Transformers
- **⚡ GPU Acceleration**: CUDA support for faster processing
- **🔧 Model Flexibility**: Easy model switching
- **💾 Optimized Storage**: Efficient vector representations

## 🚀 Quick Start

### 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Code-Repository-RAG

# Install dependencies
pip install langchain langchain-community langchain-huggingface langchain-openai chromadb python-dotenv

# For Azure authentication (optional)
pip install azure-identity azure-identity-broker
```

### ⚙️ Configuration

Create a `.env` file in the project root:

```env
# 🔷 Azure OpenAI Configuration
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT=your-deployment-name
API_VERSION=your-api-version
```

### 🎮 Basic Usage

```python
from main import CodeRepositoryRAG

# Initialize with file-level granularity
print("🚀 Initializing Code Repository RAG System...")
rag_system = CodeRepositoryRAG(granularity="file")

# Process a repository
success = rag_system.run_full_pipeline("./repos/youtube-dl")

if success:
    print("✅ System ready! Ask questions about the codebase.")

    # Ask intelligent questions
    questions = [
        "What is the main functionality of this project?",
        "How does the download mechanism work?",
        "What are the key classes and their purposes?"
    ]

    for question in questions:
        print(f"\n❓ {question}")
        result = rag_system.ask_question(question)
        print(f"💡 {result['answer']}")
        print(f"📚 Sources: {len(result['context_sources'])} files")
```

### 🎯 Advanced Usage

```python
# Initialize with chunk-level granularity for detailed analysis
rag_detailed = CodeRepositoryRAG(granularity="chunk")

# Custom configuration for specific needs
rag_detailed.chunk_size = 300  # Smaller chunks
rag_detailed.chunk_overlap = 50  # More overlap

# Process repository
rag_detailed.run_full_pipeline("./repos/youtube-dl")

# Interactive Q&A session
print("🤖 Interactive Code Analysis Session")
print("Type 'quit' to exit")

while True:
    question = input("\n❓ Your question: ").strip()
    if question.lower() == 'quit':
        break

    result = rag_detailed.ask_question(question)

    print(f"\n💡 Answer: {result['answer']}")
    print(f"📚 Referenced files: {', '.join(result['context_sources'])}")
    print(f"📊 Total sources: {result['num_sources']}")
```

## 🔧 Configuration Guide

### 🎛️ System Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `granularity` | `"chunk"` | Processing mode: `"file"` or `"chunk"` |
| `chunk_size` | `500` | Text chunk size in characters |
| `chunk_overlap` | `200` | Overlap between chunks |
| `embedding_model` | `"all-MiniLM-L6-v2"` | HuggingFace embedding model |

### 🔧 Advanced Configuration

```python
# Create custom RAG instance
rag = CodeRepositoryRAG()

# Modify processing parameters
rag.granularity = "file"  # or "chunk"
rag.chunk_size = 1000     # Larger chunks for better context
rag.chunk_overlap = 100   # Less overlap for efficiency

# Change embedding model
rag.embedding_model = "sentence-transformers/all-mpnet-base-v2"

# Custom persist directory
rag.processed_repos_dir = "./my_custom_cache"

# Initialize and use
rag.run_full_pipeline("./target-repo")
```

## 📊 Performance Analysis

### ⚡ Processing Performance

| Granularity | First Run | Cached Run | Memory Usage |
|-------------|-----------|------------|--------------|
| File-Level | 🐌 Slower (LLM calls) | ⚡ Fast (cached summaries) | 💚 Lower |
| Chunk-Level | ⚡ Faster (no LLM) | ⚡ Fast (vector loading) | 💛 Higher |

### 📈 Use Case Recommendations

#### Choose **File Granularity** when:
- 🔍 Exploring new codebases
- 🏗️ Understanding architecture
- 📖 Getting high-level overviews
- 💾 Working with smaller projects

#### Choose **Chunk Granularity** when:
- 🐛 Debugging specific functions
- 🔧 Analyzing implementation details
- 📚 Working with large codebases
- 🎯 Needing precise code sections

## 🛠️ API Reference

### `CodeRepositoryRAG` Class

#### Constructor
```python
CodeRepositoryRAG(granularity="chunk")
```

**Parameters:**
- `granularity` (str): `"file"` or `"chunk"` processing mode

#### Core Methods

##### `run_full_pipeline(repo_path: str) -> bool`
🚀 **Complete processing pipeline**
```python
success = rag.run_full_pipeline("./my-repo")
```

##### `ask_question(question: str) -> Dict[str, Any]`
❓ **Intelligent question answering**
```python
result = rag.ask_question("How does authentication work?")
print(result["answer"])  # The answer
print(result["context_sources"])  # Source files
print(result["num_sources"])  # Number of sources
```

##### `load_existing_vectorstore(repo_path: str) -> bool`
💾 **Load cached vector store**
```python
loaded = rag.load_existing_vectorstore("./my-repo")
```

##### `setup_qa_system()`
🤖 **Initialize Azure OpenAI integration**
```python
rag.setup_qa_system()
```

## 🎨 Supported File Types

### ✅ Programming Languages
- 🐍 **Python**: `.py`
- 🌐 **JavaScript**: `.js`
- ☕ **Java**: `.java`
- ⚡ **C/C++**: `.c`, `.cpp`, `.h`
- 📄 **Documentation**: `.md`, `.txt`

### 🚫 Excluded Patterns
- 📁 `__pycache__/` - Python cache
- 📁 `.git/` - Git repository
- 📁 `node_modules/` - Dependencies
- 📄 `*.log` - Log files
- 📁 Various build artifacts

## 💾 Caching Strategy

### 🏗️ Repository Hashing
- **🎯 Purpose**: Unique repository identification
- **🔧 Method**: MD5 hash of normalized path
- **💡 Benefits**: Multi-repository support

### 📝 Summary Cache Structure
```
processed_repos/
└── {repo_hash}/
    └── {granularity}/
        └── summary_cache/
            ├── src/main.py.txt
            ├── utils/helpers.py.txt
            └── ...
```

### 🔍 Vector Store Cache Structure
```
processed_repos/
└── {repo_hash}/
    └── {granularity}/
        └── chroma_db/
            ├── chroma.sqlite3
            └── {uuid}/
                ├── data_level0.bin
                ├── header.bin
                └── ...
```

## 🔍 Example Queries

### 📚 Architecture Questions
```python
questions = [
    "What is the overall architecture of this system?",
    "What are the main components and their responsibilities?",
    "How do different modules interact with each other?",
    "What design patterns are used in this codebase?"
]
```

### 🐛 Implementation Questions
```python
questions = [
    "How does the authentication system work?",
    "Explain the data flow in the main processing pipeline",
    "What are the key algorithms used in this project?",
    "How are errors handled throughout the system?"
]
```

### 🔧 Code Quality Questions
```python
questions = [
    "What are the potential security vulnerabilities?",
    "Where can we improve error handling?",
    "What parts of the code need refactoring?",
    "Are there any performance bottlenecks?"
]
```

## 🛡️ Error Handling

### 📁 File Processing Errors
- **🔄 Graceful Skipping**: Continue with other files
- **📊 Detailed Logging**: Track problematic files
- **🔄 Fallback Mechanisms**: Use raw content when parsing fails

### 🌐 Network/API Errors
- **🔄 Retry Logic**: Automatic retry for transient failures
- **💾 Cache Utilization**: Prevent repeated failed requests
- **📊 Error Reporting**: Comprehensive error information

## ⚡ Optimization Tips

### 🚀 Performance Optimization
1. **📊 Choose Right Granularity**: File-level for exploration, chunk-level for details
2. **💾 Leverage Caching**: Reuse processed repositories
3. **🔧 Adjust Chunk Size**: Balance context vs. precision
4. **⚡ GPU Acceleration**: Use CUDA for embedding generation

### 💾 Memory Optimization
1. **🗂️ Selective Processing**: Process only relevant files
2. **🧹 Cache Cleanup**: Remove unused cached data
3. **📦 Chunk Size Tuning**: Smaller chunks for memory efficiency
4. **🔄 Incremental Updates**: Process only changes


## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **🎨 LangChain**: Core framework for LLM applications
- **🔷 Azure OpenAI**: Powerful language models
- **🤗 HuggingFace**: High-quality embedding models
- **💾 Chroma**: Efficient vector database
- **🐍 Python**: Amazing programming language

---

<div align="center">

**Made with ❤️ for developers, by developers**

⭐ **Star this repo** if you find it helpful!

[⬆️ Back to Top](#-code-repository-rag-system)

</div>