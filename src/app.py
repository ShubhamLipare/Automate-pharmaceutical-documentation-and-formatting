from exceptions.custom_exception import CustomException
from logger import GLOBAL_LOGGER as log
from utils.config_loader import load_config
from utils.model_loader import ModelLoader


log.info("adding custom logging")

try:
    1/0
except Exception as e:
    log.error("division by zero")
    raise CustomException(e)