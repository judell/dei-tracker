import unittest
from datetime import datetime
from dei import DEISourceManager

class TestDEISourceManager(unittest.TestCase):
    def setUp(self):
        self.manager = DEISourceManager()

    def test_retreating_company_with_newer_source_should_override(self):
        """A newer retreating source should override an earlier holding entry."""
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
        """Ensure a company previously in holding is moved to retreating and holding is cleared."""
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
        # Verify original holding reference is completely removed
        self.assertNotIn("H1", self.manager.holding_companies.get("CompanyC", []))

    def test_company_in_both_retreating_and_holding_same_source(self):
        """If a company appears in both retreating and holding at the same time, retreating wins."""
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
        """Verify sources are processed in chronological order"""
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

    def test_retreating_company_never_seen_before(self):
        """Company not seen before -> should simply appear in retreating"""
        self.manager.retreating_sources = [{
            "date": "2025-02-17",
            "title": "Test Source",
            "url": "http://test.com",
            "companies": ["CompanyA"]
        }]
        self.manager.process_sources()
        
        self.assertIn("CompanyA", self.manager.retreating_companies)
        self.assertEqual(self.manager.retreating_companies["CompanyA"], ["R1"])
        self.assertNotIn("CompanyA", self.manager.holding_companies)

    def test_retreating_company_already_in_retreating(self):
        """Adding a new retreating source for a company already in retreating => append label"""
        self.manager.retreating_sources = [
            {
                "date": "2025-02-17",
                "title": "First Source",
                "url": "http://test1.com",
                "companies": ["CompanyB"]
            },
            {
                "date": "2025-02-16",
                "title": "Second Source",
                "url": "http://test2.com",
                "companies": ["CompanyB"]
            }
        ]
        self.manager.process_sources()
        
        self.assertIn("CompanyB", self.manager.retreating_companies)
        self.assertCountEqual(self.manager.retreating_companies["CompanyB"], ["R1", "R2"])
        self.assertNotIn("CompanyB", self.manager.holding_companies)

    def test_retreating_company_already_in_holding(self):
        """Adding a retreating source for a company in holding => remove from holding"""
        self.manager.holding_sources = [{
            "date": "2025-02-17",
            "title": "Hold Source",
            "url": "http://test.com",
            "companies": ["CompanyC"]
        }]
        self.manager.retreating_sources = [{
            "date": "2025-02-18",  # Newer source
            "title": "Retreat Source",
            "url": "http://test.com",
            "companies": ["CompanyC"]
        }]
        self.manager.process_sources()
        
        self.assertIn("CompanyC", self.manager.retreating_companies)
        self.assertEqual(self.manager.retreating_companies["CompanyC"], ["R1"])
        self.assertNotIn("CompanyC", self.manager.holding_companies)

    def test_holding_company_never_seen_before(self):
        """Company not seen before -> should appear in holding"""
        self.manager.holding_sources = [{
            "date": "2025-02-17",
            "title": "Test Source",
            "url": "http://test.com",
            "companies": ["CompanyD"]
        }]
        self.manager.process_sources()
        
        self.assertIn("CompanyD", self.manager.holding_companies)
        self.assertEqual(self.manager.holding_companies["CompanyD"], ["H1"])
        self.assertNotIn("CompanyD", self.manager.retreating_companies)

    def test_holding_company_already_in_holding(self):
        """Adding a new holding source for a company already in holding => append label"""
        self.manager.holding_sources = [
            {
                "date": "2025-02-17",
                "title": "First Source",
                "url": "http://test1.com",
                "companies": ["CompanyE"]
            },
            {
                "date": "2025-02-16",
                "title": "Second Source",
                "url": "http://test2.com",
                "companies": ["CompanyE"]
            }
        ]
        self.manager.process_sources()
        
        self.assertIn("CompanyE", self.manager.holding_companies)
        self.assertCountEqual(self.manager.holding_companies["CompanyE"], ["H1", "H2"])
        self.assertNotIn("CompanyE", self.manager.retreating_companies)

    def test_holding_company_already_in_retreating(self):
        """Adding a holding source for a company in retreating => skip it"""
        self.manager.retreating_sources = [{
            "date": "2025-02-17",
            "title": "Retreat Source",
            "url": "http://test.com",
            "companies": ["CompanyF"]
        }]
        self.manager.holding_sources = [{
            "date": "2025-02-18",  # Even though newer
            "title": "Hold Source",
            "url": "http://test.com",
            "companies": ["CompanyF"]
        }]
        self.manager.process_sources()
        
        self.assertIn("CompanyF", self.manager.retreating_companies)
        self.assertEqual(self.manager.retreating_companies["CompanyF"], ["R1"])
        self.assertNotIn("CompanyF", self.manager.holding_companies)

if __name__ == '__main__':
    unittest.main()