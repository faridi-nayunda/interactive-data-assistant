from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.nl2sql import generate_sql
from backend.services.queryExecutor import execute_query
from backend.services.summarizer import generate_summary
from backend.services.visualization import generate_chart_config
import logging

router = APIRouter()

# Pydantic model for input validation
class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query_endpoint(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Generate SQL
        sql = generate_sql(question)

        # Execute SQL
        results = execute_query(sql)

        # Generate summary
        summary = generate_summary(question, results)

        # Generate chart config
        chart = generate_chart_config(results)

        return {
            "sql": sql,
            "results": results,
            "summary": summary,
            "chart": chart
        }

    except Exception as e:
        logging.exception(f"Error processing question: {question}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )