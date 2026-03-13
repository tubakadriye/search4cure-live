#import fitz  # PyMuPDF
import camelot
#from io import BytesIO
#from PIL import Image

def extract_tables_from_pdf(pdf):
    """
    Extract tables from PDF pages. Returns a list of dicts with page_number, table_data, and optionally CSV bytes.
    """
    temp_path = "/tmp/temp_paper.pdf"
    pdf.save(temp_path)

    tables = camelot.read_pdf(temp_path, pages="all")

    results = []

    for i, table in enumerate(tables):

        results.append({
            "page_number": table.page,
            "table_index": i,
            "dataframe": table.df
        })

    return results

    # for page_index in range(len(pdf)):
    #     page = pdf[page_index]

    #     # Try Camelot (works if PDF has embedded table structures)
    #     try:
    #         # Camelot requires a file, so save page temporarily
    #         temp_path = f"/tmp/page_{page_index}.pdf"
    #         pdf[page_index].write(temp_path)
    #         camelot_tables = camelot.read_pdf(temp_path, flavor='stream')  # or 'lattice'

    #         for t_idx, table in enumerate(camelot_tables):
    #             tables.append({
    #                 "page_number": page_index,
    #                 "table_index": t_idx,
    #                 "dataframe": table.df,  # pandas dataframe
    #                 "csv_bytes": table.csv.encode('utf-8')
    #             })

    #     except Exception as e:
    #         print(f"[!] Table extraction failed on page {page_index}: {e}")

    # return tables
