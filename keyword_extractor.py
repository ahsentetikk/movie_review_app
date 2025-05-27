import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def extract_keywords_from_comments(comments, top_n=10):
    if not comments:
        return []

    # Türkçe stopwords
    turkish_stopwords = stopwords.words('turkish')

    # DataFrame oluştur
    df = pd.DataFrame({'comment': comments})

    # Boş ya da sadece boşluk olan yorumları temizle
    df = df[df['comment'].notnull()]
    df = df[df['comment'].str.strip() != ""]

    if df.empty:
        return []

    try:
        vectorizer = TfidfVectorizer(stop_words=turkish_stopwords, max_features=1000)
        X = vectorizer.fit_transform(df['comment'])

        if X.shape[1] == 0:
            return []

        tfidf_scores = X.sum(axis=0).A1
        feature_names = vectorizer.get_feature_names_out()
        tfidf_dict = dict(zip(feature_names, tfidf_scores))

        sorted_keywords = sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, score in sorted_keywords[:top_n]]

    except ValueError:
        # Örn. sadece stopword varsa veya tüm yorumlar boşsa
        return []
