from auctions.models import Category

def extras(request):
    categories = Category.objects.order_by('name').all()
    return {'categories': categories}