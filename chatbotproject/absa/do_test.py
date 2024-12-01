from absa.modeling.model import ABSAModel
from absa.modeling.trainer import test_fn
from absa.utils.model_utils import device_setting, load_model
from absa.data_manager.dataset.absa import ABSADataset
import os
import sys
import joblib
import warnings
warnings.filterwarnings(action='ignore')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "absa")))

class ABSA():
    def __init__(self, config):
        model_path = os.path.join(config.base_path, config.out_model_path)
        
        meta_data = joblib.load(os.path.join(config.base_path, config.label_info_file))
        self.enc_sentiment, self.enc_aspect = meta_data["enc_sentiment"], meta_data["enc_aspect"]
        num_sentiment = len(list(meta_data["enc_sentiment"].classes_))
        num_aspect, num_aspect2 = len(list(meta_data["enc_aspect"].classes_)), len(list(meta_data["enc_aspect2"].classes_))

        # Device Setting (GPU/CPU)
        self.device = device_setting()

        # model Architecture 생성
        model = ABSAModel(num_sentiment=num_sentiment, num_aspect=num_aspect, num_aspect2=num_aspect2, config=config, need_birnn=bool(config.need_birnn))
        # 저장된 모델 load
        self.model = load_model(model=model, state_dict_path=model_path, device=self.device)

        self.dataset = ABSADataset(config=config, enc_aspect=meta_data["enc_aspect"], enc_aspect2=meta_data["enc_aspect2"], enc_sentiment=meta_data["enc_sentiment"], batch_size=config.eval_batch_size)
        
        # 각 sample의 예측 결과 출력 여부
        self.flag = "eval" if config.print_sample == 1 else "valid"


    def test(self, sentence):
        self.input_data = [self.dataset.get_data(sentence)]
        # 평가 수행
        return test_fn(self.input_data, self.model, self.enc_sentiment, self.enc_aspect, self.device, f1_mode='micro', flag=self.flag)
