from nltk import pos_tag, word_tokenize
from simple_grammar import SimpleGrammar

grammars = []


def init(grammar_strings):
    for grammar_string in grammar_strings:
        grammars.append(
            SimpleGrammar(grammar_string)
        )


def transform(phrase):
    results = []
    phrase_tags = __get_tags(phrase)
    results.append('Original: ' + phrase)
    for grammar in grammars:
        sub_results = grammar.generate_from(phrase_tags)
        for sub_result in sub_results:
            if phrase != sub_result:
                results.append(sub_result)
    return results


def transform_batch(phrase_list):
    results = []
    for phrase in phrase_list:
        sub_results = transform(phrase)
        for sub_result in sub_results:
            results.append(sub_result)
        results.append('------------------')
    return results


def __get_tags(phrase):
    tags = pos_tag(word_tokenize(phrase))

    # Exceptions occur
    command_verbs = ['find', 'fetch', 'search', 'buy', 'get', 'create', 'delete', 'discover', 'check', 'request']
    if tags[0][1] != 'VB' and tags[0][0] in command_verbs:
        tags[0] = (tags[0][0], 'VB')

    for index, tag_tuple in enumerate(tags):
        tag = tag_tuple[1]
        to_replace = None
        if 'NN' in tag:
            to_replace = 'NN'

        if to_replace:
            tags[index] = (tags[index][0], 'NN')

    return tags
