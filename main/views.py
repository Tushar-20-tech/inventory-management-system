import json
from django.shortcuts import render, redirect
from .models import UserProfile
from .models import Product
from django.db.models import Sum
from .models import StockIn
from .models import StockOut
from collections import Counter

def home(request):
    return render(request, "index.html")


def signup_view(request):

    if request.method == "POST":

        company = request.POST.get("company")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        country = request.POST.get("country")
        state = request.POST.get("state")
        profile = request.FILES.get("profile")

        # JPG validation

        if profile and not profile.name.lower().endswith(".jpg"):

            return render(request,
                          "signup.html",
                          {"error": "Only JPG format allowed"})

        user = UserProfile.objects.create(

            company_name=company,
            email=email,
            phone=phone,
            password=password,
            country=country,
            state=state,
            profile_image=profile

        )

        return render(request,
                      "signup_success.html",
                      {"company": company})

    return render(request, "signup.html")

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(email=email)

            if user.password == password:

                request.session["user_id"] = user.id
                return redirect("dashboard")

            else:
                return render(
                    request,
                    "login.html",
                    {"error_type": "password"}
                )

        except UserProfile.DoesNotExist:

            return render(
                request,
                "login.html",
                {"error_type": "nouser"}
            )

    return render(request, "login.html")

def dashboard(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")


    user = UserProfile.objects.get(id=user_id)

    products = Product.objects.filter(user=user)


    total_products = products.count()

    total_stock = products.aggregate(
        Sum("quantity")
    )["quantity__sum"] or 0


    low_stock_products = products.filter(quantity__lt=5)

    low_stock = low_stock_products.count()


    # SMART QUICK INFO ENGINE

    if low_stock == 0:

        quick_message = "Inventory levels look healthy ✅"

    elif low_stock <= 2:

        quick_message = "⚠ Some products running low — restock soon"

    else:

        quick_message = "🚨 Multiple products critically low — immediate action required"


    # 📊 BAR GRAPH DATA FOR DASHBOARD ANALYTICS

    product_names = json.dumps(
        list(products.values_list("name", flat=True))
    )

    product_quantities = json.dumps(
        list(products.values_list("quantity", flat=True))
    )


    context = {

        "user": user,
        "products": products,

        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock": low_stock,

        "low_stock_products": low_stock_products,

        "quick_message": quick_message,

        # chart analytics data
        "product_names": product_names,
        "product_quantities": product_quantities,
    }


    return render(request, "dashboard.html", context)

def add_product(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":

        user = UserProfile.objects.get(id=user_id)

        Product.objects.create(

            user=user,

            name=request.POST.get("name"),

            category=request.POST.get("category"),

            quantity=request.POST.get("quantity"),

            price=request.POST.get("price"),

            supplier=request.POST.get("supplier")

        )

        return redirect("products")

    return redirect("products")

def delete_product(request, product_id):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    Product.objects.get(
        id=product_id,
        user_id=user_id
    ).delete()

    return redirect("products")

def edit_product(request, product_id):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    product = Product.objects.get(
        id=product_id,
        user_id=user_id
    )

    if request.method == "POST":

        product.name = request.POST.get("name")

        product.category = request.POST.get("category")

        product.quantity = request.POST.get("quantity")

        product.price = request.POST.get("price")

        product.supplier = request.POST.get("supplier")

        product.save()

        return redirect("products")

    return render(
        request,
        "edit_product.html",
        {"product": product}
    )


def stock_in_view(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = UserProfile.objects.get(id=user_id)

    products = Product.objects.filter(user=user)


    if request.method == "POST":

        product_id = request.POST.get("product")

        quantity_added = int(
            request.POST.get("quantity_added")
        )

        supplier = request.POST.get("supplier")

        invoice_number = request.POST.get("invoice_number")

        date = request.POST.get("date")

        notes = request.POST.get("notes")


        product = Product.objects.get(
            id=product_id,
            user=user
        )


        # update product quantity automatically
        product.quantity += quantity_added
        product.save()


        # save stock entry history
        StockIn.objects.create(

            user=user,

            product=product,

            quantity_added=quantity_added,

            supplier=supplier,

            invoice_number=invoice_number,

            date=date,

            notes=notes

        )


        return redirect("stock_in")


    stock_history = StockIn.objects.filter(
        user=user
    ).order_by("-id")


    return render(

        request,

        "stock_in.html",

        {

            "products": products,

            "stock_history": stock_history,

            "user": user

        }

    )


def stock_out_view(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = UserProfile.objects.get(id=user_id)

    products = Product.objects.filter(user=user)

    stock_history = StockOut.objects.filter(
        user=user
    ).order_by("-id")


    if request.method == "POST":

        product_id = request.POST.get("product")

        quantity_removed = int(
            request.POST.get("quantity_removed")
        )

        customer = request.POST.get("customer")

        invoice_number = request.POST.get("invoice_number")

        date = request.POST.get("date")

        reason = request.POST.get("reason")


        if not date:

            return render(

                request,

                "stock_out.html",

                {

                    "products": products,

                    "stock_history": stock_history,

                    "error": "Please select removal date 📅"

                }

            )


        product = Product.objects.get(
            id=product_id,
            user=user
        )


        # STOCK VALIDATION

        if quantity_removed > product.quantity:

            return render(

                request,

                "stock_out.html",

                {

                    "products": products,

                    "stock_history": stock_history,

                    "error": f"Only {product.quantity} items available ⚠️"

                }

            )


        # REDUCE STOCK

        product.quantity -= quantity_removed
        product.save()


        # SAVE HISTORY

        StockOut.objects.create(

            user=user,

            product=product,

            quantity_removed=quantity_removed,

            customer=customer,

            invoice_number=invoice_number,

            date=date,

            reason=reason

        )


        return redirect("stock_out")


    return render(

        request,

        "stock_out.html",

        {

            "products": products,

            "stock_history": stock_history

        }

    )

def profile_view(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = UserProfile.objects.get(id=user_id)

    return render(request, "profile.html", {
        "user": user
    })

def delete_account(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = UserProfile.objects.get(id=user_id)

    user.delete()

    request.session.flush()

    return redirect("signup")

def products_view(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = UserProfile.objects.get(id=user_id)

    products = Product.objects.filter(user=user)

    return render(

        request,

        "products.html",

        {

            "products": products,

            "user": user

        }

    )


def reports_view(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")


    products = Product.objects.filter(user_id=user_id)
    stock_in = StockIn.objects.filter(user_id=user_id)
    stock_out = StockOut.objects.filter(user_id=user_id)


    total_products = products.count()

    total_stock = products.aggregate(
        Sum("quantity")
    )["quantity__sum"] or 0


    low_stock_products = products.filter(quantity__lt=5)


    total_stock_in = stock_in.aggregate(
        Sum("quantity_added")
    )["quantity_added__sum"] or 0


    total_stock_out = stock_out.aggregate(
        Sum("quantity_removed")
    )["quantity_removed__sum"] or 0


    # CATEGORY DISTRIBUTION LOGIC

    category_counter = Counter(
        products.values_list("category", flat=True)
    )


    category_labels = json.dumps(
        list(category_counter.keys())
    )


    category_values = json.dumps(
        list(category_counter.values())
    )


    context = {

        "products": products,
        "stock_in": stock_in,
        "stock_out": stock_out,

        "low_stock_products": low_stock_products,

        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock": low_stock_products.count(),

        "total_stock_in": total_stock_in,
        "total_stock_out": total_stock_out,

        "category_labels": category_labels,
        "category_values": category_values,
    }


    return render(
        request,
        "reports.html",
        context
    )


def how_to_use_view(request):

    if not request.session.get("user_id"):
        return redirect("login")

    return render(request, "how_to_use.html")