from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import MainCategorySerializer, SubCategorySerializer
from .models import MainCategory , SubCategory

def index(request):
    return HttpResponse("안녕하세요. 기본 페이지입니다.")

@api_view(['GET'])
def getMainCaterogy(request):
    main_categories = MainCategory.objects.all()
    # return render(request, 'index.html', {'main_categories': main_categories})
    serializer = MainCategorySerializer(main_categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sub_categories(request, main_category_id):
    sub_categories = SubCategory.objects.filter(main_category_id=main_category_id)
    sub_categories_list = [{'id': sub_cat.id, 'name': sub_cat.name} for sub_cat in sub_categories]
    return JsonResponse({'sub_categories': sub_categories_list})

    # serializer = subCategorySerializer(sub_categories, many=True)
    # return Response(serializer.data)
