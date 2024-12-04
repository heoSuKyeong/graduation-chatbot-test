from django.apps import AppConfig
from absa.do_test import ABSA
from absa.config import Config
from types import SimpleNamespace


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'

    def ready(self):
        # ABSA 모델 초기화
        config = SimpleNamespace(**Config)
        absa_model = ABSA(config)

        # 모델 객체를 전역으로 사용할 수 있도록 저장
        from django.conf import settings
        settings.ABSA_MODEL = absa_model