import json
from django.shortcuts import render
from django.http import HttpResponse
import shelve

# Create your views here.
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def demo(request):
    return render(request, 'demo.html')

def get_top(request):
    name = request.GET.get('name', 0)
    k = request.GET.get('k', 0)
    neighbor = network.get_top(name, int(k))
    lt = []
    neighbor.append(name)
    for k in range(0, len(neighbor)):
        for v in range(k+1, len(neighbor)):
            try:
                if network.graph[neighbor[k]][neighbor[v]] != 0:
                    lt.append((neighbor[k],neighbor[v],network.graph[neighbor[k]][neighbor[v]]['w']))
            except:
                pass
    t_from = [0]*len(lt)
    t_to = [0]*len(lt)
    t_edgew = [0]*len(lt)
    clustering = []
    prank = []
    central = []
    for i in range(0,len(lt)):
        t_from[i] = lt[i][0]
        t_to[i] = lt[i][1]
        t_edgew[i] = lt[i][2]
    t_topk = [0]*len(set(t_from + t_to))
    t_topk = list(set(t_from + t_to))
    for i in range(0, len(t_topk)):
        clustering.append(network.get_cluster(t_topk[i]))
        prank.append(network.get_rank(t_topk[i]))
        central.append(network.get_central(t_topk[i]))
    return HttpResponse(json.dumps({
        "t_topk": t_topk,
        "t_from": t_from,
        "t_to": t_to,
        "t_edgew": t_edgew,
        "clustering": clustering,
        "prank": prank,
        "central": central
    }))

def get_allpath(request):
    name1 = request.GET.get('name1', 0)
    name2 = request.GET.get('name2', 0)
    clustering = []
    prank = []
    central = []
    name_list = []
    path_list = network.find_route(name1, name2)
    if len(path_list) >= 10:
        path_list = path_list[:10]
    for i in range(0, len(path_list)):
        name_list = name_list+path_list[i]
    name_list = list(set(name_list))
    for i in range(0, len(name_list)):
        clustering.append(network.get_cluster(name_list[i]))
        prank.append(network.get_rank(name_list[i]))
        central.append(network.get_central(name_list[i]))
    return HttpResponse(json.dumps({
        "path_list": path_list,
        "name_list": name_list,
        "clustering": clustering,
        "prank": prank,
        "central": central
    }))

def get_kpath(request):
    pass
    
newsDic = json.load(open('clean.json', encoding='utf-8'))['response']['docs']
def get_newslist(request):
    name1 = request.GET.get('name1', 0)
    name2 = request.GET.get('name2', 0)
    try:
        news_list = []
        time_list = []
        news_lists = network.graph[name1][name2]['l']
        for l in news_lists:
            # news_list.append(newsDic[l]['Url'])
            news_list.append("<a href=\""+newsDic[l]['Url']+"\">"+newsDic[l]['Title']+"</a>")
            time_list.append(newsDic[l]['Time'])
            # newsDic[l]['Url']
            # newsDic[l]['Text']
            # newsDic[l]['Time']
    except:
        news_list = []
        time_list = []
        print("error")
    return HttpResponse(json.dumps({
        "news_list": news_list,
        "time_list": time_list
    }))

def get_demo(request):
    number1 = request.GET.get('number1', 0)
    number2 = request.GET.get('number2', 0)
    nodelist = ['A', 'B']
    valuelist = [number1, number2]
    return HttpResponse(json.dumps({
        "nodelist": nodelist,
        'valuelist': valuelist
    }))

network = shelve.open('network')['g']
# print (sorted(network.clustering, key=lambda asd:asd[1], reverse=False)[:20])
