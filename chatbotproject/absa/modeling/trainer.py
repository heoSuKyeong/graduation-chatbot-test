from collections import Counter
import numpy as np
import torch

def parsing_batch(data, device):
    d = {}
    for k in data[0].keys():
        d[k] = list(d[k] for d in data)
    for k in d.keys():
        d[k] = torch.stack(d[k]).to(device)
    return d


def get_result(sentiments, aspects):
    aspect_names = [aspect.split('-')[1] for aspect in aspects]
    unique_aspects = list(set(aspect_names))

    # Step 1: Extract aspects and unique categories
    aspect_names = [aspect.split('-')[1] for aspect in aspects]
    unique_aspects = list(set(aspect_names))

    # Step 2: Map sentiments to each aspect
    aspect_sentiments = {aspect: [] for aspect in unique_aspects}
    for aspect, sentiment in zip(aspect_names, sentiments):
        aspect_sentiments[aspect].append(sentiment.split('-')[1])  # Extract '긍정' or '부정'

    # Step 3: Count sentiments and determine polarity sentiment
    results = {}
    for aspect, sentiment_list in aspect_sentiments.items():
        sentiment_counts = Counter(sentiment_list)
        polarity_sentiment = max(sentiment_counts, key=sentiment_counts.get)  # Get the most frequent sentiment
        polarity_sentiment_numeric = 1 if polarity_sentiment == "긍정" else 0   # Convert polarity to 1 (긍정) or 0 (부정)
        counts_numeric = {"긍정": sentiment_counts.get("긍정", 0), "부정": sentiment_counts.get("부정", 0)}   # Convert counts to numeric form
        results[aspect] = {"polarity": polarity_sentiment_numeric, "counts": counts_numeric}

    return results


def test_fn(input_data, model, enc_sentiment, enc_aspect, device, f1_mode='micro', flag='valid'):
    model.eval()
    final_loss = 0
    nb_eval_steps = 0
    sentiment_preds, aspect_preds = [], []

    data = parsing_batch(input_data, device)

    loss, predict_sentiment, predict_aspect, predict_aspect2 = model(**data)
    sentiment_label = data['target_sentiment'].cpu().numpy().reshape(-1) #한줄로 핌
    aspect_label = data['target_aspect2'].cpu().numpy().reshape(-1)

    sentiment_pred = np.array(predict_sentiment).reshape(-1)
    aspect_pred = np.array(predict_aspect).reshape(-1)

    #remove padding indices
    pad_label_indices = np.where(sentiment_label == 0) #pad 레이블
    sentiment_pred = np.delete(sentiment_pred, pad_label_indices)
    pad_label_indices = np.where(aspect_label == 0)  # pad 레이블
    aspect_pred = np.delete(aspect_pred, pad_label_indices)

    sentiment_preds.extend(sentiment_pred)
    aspect_preds.extend(aspect_pred)

    final_loss += loss.item()
    nb_eval_steps += 1

    # encoding 된 Sentiment와 Aspect Category를 Decoding (원 형태로 복원)
    sentiment_pred_names = enc_sentiment.inverse_transform(sentiment_preds)
    aspect_pred_names = enc_aspect.inverse_transform(aspect_preds)

    if flag == 'eval':
        for i in range(len(sentiment_pred_names)):
            print(f"[{i} >> predicted sentiment label: {sentiment_pred_names[i]} | "
                     f"predicted aspect label: {aspect_pred_names[i]}]")

    # return sentiments, aspects
    return get_result(sentiment_pred_names, aspect_pred_names)
    