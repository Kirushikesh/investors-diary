# src/app.py

import uvicorn
from pydantic import BaseModel,  Field
from typing import Any, List, Union

from src.core.graph_builder import main_graph

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from langserve import add_routes
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage

app = FastAPI(
    title="Investors Diary",
    version="1.0",
    description="An API server to register stock purchases, analysis records, research stocks and much more..."
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# add routes
add_routes(
   app,
    main_graph,
    path="/diary",
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)