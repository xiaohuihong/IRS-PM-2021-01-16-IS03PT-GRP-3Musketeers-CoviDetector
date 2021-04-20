import shutil
import os
from distutils.sysconfig import get_python_lib

corpus_dir = os.path.join(get_python_lib(), 'chatterbot_corpus\data\custom')
shutil.move(os.path.join('chatbot\data', 'covid.yml'), os.path.join(corpus_dir, 'covid.yml'))
