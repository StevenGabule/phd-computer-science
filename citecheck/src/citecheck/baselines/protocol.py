"""Common interface for all CiteCheck baselines and the main verify loop.

The :class:`BaselineProtocol` is a structural :class:`typing.Protocol` rather
than an ABC so that :class:`~citecheck.agent.VerifyLoop` (which inherits from
nothing) satisfies it implicitly. The eval harness can therefore treat all six
systems uniformly without forcing a base class on the agent.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from citecheck.agent.loop import AnswerWithCitations


@runtime_checkable
class BaselineProtocol(Protocol):
    """Minimal contract every Phase-2 system must satisfy.

    Implementers must produce a :class:`~citecheck.agent.loop.AnswerWithCitations`
    for each input question. The ``citations`` field may be empty if the system
    chooses not to emit citations (e.g. :class:`VanillaBaseline` on questions it
    refuses), but the field must always be present.
    """

    def answer(self, question: str) -> AnswerWithCitations:  # pragma: no cover
        """Return a citation-checked answer for ``question``."""
        ...
