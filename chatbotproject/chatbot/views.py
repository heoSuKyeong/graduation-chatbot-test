from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *
from .models import *

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


@api_view(['GET'])
def get_products(request, sub_category_id):
    try:
        sub_category = SubCategory.objects.get(id=sub_category_id)
    except SubCategory.DoesNotExist:
        return Response({"error": "Sub Category not found."}, status=status.HTTP_404_NOT_FOUND)
    
    products = Product.objects.filter(sub_category=sub_category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_aspects(request):
    aspects = Aspect.objects.all()
    serializer = AspectSerializer(aspects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def recommend_products(request, sub_category_id):
    try:
        sub_category = SubCategory.objects.get(id=sub_category_id)
    except SubCategory.DoesNotExist:
        return Response({"error": "Sub Category not found."}, status=status.HTTP_404_NOT_FOUND)
    
    condition = request.data.get('condition', '')

    if not condition:
        return Response({"error": "Condition text is required."}, status=status.HTTP_400_BAD_REQUEST)

    absa_model = settings.ABSA_MODEL
    results = absa_model.test(condition)    # {'편의성': {'polarity': 0, 'counts': {'긍정': 0, '부정': 7}}, '소음': {'polarity': 1, 'counts': {'긍정': 4, '부정': 0}}}
    
    # 분석 결과 파싱 (긍정 또는 부정에 따라 검색 조건 설정)
    matching_aspects = []
    aspect_polarity = {}

    for aspect, data in results.items():
        matching_aspects.append(aspect)
        aspect_polarity[aspect] = {
            "polarity": data["polarity"],  # 긍정(1) 또는 부정(0)
            "counts": data["counts"]
        }

    if not matching_aspects:
        return Response({"error": "No matching aspects found."}, status=status.HTTP_200_OK)

    # Sub Category에 속한 상품 중 조건에 맞는 상품 필터링
    products = Product.objects.filter(sub_category=sub_category)
    product_scores = {}

    for product in products:
        total_score = 0
        aspect_counts = {}

        for review in product.reviews.all():
            for review_aspect in review.review_aspects.all():
                if review_aspect.aspect.aspect in matching_aspects:
                    aspect_data = aspect_polarity[review_aspect.aspect.aspect]

                    # 긍정/부정 가중치 계산
                    if review_aspect.sentiment_polarity == 1:  # 긍정
                        total_score += aspect_data["counts"]["긍정"]
                    elif review_aspect.sentiment_polarity == 0:  # 부정
                        total_score += aspect_data["counts"]["부정"]

                    # aspect별 긍정/부정 개수 누적
                    if review_aspect.aspect.aspect not in aspect_counts:
                        aspect_counts[review_aspect.aspect.aspect] = {
                            "긍정": 0,
                            "부정": 0
                        }
                    aspect_counts[review_aspect.aspect.aspect]["긍정"] += aspect_data["counts"]["긍정"]
                    aspect_counts[review_aspect.aspect.aspect]["부정"] += aspect_data["counts"]["부정"]


        # 상품별 총 점수 저장
        if total_score > 0:
            product_scores[product.id] = {
                "product": product,
                "score": total_score,
                "aspect_counts": aspect_counts
            }

    # 상품을 가중치 점수로 정렬
    sorted_products = sorted(
        product_scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    # 정렬된 상품을 직렬화
    recommendations = {
        "aspects": matching_aspects,
        "products": [
            {
                "product": ProductSerializer(entry["product"]).data,
                "score": entry["score"],
                "aspect_counts": entry["aspect_counts"]
            }
            for entry in sorted_products[:5]
        ]
    }

    return Response(recommendations, status=status.HTTP_200_OK)
