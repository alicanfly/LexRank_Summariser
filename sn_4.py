def main():
    parser = argparse.ArgumentParser(description="Generic LexRank Summarizer")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', type=str, help='Text to summarize')
    group.add_argument('-f', '--file', type=argparse.FileType('r'), help='File with text')
    parser.add_argument('-n', '--sentences', type=int, default=3, help='Number of sentences in summary')
    parser.add_argument('--min-len', type=int, default=20, help='Minimum sentence length')
    parser.add_argument('--max-len', type=int, default=1000, help='Maximum sentence length')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Write summary to file')
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
