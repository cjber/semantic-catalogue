@asset(compute_kind="OpenAI", deps=["pinecone_index"])
def search(context: AssetExecutionContext, openai: OpenAIResource):
    with openai.get_client(context) as client:
        embeddings = OpenAIEmbeddings(
            client=client.embeddings, model=cfg.datastore.embed_model
        )
        vectorstore = PineconeVectorStore(
            index_name=cfg.datastore.index_name, embedding=embeddings
        )

    # retriever = vectorstore.as_retriever()


from typing import Any, Dict

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class RunConfig(BaseModel):
    run_config: Dict[str, Any]


def launch_dagster_run(pipeline_name: str, run_config: dict, mode: str = "default"):
    url = "http://<your-dagster-instance>/graphql"
    headers = {
        "Content-Type": "application/json",
    }
    query = """
    mutation($pipelineName: String!, $runConfigData: RunConfigData, $mode: String!) {
        launchPipelineExecution(
            executionParams: {
                selector: {
                    pipelineName: $pipelineName
                },
                runConfigData: $runConfigData,
                mode: $mode
            }
        ) {
            __typename
            ... on LaunchPipelineRunSuccess {
                run {
                    runId
                }
            }
            ... on PythonError {
                message
                stack
            }
        }
    }
    """
    variables = {
        "pipelineName": pipeline_name,
        "runConfigData": run_config,
        "mode": mode,
    }
    response = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )
    return response.json()


@app.post("/trigger-asset")
def trigger_asset(pipeline_name: str, run_config: RunConfig, mode: str = "default"):
    try:
        result = launch_dagster_run(pipeline_name, run_config.run_config, mode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
