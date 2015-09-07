"""Pystagram MVP version tests.
Usage : python manage.py test
"""
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.contrib.auth.decorators import login_required

from .models import (
    Photo,
    Comment,
)
from .forms import (
    PhotoForm,
    CommentForm,
)


def list_photo(request):
    """사진을 목록으로 나열합니다.
    """
    # todo
    photos = Photo.objects.all()

    return render(request, 'mvp/list_photo.html', {
        'photos': photos,
    })

@login_required()
def create_photo(request):
    """새 사진을 게시합니다.
    """
    status_code = 200
    # todo
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect("mvp.views.detail_photo", photo.pk)
        else:
            return render(request, 'mvp/create_photo.html', {
                'form': form,
            }, status=400)
    else:
        form = PhotoForm()

    return render(request, 'mvp/create_photo.html', {
        'form': form,
    }, status=status_code)


def detail_photo(request, pk):
    """개별 사진과 사진에 달린 댓글을 보여줍니다.
    :param str pk: photo primary key.
    """
    # todo
    photo = get_object_or_404(Photo, pk=pk)

    return render(request, 'mvp/detail_photo.html', {
        'photo': photo,
    })

@login_required()
def delete_photo(request, pk):
    """지정한 사진을 지웁니다.
    :param str pk: photo primary key.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed('not allowed method')
    # todo
    photo = get_object_or_404(Photo, pk=pk)

    # todo : 남의 사진을 권한없이 지우려하는 경우.
    if photo.user != request.user:
        return HttpResponseForbidden('required permission to delete')

    # todo
    photo.delete()

    return redirect('mvp.views.list_photo')

@login_required()
def create_comment(request, pk):
    """지정한 사진에 댓글을 추가합니다.
    :param str pk: photo primary key.
    """
    status_code = 200
    # todo
    photo = get_object_or_404(Photo, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = get_object_or_404(Photo, pk=pk)
            comment.user = request.user
            comment.save()
            return redirect("mvp.views.detail_photo", pk)
        else:
            return render(request, 'mvp/detail_photo.html', {
                'photo': photo,
                'form': form,
            }, status=400)
    else:
        form = CommentForm()

    return render(request, 'mvp/detail_photo.html', {
        'photo': photo,
        'form': form,
    }, status=status_code)

@login_required()
def delete_comment(request, pk):
    """지정한 댓글을 지웁니다.
    :param str pk: comment primary key.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed('not allowed method')
    # todo
    comment = get_object_or_404(Comment, pk=pk)

    # todo : 남의 댓글을 권한없이 지우려하는 경우.
    if comment.user != request.user:
        return HttpResponseForbidden('required permission to delete')

    # todo
    comment.delete()

    return redirect('mvp.views.detail_photo', comment.photo.pk)

@login_required()
def like_photo(request, pk):
    """지정한 사진에 좋아요 표식을 남기거나 취소합니다.
    :param str pk: photo primary key.
    """
    # todo
    photo = get_object_or_404(Photo, pk=pk)

    if not photo.likes.filter(pk=request.user.pk).exists():
        if photo.user != request.user:
            photo.likes.add(request.user)
        else:
            return render(request, 'mvp/detail_photo.html', {
                'photo': photo,
            }, status=400)
    else:
        photo.likes.remove(request.user)

    return redirect('mvp.views.detail_photo', photo.pk)
