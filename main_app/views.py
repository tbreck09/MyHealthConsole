import uuid
import boto3
import os
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib import messages

# auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#
from .models import Care_provider, Prescription, Photo, User, Appointment
from .forms import AppointmentForm, UpdateUserForm, AppointmentUpdateForm

# Create your views here.


@login_required
def password_change_view(request):
    pass


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('form validated')
            login(request, user)
            return redirect(reverse('users_detail', kwargs={'user_id': user.id}))
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def delete_photo(request, photo_id, user_id):
    photo = Photo.objects.get(id=photo_id)
    if request.user.id == photo.user_id:
        photo.delete()
        return redirect('users_detail', user_id=user_id)


@login_required
def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    try:
        current_photo = Photo.objects.get(user_id=request.user.id)
        current_photo.delete()
    except Photo.DoesNotExist:
        pass
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"

            Photo.objects.create(url=url, user_id=user_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('users_detail', user_id=user_id)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def care_provider_detail(request, care_provider_id):
    care_provider = Care_provider.objects.get(id=care_provider_id)
    return render(request, 'care_providers/detail.html', {
        'care_provider': care_provider
    })


@login_required
def prescription_detail(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    return render(request, 'prescriptions/detail.html', {
        'prescription': prescription
    })


@login_required
def appointment_detail(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'appointment_detail.html', {
        'appointment': appointment
    })


@login_required
def care_providers_index(request):
    care_providers = Care_provider.objects.filter(users=request.user)
    # care_providers = request.user.care_provider_set.all()
    print(care_providers)
    return render(request, 'care_providers/index.html', {'care_providers': care_providers})


@login_required
def users_detail(request, user_id):
    care_providers = Care_provider.objects.filter(users=request.user)

    if len(care_providers) <= 0:
        care_providers = None
        print('no docs found')
        error_msg = 'No appointments to show.'
        messages.error(request, error_msg)

    try:
        prescriptions = Prescription.objects.filter(user=request.user)
    except Prescription.DoesNotExist:
        prescriptions = None

    # Initialize appointment_form conditionally with care_provider_choices
    appointment_form = None
    if care_providers is not None and len(care_providers) > 0:
        appointment_form = AppointmentForm(
            care_provider_choices=care_providers)

    return render(request, 'users/detail.html', {
        'care_providers': care_providers,
        'appointment_form': appointment_form,
        'prescriptions': prescriptions,
    })


@login_required
def prescription_index(request):
    prescriptions = Prescription.objects.filter(user_id=request.user.id)
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})


class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['name', 'description', 'instructions', 'date_issued']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    model = Prescription
    fields = ['name', 'description', 'instructions', 'date_issued']


class CareProviderCreate(LoginRequiredMixin, CreateView):
    model = Care_provider
    fields = ['name', 'facility', 'department']

    def form_valid(self, form):
        valid_form = form.save()
        valid_form.users.add(self.request.user)

        return super().form_valid(form)


class CareProviderUpdate(LoginRequiredMixin, UpdateView):
    model = Care_provider
    fields = ['name', 'facility', 'department']
    success_url = '/care_providers'


class CareProviderDelete(LoginRequiredMixin, DeleteView):
    model = Care_provider
    success_url = '/care_providers'


class UsersDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = '/care_providers'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        care_provider = user.care_provider

        if care_provider is not None:
            care_provider.delete()

        return super().delete(request, *args, **kwargs)


class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentUpdateForm
    template_name = 'update_appointment.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Appointment'
        care_providers = Care_provider.objects.filter(users=self.request.user)
        context['appointment_update_form'] = AppointmentUpdateForm(
            care_provider_choices=care_providers,
            instance=self.object
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the appointment instance
        form = self.get_form()

        # Get care providers for the current user and pass it to the form
        care_providers = Care_provider.objects.filter(users=self.request.user)
        form.fields['care_provider'].queryset = care_providers

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def add_appointment(request, user_id):
    care_providers = Care_provider.objects.filter(users=request.user)

    form = AppointmentForm(request.POST, care_provider_choices=care_providers)

    if form.is_valid():
        new_appointment = form.save(commit=False)
        new_appointment.user_id = user_id
        new_appointment.save()
        return redirect('users_detail', user_id=user_id)
    else:
        error_msg = 'A care provider is required to create appointments!'
        messages.error(request, error_msg)
        return redirect('users_detail', user_id=user_id)


@login_required
def delete_appointment(request, appointment_id, user_id):
    try:
        appointment = Appointment.objects.get(
            id=appointment_id, user=request.user)
        print(appointment)
        appointment.delete()
    except Appointment.DoesNotExist:
        pass

    return redirect('users_detail', user_id=user_id)


@login_required
def delete_prescription(request, prescription_id, user_id):
    try:
        prescription = Prescription.objects.get(
            id=prescription_id, user=request.user)
        prescription.delete()
    except Prescription.DoesNotExist:
        pass

    return redirect('prescription_index')


# delete not working correctly


def update_user(request, user_id):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            # Redirect to the user's profile page
            return redirect('users_detail', user_id=user_id)
    else:
        user_form = UpdateUserForm(instance=request.user, )

    return render(request, 'update_user.html', {'user_form': user_form})
