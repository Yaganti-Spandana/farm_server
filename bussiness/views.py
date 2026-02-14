from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "User created"}, status=201)
    return Response(serializer.errors, status=400)

from rest_framework import viewsets
from .models import Animal
from .serializers import AnimalSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

from .models import MilkRecord
from .serializers import MilkRecordSerializer

class MilkRecordViewSet(viewsets.ModelViewSet):
    queryset = MilkRecord.objects.all().order_by('-date')
    serializer_class = MilkRecordSerializer

from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-date')
    serializer_class = SaleSerializer

from rest_framework import viewsets
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date')
    serializer_class = ExpenseSerializer

from rest_framework import viewsets
from .models import FeedStock, FeedUsage
from .serializers import FeedStockSerializer, FeedUsageSerializer

class FeedStockViewSet(viewsets.ModelViewSet):
    queryset = FeedStock.objects.all().order_by('-date')
    serializer_class = FeedStockSerializer

class FeedUsageViewSet(viewsets.ModelViewSet):
    queryset = FeedUsage.objects.all().order_by('-date')
    serializer_class = FeedUsageSerializer

from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def feed_remaining(request):
    stock = FeedStock.objects.values('feed_type').annotate(
        total_in=Sum('quantity_in')
    )
    usage = FeedUsage.objects.values('feed_type').annotate(
        total_used=Sum('quantity_used')
    )

    result = {}
    for s in stock:
        feed = s['feed_type']
        used = next((u['total_used'] for u in usage if u['feed_type'] == feed), 0)
        result[feed] = s['total_in'] - (used or 0)

    return Response(result)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Sale
from .models import Expense

@api_view(['GET'])
def profit_loss(request):
    total_income = Sale.objects.aggregate(
        Sum('total_income')
    )['total_income__sum'] or 0

    total_expenses = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    profit = total_income - total_expenses

    return Response({
        "total_income": total_income,
        "total_expenses": total_expenses,
        "profit": profit
    })

from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def monthly_report(request):
    start = request.GET.get("from")
    end = request.GET.get("to")
    animal_id = request.GET.get("animal")

    milk_qs = MilkRecord.objects.all()
    sales_qs = Sale.objects.all()
    expense_qs = Expense.objects.all()

    if start and end:
        milk_qs = milk_qs.filter(date__range=[start, end])
        sales_qs = sales_qs.filter(date__range=[start, end])
        expense_qs = expense_qs.filter(date__range=[start, end])

    if animal_id:
        milk_qs = milk_qs.filter(animal_id=animal_id)

    total_milk = milk_qs.aggregate(Sum("total_milk"))["total_milk__sum"] or 0
    milk_sold = milk_qs.aggregate(Sum("milk_sold"))["milk_sold__sum"] or 0
    total_income = sales_qs.aggregate(Sum("total_income"))["total_income__sum"] or 0
    total_expenses = expense_qs.aggregate(Sum("amount"))["amount__sum"] or 0

    # 🔥 THIS IS THE IMPORTANT PART
    expenses_by_category = (
        expense_qs
        .values("category")
        .annotate(total=Sum("amount"))
    )

    profit = total_income - total_expenses

    return Response({
        "total_milk": total_milk,
        "milk_sold": milk_sold,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "profit": profit,
        "expenses_by_category": expenses_by_category
    })
