import gensim
import numpy as np
from nltk.tokenize import WordPunctTokenizer
import re
import nltk
import string
# nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from copy import deepcopy

THRESHHOLD = 0.75

tokenizer = WordPunctTokenizer()
wv_embeddings = gensim.models.KeyedVectors.load('../notebooks/model.model')
stopWords = set(stopwords.words('russian'))

def text_prepare(text):
    """
        text: a string

        return: modified string
    """
    text = text.lower()
    text = re.sub(r'[{}]'.format(string.punctuation), ' ', text)
    text = re.sub('[^А-Яа-яA-Za-z0-9 ]', '', text)
    stopWords = set(stopwords.words('russian'))
    for stopWord in stopWords:
        # text = text.replace(stopWord, '')
        text = re.sub('^{}$'.format(stopWord), '', text)
    return text

def question_to_vec(question, embeddings, dim=300):
    """
        question: строка
        embeddings: наше векторное представление
        dim: размер любого вектора в нашем представлении
        
        return: векторное представление для вопроса
    """
    words = question.replace("?", '').split()
    n_known = 0
    result = np.array([0] * dim, dtype=float)
    for word in words:
        if word in embeddings:
            result += embeddings[word]
            n_known += 1
    if n_known != 0:
        return result/n_known
    else:
        return result

def get_most_simmilar(question, candidates):
    candidates_embeddings = [
        question_to_vec(text_prepare(candidate), wv_embeddings, dim=300) 
        for candidate in candidates
    ]
    dist_s = cosine_similarity(
        candidates_embeddings, 
        np.array(
            [question_to_vec(text_prepare(question), wv_embeddings, dim=300)]
        )
    )[:, 0]

    if dist_s.max() > THRESHHOLD: 
        return candidates[dist_s.argmax()]
    else:
        return None
