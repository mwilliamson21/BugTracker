from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from bugtracker.forms import login_form, Create_ticket_form
from bugtracker.models import Ticket


@login_required
def index(request):
    html = 'index.html'
    new = Ticket.objects.filter(
        status='New').order_by('-post_date')
    in_progress = Ticket.objects.filter(
        status='In Progress').order_by('-post_date')
    done = Ticket.objects.filter(
        status='Done').order_by('-post_date')
    invalid = Ticket.objects.filter(
        status='Invalid').order_by('-post_date')
    return render(request, html, {
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
    })


@login_required
def create_ticket_form_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = Create_ticket_form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                status=data['status'],
                filed_by=request.user,
            )
            return HttpResponseRedirect(reverse('homepage'))
    # this is for GET requests, serves the blank form and renders it
    form = Create_ticket_form()
    return render(request, html, {'form': form})


def login_view(request):
    html = "generic_form.html"

    if request.method == "POST":
        form = login_form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = login_form()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def user_view(request, id):
    html = 'user.html'
    created = Ticket.objects.filter(created_by=id)
    assigned = Ticket.objects.filter(assigned_by=id)
    completed = Ticket.objects.filter(completed_by=id)

    return render(request, html,
                  {'created': created, 'assigned': assigned,
                   'completed': completed})


@login_required
def ticket_detail_view(request, id):
    html = 'ticket.html'
    ticket = Ticket.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


@login_required
def ticket_edit_view(request, id):
    html = 'generic_form.html'

    instance = Ticket.objects.get(id=id)

    if request.method == 'POST':
        form = Create_ticket_form(
            request.POST,
            instance=instance
            )
        form.save()

        if instance.status == 'Done':
            instance.completed_by = instance.assigned_by
            instance.assigned_by = None
            form.save()
        elif instance.status == 'Invalid':
            instance.assigned_by = None
            instance.completed_by = None
            form.save()
        elif instance.status == 'In Progress':
            instance.assigned_by = None
            instance.assigned_by = instance.filed_by
            instance.completed_by = None
            form.save()
        elif instance.assigned_by is not None:
            instance.status = 'In Progress'
            instance.completed_by = None
            form.save()
        return HttpResponseRedirect(reverse('homepage'))

    form = Create_ticket_form(instance=instance)
    return render(request, html, {'form': form})
