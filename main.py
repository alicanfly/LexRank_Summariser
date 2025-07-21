'''

A generic CLI extractive summarizer using Sumy’s LexRank:
• Cleans whitespace and smart quotes/dashes
• Filters sentences by length (min/max bounds)
• Extracts top-N sentences
• Ensures diversity with at least one from the latter half
• Reorders output to match original flow


Usage:
  python main.py -i "Your paragraph here." -n 3
 

Requirements:
  pip install sumy nltk
  
  
'''
import argparse
import sys
import re
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


nltk.download('punkt', quiet=True)


def preprocess(text: str) -> str:
    """Normalize whitespace and replace smart quotes/dashes."""
    text = text.strip()
    replacements = {'“':'"', '”':'"', '‘':'"', '’':'"', '—':'-', '–':'-'}
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return re.sub(r"\s+", " ", text)


def split_sentences(text: str) -> list:
    """Split text into sentences."""
    return nltk.sent_tokenize(text)


def filter_sentences(sentences: list, min_len: int, max_len: int) -> list:
    """Keep sentences within specified length bounds."""
    return [s for s in sentences if min_len <= len(s) <= max_len]


def lexrank_summarize(text: str, count: int) -> list:
    """Extract top 'count' sentences with LexRank."""
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    ranked = summarizer(parser.document, count)
    return [str(s).strip() for s in ranked]


def enforce_diversity(all_sents: list, summary: list) -> list:
    """Ensure at least one sentence comes from the latter half of the text."""
    half = len(all_sents) // 2
    if half < len(all_sents):
        second_half = all_sents[half:]
        candidate = lexrank_summarize(' '.join(second_half), 1)
        if candidate and candidate[0] not in summary:
            summary[-1] = candidate[0]
    return summary


def reorder_and_pad(summary: list, all_sents: list, desired: int) -> list:
    """Reorder to original flow and pad if fewer than desired."""
    # Reorder
    ordered = [s for s in all_sents if s in summary]
    # Add any missing
    for s in summary:
        if s not in ordered:
            ordered.append(s)
    # Pad
    if len(ordered) < desired:
        extras = [s for s in all_sents if s not in ordered]
        ordered += extras[:desired - len(ordered)]
    return ordered


def read_input(args) -> str:
    """Retrieve text from --input, --file, STDIN, or prompt."""
    if args.input:
        return args.input
    if args.file:
        return args.file.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return input("Enter text to summarize: ")


def main():
    parser = argparse.ArgumentParser(description="Generic LexRank Summarizer")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', type=str, help='Text to summarize')
    group.add_argument('-f', '--file', type=argparse.FileType('r'), help='File with text')
    parser.add_argument('-n', '--sentences', type=int, default=3,
                        help='Number of sentences in summary')
    parser.add_argument('--min-len', type=int, default=20,
                        help='Minimum sentence length')
    parser.add_argument('--max-len', type=int, default=1000,
                        help='Maximum sentence length')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        help='Write summary to file')
    args = parser.parse_args()

    raw = read_input(args)
    text = preprocess(raw)
    sents = split_sentences(text)
    valid = filter_sentences(sents, args.min_len, args.max_len)
    if not valid:
        print("Error: No valid sentences after filtering.")
        sys.exit(1)

    desired = min(args.sentences, len(valid))
    summary = lexrank_summarize(text, desired)
    summary = enforce_diversity(valid, summary)
    final = reorder_and_pad(summary, valid, desired)

    
    header = "=== Summary ==="
    if args.output:
        args.output.write(header + "\n\n")
        for idx, sent in enumerate(final, 1):
            args.output.write(f"{idx}. {sent}\n")
        args.output.close()
    else:
        print(f"\n{header}\n")
        for idx, sent in enumerate(final, 1):
            print(f"{idx}. {sent}")

if __name__ == '__main__':
    main()
