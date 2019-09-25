from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from mintama.get_outer_model import get_category_model, get_reference_model

from .models import Diary, Section
from .serializers import DiarySerializer, SectionSerializer
from .views import DiaryViewSet, SectionViewSet
from accounts.models import Category, Reference

User = get_user_model()


class TestDiaryModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='test_user', password='asdkjfalsfjflas', email="shoutaro425@gmail.com")

    @classmethod
    def tearDownClass(cls):
        del cls.user

    def creating_a_diary_and_saving(self, title=None):
        diary = Diary()
        diary.user = self.user
        if title is not None:
            diary.title = title
        
        diary.save()


    def test_is_empty(self):
        diary = Diary.objects.all()
        self.assertEqual(diary.count(), 0)

    def test_count_one(self):
        diary = Diary.objects.create(user=self.user)
        saved_diaries = Diary.objects.all()
        self.assertEqual(saved_diaries.count(), 1)

    def test_saving_and_retrieving_diary(self):
        title = 'test_diary'
        self.creating_a_diary_and_saving(title)
        
        saved_diary = Diary.objects.all()
        actual_diary = saved_diary[0]

        self.assertEqual(actual_diary.user, self.user)
        self.assertEqual(actual_diary.title, title)
        self.assertTrue(actual_diary.written_at)

    def test_title_over_length_save(self):
        title = 'texttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttext'
        self.creating_a_diary_and_saving(title)


class TestSectionModel(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='test_section', password='asdkjfalsfjflas', email="shoutaro425@gmail.com")
        cls.diary = Diary.objects.create(user=cls.user, title='test_title')
        cls.category_python = Category.objects.create(name='Python')
        cls.category_javascript = Category.objects.create(name='JavaScript')
        cls.reference_python = Reference.objects.create(
            user=cls.user, title="python", evaluation=4.5, content="nice"
            )
        cls.reference_javascript = Reference.objects.create(
            user=cls.user, title="javascript", evaluation=4.0, content="ok"
            )
        
    @classmethod
    def tearDownClass(cls):
        del cls.user
        del cls.diary
        del cls.category_python
        del cls.category_javascript
        del cls.reference_python
        del cls.reference_javascript

    def creating_a_section_and_saving(self, heading=None, content=None):
        section = Section()
        section.diary = self.diary
        section.save()
        section.categories.add(self.category_python)
        section.references.add(self.reference_javascript)

        if heading is not None:
            section.heading = heading
        if content is not None:
            section.content = content

        section.save()
        print(section.heading)

    def test_is_empty(self):
        section = Section.objects.all()
        self.assertEqual(section.count(), 0)

    def test_count_one(self):
        heading = 'java'
        content = 'difficult'
        self.creating_a_section_and_saving(heading=heading, content=content)
        saved_sections = Section.objects.all()
        self.assertEqual(saved_sections.count(), 1)

    def test_saving_and_retrieving_section(self):
        heading = 'test_heading'
        content = 'test_content'
        self.creating_a_section_and_saving(heading, content)
        
        saved_section = Section.objects.all()
        actual_section = saved_section[0]

        self.assertEqual(actual_section.heading, heading)
        self.assertEqual(actual_section.content, content)

    def test_heading_over_length_save(self):
        heading = 'texttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttexttext'
        self.creating_a_section_and_saving(heading)


        
class TestDiarySerializer(TestCase):
    pass


class TestSectionSerialzier(TestCase):
    pass


class TestDiaryViewSet(TestCase):
    pass


class TestSectionViewSet(TestCase):
    pass


class TestUrl(TestCase):
    pass