import requests
from langchain_community.document_loaders import ArxivLoader
from io import BytesIO
import fitz
import time

class ArxivPDFLoader:
    def __init__(self, query, max_docs=300, top_k_results = 300, delay =3):
        self.query = query
        self.max_docs = max_docs
        self.top_k_results = top_k_results
        self.delay = delay
        self.loader = ArxivLoader(query=query, top_k_results=max_docs, load_max_docs=max_docs, load_all_available_meta=True)

    def get_pdf_urls(self):
        docs = self.loader.get_summaries_as_docs()
        pdf_urls = []
        for doc in docs:
            entry_id = doc.metadata.get("Entry ID")
            if entry_id:
                arxiv_id = entry_id.split("/")[-1]
                pdf_urls.append(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
        return pdf_urls

    def download_pdfs(self):
        docs = self.loader.get_summaries_as_docs()
        pdf_docs_with_meta = []

        for doc in docs:
            entry_id = doc.metadata.get("Entry ID")
            title = doc.metadata.get("Title", "untitled").replace(" ", "_").replace("/", "_")
            if entry_id:
                arxiv_id = entry_id.split("/")[-1]
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                try:
                    r = requests.get(pdf_url)
                    if r.status_code == 200:
                        pdf_stream = BytesIO(r.content)
                        pdf = fitz.open(stream=pdf_stream, filetype="pdf")
                        pdf_docs_with_meta.append({
                            "pdf": pdf,
                            "title": title,
                            "url": pdf_url,
                            "arxiv_id": arxiv_id
                        })
                    else:
                        print(f"Failed to download {pdf_url}")
                except Exception as e:
                    print(f"Error downloading {pdf_url}: {e}")

        return pdf_docs_with_meta

    def stream_pdfs(self):

        docs = self.loader.get_summaries_as_docs()

        for doc in docs:

            entry_id = doc.metadata.get("Entry ID")
            title = doc.metadata.get("Title", "untitled").replace(" ", "_").replace("/", "_")

            if not entry_id:
                continue

            arxiv_id = entry_id.split("/")[-1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            retries = 5

            for attempt in range(retries):

                try:
                    r = requests.get(pdf_url, timeout=60)

                    if r.status_code == 200:

                        pdf_stream = BytesIO(r.content)
                        pdf = fitz.open(stream=pdf_stream, filetype="pdf")

                        yield {
                            "pdf": pdf,
                            "title": title,
                            "url": pdf_url,
                            "arxiv_id": arxiv_id
                        }

                        # RATE LIMIT PROTECTION
                        time.sleep(self.delay)

                        break

                    elif r.status_code == 429:
                        print("arXiv rate limit hit. Waiting 30 seconds...")
                        time.sleep(30)

                    else:
                        print(f"Failed to download {pdf_url}")

                except Exception as e:

                    print(f"Retry {attempt+1} for {pdf_url}")
                    time.sleep(10)

                    if attempt == retries - 1:
                        print(f"Skipping {pdf_url}: {e}")
