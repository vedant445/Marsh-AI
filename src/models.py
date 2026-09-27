from pydantic import BaseModel, Field
from typing import List, Optional


class PolicyPage(BaseModel):
    policy_id: str
    policy_name: str
    page_number: int
    text: str


class PolicyChunk(BaseModel):
    chunk_id: str
    policy_id: str
    policy_name: str
    page_number: int
    chunk_index: int
    text: str


class CompanyProfile(BaseModel):
    company_name: str

    industry: str
    company_size: str
    key_risks: List[str]

    facts: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class PolicyEvidence(BaseModel):
    policy_id: str
    policy_name: str
    page_number: int
    evidence: str


class PitchClaim(BaseModel):
    claim: str
    evidence: List[PolicyEvidence] = Field(default_factory=list)


class PitchSlide(BaseModel):
    slide_number: int
    title: str
    content: List[str]
    claims: List[PitchClaim] = Field(default_factory=list)


class PitchRecommendation(BaseModel):
    title: str
    description: str
    policy_name: str
    page_number: int
    evidence: str


class MarketingPitch(BaseModel):
    company_name: str
    recommendations: List[PitchRecommendation]