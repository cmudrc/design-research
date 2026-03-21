"""Thin wrappers for primary agent execution and coordination APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._lazy import module_dir, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = {
    "DirectLLMCall": "design_research_agents:DirectLLMCall",
    "MultiStepAgent": "design_research_agents:MultiStepAgent",
    "Toolbox": "design_research_agents:Toolbox",
    "Workflow": "design_research_agents:Workflow",
    "ModelStep": "design_research_agents:ModelStep",
    "LLMRequest": "design_research_agents:LLMRequest",
    "LLMMessage": "design_research_agents:LLMMessage",
    "LlamaCppServerLLMClient": "design_research_agents:LlamaCppServerLLMClient",
    "OpenAIServiceLLMClient": "design_research_agents:OpenAIServiceLLMClient",
    "OllamaLLMClient": "design_research_agents:OllamaLLMClient",
    "CompiledExecution": "design_research_agents:CompiledExecution",
    "ModelSelector": "design_research_agents:ModelSelector",
    "Tracer": "design_research_agents:Tracer",
    "TwoSpeakerConversationPattern": "design_research_agents:TwoSpeakerConversationPattern",
    "DebatePattern": "design_research_agents:DebatePattern",
    "PlanExecutePattern": "design_research_agents:PlanExecutePattern",
    "ProposeCriticPattern": "design_research_agents:ProposeCriticPattern",
    "RouterDelegatePattern": "design_research_agents:RouterDelegatePattern",
    "RoundBasedCoordinationPattern": "design_research_agents:RoundBasedCoordinationPattern",
    "BlackboardPattern": "design_research_agents:BlackboardPattern",
    "BeamSearchPattern": "design_research_agents:BeamSearchPattern",
    "RAGPattern": "design_research_agents:RAGPattern",
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_agents``."""
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)


if TYPE_CHECKING:
    from design_research_agents import BeamSearchPattern as BeamSearchPattern
    from design_research_agents import BlackboardPattern as BlackboardPattern
    from design_research_agents import CompiledExecution as CompiledExecution
    from design_research_agents import DebatePattern as DebatePattern
    from design_research_agents import DirectLLMCall as DirectLLMCall
    from design_research_agents import LlamaCppServerLLMClient as LlamaCppServerLLMClient
    from design_research_agents import LLMMessage as LLMMessage
    from design_research_agents import LLMRequest as LLMRequest
    from design_research_agents import ModelSelector as ModelSelector
    from design_research_agents import ModelStep as ModelStep
    from design_research_agents import MultiStepAgent as MultiStepAgent
    from design_research_agents import OllamaLLMClient as OllamaLLMClient
    from design_research_agents import OpenAIServiceLLMClient as OpenAIServiceLLMClient
    from design_research_agents import PlanExecutePattern as PlanExecutePattern
    from design_research_agents import ProposeCriticPattern as ProposeCriticPattern
    from design_research_agents import RAGPattern as RAGPattern
    from design_research_agents import (
        RoundBasedCoordinationPattern as RoundBasedCoordinationPattern,
    )
    from design_research_agents import RouterDelegatePattern as RouterDelegatePattern
    from design_research_agents import Toolbox as Toolbox
    from design_research_agents import Tracer as Tracer
    from design_research_agents import (
        TwoSpeakerConversationPattern as TwoSpeakerConversationPattern,
    )
    from design_research_agents import Workflow as Workflow
