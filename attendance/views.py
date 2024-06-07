from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, schema
from rest_framework.parsers import JSONParser
from .models import  Employee, Attendance_Record
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Employee, Attendance_Record

# @login_required(login_url='/attendance/accounts/login/')
@api_view(['GET', 'POST'])
def checkIn(request):
    card_id = request.data.get('id')
    print(card_id)

    if request.method == 'GET':
        return Response({"message": "I am GET"})

    if request.method == 'POST':
        try:
            # Check if an employee with the given card ID exists
            employee = Employee.objects.get(card_id=card_id)

            # Check if an attendance record already exists for this employee
            existing_record = Attendance_Record.objects.filter(card_id=employee, status='In',).exists()
           
            if existing_record:
                print("message: Attendance record already exists for this employee.")
                return Response({"message": "Attendance record already exists for this employee."})

            # Create a new attendance record
            Attendance_Record.objects.create(
                status='In',  # Set the appropriate status
                entrance_time=datetime.now(),  # Set the entrance time
                card_id=employee,
            )

            messages.success(request, 'Record successfully entered!')
            return Response({"message": "Attendance record added successfully."})
        except Employee.DoesNotExist:
            # Handle case when employee does not exist
            return Response({"message": "Employee does not exist."})

    return Response({"message": "Checking in."})

def success(request):
    return  render(request, 'success.html')

# @login_required(login_url='/attendance/accounts/login/')
@api_view(['GET', 'POST'])
def checkOut(request):
    
    card_id = request.data.get('id', None)  # Replace with actual field name

    print(card_id)

    if request.method == 'POST':
        try:
            # Check if an employee with the given card ID exists
            employee = Employee.objects.get(card_id=card_id)

            attendance_records = Attendance_Record.objects.filter(card_id=employee).order_by('-entrance_time').first()

            if attendance_records:

                print(card_id)

                # Get the first attendance record associated with this employee
                attendance_records.status = 'Out'
                attendance_records.exit_time = timezone.now()
                attendance_records.save()
        
                
                return Response({"message": "Attendance record deleted successfully."})
            else:
                # Handle case when no attendance record found
                return Response({"message": "Attendance record not found."})
        except Employee.DoesNotExist:
            # Handle case when employee does not exist
            return Response({"message": "Employee does not exist."})

    return Response({"message": "Checking out."})

def error(request):
    return render(request, 'error.html')

@login_required(login_url='/attendance/accounts/login/')
def HomeAttendance(request):
    employees = Employee.objects.all()
    attendance_records = Attendance_Record.objects.exclude(exit_time__isnull=False).order_by('entrance_time').reverse()

    

    
        
    # data = JSONParser().parse(request)

    # id = data['id']
    # print(type(data))

    # if request.method == 'POST':
       
    #     return Response(data)
    
    # return Response({"message" : "jhdjhsdjs"})
    return  render(request, 'index.html', {'employees': employees, 'attendance_records' : attendance_records })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the login page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



