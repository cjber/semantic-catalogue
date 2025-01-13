import ast

import polars as pl


def parse_structs(s):
    return ast.literal_eval(s)


df = pl.read_csv("./dataset_683ed2dd-1f9c-4f69-b41b-3bfe58bfdd0c.csv").drop_nulls(
    "input_query"
)

item = {"query": [], "documents": []}
for row in df.rows(named=True):
    if row["output_documents"] and row["input_query"]:
        output_documents = ast.literal_eval(row["output_documents"])
        for doc in output_documents:
            item["query"].append(row["input_query"])
            item["documents"].append(doc["metadata"])

df = pl.DataFrame(item).unnest("documents").filter(pl.col("source") == "CDRC")

df.write_csv("semantic-search-outputs-spelling.csv")
