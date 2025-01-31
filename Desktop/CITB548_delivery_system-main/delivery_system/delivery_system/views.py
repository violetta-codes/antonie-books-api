from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileEditForm

@login_required
def home(request):
    context = {
        'user_is_employee': request.user.employee,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_account')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/edit_account.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Package, CustomUser, Office

@csrf_exempt
@login_required
def submit_package_api(request):
    if not request.user.employee:  # Only employees can submit
        return JsonResponse({"error": "Access denied. Only employees can submit packages."}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            receiver_id = data.get('receiver')
            delivery_address = data.get('delivery_address', None)
            office_id = data.get('office', None)
            weight = data.get('weight')
            delivery_type = data.get('delivery_type')
            content = data.get('content')

            try:
                receiver = CustomUser.objects.get(id=receiver_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "Receiver not found."}, status=400)

            office = None
            if office_id:
                try:
                    office = Office.objects.get(id=office_id)
                except Office.DoesNotExist:
                    return JsonResponse({"error": "Office not found."}, status=400)

            if delivery_type not in ['office', 'address']:
                return JsonResponse({"error": "Invalid delivery type."}, status=400)

            package = Package.objects.create(
                sender=request.user,
                receiver=receiver,
                delivery_address=delivery_address,
                office=office,
                weight=weight,
                delivery_type=delivery_type,
                content=content,
                status='submitted'
            )

            return JsonResponse({"message": "Package submitted successfully!", "package_id": package.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)
