from sub_loader.raw_sub_loader import Subtitle
from tokenizer import simple_tokenizer
from functional import seq
from typing import List
from collections import Counter


class MovieTf:
    def __init__(self, subs: List[Subtitle]):
        self.bag_of_words: Counter = get_tokens_from_subs(subs)
        self.words = len(self.bag_of_words)

    def contains(self, word: str) -> bool:
        return self.bag_of_words[word] != 0

    def get_tf(self, word: str) -> float:
        return 0.5 + 0.5 * self.bag_of_words[word] / self.words


def get_tokens_from_subs(subs: List[Subtitle]) -> Counter:
    return Counter(seq(subs).flat_map(get_tokens_from_sub))


def get_tokens_from_sub(sub: Subtitle) -> List[str]:
    return simple_tokenizer.tokenize(sub.text)
