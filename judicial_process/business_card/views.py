from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from .models import (
                    BusinessCard, Category,
                    SidesCase, SidesCaseInCase,
                    BusinessMovement, PetitionsInCase)

from .forms import (CardForm, SideForm, SidesCaseInCaseForm,
                    MovementForm, PetitionsInCaseForm)
from .utils import paginator_list


POSTS_NUMBER = 6

User = get_user_model()


# Главная страница
def index(request):
    template = 'index.html'
    title = 'Первый проект. Главная страница'
    business_card = BusinessCard.objects.select_related(
        'case_category', 'author'
        )
    sides_case_in_case_data = SidesCaseInCase.objects.all()
    decision_case_data = BusinessMovement.objects.all()
    petition_case_data = PetitionsInCase.objects.all()
    cards = BusinessCard.objects.select_related('case_category', 'author')
    page_obj = paginator_list(request, cards)
    context = {
        'title': title,
        'text': 'Главная страница',
        'business_card': business_card,
        'page_obj': page_obj,
        'sides_case_in_case_data': sides_case_in_case_data,
        'decision_case_data': decision_case_data,
        'petition_case_data': petition_case_data,
    }
    return render(request, template, context)


def business_card(request, slug):
    '''Карточка дела'''
    template = 'business_card'
    category = get_object_or_404(Category, slug=slug)
    title = 'Здесь будет информация о категориях'
    cards = category.objects.select_related('case_category')
    page_obj = paginator_list(request, cards)
    context = {
        'title': title,
        'category': category,
        'cards': cards,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def business_card_detail(request, card_id):
    '''страница подробней о карточке'''
    card = get_object_or_404(BusinessCard, pk=card_id)
    sides_case_in_case_data = SidesCaseInCase.objects.filter(
        business_card=card
    )
    decision_case_data = BusinessMovement.objects.filter(
        business_card=card
    )
    author = card.author
    author_card = author.cards.count()
    context = {
        'card': card,
        'author': author,
        'author_card': author_card,
        'sides_case_in_case_data': sides_case_in_case_data,
        'decision_case_data': decision_case_data,
    }
    return render(request, 'business_card_detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    cards = author.cards.select_related('case_category')
    page_obj = paginator_list(request, cards)
    context = {
        'author': author,
        'cards': cards,
        'page_obj': page_obj,
    }
    return render(request, 'profile.html', context)


@login_required
def card_create(request):
    '''Шаблон создание карточки'''
    template = 'create_card.html'
    form = CardForm(request.POST or None)
    if form.is_valid():
        card = form.save(commit=False)
        card.author = request.user
        card.save()
        form = CardForm()
        return redirect('business_card:profile', request.user)
    return render(request, template, {'form': form})


@login_required
def card_edit(request, post_id):
    '''Шаблон редактирования карточки'''
    card = get_object_or_404(
        BusinessCard.objects.select_related(
            'case_category', 'author'), id=post_id
    )
    if request.user != card.author:
        return redirect('business_card:business_card_detail', card.pk)
    form = CardForm(request.POST or None, instance=card)
    if form.is_valid():
        form.save()
        return redirect('business_card:business_card_detail', card.pk)
    form = CardForm(instance=card)
    context = {
        'form': form,
        'is_edit': True,
        'card': card,
    }
    return render(request, 'create_card.html', context)


@login_required
def add_side(request, card_id):
    '''Шаблон добавления сторон'''
    card = get_object_or_404(
        BusinessCard.objects.select_related(
            'case_category', 'author'), id=card_id
    )
    side = get_object_or_404(SidesCase, id=card_id)
    if request.method == 'POST':
        form = SideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_card:business_card_detail', card.pk)
    else:
        form = SideForm()
    context = {
        'form': form,
        'card': card,
        'side': side,
    }
    return render(request, 'add_side.html', context)


@login_required
def edit_side(request, side_case_id):
    '''Шаблон редактирования сторон'''
    side_case = get_object_or_404(SidesCaseInCase, pk=side_case_id)

    if request.method == 'POST':
        form = SidesCaseInCaseForm(request.POST, instance=side_case)
        if form.is_valid():
            form.save()
            return redirect(
                'business_card:business_card_detail',
                card_id=side_case.business_card.id
            )
    else:
        form = SidesCaseInCaseForm(instance=side_case)

    context = {
        'form': form,
        'is_edit': True,
        'side_case': side_case,
    }

    return render(request, 'add_side.html', context)


@login_required
def delete_side(request, side_case_id):
    '''Шаблон удаления стороны по делу'''
    side_case = get_object_or_404(SidesCaseInCase, pk=side_case_id)

    # Проверяем, что текущий пользователь имеет право удалять сторону
    if request.user != side_case.business_card.author:
        return HttpResponseBadRequest("Вы не можете удалить эту сторону.")

    if request.method == 'POST':
        side_case.delete()
        return redirect(
            'business_card:business_card_detail',
            card_id=side_case.business_card.id
        )

    context = {
        'side_case': side_case,
    }

    return render(request, 'delete_side.html', context)


@login_required
def add_movement(request, decision_case_id):
    '''Шаблон добавления движения дела'''
    card = get_object_or_404(
        BusinessCard.objects.select_related(
            'case_category', 'author'), id=decision_case_id
    )
    # side = get_object_or_404(SidesCase, id=card_id)
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_card:business_card_detail', card.pk)
    else:
        form = MovementForm()
    context = {
        'form': form,
        'card': card,
    }
    return render(request, 'add_movement.html', context)


@login_required
def edit_movement(request, decision_case_id):
    '''Шаблон редактирования движения дела'''
    decision_case = get_object_or_404(BusinessMovement, pk=decision_case_id)

    if request.method == 'POST':
        form = MovementForm(request.POST, instance=decision_case)
        if form.is_valid():
            form.save()
            return redirect(
                'business_card:business_card_detail',
                card_id=decision_case.business_card.id
            )
    else:
        form = MovementForm(instance=decision_case)

    context = {
        'form': form,
        'is_edit': True,
        'side_case': decision_case,
    }

    return render(request, 'add_side.html', context)


@login_required
def delete_movement(request, decision_case_id):
    '''Шаблон удаления движения дела'''
    decision_case = get_object_or_404(BusinessMovement, pk=decision_case_id)

    if request.user != decision_case.business_card.author:
        return HttpResponseBadRequest("Вы не можете удалить эту запись.")

    if request.method == 'POST':
        decision_case.delete()
        return redirect(
            'business_card:business_card_detail',
            card_id=decision_case.business_card.id
        )

    context = {
        'decision_case': decision_case,
    }

    return render(request, 'delete_movement.html', context)


@login_required
def add_petition(request, card_id):
    '''Шаблон добавления ходатайства'''
    card = get_object_or_404(
        BusinessCard.objects.select_related(
            'case_category', 'author'), id=card_id
    )
    if request.method == 'POST':
        form = PetitionsInCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_card:business_card_detail', card.pk)
    else:
        form = PetitionsInCaseForm()
    context = {
        'form': form,
        'card': card,
    }
    return render(request, 'add_petition.html', context)


@login_required
def edit_petition(request, petition_case_id):
    '''Шаблон редактирования ходатайства'''
    petition_case = get_object_or_404(PetitionsInCase, pk=petition_case_id)

    if request.method == 'POST':
        form = PetitionsInCaseForm(request.POST, instance=petition_case)
        if form.is_valid():
            form.save()
            return redirect(
                'business_card:business_card_detail',
                card_id=petition_case.business_card.id
            )
    else:
        form = PetitionsInCaseForm(instance=petition_case)

    context = {
        'form': form,
        'is_edit': True,
        'petition_case': petition_case,
    }

    return render(request, 'add_petition.html', context)


@login_required
def delete_petition(request, petition_case_id):
    '''Шаблон удаления ходатайства'''
    petition_case = get_object_or_404(PetitionsInCase, pk=petition_case_id)

    if request.user != petition_case.business_card.author:
        return HttpResponseBadRequest("Вы не можете удалить эту запись.")

    if request.method == 'POST':
        petition_case.delete()
        return redirect(
            'business_card:business_card_detail',
            card_id=petition_case.business_card.id
        )

    context = {
        'petition_case': petition_case,
    }

    return render(request, 'delete_petition.html', context)
