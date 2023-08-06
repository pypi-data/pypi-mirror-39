import os
import sys
from argparse import ArgumentParser

from mlmorph import Analyser
from mlmorph_spellchecker import spellcheck, getSuggestions


def main():
    analyser = Analyser()
    parser = ArgumentParser()
    parser.add_argument('words', nargs="*",  help="word to spellcheck")
    args = parser.parse_args()
    if args.words:
        for word in args.words:
            word = word.strip()
            if spellcheck(word, analyser) is True:
                print('%s ✔️' % (word))
            else:
                print('%s ❌ Suggestions: %s' %
                      (word, getSuggestions(word, analyser)))


if __name__ == "__main__":
    main()
