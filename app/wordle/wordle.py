import nltk


def get_corpus():
    return {word.lower() for word in nltk.corpus.brown.words()}


def filter_numeric(words):
    return [word for word in words if not any(x.isdigit() for x in word)]


def return_candidates(pattern='_____', exclude_letters=None, include_letters=None, corpus=get_corpus(), include_numeric=False):
    if exclude_letters is None:
        exclude_letters = []
    if isinstance(exclude_letters, str):
        exclude_letters = list(exclude_letters.lower())

    word_len = len(pattern)

    known = {i: x for i, x in enumerate(pattern) if x != '_'}

    candidates = [word for word in corpus
                  if len(word) == word_len
                  and not any(x in word.lower() for x in exclude_letters)
                  and all(word[k] == v for k, v in known.items())]

    if include_letters is not None:
        if isinstance(include_letters, str):
            include_letters = list(include_letters.lower())
        candidates = [word for word in candidates if all(x in word for x in include_letters)]

    if not include_numeric:
        candidates = filter_numeric(candidates)

    return sorted(candidates)
