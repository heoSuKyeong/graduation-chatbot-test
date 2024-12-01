import os

Config = {
    "eval_batch_size": 4,
    # ============= [Model Parameter] =================
    # 평가를 수행할 모델을 생성할 때, 사용 했던 parameter와 동일하지 않을 시, 오류 발생!
    "init_model_path": "klue/bert-base",    # 사용된 BERT의 종류
    "max_length": 512,                      # 토큰화된 문장의 최대 길이(bert는 기본 512)
    "need_birnn": 0,                        # model에 Birnn Layer를 추가했는지 여부 (True: 1/False: 0)
    "sentiment_drop_ratio": 0.3,            # Sentiment 속성의 과적합 방지를 위해 dropout을 수행한 비율
    "aspect_drop_ratio": 0.3,               # Aspect Category 속성의 과적합 방지를 위해 dropout을 수행한 비율
    "sentiment_in_feature": 768,            # 각 Sentiment input sample의 size
    "aspect_in_feature": 768,               # 각 Aspect Category input sample의 size
    # ===================================================
    "base_path": "./absa/ckpt/result_model",    # 평가를 수행할 Model과 Encoder가 저장된 경로
    "label_info_file": "meta.bin",          # 사용할 Encoder 파일명
    "out_model_path": "pytorch_model.bin",  # 평가할 model의 파일명
    "print_sample": 1,                      # 각 sample의 예측 결과 출력 여부를 결정 (True: 1/False: 0)
}