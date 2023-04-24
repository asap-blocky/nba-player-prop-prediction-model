"""
This module contains functions for searching player names on basketball-reference.com.
"""

import os
import unidecode


def levenshtein(s1, s2, maximum):
    """
    Calculate the Levenshtein distance between two strings, which is the number of 
    single-character edits (insertions, deletions, or substitutions) needed to 
    transform one string into the other.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.
        maximum (int): The maximum allowable Levenshtein distance. If the distance 
            between the strings exceeds this value, the function returns -1.

    Returns:
        int: The Levenshtein distance between s1 and s2, or -1 if the distance 
        exceeds the maximum.

    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        if all((x >= maximum for x in distances_)):
            return -1
        distances = distances_
    return distances[-1]


def lookup(player, ask_matches=True):
    path = os.path.join(os.path.dirname(__file__), '..',
                        'data', 'active_players_names.txt')

    normalized = unidecode.unidecode(player)

    matches = []

    with open(path, encoding='utf-8') as file:
        Lines = file.readlines()
        for line in Lines:

            dist = levenshtein(normalized.lower(), line[:-1].lower(), 5)
            if dist >= 0:
                matches += [(line[:-1], dist)]

    if len(matches) == 1 or ask_matches == False:
        matches.sort(key=lambda tup: tup[1])
        if ask_matches:
            print("You searched for \"{}\"\n{} result found.\n{}".format(
                player, len(matches), matches[0][0]))
            print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]

    elif len(matches) > 1:
        print("You searched for \"{}\"\n{} results found.".format(
            player, len(matches)))
        matches.sort(key=lambda tup: tup[1])
        return matches[0][0]

    elif len(matches) < 1:
        print("You searched for \"{}\"\n{} results found.".format(
            player, len(matches)))
        return ""

    else:
        print("You searched for \"{}\"\n{} result found.\n{}".format(
            player, len(matches), matches[0][0]))
        print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]

    return ""
