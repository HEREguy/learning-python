"""
Pydantic data model for basic AI job replacement data.

Includes core identifying and risk metrics:
- job_id, job_role, industry, country, year
- automation_risk_percent
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class AIJobBasic(BaseModel):
    """Basic data model for AI job replacement dataset."""

    job_id: int = Field(..., description="Unique identifier for each job record")
    
    job_role: str = Field(
        ...,
        description="Job title/role name",
        min_length=1,
    )
    
    industry: Literal[
        "Technology",
        "Finance",
        "Healthcare",
        "Manufacturing",
        "Retail",
        "Education",
        "Transportation",
        "Energy",
    ] = Field(..., description="Industry sector")
    
    country: Literal[
        "USA",
        "Canada",
        "Brazil",
        "Australia",
        "Japan",
        "Singapore",
        "Germany",
    ] = Field(..., description="Country where the job exists")
    
    year: int = Field(
        ...,
        ge=2020,
        le=2026,
        description="Year of the data record",
    )
    
    automation_risk_percent: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage risk of job automation",
    )

    model_config = ConfigDict(
        title="AI Job Basic Data Model",
        json_schema_extra={
            "description": "Basic schema for AI job replacement dataset"
        },
    )


if __name__ == "__main__":
    # Example usage
    job = AIJobBasic(
        job_id=0,
        job_role="Data Analyst",
        industry="Technology",
        country="Canada",
        year=2021,
        automation_risk_percent=26.22,
    )
    print(job)
    print(job.model_dump())
