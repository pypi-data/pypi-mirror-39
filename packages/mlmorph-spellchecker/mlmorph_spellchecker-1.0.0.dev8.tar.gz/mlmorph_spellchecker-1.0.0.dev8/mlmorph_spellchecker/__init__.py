"""
Define a family of algorithms, encapsulate each one, and make them
interchangeable. Strategy lets the algorithm vary independently from
clients that use it.
"""
from __future__ import absolute_import

import abc
import importlib
from .strategies import *


class Suggestion:
    """
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def suggest(self, word):
        return self._strategy.suggest(word)


def getSuggestions(word, analyser):
    # Order of the items in STRATEGIES is important
    STRATEGIES = ['VisualSimilarity', 'Ykkuka', 'TTaCorrection', 'NtaCorrection', 'MpaCorrection', 'LLaCorrection',
                  'GeminateConsonants', 'ViramaInsertion', 'VowelElongation', 'VowelShortening',
                  'ChilluToConsonantVirama', 'ConsonantViramaToChillu',
                  'ChilluNormalization',
                  'ConsonantAspirationCorrection', 'ConsonantVoiceCorrection']

    weighted_suggestions = {}
    for i in range(len(STRATEGIES)):
        strategy = globals()[STRATEGIES[i]]()
        context = Suggestion(strategy)
        candidates = context.suggest(word)
        for candidate in candidates:
            if candidate in weighted_suggestions:
                continue
            weighted_analysis = analyser.analyse(candidate, True)
            if len(weighted_analysis) > 0:
                weighted_suggestions[candidate] = weighted_analysis[0][1]

    # Sort by the increasing order of weights
    suggestions = sorted(weighted_suggestions.items(), key=lambda t: t[1])
    # Return the words array
    return [suggestion[0] for suggestion in suggestions]


def spellcheck(word, analyser):
    analysis = analyser.analyse(word, False)
    return len(analysis) > 0


__all__ = ['spellcheck', 'getSuggestions']
