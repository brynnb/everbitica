from django.test import TestCase
from .views import get_party_members

class GetPartyMembersTest(TestCase):
    def test_get_party_members(self):
        party_members = get_party_members()

        #assert it's at least one long
        self.assertTrue(len(party_members) > 0)

        for member in party_members:
            self.assertTrue("hp" in member)
            self.assertTrue("mp" in member)
            self.assertTrue("maxMP" in member)
            self.assertTrue("maxHealth" in member)
            self.assertTrue("username" in member)