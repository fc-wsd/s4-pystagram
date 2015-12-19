import os
import base64

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile

from .forms import PhotoForm
from .forms import CommentForm
from .models import Photo
from .models import Comment
from .models import Like


def get_base64_image(data):
    if data is None or ';base64,' not in data:
        return None

    _format, _content = data.split(';base64,')
    return base64.b64decode(_content)


@login_required
def create_photo(request):
    if request.method == 'GET':
        form = PhotoForm()
    elif request.method == 'POST':
        filtered = request.POST.get('filtered_image')
        if filtered:
            filtered_image = get_base64_image(filtered)
            filename = request.FILES['image'].name.split(os.sep)[-1]
            _filedata = {
                'image': SimpleUploadedFile(
                    filename, filtered_image
                )
            }
        else:
            _filedata = request.FILES

        form = PhotoForm(request.POST, _filedata)

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


@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    like, is_created = Like.objects.get_or_create(
        user=request.user, photo=photo,
        defaults={
            'photo': photo,
            'user': request.user,
        }
    )

    if is_created is False:
        like.delete()

    return redirect('photos:view_photo', photo.pk)








