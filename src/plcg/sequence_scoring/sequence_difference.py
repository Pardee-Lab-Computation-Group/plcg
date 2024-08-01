import Levenshtein

from src.plcg.sequence_scoring.sequence_difference import num_list_to_aa_seq
from src.plcg.constants.values import AMINO_ACIDS


def get_sequence_diff(sequence_one: list[int], sequence_two: str) -> float:
    sequence_one = num_list_to_aa_seq(AMINO_ACIDS, sequence_one)
    sequence_diff = Levenshtein.distance(sequence_one, sequence_two)
    return sequence_diff


def get_min_sequence_diff(sequence, s1: list[list[int]], s2: str) -> float:
    s1 = [num_list_to_aa_seq(sequence, x) for x in s1]
    sequence_diff = [Levenshtein.distance(x, s2) for x in s1]
    return min(sequence_diff)
