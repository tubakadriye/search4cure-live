#import fitz  # PyMuPDF
#import camelot
#from io import BytesIO
#from PIL import Image

from backend.utils.gcs_utils import upload_bytes_to_gcs
import json


def extract_tables_from_pdf(pdf):

    tables = []

    for page_index, page in enumerate(pdf):
        try:
            page_tables = page.find_tables()

            for i, table in enumerate(page_tables.tables):
                df = table.to_pandas()

                json_bytes = json.dumps(df.to_dict()).encode()

                gcs_key = upload_bytes_to_gcs(
                    json_bytes,
                    "tables",
                    "application/json"
                )

                tables.append({
                    "page_number": page_index + 1,
                    "table_index": i,
                    "dataframe": df,
                    "gcs_key": gcs_key,
                })

        except Exception:
            pass

    return tables


# def extract_tables_from_pdf(pdf):
#     """
#     Extract tables from PDF pages. Returns a list of dicts with page_number, table_data, and optionally CSV bytes.
#     """
#     temp_path = "/tmp/temp_paper.pdf"
#     pdf.save(temp_path)

#     tables = camelot.read_pdf(temp_path, pages="all")

#     results = []

#     for i, table in enumerate(tables):

#         results.append({
#             "page_number": table.page,
#             "table_index": i,
#             "dataframe": table.df
#         })

#     return results

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
