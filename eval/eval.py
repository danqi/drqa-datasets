import re
import argparse
import string


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match_score(prediction, ground_truth):
    """Check if the prediction is a (soft) exact match with the ground truth."""
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def regex_match_score(prediction, pattern):
    """Check if the prediction matches the given regular expression."""
    try:
        compiled = re.compile(
            pattern,
            flags=re.IGNORECASE + re.UNICODE + re.MULTILINE
        )
    except BaseException:
        print('Regular expression failed to compile: %s' % pattern)
        return False
    return compiled.match(prediction) is not None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', '-p', type=str, required=True)
    parser.add_argument('--gold', '-g', type=str, required=True)
    parser.add_argument('--regex', action='store_true')
    args = parser.parse_args()

    fn = regex_match_score if args.regex else exact_match_score
    print('pred=%s' % args.pred)
    print('gold=%s' % args.gold)
    print('matched?=%s' % fn(args.pred, args.gold))

