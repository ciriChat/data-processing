from config import file_config
from functional import seq
import time
from datetime import datetime

from tfidf.idf import idf_repository

result = idf_repository.select_all()
d = dict(result)

print(d['dawid'])
print(d['jabłko'])


