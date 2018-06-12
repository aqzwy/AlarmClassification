# 参考代码
import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from kombu.utils import json

from main.crawer.address_crawer import get_address_by_crawer
from main.xgboost.getPrediction import predictionCase
from main.models.alarm import Alarm
from main.ltp.address_extract import get_address


class IndexView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        """
        过滤数据，并转为html格式
        Returns:

        """
        return

def index_test(request, ):
    global alarm_content
    if request.method == 'Post':
        received_json_data = json.loads(request.body)
        return HttpResponse(received_json_data)
    else:
        print("function test start:")
        result_head = {}
        result_data = {}

        print(str(request))
        if 'alarm_content' in str(request):
            alarm_content = str(request.GET['alarm_content'])
            result_head['result'] = '200'
            result_head['detail'] = 'successful'
            result_data['content'] = alarm_content
            result_data['type'] = predictionCase(alarm_content)

            address = get_address(alarm_content)
            result_data['type'] += ';' + address

            # save alarm and result
            alarm_obj = Alarm(content=alarm_content, alarm_id=uuid.uuid1(), first_type=' ', second_type=' ',
                              third_type=result_data['type'], fourth_type=' ')
            alarm_obj.save()
        else:
            detail = "parameter error, alarm_content can't be null!"
            result_head['result'] = '400'
            result_head['detail'] = detail

        result = {}
        result['head'] = result_head
        result['data'] = result_data

        get_address_by_crawer()

        response = json.dumps(result)
        return HttpResponse(response)
