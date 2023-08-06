from .suggestion_strategy import SuggestionStrategy


class PhoneticSimilarity(SuggestionStrategy):
    def suggest(self, word):
        confusables = ['കഖഗഘ', 'ചഛജഝ', 'ടഠഡഢ','തഥദധ','പഫബഭ', 'രറ', 'ലള', 'ശഷസ']
        candidates = []
        for confusable in confusables:
            candidates += self.getCandidatesWithReplacements(word, confusable)
        return candidates


if __name__ == "__main__":
    print(PhoneticSimilarity().suggest('സംഗഗാനം'))
