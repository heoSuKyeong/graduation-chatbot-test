from sklearn import preprocessing
from sklearn.utils import column_or_1d
import pandas as pd
import transformers
import torch
import re



class MyLabelEncoder(preprocessing.LabelEncoder):
    def fit(self, y):
        y = column_or_1d(y, warn=True)
        self.classes_ = pd.Series(y).unique()
        return self


class ABSADataset():
    def __init__(self, config, enc_aspect, enc_aspect2, enc_sentiment, batch_size, data_len=0):
        self.data_len = data_len
        self.batch_size = batch_size
        self.max_len = config.max_length
        self.config = config
        
        self.enc_aspect = enc_aspect
        self.enc_aspect2 = enc_aspect2
        self.enc_sentiment = enc_sentiment

        self.tokenizer = transformers.BertTokenizer.from_pretrained(config.init_model_path, do_lower_case=False)
        self.CLS_IDS = self.tokenizer.encode('[CLS]', add_special_tokens=False)  # [2]
        self.PAD_IDS = self.tokenizer.encode('[PAD]', add_special_tokens=False)  # [0]
        self.SEP_IDS = self.tokenizer.encode('[SEP]', add_special_tokens=False)  # [3]
        self.PADDING_TAG_IDS = [0]
        self.s_len = 0


    def get_data(self, text):
        text = sentence2words(text)
        
        # dummy data
        aspect = ['B-소음'] * len(text)
        aspect2 = ['B-사용감/착용감'] * len(text)
        sentiment = ['B-부정'] * len(text)

        aspect = self.enc_aspect.transform(aspect)
        aspect2 = self.enc_aspect2.transform(aspect2)
        sentiment = self.enc_sentiment.transform(sentiment)

        return self.parsing_data(text, aspect, aspect2, sentiment)


    def parsing_data(self, text, aspect, aspect2, sentiment):
        ids = []
        target_aspect = [] # target Aspect Category tensor ids 저장 리스트
        target_aspect2 = []  # target 대분류 Aspect Category tensor ids 저장 리스트 (대분류 기준 성능 측정을 위함)
        target_sentiment = [] # target Sentiment tensor ids 저장 리스트

        for i, s in enumerate(text):
            inputs = self.tokenizer.encode(s, add_special_tokens=False)
            input_len = len(inputs)
            ids.extend(inputs)
            target_aspect.extend([aspect[i]] * input_len)
            target_aspect2.extend([aspect2[i]] * input_len)
            target_sentiment.extend([sentiment[i]] * input_len)

        # BERT가 처리할 수 있는 길이 (max_length)에 맞추어 slicing
        ids = ids[:self.max_len - 2]
        target_aspect = target_aspect[:self.max_len - 2]
        target_aspect2 = target_aspect2[:self.max_len - 2]
        target_sentiment = target_sentiment[:self.max_len - 2]

        # SPECIAL TOKEN 추가 및 PADDING 수행
        ids = self.CLS_IDS + ids + self.SEP_IDS
        target_aspect = self.PADDING_TAG_IDS + target_aspect + self.PADDING_TAG_IDS  # CLS, SEP 태그 0
        target_aspect2 = self.PADDING_TAG_IDS + target_aspect2 + self.PADDING_TAG_IDS
        target_sentiment = self.PADDING_TAG_IDS + target_sentiment + self.PADDING_TAG_IDS

        mask = [1] * len(ids)
        token_type_ids = self.PAD_IDS * len(ids)
        padding_len = self.max_len - len(ids)
        ids = ids + (self.PAD_IDS * padding_len)
        mask = mask + ([0] * padding_len)

        token_type_ids = token_type_ids + (self.PAD_IDS * padding_len)
        target_aspect = target_aspect + (self.PADDING_TAG_IDS * padding_len)
        target_aspect2 = target_aspect2 + (self.PADDING_TAG_IDS * padding_len)
        target_sentiment = target_sentiment + (self.PADDING_TAG_IDS * padding_len)

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "target_aspect": torch.tensor(target_aspect, dtype=torch.long),
            "target_aspect2": torch.tensor(target_aspect2, dtype=torch.long),
            "target_sentiment": torch.tensor(target_sentiment, dtype=torch.long), }


def preprocess_sentence(sentence):
    words = sentence.replace("\n", " ")
    words = words.replace(",", " ")  #
    words = words.replace(",", " ")  #
    words = re.sub(' +', ' ', words)  # to single white_space
    return words


def sentence2words(sentence):
    words = preprocess_sentence(sentence)
    words = words.split(" ")
    words = list(filter(None, words))
    return words