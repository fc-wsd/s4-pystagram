from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import PhotoForm
from .forms import CommentForm
from .models import Photo
from .models import Comment


@login_required
def create_photo(request):
    if request.method == 'GET':
        form = PhotoForm()
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photos:view_photo', photo.pk)

    return render(request, 'edit_photo.html', {
        'form': form,
    })


def view_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comment_set.select_related().all()

    if request.method == 'GET':
        comment_form = CommentForm()
    else:
        if request.user.is_authenticated() is False:
            return redirect('login_url')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.photo = photo
            new_comment.user = request.user
            new_comment.save()

    return render(request, 'view_photo.html', {
        'photo': photo,
        'comment_form': comment_form,
        'comments': comments,
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'GET':
        pass
    else:
        if request.user != comment.user:
            raise PermissionDenied

        comment.delete()
        return redirect('photos:view_photo', comment.photo.pk)

    return render(request, 'comment_delete.html', {
        'comment': comment,
    })
