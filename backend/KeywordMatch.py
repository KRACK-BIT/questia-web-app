import yake
from nltk.stem import PorterStemmer


class KeywordMatch:
    def __init__(self):
        language = "en"
        max_ngram_size = 3
        deduplication_threshold = 0.9
        numOfKeywords = 5
        self.custom_kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedupLim=deduplication_threshold,
            top=numOfKeywords,
            features=None,
        )

    def stem_phrases(self, words):
        stemmed = set()
        stemmer = PorterStemmer()
        for word in words:
            stemmed.add(" ".join([stemmer.stem(x) for x in word.split(" ")]))
        return stemmed

    def find_keyword_match(self, text1, text2):
        keywords1 = [
            x[0]
            for x in sorted(
                self.custom_kw_extractor.extract_keywords(text1),
                key=lambda x: x[1],
                reverse=True,
            )
        ]
        keywords2 = [
            x[0]
            for x in sorted(
                self.custom_kw_extractor.extract_keywords(text2),
                key=lambda x: x[1],
                reverse=True,
            )
        ]

        keyword_set_1 = self.stem_phrases(keywords1)
        keyword_set_2 = self.stem_phrases(keywords2)

        if len(keyword_set_1) + len(keyword_set_2) <= 6:
            threshold = 1
        else:
            threshold = 2

        score = len(set.intersection(keyword_set_1, keyword_set_2))

        return score if score >= threshold else None
