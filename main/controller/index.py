# 参考代码
from audioop import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView
from kombu.utils import json

from main.CaseClassification.getPrediction import predictionCase


class IndexView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        """
        过滤数据，并转为html格式
        Returns:

        """
        return

def index_test(request, ):
    if request.method == 'Post':
        received_json_data = json.loads(request.body)
        return HttpResponse(received_json_data)
    else:
        print("function test start:")
        result_head = {}
        result_data = {}

        print(str(request))
        if 'alarm_content' in str(request):
            content = str(request.GET['alarm_content'])
            result_head['result'] = '200'
            result_head['detail'] = 'successful'
            result_data['content'] = content
            result_data['type'] = predictionCase(content)
        else:
            detail = "parameter error, alarm_content can't be null!"
            result_head['result'] = '400'
            result_head['detail'] = detail

        result = {}
        result['head'] = result_head
        result['data'] = result_data

        response = json.dumps(result)
        return HttpResponse(response)
