from django.test import TestCase
from .views import get_party_members
from .models import *


class GetPartyMembersTest(TestCase):
    def test_get_party_members(self):
        party_members = get_party_members()

        # assert it's at least one long
        self.assertTrue(len(party_members) > 0)

        for member in party_members:
            self.assertTrue("hp" in member)
            self.assertTrue("mp" in member)
            self.assertTrue("maxMP" in member)
            self.assertTrue("maxHealth" in member)
            self.assertTrue("username" in member)


class BooksModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Books.objects.create(name="Test Book", txtfile="Test content")

    def test_name_label(self):
        book = Books.objects.get(id=1)
        field_label = book._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        book = Books.objects.get(id=1)
        max_length = book._meta.get_field("name").max_length
        self.assertEqual(max_length, 30)

    def test_object_name_is_name(self):
        book = Books.objects.get(id=1)
        expected_object_name = f"{book.name}"
        self.assertEqual(expected_object_name, str(book))

    def test_txtfile_label(self):
        book = Books.objects.get(id=1)
        field_label = book._meta.get_field("txtfile").verbose_name
        self.assertEqual(field_label, "txtfile")


class FactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Faction.objects.create(
            id=1,
            name="Test Faction",
            base=0,
            see_illusion=True,
            min_cap=0,
            max_cap=0
        )

    def test_name_label(self):
        faction = Faction.objects.get(id=1)
        field_label = faction._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        faction = Faction.objects.get(id=1)
        max_length = faction._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_name(self):
        faction = Faction.objects.get(id=1)
        expected_object_name = f"{faction.name}"
        self.assertEqual(expected_object_name, str(faction))

    def test_base_default(self):
        faction = Faction.objects.get(id=1)
        default = faction._meta.get_field('base').default
        self.assertEqual(default, 0)

    def test_see_illusion_default(self):
        faction = Faction.objects.get(id=1)
        default = faction._meta.get_field('see_illusion').default
        self.assertEqual(default, True)

    def test_min_cap_default(self):
        faction = Faction.objects.get(id=1)
        default = faction._meta.get_field('min_cap').default
        self.assertEqual(default, 0)

    def test_max_cap_default(self):
        faction = Faction.objects.get(id=1)
        default = faction._meta.get_field('max_cap').default
        self.assertEqual(default, 0)


class LootdropModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lootdrop.objects.create(id=1, name='Test Lootdrop')

    def test_name_label(self):
        lootdrop = Lootdrop.objects.get(id=1)
        field_label = lootdrop._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        lootdrop = Lootdrop.objects.get(id=1)
        max_length = lootdrop._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)


class LootdropEntryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lootdrop.objects.create(id=1, name='Test Lootdrop Entry')
        LootdropEntry.objects.create(lootdrop_id=1, item_id=1)

    def test_item_id_label(self):
        entry = LootdropEntry.objects.get(id=1)
        field_label = entry._meta.get_field('item_id').verbose_name
        self.assertEqual(field_label, 'item id')


class LoottableModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Loottable.objects.create(id=1, name='Test Loottable')

    def test_name_label(self):
        loottable = Loottable.objects.get(id=1)
        field_label = loottable._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        loottable = Loottable.objects.get(id=1)
        max_length = loottable._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)


class LoottableEntryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        loottable = Loottable.objects.create(name='Test Loottable')
        lootdrop = Lootdrop.objects.create(name='Test Lootdrop')
        LoottableEntry.objects.create(loottable=loottable, lootdrop=lootdrop)

    def test_loottable_label(self):
        entry = LoottableEntry.objects.get(id=1)
        field_label = entry._meta.get_field('loottable').verbose_name
        self.assertEqual(field_label, 'loottable')