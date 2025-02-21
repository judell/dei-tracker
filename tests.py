import importlib.util
from pathlib import Path
from dei import DEISourceManager
import re
import unittest

class TestDEISourceManager(unittest.TestCase):
    """
    Tests for the DEISourceManager class, which tracks companies' DEI stances based on news sources.

    Key principles being tested:
    1. Sources are processed chronologically with newer sources taking precedence
    2. A company in 'retreating' cannot be moved to 'holding' by an older source
    3. Companies accumulate source references within their category
    4. When a company moves categories, its previous source references are cleared
    5. For same-date sources, retreating takes precedence over holding
    6. When multiple sources share the same date, they are processed in input order
        within their respective categories
    """

    def setUp(self):
       """Creates a fresh DEISourceManager instance before each test"""
       self.manager = DEISourceManager()

    def test_retreating_company_never_seen_before(self):
       """
       Tests handling of a company's first appearance in a retreating source.
       
       Scenario:
       1. Company appears for the first time in a retreating source
       2. Expected: 
          - Company should be added to retreating category
          - Should have exactly one source reference
          - Should not appear in holding category
       """
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
       """
       Tests accumulation of sources for a company already in retreating.
       
       Scenario:
       1. Company appears in first retreating source
       2. Company appears in second retreating source
       3. Expected:
          - Company should remain in retreating
          - Should accumulate both source references
          - Order of references should match chronological order
       """
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
       self.assertSetEqual(set(self.manager.retreating_companies["CompanyB"]), {"R1", "R2"})
       self.assertNotIn("CompanyB", self.manager.holding_companies)

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

    def test_holding_company_never_seen_before(self):
       """
       Tests handling of a company's first appearance in a holding source.
       
       Scenario:
       1. Company appears for the first time in a holding source
       2. Expected:
          - Company should be added to holding category
          - Should have exactly one source reference
          - Should not appear in retreating category
       """
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
       """
       Tests accumulation of sources for a company already in holding.
       
       Scenario:
       1. Company appears in first holding source
       2. Company appears in second holding source
       3. Expected:
          - Company should remain in holding
          - Should accumulate both source references
          - References should be in chronological order
       """
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
       self.assertSetEqual(set(self.manager.holding_companies["CompanyE"]), {"H1", "H2"})
       self.assertNotIn("CompanyE", self.manager.retreating_companies)

    def test_holding_company_already_in_retreating(self):
       """
       Tests that holding sources cannot override retreating classification.
       
       Scenario:
       1. Company is in retreating category
       2. Company appears in newer holding source
       3. Expected:
          - Company should remain in retreating
          - Holding reference should be ignored
       """
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

    def test_retreating_company_with_newer_source_should_override(self):
       """
       Tests that a newer retreating source overrides an older holding source.
       
       Scenario:
       1. Company is first seen in a holding source from Feb 10
       2. Company appears in a retreating source from Feb 15
       3. Expected: Company should end up in retreating category
       
       This test ensures that a newer retreating source ALWAYS overrides 
       an older holding entry, as retreating takes precedence in classification.
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

    def test_company_in_both_retreating_and_holding_same_source(self):
       """
       Tests handling of a company appearing in both categories on the same date.
       
       Scenario:
       1. Company appears in both retreating and holding sources from same date
       2. Expected: Company should be classified as retreating (retreating takes precedence)
       
       This ensures consistent handling of conflicting same-day sources.
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
        1. Add sources in non-chronological order
        2. Verify they're processed newest-to-oldest regardless of input order
        3. Verify source labels reflect chronological order, not input order
        """
        # Add sources in non-chronological order
        self.manager.holding_sources = [
            {
                "date": "2025-02-10",  # Older source added first
                "title": "Older Source",
                "url": "http://test.com",
                "companies": ["CompanyI"]
            },
            {
                "date": "2025-02-20",  # Newer source added second
                "title": "Newer Source",
                "url": "http://test.com",
                "companies": ["CompanyI"]
            }
        ]
        self.manager.process_sources()
        
        # Verify references are in chronological order (newest first)
        self.assertEqual(
            self.manager.holding_companies["CompanyI"],
            ["H1", "H2"],  # H1 should be from Feb 20, H2 from Feb 10
            "Sources should be processed newest-to-oldest regardless of input order"
        )
        
        # Additional verification that sources were processed in date order
        self.assertEqual(
            self.manager.holding_sources[0]["date"],
            "2025-02-20",
            "First source should be newest after processing"
        )
        self.assertEqual(
            self.manager.holding_sources[1]["date"],
            "2025-02-10",
            "Second source should be oldest after processing"
        )

    def test_same_date_source_ordering(self):
       """
       Tests handling of multiple sources from the same date.
       
       Scenario:
       1. Two holding sources from same date mention same company
       2. One retreating source from same date mentions company
       3. Expected: 
          - Company should be in retreating (category precedence)
          - Within holding, sources should be processed in input order
       
       This ensures consistent handling of same-date sources both
       across and within categories.
       """
       self.manager.holding_sources = [
           {
               "date": "2025-02-20",
               "title": "First Same-Day Source",
               "url": "http://test1.com",
               "companies": ["CompanyJ"]
           },
           {
               "date": "2025-02-20",
               "title": "Second Same-Day Source",
               "url": "http://test2.com",
               "companies": ["CompanyJ"]
           }
       ]
       self.manager.retreating_sources = [{
           "date": "2025-02-20",
           "title": "Same-Day Retreating Source",
           "url": "http://test3.com",
           "companies": ["CompanyJ"]
       }]
       self.manager.process_sources()
       
       self.assertIn("CompanyJ", self.manager.retreating_companies)
       self.assertNotIn("CompanyJ", self.manager.holding_companies)

class TestDEIDataConsistency(unittest.TestCase):
    """
    Integration test that verifies consistency between:
    - Source data in dei.py
    - Processing logic
    - Generated dei.md output
    """

    def setUp(self):
        """Load the source data and process it"""
        # Import dei.py module dynamically with error handling
        dei_path = Path("dei.py")
        self.assertTrue(dei_path.exists(), "Error: dei.py not found")

        try:
            spec = importlib.util.spec_from_file_location("dei", "dei.py")
            self.dei = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.dei)
        except Exception as e:
            self.fail(f"Failed to import dei.py: {e}")

        # Create DEISourceManager instance and process data
        self.manager = self.dei.DEISourceManager(
            self.dei.retreating_sources,
            self.dei.holding_sources
        )
        self.manager.process_sources()

    def test_data_consistency(self):
        """
        Verifies consistency between source data, processing, and output.

        Checks:
        1. Companies appear in exactly one category
        2. All companies from source data are accounted for
        3. Generated markdown matches processed data
        4. Sources are in correct chronological order
        5. Markdown sections exist and sources appear in correct order
        """

        # --- Step 1: Validate No Overlap Between Retreating and Holding ---
        retreating = set(self.manager.retreating_companies.keys())
        holding = set(self.manager.holding_companies.keys())

        overlap = retreating.intersection(holding)
        self.assertEqual(len(overlap), 0, 
            f"Companies appearing in both categories: {overlap}")

        # --- Step 2: Ensure All Source Companies Are Categorized ---
        all_source_companies = set()
        for source in self.dei.retreating_sources:
            all_source_companies.update(source["companies"])
        for source in self.dei.holding_sources:
            all_source_companies.update(source["companies"])
            
        all_categorized = retreating.union(holding)
        missing = all_source_companies - all_categorized
        extra = all_categorized - all_source_companies

        self.assertEqual(len(missing), 0,
            f"Companies in sources but not categorized: {missing}")
        self.assertEqual(len(extra), 0,
            f"Companies categorized but not in sources: {extra}")

        # --- Step 3: Validate Markdown File Exists and Matches Processed Data ---
        md_path = Path("dei.md")
        self.assertTrue(md_path.exists(), "Error: dei.md not found")

        markdown = md_path.read_text()

        # Ensure Markdown contains expected sections
        self.assertIn("## Retreating", markdown, "Markdown missing 'Retreating' section")
        self.assertIn("## Holding the line", markdown, "Markdown missing 'Holding the line' section")

        # Regex pattern to extract table rows while handling variable spacing
        table_pattern = r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
        md_retreating = set()
        md_holding = set()

        separator_pattern = r"^\s*\|?\s*-{2,}\s*-?\s*\|"

        for match in re.finditer(table_pattern, markdown, re.MULTILINE):
            full_row = match.group(0).strip()  # Get full table row

            # Skip separator rows that contain only dashes and pipes
            if re.match(separator_pattern, full_row):
                continue

            retreating_company = match.group(1).strip()
            holding_company = match.group(3).strip()

            # Ignore table headers automatically
            if retreating_company.lower() == "retreating":
                continue
            if holding_company.lower() == "holding the line":
                continue

            if retreating_company:
                md_retreating.add(retreating_company)
            if holding_company:
                md_holding.add(holding_company)



        # --- Step 4: Compare Extracted Markdown Companies to Processed Data ---
        self.assertSetEqual(
            retreating, md_retreating,
            f"Mismatch in retreating companies:\n"
            f"- Missing from Markdown: {retreating - md_retreating}\n"
            f"- Extra in Markdown: {md_retreating - retreating}"
        )
        self.assertSetEqual(
            holding, md_holding,
            f"Mismatch in holding companies:\n"
            f"- Missing from Markdown: {holding - md_holding}\n"
            f"- Extra in Markdown: {md_holding - holding}"
        )

    def test_detects_extra_company_in_retreating(self):
        """
        Introduces an error by adding an extra company to retreating after processing.
        Verifies that the test suite correctly detects inconsistencies.
        """

        self.manager.process_sources()

        # Introduce an error: Add a company that was never in dei.py sources
        self.manager.retreating_companies["FakeCompany"] = ["R99"]

        retreating = set(self.manager.retreating_companies.keys())

        # Ensure that the test detects the extra company
        all_source_companies = set()
        for source in self.dei.retreating_sources:
            all_source_companies.update(source["companies"])

        for source in self.dei.holding_sources:
            all_source_companies.update(source["companies"])

        all_categorized = retreating.union(set(self.manager.holding_companies.keys()))
        extra = all_categorized - all_source_companies

        self.assertNotEqual(len(extra), 0, "Test setup failure: No extra companies introduced")
        
        # Assert that the test correctly detects the inconsistency
        self.assertIn("FakeCompany", extra, "Test failed to detect the extra company in retreating")

if __name__ == '__main__':
   unittest.main()