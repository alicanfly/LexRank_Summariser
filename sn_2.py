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
