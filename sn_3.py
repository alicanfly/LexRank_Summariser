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
    ordered = [s for s in all_sents if s in summary]
    for s in summary:
        if s not in ordered:
            ordered.append(s)
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
