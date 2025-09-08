import os
import glob
import hashlib
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from cloudgpt_aoai import get_openai_token_provider
load_dotenv()


class CodeRepositoryRAG:
    """Simplified Code Repository RAG System"""
    
    def __init__(self, granularity="chunk"):
        """Initialize the system with specified granularity

        Args:
            granularity (str): Processing granularity - "chunk" or "file"
        """
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None

        # Configuration
        self.granularity = granularity  # "chunk" or "file"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.chunk_size = 500
        self.chunk_overlap = 200
        self.processed_repos_dir = "./processed_repos"

        print(f"RAG system initialized with {granularity} granularity")

    def _get_repo_hash(self, repo_path: str) -> str:
        """Generate a unique hash for the repository path"""
        # Normalize path to handle different path separators
        normalized_path = os.path.abspath(repo_path).replace(os.sep, '/')
        return hashlib.md5(normalized_path.encode('utf-8')).hexdigest()[:8]

    def _get_repo_persist_dir(self, repo_path: str) -> str:
        """Get the persist directory for a specific repository"""
        repo_hash = self._get_repo_hash(repo_path)
        return os.path.join(self.processed_repos_dir, repo_hash, self.granularity , "chroma_db")

    def _is_repo_processed(self, repo_path: str) -> bool:
        """Check if repository has already been processed"""
        persist_dir = self._get_repo_persist_dir(repo_path)
        return os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3"))

    def load_code_files(self, repo_path: str) -> List[str]:
        """Load code files"""
        print(f"Loading code files: {repo_path}")
        
        # Supported code file extensions
        code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.txt', '.md']
        
        documents = []
        for extension in code_extensions:
            pattern = os.path.join(repo_path, f"**/*{extension}")
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                # Skip some unwanted files
                skip_patterns = ['__pycache__', '.git', 'node_modules', '.log']
                if any(pattern in file_path for pattern in skip_patterns):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if content.strip():  # Only process non-empty files
                            documents.append({
                                'content': content,
                                'source': file_path,
                                'extension': extension
                            })
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
                    continue
        
        print(f"Loaded {len(documents)} code files")
        return documents

    def process_documents(self, documents: List[Dict], repo_path: str) -> List[Dict]:
        """Process documents according to specified granularity

        Args:
            documents: List of document dictionaries
            repo_path: Path to the repository root

        Returns:
            List of processed document chunks/files
        """
        print(f"Processing documents with {self.granularity} granularity...")

        if self.granularity == "file":
            # File-level processing: summarize each file and store both summary and original content
            processed_docs = []
            for doc in documents:
                print(f"Summarizing file: {doc['source']}")
                # Generate summary using LLM
                summary_text = self.summarize_file_content(doc['content'], doc['source'], repo_path)

                processed_doc = {
                    'content': summary_text,  # Summary text for embedding
                    'source': doc['source'],
                    'extension': doc['extension'],
                    'chunk_id': 0,  # Single chunk per file
                    'original_content': doc['content']  # Store original file content
                }
                processed_docs.append(processed_doc)

            print(f"Processed {len(processed_docs)} files with LLM summaries")
            return processed_docs

        else:  # chunk granularity
            return self.chunk_documents(documents)

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Chunk documents"""
        print("Chunking documents...")
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        all_chunks = []
        for doc in documents:
            # Split text
            chunks = text_splitter.split_text(doc['content'])
            
            # Add metadata to each chunk
            for i, chunk in enumerate(chunks):
                chunk_doc = {
                    'content': chunk,
                    'source': doc['source'],
                    'extension': doc['extension'],
                    'chunk_id': i
                }
                all_chunks.append(chunk_doc)
        
        print(f"Documents split into {len(all_chunks)} chunks")
        return all_chunks

    def _get_summary_cache_path(self, file_path: str, repo_path: str) -> str:
        """Get the cache file path for a given file using project hash structure"""
        # Get project hash for directory structure
        repo_hash = self._get_repo_hash(repo_path)

        # Create project-specific cache directory
        project_cache_dir = os.path.join(self.processed_repos_dir, repo_hash, self.granularity, "summary_cache")

        # Use relative path from repo root, keeping directory structure
        rel_path = os.path.relpath(file_path, repo_path)

        # Create the full path with .txt extension
        cache_path = os.path.join(project_cache_dir, rel_path + '.txt')

        return cache_path

    def load_summary(self, file_path: str, repo_path: str) -> str:
        """Load summary from cache if it exists"""
        cache_path = self._get_summary_cache_path(file_path, repo_path)

        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Failed to load summary from cache: {e}")
                return None
        return None

    def save_summary(self, file_path: str, repo_path: str, summary: str):
        """Save summary to cache"""
        cache_path = self._get_summary_cache_path(file_path, repo_path)

        # Ensure cache directory exists
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                f.write(summary)
        except Exception as e:
            print(f"Failed to save summary to cache: {e}")

    def summarize_file_content(self, file_content: str, file_path: str, repo_path: str) -> str:
        """Summarize file content using LLM with caching

        Args:
            file_content: The content of the file to summarize
            file_path: Path to the file for context
            repo_path: Path to the repository root

        Returns:
            Summary text of the file content
        """
        # Check if summary already exists in cache
        cached_summary = self.load_summary(file_path, repo_path)
        if cached_summary:
            print(f"Using cached summary for {file_path}")
            return cached_summary

        print(f"Generating new summary for {file_path}")
        if self.llm is None:
            self.setup_qa_system()

        # Create summary prompt
        summary_prompt = f"""
        Please provide a concise but comprehensive summary of the following code file.
        Focus on the main functionality, key classes/functions, and important implementation details.

        File: {file_path}

        Code:
        {file_content}

        Summary:
        """

        try:
            response = self.llm.invoke(summary_prompt)
            summary = response.content.strip()
            # Save summary to cache
            self.save_summary(file_path, repo_path, summary)
            return summary
        except Exception as e:
            print(f"Failed to summarize file {file_path}: {e}")
            # Fallback to first 500 characters if LLM fails
            fallback_summary = file_content[:500] + "..." if len(file_content) > 500 else file_content
            # Save fallback summary to cache as well
            self.save_summary(file_path, repo_path, fallback_summary)
            return fallback_summary

    def build_vectorstore(self, processed_docs: List[Dict], repo_path: str):
        """Build vector store from processed documents

        Args:
            processed_docs: List of processed document chunks/files
            repo_path: Path to the repository
        """
        print("Building vector store...")

        # Get repository-specific persist directory
        persist_dir = self._get_repo_persist_dir(repo_path)

        # Initialize embedding model for M2 chip
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cuda'}  # Use Metal Performance Shaders for M2
        )

        # Prepare document format for Chroma
        texts = [doc['content'] for doc in processed_docs]
        metadatas = [
            {
                'source': doc['source'],
                'extension': doc['extension'],
                'chunk_id': doc['chunk_id'],
                'original_content': doc.get('original_content', doc['content'])  # Store original content in metadata
            }
            for doc in processed_docs
        ]

        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=persist_dir
        )

        print("Vector store built successfully")

    def load_existing_vectorstore(self, repo_path: str) -> bool:
        """Load existing vector store for a repository"""
        print(f"Loading existing vector store for repository: {repo_path}")

        if not self._is_repo_processed(repo_path):
            print("No existing vector store found")
            return False

        try:
            persist_dir = self._get_repo_persist_dir(repo_path)

            # Initialize embedding model (same as used for building)
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cuda'} 
            )

            # Load existing vector store
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )

            print("Existing vector store loaded successfully")
            return True

        except Exception as e:
            print(f"Failed to load existing vector store: {e}")
            return False

    def setup_qa_system(self):
        """Setup QA system with Azure OpenAI"""
        print("Setting up QA system with Azure OpenAI...")

        token_provider = get_openai_token_provider()

        self.llm = AzureChatOpenAI(
            azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
            azure_deployment=os.environ.get("AZURE_DEPLOYMENT"),
            api_version=os.environ.get("API_VERSION"),
            azure_ad_token_provider=token_provider
        )

        # Create prompt template
        template = """
        You are a code analysis expert. Answer questions based on the following code context.

        Code Context:
        {context}

        Question: {question}

        Please provide a detailed answer including:
        1. Direct answer to the question
        2. Relevant code examples
        3. Implementation details
        4. Improvement suggestions (if applicable)

        Answer:
        """

        self.prompt = ChatPromptTemplate.from_template(template)
        print("Azure OpenAI QA system setup complete")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question"""
        if self.vectorstore is None or self.llm is None:
            return {"error": "System not fully initialized"}
        
        print(f"Processing question: {question}")
        
        # Retrieve relevant documents
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        relevant_docs = retriever.get_relevant_documents(question)

        # Merge context - use original content for files, page_content for chunks
        context_parts = []
        for doc in relevant_docs:
            if self.granularity == "file" and 'original_content' in doc.metadata:
                # For file granularity, use the original file content
                context_parts.append(doc.metadata['original_content'])
            else:
                # For chunk granularity, use the chunk content
                context_parts.append(doc.page_content)
        context = "\n\n".join(context_parts)

        # Generate answer
        messages = self.prompt.format_messages(
            context=context,
            question=question
        )
        
        response = self.llm(messages)
        answer = response.content
        
        # Return results
        result = {
            "question": question,
            "answer": answer,
            "context_sources": [doc.metadata.get('source', 'Unknown') for doc in relevant_docs],
            "num_sources": len(relevant_docs)
        }
        
        print("Question processed successfully")
        return result
    
    def run_full_pipeline(self, repo_path: str):
        """Run complete pipeline"""
        print("Starting complete RAG pipeline...")

        # Check if repository has already been processed
        repo_hash = self._get_repo_hash(repo_path)
        persist_dir = self._get_repo_persist_dir(repo_path)
        print(f"Repository hash: {repo_hash}")
        print(f"Persist directory: {persist_dir}")

        if self._is_repo_processed(repo_path):
            print("Repository already processed, loading existing data...")
            # Try to load existing vector store
            if self.load_existing_vectorstore(repo_path):
                # Setup QA system
                self.setup_qa_system()
                print("RAG system ready! (loaded from cache)")
                return True
            else:
                print("Failed to load existing data, processing from scratch...")

        # Repository not processed yet, run full pipeline
        print("Processing repository from scratch...")

        # 1. Load code files
        documents = self.load_code_files(repo_path)
        if not documents:
            print("No code files found")
            return False

        # 2. Process documents according to granularity
        processed_docs = self.process_documents(documents, repo_path)

        # 3. Build vector store
        self.build_vectorstore(processed_docs, repo_path)

        # 4. Setup QA system
        self.setup_qa_system()

        print("RAG system ready! (processed from scratch)")
        return True


def demo():
    """Demo function with both granularity modes"""
    print("=== Code Repository RAG System Demo ===\n")

    example_path = "./repos/youtube-dl"
    question = "What is the main functionality of this project?"

    # Test file granularity
    print("Testing FILE granularity:")
    print("-" * 40)
    rag_file = CodeRepositoryRAG(granularity="file")
    success_file = rag_file.run_full_pipeline(example_path)

    if success_file:
        # Test with file granularity
        result = rag_file.ask_question(question)
        if "error" not in result:
            print(f"File mode - Used {result['num_sources']} code files as context")
            print(f"Answer: {result['answer']}")
        else:
            print(f"File mode error: {result['error']}")
    else:
        print("File mode initialization failed")

    print("\nDemo completed!")


if __name__ == "__main__":
    demo()
