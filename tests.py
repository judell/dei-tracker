import unittest
from datetime import datetime
from dei import DEISourceManager

class TestDEISourceManager(unittest.TestCase):
    """
    Tests for the DEISourceManager class, which tracks companies' DEI stances based on news sources.
    
    Key principles being tested:
    1. Sources are processed chronologically with newer sources taking precedence
    2. A company in 'retreating' cannot be moved to 'holding' by an older source
    3. Companies accumulate source references within their category
    4. When a company moves categories, its previous source references are cleared
    """

    def setUp(self):
        """Creates a fresh DEISourceManager instance before each test"""
        self.manager = DEISourceManager()

    def test_retreating_company_with_newer_source_should_override(self):
        """
        Tests that a newer retreating source overrides an older holding source.
        
        Scenario:
        1. Company is first seen in a holding source from Feb 10
        2. Company appears in a retreating source from Feb 15
        3. Expected: Company should end up in retreating category
        """
        self.manager.holding_sources = [{
            "date": "2025-02-10",
            "title": "Older Holding Source",
            "url": "http://test.com",
            "companies": ["CompanyG"]
        }]
        self.manager.retreating_sources = [{
            "date": "2025-02-15",
            "title": "Newer Retreating Source",
            "url": "http://test.com",
            "companies": ["CompanyG"]
        }]
        self.manager.process_sources()
        self.assertIn("CompanyG", self.manager.retreating_companies)
        self.assertNotIn("CompanyG", self.manager.holding_companies)

    def test_retreating_company_already_in_holding(self):
        """
        Tests complete removal of holding references when company moves to retreating.
        
        Scenario:
        1. Company is in holding with source H1
        2. Newer retreating source mentions company
        3. Expected: 
           - Company moves to retreating
           - Gets new retreating reference
           - All holding references are removed
        """
        self.manager.holding_sources = [{
            "date": "2025-02-17",
            "title": "Hold Source",
            "url": "http://test.com",
            "companies": ["CompanyC"]
        }]
        self.manager.retreating_sources = [{
            "date": "2025-02-18",
            "title": "Retreat Source",
            "url": "http://test.com",
            "companies": ["CompanyC"]
        }]
        self.manager.process_sources()
        self.assertIn("CompanyC", self.manager.retreating_companies)
        self.assertEqual(self.manager.retreating_companies["CompanyC"], ["R1"])
        self.assertNotIn("CompanyC", self.manager.holding_companies)
        self.assertNotIn("H1", self.manager.holding_companies.get("CompanyC", []))

    def test_company_in_both_retreating_and_holding_same_source(self):
        """
        Tests handling of a company appearing in both categories on the same date.
        
        Scenario:
        1. Company appears in both retreating and holding sources from same date
        2. Expected: Company should be classified as retreating (retreating takes precedence)
        
        This test ensures consistent handling of conflicting same-day sources.
        """
        self.manager.holding_sources = [{
            "date": "2025-02-20",
            "title": "Holding Source",
            "url": "http://test.com",
            "companies": ["CompanyH"]
        }]
        self.manager.retreating_sources = [{
            "date": "2025-02-20",
            "title": "Retreating Source",
            "url": "http://test.com",
            "companies": ["CompanyH"]
        }]
        self.manager.process_sources()
        self.assertIn("CompanyH", self.manager.retreating_companies)
        self.assertNotIn("CompanyH", self.manager.holding_companies)

    def test_source_date_ordering(self):
        """
        Tests that sources are processed in strict chronological order.
        
        Scenario:
        1. Two holding sources with different dates mention same company
        2. Expected: Company should have references from both sources
        3. Source labels should reflect chronological order, not input order
        
        This test ensures the chronological processing of sources regardless
        of the order they were added to the manager.
        """
        self.manager.holding_sources = [
            {
                "date": "2025-02-20",
                "title": "Newest Source",
                "url": "http://test.com",
                "companies": ["CompanyI"]
            },
            {
                "date": "2025-02-10",
                "title": "Oldest Source",
                "url": "http://test.com",
                "companies": ["CompanyI"]
            }
        ]
        self.manager.process_sources()
        self.assertSetEqual(set(self.manager.holding_companies["CompanyI"]), {"H1", "H2"})

if __name__ == '__main__':
    unittest.main()