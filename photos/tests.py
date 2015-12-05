import os

from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Photo
from .forms import PhotoForm


class PhotoTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            username='test1',
            password='1'
        )
        self.client = Client()
        self.image_file_path = os.path.join(settings.MEDIA_ROOT, 'hannal.png')

    def test_save_photo_by_model(self):
        """모델을 이용해 사진 게시물을 저장하는 테스트.
        """
        # 정상 저장 테스트.
        new_photo = Photo()
        new_photo.user = self.user1
        new_photo.image = self.image_file_path
        new_photo.description = ''
        # # 저장하기 전이므로 pk는 None.
        self.assertIsNone(new_photo.pk)
        new_photo.save()
        # # 저장한 후이므로 pk는 None이 아님.
        self.assertIsNotNone(new_photo.pk)

        # user 가 없어서 오류가 발생하는 테스트.
        new_photo2 = Photo()
        new_photo2.image = self.image_file_path
        new_photo2.description = ''
        # # user에 제대로 된 값을 할당하지 않았으므로 ValueError 발생.
        with self.assertRaises(ValueError):
            new_photo2.user = 'hannal'

    def test_save_photo_by_model_with_form(self):
        """모델폼을 이용해 사진 게시물을 저장하는 테스트.
        """
        # image 폼 필드에 유효하지 않은 값 할당 테스트.
        form = PhotoForm(data={
            'image': self.image_file_path,
            'description': 'asdf'
        })
        validation_result = form.is_valid()
        # # form validation을 통과하지 못했으므로 False
        self.assertFalse(validation_result)

        # # 폼에 첫 번째 인자로 POST로 넘어온 폼 값, 두 번째 인자로 POST로 업로드 된 파일 전달.
        with open(self.image_file_path, 'rb') as fp:
            form = PhotoForm(
                {
                    'description': 'asdf'
                },
                {
                    'image': SimpleUploadedFile(fp.name, fp.read()),
                },
            )
        validation_result = form.is_valid()
        # # 폼 validation을 통과했으므로 True
        self.assertTrue(validation_result)
        new_photo = form.save(commit=False)
        new_photo.user = self.user1
        new_photo.save()

        # # 게시물이 저장됐으므로 pk는 None이 아님.
        self.assertIsNotNone(new_photo.pk)

    def test_view_get_create_photo(self):
        """create_photo 뷰 함수에 GET으로 접근하는 테스트.
        """
        url = '/photos/create/'
        # 로그인 안 하고 접속하기
        # # login_required가 redirect하는 걸 따라가야 하므로 follow=True
        # # 참고 response attributes : https://goo.gl/elVe2c
        res = self.client.get(url, follow=True)
        # # redirect되어 도착한 곳은 200 응답.
        self.assertEqual(res.status_code, 200)
        # # redirect되어 도착한 곳의 뷰 함수 이름은 login 이어야 한다.
        self.assertEqual(res.resolver_match.func.__name__, 'login')

        # 로그인 한 뒤에 접속 시도
        self._login('test1', '1')
        res = self.client.get(url, follow=True)
        # # 200 응답.
        self.assertEqual(res.status_code, 200)
        # # 로그인 한 상태이므로 create_photo 뷰 함수가 호출된 것.
        self.assertEqual(res.resolver_match.func.__name__, 'create_photo')
        # # 템플릿 컨텍스트가 존재하는 응답이므로 context는 None이 아님.
        self.assertIsNotNone(res.context)
        # # 템플릿 컨텍스트에 form 이 존재함.
        self.assertIn('form', res.context)
        # # 이 form 은 PhotoForm으로 생성된 객체.
        self.assertIsInstance(res.context['form'], PhotoForm)

    def test_view_post_create_photo(self):
        """create_photo 뷰 함수를 이용해 사진을 게시하는 테스트.
        """
        url = '/photos/create/'

        # 로그인 안 하고 게시 시도.
        with open(self.image_file_path, 'rb') as fp:
            res = self.client.post(url, {
                'image': fp,
                'description': 'hi',
            }, follow=True)
        # # redirect되어 도착한 곳의 뷰 함수 이름은 login 이어야 한다.
        self.assertEqual(res.resolver_match.func.__name__, 'login')

        # 로그인한 뒤에 게시하는 테스트.
        self._login('test1', '1')
        # # image 필드를 빠뜨리고 게시 시도.
        res = self.client.post(url, {
            'description': 'hi',
        }, follow=True)
        # # form validation을 실패했으므로 create_photo 뷰 함수 호출
        self.assertEqual(res.resolver_match.func.__name__, 'create_photo')
        self.assertIsNotNone(res.context)
        self.assertIn('form', res.context)
        # # form 컨텍스트 변수의 image 폼 필드에 오류 내용이 있는 지 확인.
        self.assertTrue(res.context['form'].has_error('image'))

        # # 제대로 된 게시 형식으로 게시 시도.
        with open(self.image_file_path, 'rb') as fp:
            res = self.client.post(url, {
                'image': fp,
                'description': 'hi',
            }, follow=True)
        # # 정상 게시되었으므로 해당 게시물을 보는 view_photo 뷰 함수 호출.
        self.assertEqual(res.resolver_match.func.__name__, 'view_photo')

    def _login(self, username, password):
        return self.client.post(settings.LOGIN_URL, {
            'username': username,
            'password': password,
        })
