
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .views import calculate_age


@api_view(['POST'])
def calculate_age_api(request):

    birth_date_str = request.data.get('birth_date')

    if not birth_date_str:
        return Response(
            {"error": "Birth date is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        birth_date = date.fromisoformat(birth_date_str)

        today = date.today()

        if birth_date > today:
            return Response(
                {"error": "Birth date cannot be in the future"},
                status=status.HTTP_400_BAD_REQUEST
            )

        years, months, days = calculate_age(
            birth_date, today
        )

        return Response({
            "years": years,
            "months": months,
            "days": days,
            "total_days": (today - birth_date).days
        })

    except (ValueError, TypeError):
        return Response(
            {"error": "Enter a valid date in YYYY-MM-DD format"},
            status=status.HTTP_400_BAD_REQUEST
        )
