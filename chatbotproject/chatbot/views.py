from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import MainCategorySerializer, SubCategorySerializer
from .models import MainCategory , SubCategory

def index(request):
    return HttpResponse("안녕하세요. 기본 페이지입니다.")


@api_view(['GET'])
def get_main_categories(request):
    main_categories = MainCategory.objects.all()
    serializer = MainCategorySerializer(main_categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET']) 
def get_sub_categories(request, main_category_id):
    try:
        main_category = MainCategory.objects.get(id=main_category_id)
    except MainCategory.DoesNotExist:
        return Response({"error": "Main Category not found."}, status=status.HTTP_404_NOT_FOUND)

    sub_categories = SubCategory.objects.filter(main_category=main_category)
    serializer = SubCategorySerializer(sub_categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
