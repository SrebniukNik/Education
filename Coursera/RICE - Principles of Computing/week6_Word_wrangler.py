"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# url_to_WORDFILE = codeskulptor.file2url(WORDFILE)
# TEMP_netfile = urllib2.urlopen(url_to_WORDFILE)


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
  Eliminate duplicates in a sorted list.

  Returns a new sorted list with the same elements in list1, but
  with no duplicates.

  This function can be iterative.
  """
    no_duplicates = []
    for item in list1:
        if item not in no_duplicates:
            no_duplicates.append(item)
    return no_duplicates


def intersect(list1, list2):
    """
  Compute the intersection of two sorted lists.

  Returns a new sorted list containing only elements that are in
  both list1 and list2.

  This function can be iterative.
  """
    intersected_list = []
    for item in list1:
        if item in list2:
            intersected_list.append(item)
    return intersected_list


# Functions to perform merge sort

def quicksort(num_list):
    """
  Recursive O(n log(n)) sorting algorithm
  Takes a list of numbers
  Returns sorted list of same numbers
  """
    if num_list == []:
        return num_list
    else:
        pivot = num_list[0]
        lesser = [num for num in num_list if num < pivot]
        pivots = [num for num in num_list if num == pivot]
        greater = [num for num in num_list if num > pivot]
        return quicksort(lesser) + pivots + quicksort(greater)


def merge(list1, list2):
    """
  Merge two sorted lists.

  Returns a new sorted list containing those elements that are in
  either list1 or list2.

  This function can be iterative.
  """
    merged_list = []
    list1 = list1[:]
    list2 = list2[:]

    while (list1 and list2):
        if (list1[0] < list2[0]):
            merged_list.append(list1.pop(0))
        else:
            merged_list.append(list2.pop(0))

    merged_list.extend(list1 if list1 else list2)

    return merged_list


def merge_sort(list1):
    """
  Sort the elements of list1.

  Return a new sorted list with the same elements as list1.

  This function should be recursive.
  """
    if len(list1) < 2:
        return list1[:]
    if len(list1) > 1:
        middle = len(list1) / 2
        sublist1 = merge_sort(list1[:middle])
        sublist2 = merge_sort(list1[middle:])
        return merge(sublist1, sublist2)


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
  Generate all strings that can be composed from the letters in word
  in any order.

  Returns a list of all strings that can be formed from the letters
  in word.

  This function should be recursive.
  """
    if not word:
        return ['']
    all_variants = []
    for letters in gen_all_strings(word[1:]):
        for index in range(len(letters) + 1):
            all_variants.append(letters[:index] + word[0] + letters[index:])
    return gen_all_strings(word[1:]) + all_variants

    # Function to load words from a file

    # def load_words(filename):
    #    """
    #    Load word list from the file named filename.
    #
    #    Returns a list of strings.
    #
    #    """
    #    file_to_read = open(filename)
    #    return [ line[:-1] for line in file_to_read]


    # def run():
    #    """
    #    Run game.
    #    """
    #    words = load_words(WORDFILE)
    #    #print words
    #    wrangler = provided.WordWrangler(words, remove_duplicates,
    #                                     intersect, merge_sort,
    #                                     gen_all_strings)
    #    provided.run_game(wrangler)

    # Uncomment when you are ready to try the game
    # run()

    # print load_words(netfile)


    # print gen_all_strings('abcdna')