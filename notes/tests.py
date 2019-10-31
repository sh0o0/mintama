from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Note, Section
from accounts.models import Category, Reference

User = get_user_model()


class TestNoteModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='test_user', password='test_password!', email="darekano@mail.com")

    @classmethod
    def tearDownClass(cls):
        del cls.user

    def creating_a_note_and_saving(self, title=None):
        note = Note()
        note.user = self.user
        if title is not None:
            note.title = title
        
        note.save()

    def test_is_empty(self):
        note = Note.objects.all()
        self.assertEqual(note.count(), 0)

    def test_count_one(self):
        Note.objects.create(user=self.user)
        saved_notes = Note.objects.all()
        self.assertEqual(saved_notes.count(), 1)

    def test_saving_and_retrieving_note(self):
        title = 'test_note'
        self.creating_a_note_and_saving(title)
        
        saved_note = Note.objects.all()
        actual_note = saved_note[0]

        self.assertEqual(actual_note.user, self.user)
        self.assertEqual(actual_note.title, title)
        self.assertTrue(actual_note.written_at)


class TestSectionModel(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='test_section', password='asdkjfalsfjflas', email="darekano@mail.com")
        cls.note = Note.objects.create(user=cls.user, title='test_title')
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
        del cls.note
        del cls.category_python
        del cls.category_javascript
        del cls.reference_python
        del cls.reference_javascript

    def creating_a_section_and_saving(self, heading=None, content=None):
        section = Section()
        section.note = self.note
        section.save()
        section.categories.add(self.category_python)
        section.references.add(self.reference_javascript)

        if heading is not None:
            section.heading = heading
        if content is not None:
            section.content = content

        section.save()

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