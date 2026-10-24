from django.shortcuts import render

# Create your views here.

from datetime import date

from django.shortcuts import render


def calculate_age(birth_date, today):
    """
    Return the age in completed years, months, and days.
    """
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1

        # Get the number of days in the previous month.
        if today.month == 1:
            previous_month = 12
            previous_month_year = today.year - 1
        else:
            previous_month = today.month - 1
            previous_month_year = today.year

        days_in_previous_month = (
            date(previous_month_year, previous_month + 1, 1)
            - date(previous_month_year, previous_month, 1)
        ).days if previous_month < 12 else (
            date(previous_month_year + 1, 1, 1)
            - date(previous_month_year, 12, 1)
        ).days

        days += days_in_previous_month

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def home(request):
    context = {
        "today": date.today().isoformat(),
        "birth_date": "",
        "age": None,
        "error": None,
    }

    if request.method == "POST":
        birth_date_str = request.POST.get("birth_date", "").strip()
        context["birth_date"] = birth_date_str

        try:
            birth_date = date.fromisoformat(birth_date_str)

            if birth_date > date.today():
                context["error"] = (
                    "Date of birth cannot be in the future."
                )
            else:
                years, months, days = calculate_age(
                    birth_date, date.today()
                )

                context["age"] = {
                    "years": years,
                    "months": months,
                    "days": days,
                    "total_days": (date.today() - birth_date).days,
                }

        except (ValueError, TypeError):
            context["error"] = (
                "Please enter a valid date of birth."
            )

    return render(request, "calculator.html", context)
