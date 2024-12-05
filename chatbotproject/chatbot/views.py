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
    product_name = request.data.get('product_name', '')
    
    if not condition:
        return Response({"error": "Condition text is required."}, status=status.HTTP_400_BAD_REQUEST)

    matching_aspects, aspect_polarity = analyze_condition_with_absa(condition)

    if not matching_aspects:
        return Response({"error": "No matching aspects found."}, status=status.HTTP_200_OK)

    # 상품 필터링 및 점수 계산
    products = Product.objects.filter(sub_category=sub_category)
    product_scores = calculate_product_scores(products, matching_aspects, aspect_polarity, product_name=product_name)

    # 상품 정렬 및 직렬화
    recommendations = serialize_sorted_products(product_scores, matching_aspects, aspect_polarity)

    return Response(recommendations, status=status.HTTP_200_OK)


def analyze_condition_with_absa(condition):
    results = settings.ABSA_MODEL.test(condition)
    matching_aspects = []
    aspect_polarity = {}

    # 분석 결과 파싱 (긍정 또는 부정에 따라 검색 조건 설정)
    for aspect, data in results.items():
        matching_aspects.append(aspect)
        aspect_polarity[aspect] = {
            "polarity": data["polarity"],   # 긍정(1) 또는 부정(0)
            "counts": data["counts"]
        }
    return matching_aspects, aspect_polarity


# 상품 필터링 및 점수 계산
def calculate_product_scores(products, matching_aspects, aspect_polarity, product_name=None):
    # `product_name` 필터링 추가
    if product_name:
        products = products.filter(name__icontains=product_name)  # 제품 이름에 `product_name` 포함 여부로 필터링
    
    product_scores = {}

    for product in products:
        total_score = 0
        aspect_counts = {}
        aspect_reviews = {}
        seen_review_ids = set()

        for review in product.reviews.all():
            for review_aspect in review.review_aspects.all():
                if review_aspect.aspect.aspect in matching_aspects:
                    aspect_data = aspect_polarity[review_aspect.aspect.aspect]
                    
                    # 긍정/부정 가중치 계산
                    if review_aspect.sentiment_polarity == 1:
                        total_score += aspect_data["counts"]["긍정"]
                    elif review_aspect.sentiment_polarity == -1:
                        total_score += aspect_data["counts"]["부정"]

                    # aspect별 긍정/부정 개수 누적
                    if review_aspect.aspect.aspect not in aspect_counts:
                        aspect_counts[review_aspect.aspect.aspect] = {
                            "긍정": 0,
                            "부정": 0
                        }
                    aspect_counts[review_aspect.aspect.aspect]["긍정"] += aspect_data["counts"]["긍정"]
                    aspect_counts[review_aspect.aspect.aspect]["부정"] += aspect_data["counts"]["부정"]
                    
                    # 제품 관련 리뷰
                    if review_aspect.aspect.id not in aspect_reviews:
                        aspect_reviews[review_aspect.aspect.id] = {
                            "aspect_id": review_aspect.aspect.id,
                            "aspect_name": review_aspect.aspect.aspect,
                            "reviews": []
                        }

                    expected_polarity = 1 if aspect_data["polarity"] == 1 else -1  # 부정은 -1로 변환
                    if (
                        review.id not in seen_review_ids and 
                        review_aspect.sentiment_polarity == expected_polarity  # 조건에 맞는 리뷰
                    ):
                        aspect_reviews[review_aspect.aspect.id]["reviews"].append({
                            "review_id": review.id,
                            "raw_text": review.raw_text,  # 리뷰 내용
                            "sentiment_polarity": review_aspect.sentiment_polarity  # 긍정(1) 또는 부정(0)
                        })
                        seen_review_ids.add(review.id)  # 중복 방지용 ID 저장

        matching_reviews = list(aspect_reviews.values())

        # 상품별 총 점수 저장
        if total_score > 0:
            product_scores[product.id] = {
                "product": product,
                "score": total_score,
                "aspect_counts": aspect_counts,
                "matching_reviews": matching_reviews,
            }
    return product_scores


# 상품 정렬 및 직렬화
def serialize_sorted_products(product_scores, matching_aspects, aspect_polarity):
    sorted_products = sorted(
        product_scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )
    return {
        "aspects": {
            aspect: "긍정" if aspect_polarity[aspect]["polarity"] == 1 else "부정"
            for aspect in matching_aspects
        },
        "products": [
            {
                "product": ProductSerializer(entry["product"]).data,
                "score": entry["score"],
                "aspect_counts": entry["aspect_counts"],
                "matching_reviews": entry["matching_reviews"],
            }
            for entry in sorted_products[:5]
        ]
    }


@api_view(['GET'])
def product_aspect_ratio(request, product_id):
    try:
        # 상품 가져오기
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # 상품의 리뷰와 속성 데이터 가져오기
    aspect_data = {}
    for review in product.reviews.all():
        for review_aspect in review.review_aspects.all():
            aspect_name = review_aspect.aspect.aspect
            if aspect_name not in aspect_data:
                aspect_data[aspect_name] = {"긍정": 0, "부정": 0, "총합": 0}
            if review_aspect.sentiment_polarity == 1:
                aspect_data[aspect_name]["긍정"] += 1
            else:
                aspect_data[aspect_name]["부정"] += 1
            aspect_data[aspect_name]["총합"] += 1

    # 속성을 리뷰 수 기준으로 정렬 후 상위 5개 선택
    sorted_aspects = sorted(
        aspect_data.items(),
        key=lambda item: item[1]["총합"],
        reverse=True
    )[:5]

    # 긍정/부정 비율 계산
    aspect_ratios = [
        {
            "aspect": aspect,
            "positive_ratio": f"{(data['긍정'] / data['총합'] * 100):.2f}" if data['총합'] > 0 else "0.00",
            "negative_ratio": f"{(data['부정'] / data['총합'] * 100):.2f}" if data['총합'] > 0 else "0.00",
            "total_reviews": data["총합"]
        }
        for aspect, data in sorted_aspects
    ]

    # 응답 반환
    return Response({"product_id": product_id, "aspect_ratios": aspect_ratios}, status=status.HTTP_200_OK)