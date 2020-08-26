import time
import subprocess
import os
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
import json
from easydict import EasyDict
from flask import (
    Flask,
    request,
    jsonify,
    send_file
)

with open('config.json', 'r') as f:
    CONFIG = EasyDict(json.load(f))
IMG_PATH = CONFIG.IMG_PATH
PDF_PATH = CONFIG.PDF_PATH
OUT_PATH = CONFIG.OUTPUT_PATH
EXE_FILE = CONFIG.EXE_PATH
PARAM = CONFIG.PARAM
app = Flask(__name__)


@app.route('/noiseCancelling', methods=['POST'])
def noiseCancelling():
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            filename = secure_filename(f.filename)
            if filename.endswith('pdf'):
                specialThing = time.time()
                specialThing *= 1e3
                specialThing = str(round(specialThing))
                filename = f'{specialThing}_{filename}'
                raw_target = os.path.join(
                    OUT_PATH,
                    filename
                )
                target = raw_target.split('.')[0] + '.jpg'
                filename = os.path.join(
                    PDF_PATH,
                    filename
                )
                f.save(filename)
                pages = convert_from_path(filename, 300)
                target_paths = list()
                for index, page in enumerate(pages):
                    index = str(index)
                    imgPath = filename.split('.')[0] + '_' + index + '.jpg'
                    target = raw_target.split('.')[0] + '_' + index + '.jpg'
                    imgPath = imgPath.replace(PDF_PATH, IMG_PATH)
                    page.save(imgPath, 'JPEG')
                    p = subprocess.Popen(
                        f'{EXE_FILE} {imgPath} -p {target} {PARAM}',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    target = target.split('/')[1:]
                    target_paths.append('/'.join(target))
                    output, error = p.communicate()
                return jsonify(target_paths)
    raise NotImplementedError


if __name__ == '__main__':
    app.run(host='0.0.0.0')
