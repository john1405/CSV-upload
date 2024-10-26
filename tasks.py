from celery import Celery
from config import Config
from models import insert_movie, update_upload_status
import pandas as pd
import os

celery = Celery(__name__)
celery.conf.broker_url = Config.CELERY_BROKER_URL
celery.conf.result_backend = Config.CELERY_RESULT_BACKEND

@celery.task(bind=True)
def process_csv_file(self, filepath):
    try:
        df = pd.read_csv(filepath, chunksize=10000)
        total_rows = sum(1 for row in df)

        for i, chunk in enumerate(pd.read_csv(filepath, chunksize=10000)):
            movies = chunk.to_dict('records')
            insert_movie(movies)

            progress = int(((i + 1) * 10000 / total_rows) * 100)
            update_upload_status(self.request.id, "processing", progress)

        update_upload_status(self.request.id, "completed", 100)
    except Exception as e:
        update_upload_status(self.request.id, "failed", 0)
    finally:
        os.remove(filepath)
