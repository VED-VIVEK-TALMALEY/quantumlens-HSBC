from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from supabase import create_client
import os
import json

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def build_embedding_text(record):

    period_values = record.get(
        "period_values",
        []
    )

    values_text = ""

    for item in period_values:

        values_text += (
            f"Period {item['period_index']}: "
            f"{item['value']}\n"
        )

    if values_text == "":
        values_text = "Not Available"

    return f"""
Metric Name:
{record.get("metric_name")}

Abbreviation:
{record.get("abbreviation")}

Workbook:
{record.get("source_workbook")}

Sheet:
{record.get("sheet_name")}

Row Number:
{record.get("row_number")}

Values

{values_text}
"""

def generate_embeddings():

    rows = (
        supabase
        .table("metrics")
        .select("*")
        .execute()
        .data
    )

    embeddings = []

    for row in rows:

        text = build_embedding_text(row)

        vector = model.encode(
            text
        ).tolist()

        embeddings.append(

            {

                "metric_id":
                    row["metric_id"],

                "metric_name":
                    row["metric_name"],

                "abbreviation":
                    row["abbreviation"],

                "sheet_name":
                    row.get(
                        "sheet_name",
                        ""
                    ),

                "source_workbook":
                    row.get(
                        "source_workbook",
                        ""
                    ),

                "row_number":
                    row.get(
                        "row_number",
                        ""
                    ),

                "period_values":
row.get(
    "period_values",
    []
),

                "text":
                    text,

                "embedding":
                    vector

            }

        )

    with open(

        "embeddings.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            embeddings,

            f,

            indent=2

        )

    print(
        f"Generated {len(embeddings)} embeddings"
    )

    print(
        "Saved embeddings.json"
    )

    return embeddings


if __name__ == "__main__":

    generate_embeddings()