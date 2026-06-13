from dataclasses import dataclass
from enum import StrEnum


class ModelRole(StrEnum):
    PLANNER = "planner"
    SUPERVISOR = "supervisor"
    RESEARCHER = "researcher"
    CODING = "coding"
    FINALIZER = "finalizer"   # reserved — finalizer is currently deterministic


@dataclass(frozen=True)
class ModelConfig:
    model: str
    temperature: float = 0.0
    timeout: int = 60
    max_retries: int = 3
    max_tokens: int = 2048
    tool_group: str | None = None
    base_url: str = "https://openrouter.ai/api/v1"


MODEL_REGISTRY: dict[ModelRole, ModelConfig] = {

    ModelRole.PLANNER: ModelConfig(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        timeout=60,
        max_tokens=800,
        max_retries=3,
    ),

    ModelRole.SUPERVISOR: ModelConfig(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        timeout=60,
        max_tokens=400,
        max_retries=3,
    ),

    ModelRole.RESEARCHER: ModelConfig(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        timeout=120,
        max_tokens=4096,
        tool_group="research",
    ),

    ModelRole.CODING: ModelConfig(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        timeout=120,
        max_tokens=8192,
        tool_group="coding",
    ),

    ModelRole.FINALIZER: ModelConfig(
        model="openai/gpt-oss-20b:free",
        temperature=0.0,
        timeout=45,
        max_tokens=800,
    ),
}
