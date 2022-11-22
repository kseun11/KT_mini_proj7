from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
from keras.models import load_model

# from pybo.model import Result
from .models import Result

# Create your views here.

logger = logging.getLogger('mylogger')

def index(request):
    return render(request, 'language/index.html')

def upload(request):
    import os

    if request.method == 'POST' and request.FILES['files']:
        files_list_type = [] # django type
        files_list_name = [] # 이름만
        preds = []

        #form에서 전송한 파일을 획득한다.
        for f in request.FILES.getlist('files'):
            files = f
            files_list_type.append(files)
            # 정답을 '이미지 파일 이름' 으로 함
            # 이미지 파일의 확장자를 제외 => name 변수에 담음
            name, _ = os.path.splitext(str(f))
            # upload 화면에 출력할 이미지 파일 이름 담기
            files_list_name.append(name) # ['a', 'e', 'l', 'o', 'v']

        # logger.error('file', file)
        # class names 준비
        class_names = list(string.ascii_lowercase)
        class_names = np.array(class_names)

        # 모델 로딩
        model_path = settings.MODEL_DIR +'/sign_model.h5'
        model = load_model(model_path)

        # print("==================")
        # print(files)
        # print(type(files))
        # print("==================")
        # print(files_list[0])
        # print(type(files_list[0]))
    
    
        for file in files_list_type:
            # history 저장을 위해 객체에 담아서 DB에 저장한다.
            # 이때 파일시스템에 저장도 된다.
            result = Result()
            result.answer = request.POST.get('answer', '')
            result.image = file
            result.pub_date = timezone.datetime.now()
            result.save()

            # 흑백으로 읽기
            img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)
            # 크기 조정
            img = cv2.resize(img, (28, 28))
            # input shape 맞추기
            test_sign = img.reshape(1, 28, 28, 1)
            # 스케일링
            test_sign = test_sign / 255.
            # 예측 : 결국 이 결과를 얻기 위해 모든 것을 했다.
            pred = model.predict(test_sign)
            pred_1 = pred.argmax(axis=1)
            preds.append(class_names[pred_1][0])

            result.result = class_names[pred_1][0]
            result.save()

            context = {
                'result': result, # a e l o v
            }

        print(context)

    # http method의 GET은 처리하지 않는다. 사이트 테스트용으로 남겨둠
    else:
        test = request.GET['test']
        logger.error(('Something went wrong!!',test))
    return render(request, 'language/result.html', context)    

