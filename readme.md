# Generic LexRank Summarizer

A CLI tool for extractive summarization of any text paragraph using Sumy’s LexRank algorithm. It produces a concise, numbered summary of the most important sentences, ensuring diversity and readability.

## 🔍 Features

- **Preprocessing**: Normalizes whitespace and converts smart quotes/dashes to ASCII equivalents.
- **Filtering**: Discards sentences outside configurable length bounds.
- **LexRank Extraction**: Selects the top-N sentences that best represent the input.
- **Diversity Enforcement**: Guarantees at least one sentence from the latter half of the text.
- **Reordering & Padding**: Restores summary sentences in their original order and pads if too few are selected.
- **Flexible I/O**:
  - `--input` (`-i`): Pass a paragraph as a CLI argument.
  - `--file`  (`-f`): Summarize a local text file.
  - STDIN: Pipe text directly.
  - Interactive fallback prompt.
- **Output Options**: Print to console or write a numbered summary to a file via `--output` (`-o`).

## 💾 Installation

```bash
pip install sumy nltk
```

_Note: The script automatically downloads the NLTK sentence tokenizer (`punkt`) on first run._

## 🚀 Usage

```bash
python main.py [OPTIONS]
```

### Options

| Flag                  | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `-i`, `--input`       | Text paragraph to summarize (in quotes).               |
| `-f`, `--file`        | Path to a text file to summarize.                      |
| `-n`, `--sentences`   | Number of sentences to include in the summary. Default: `3`. |
| `--min-len`           | Minimum sentence length (characters). Default: `20`.    |
| `--max-len`           | Maximum sentence length (characters). Default: `1000`.  |
| `-o`, `--output`      | File path to write the summary. If omitted, prints to console. |

### Examples

**Summarize a quoted string:**
```bash
python main.py -i "Your long paragraph here." -n 3
```

**Summarize a text file and write to `summary.txt`:**
```bash
python main.py -f article.txt --min-len 30 --max-len 500 -n 4 -o summary.txt
```

**Pipe input via STDIN:**
```bash
cat article.txt | python main.py -n 2
```

> 📋 **Tip:** If your paragraph has more than 5–6 sentences and you want full coverage of all major points, increase `-n` accordingly.

## 🤝 Contributing

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m "Add my feature"`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a pull request.

Please ensure your code follows the existing style and includes tests where applicable.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

