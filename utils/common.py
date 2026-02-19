from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
import os
from pathlib import Path
import uuid
import re
from datetime import datetime, timezone, timedelta

def root_path():
    log.info("returninig root path of project")
    return Path(__file__).resolve().parent.parent

def generate_session_id(prefix: str = "session") -> str:
    # IST is UTC+5:30
    ist = timezone(timedelta(hours=5, minutes=30))
    return f"{prefix}_{datetime.now(ist).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def save_uploaded_file(files,save_path):
    try:
        os.makedirs(save_path,exist_ok=True)
        log.info(f"saving uploaded file in {save_path}")
        saved=[]
        for uf in files:
            if hasattr(uf,"filename"):
                name=uf.filename
                file_bytes=uf.file.read()
            elif hasattr(uf,"name"):
                name=uf.name
                file_bytes=uf.getbuffer()
            else:
                raise CustomException("Unsupported uploaded file")
            ext = Path(name).suffix.lower()
            # Clean file name (only alphanum, dash, underscore)
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', Path(name).stem).lower()
            fname=f"{safe_name}{ext}"
            log.info(f"saving file:{fname}")
            out=os.path.join(save_path,fname)
            with open(out,"wb") as f:
                f.write(file_bytes)

            saved.append(out)
        log.info(f"saved uploaded files:{saved}")
        return saved
    except Exception as e:
        log.info(f"Error while saving file:{e}")
        raise CustomException(f"Error while saving file:{e}")