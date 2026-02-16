from exceptions.custom_exception import CustomException
from logger import Global_logger as log


log.info("adding custom logging")

try:
    1/0
except Exception as e:
    log.error("division by zero")
    raise CustomException(e)