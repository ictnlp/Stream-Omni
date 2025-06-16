import json
import argparse


from stream_omni.eval.text_normalization.basic import BasicTextNormalizer
from stream_omni.eval.text_normalization.cn_tn import TextNorm
from stream_omni.eval.text_normalization.en import EnglishTextNormalizer

english_normalizer = EnglishTextNormalizer()
chinese_normalizer = TextNorm(
    to_banjiao=False,
    to_upper=False,
    to_lower=False,
    remove_fillers=False,
    remove_erhua=False,
    check_chars=False,
    remove_space=False,
    cc_mode="",
)
basic_normalizer = BasicTextNormalizer()


def main():
    parser = argparse.ArgumentParser(description="Calculate accuracy based on JSONL file.")
    parser.add_argument("--file", required=True, help="Path to the JSONL file")
    args = parser.parse_args()

    total = 0
    correct = 0

    with open(args.file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            answer = data["answer"]
            output = data["output"].lower()

            if isinstance(answer, str):
                answer_list = [answer]
            else:
                answer_list = answer

            answer_list = [x.lower() for x in answer_list]

            found = False
            for a in answer_list:
                if str(a) in output:
                    found = True
                    break

            if found:
                correct += 1
            total += 1

    accuracy = (correct / total) * 100 if total > 0 else 0
    print(f"{accuracy:.2f}")


if __name__ == "__main__":
    main()
