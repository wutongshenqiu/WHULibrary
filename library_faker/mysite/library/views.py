from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .library_spider import check_valid_cookie, LibrarySpider
from .models import CookieModel
import time
import json
import os

ROOM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rooms.json")

def log_in(request):
    if request.method == 'GET':
        return render(request,'library/log_in.html')
    elif request.method == 'POST':
        ssid = request.POST.get("ssid")
        print(ssid)
        return redirect(reverse('library:library'))
    

def library_form(request):
    object = get_object_or_404(CookieModel, ip=request.META.get("REMOTE_ADDR"))
    now_time = int(time.time())
    if now_time - object.last_time >= 1750:
        return redirect(reverse("library:log_in"))
    cookies = eval(object.cookies)
    if request.method == 'GET':
        # 感觉这里写的很不好，先实现了逻辑再说
        seat_info = LibrarySpider.get_seat_info(cookies=cookies)
        return render(request,'library/text.html', context={"seat_info": seat_info})
    elif request.method == 'POST':
        # print(request.POST.get('library'))
        building = request.POST.get("library")
        startMin = request.POST.get("startMin")
        endMin = request.POST.get("endMin")
        onDate = request.POST.get("onDate")
        room_not_expected = request.POST.getlist("roomNotExpected")
        mode = request.POST.get("mode")
        if not len(room_not_expected):
            room_not_expected = None

        spider = LibrarySpider(cookies=cookies)
        if mode == "1":
            spider.send_req_by_time(building=building, startMin=startMin, endMin=endMin, onDate=onDate,
                                    room_not_expected=room_not_expected)
        elif mode == "2":
            spider.send_req_humanly(building=building, startMin=startMin, endMin=endMin,
                                    onDate=onDate, room_not_expected=room_not_expected)
        ## debug use
        # print(building)
        # print(startMin, endMin)
        # print(onDate)
        # print(room_not_expected)
        # print(type(room_not_expected))
        # print(mode)
        # time.sleep(5)
        # return redirect(reverse("library:library"))

        return HttpResponse(str(spider.seat_info))
# Create your views here.


@csrf_exempt
def ssid_check(request):
    if request.method != "POST":
        raise Http404
    else:
        ssid = str(request.POST.get("ssid"))
        cookies = {"JSESSIONID": ssid}
        result = check_valid_cookie(cookies)
        if result:
            if result == 2:
                return JsonResponse({"status": "2"})

            ip_addr = request.META.get("REMOTE_ADDR")
            object, created = CookieModel.objects.get_or_create(ip=ip_addr)
            object.last_time = int(time.time())
            object.cookies = str(cookies)
            object.save()

            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@csrf_exempt
def get_room(request):
    if request.method != "POST":
        raise Http404
    else:
        library = request.POST.get("library")
        with open(ROOM_PATH, "r", encoding="utf8") as f:
            rooms = json.loads(f.read()).get("rooms").get(library)
        return JsonResponse({"rooms": rooms})


