from collections import Counter
import textstat


def text_complexity_scores(text):
    print(f"Flesch kincaid score = {textstat.flesch_kincaid_grade(text)}")
    print(f"Flesch reading ease = {textstat.flesch_reading_ease(text)}")

    tokens = text.split()
    token_counts = Counter(tokens)
    num_types = len(token_counts)
    num_tokens = sum(token_counts.values())
    type_token_ratio = num_types / num_tokens
    print(f"Type Token Ratio = {type_token_ratio}")

    num_hapax_legomena = sum(
        1 for count in token_counts.values() if count == 1)
    hapax_legomena_ratio = num_hapax_legomena / num_tokens
    print(f"Hapax Legomena Ratio = {hapax_legomena_ratio}")


def main():
    filename = "bing-results\\result2.txt"
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    file.close()
    text_complexity_scores(text)


if __name__ == "__main__":
    main()
