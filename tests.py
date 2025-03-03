import importlib.util
from pathlib import Path
import re
import unittest
from datetime import datetime as dt
from dei import DEISourceManager

class TestDEISourceManager(unittest.TestCase):
    """
    Tests for the DEISourceManager class, tracking companies' DEI stances.

    Key principles:
    1. Sources are processed chronologically
    2. Companies can appear in both retreating and holding categories
    3. Full history of DEI stance is preserved
    4. Source references are accumulated across categories
    """

    def setUp(self):
        """Creates a fresh DEISourceManager instance before each test"""
        self.manager = DEISourceManager()

    def test_retreating_company_first_appearance(self):
        """
        Tests handling of a company's first appearance in a retreating source.
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

    def test_holding_company_first_appearance(self):
            """
            Tests handling of holding company's first appearance in a holding source.
            """
            self.manager.holding_sources = [{
                "date": "2025-02-17",
                "title": "Test Source",
                "url": "http://test.com",
                "companies": ["CompanyA"]
            }]
            self.manager.process_sources()

            self.assertIn("CompanyA", self.manager.holding_companies)
            self.assertEqual(self.manager.holding_companies["CompanyA"], ["H1"])

    def test_company_in_both_categories_different_dates(self):
        """
        Tests tracking a company that appears in both retreating and holding sources.
        Sources are from different dates.
        """
        self.manager.holding_sources = [{
            "date": "2025-02-10",
            "title": "Holding Source",
            "url": "http://holding.com",
            "companies": ["CompanyB"]
        }]
        self.manager.retreating_sources = [{
            "date": "2025-02-15",
            "title": "Retreating Source",
            "url": "http://retreating.com",
            "companies": ["CompanyB"]
        }]
        self.manager.process_sources()

        # Verify company appears in both categories
        self.assertIn("CompanyB", self.manager.holding_companies)
        self.assertIn("CompanyB", self.manager.retreating_companies)

        # Verify source references are correct
        self.assertEqual(self.manager.holding_companies["CompanyB"], ["H1"])
        self.assertEqual(self.manager.retreating_companies["CompanyB"], ["R1"])

    def test_company_in_both_categories_same_date(self):
        """
        Tests tracking a company that appears in both retreating and holding sources
        on the same date.
        """
        self.manager.holding_sources = [
            {
                "date": "2025-02-20",
                "title": "First Holding Source",
                "url": "http://test1.com",
                "companies": ["CompanyC"]
            },
            {
                "date": "2025-02-20",
                "title": "Second Holding Source",
                "url": "http://test2.com",
                "companies": ["CompanyC"]
            }
        ]
        self.manager.retreating_sources = [{
            "date": "2025-02-20",
            "title": "Retreating Source",
            "url": "http://test3.com",
            "companies": ["CompanyC"]
        }]
        self.manager.process_sources()

        # Verify company appears in both categories
        self.assertIn("CompanyC", self.manager.holding_companies)
        self.assertIn("CompanyC", self.manager.retreating_companies)

        # Verify source references are correct
        self.assertEqual(
            set(self.manager.holding_companies["CompanyC"]),
            {"H1", "H2"}
        )
        self.assertEqual(self.manager.retreating_companies["CompanyC"], ["R1"])

    def test_multiple_sources_chronological_ordering(self):
        """
        Tests that sources are processed in strict chronological order,
        and source labels reflect this order.
        """
        self.manager.holding_sources = [
            {
                "date": "2025-02-10",
                "title": "Older Source",
                "url": "http://test.com",
                "companies": ["CompanyD"]
            },
            {
                "date": "2025-02-20",
                "title": "Newer Source",
                "url": "http://test.com",
                "companies": ["CompanyD"]
            }
        ]
        self.manager.process_sources()

        # Verify sources are processed in chronological order
        self.assertIn("CompanyD", self.manager.holding_companies)
        self.assertEqual(
            self.manager.holding_companies["CompanyD"],
            ["H1", "H2"],
            "Sources should be labeled based on chronological order"
        )

    def test_source_accumulation(self):
        """
        Tests that multiple sources for the same company are accumulated.
        """
        self.manager.retreating_sources = [
            {
                "date": "2025-02-15",
                "title": "First Retreating Source",
                "url": "http://test1.com",
                "companies": ["CompanyE"]
            },
            {
                "date": "2025-02-16",
                "title": "Second Retreating Source",
                "url": "http://test2.com",
                "companies": ["CompanyE"]
            }
        ]
        self.manager.process_sources()

        # Verify sources are accumulated
        self.assertIn("CompanyE", self.manager.retreating_companies)
        self.assertEqual(
            set(self.manager.retreating_companies["CompanyE"]),
            {"R1", "R2"}
        )

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
        1. Companies can appear in both retreating and holding categories
        2. Source references for companies are correctly preserved
        3. Provides insights into category dynamics
        """
        # Collect all source references for each company
        retreating_source_refs = {}
        for index, source in enumerate(self.dei.retreating_sources, start=1):
            for company in source["companies"]:
                if company not in retreating_source_refs:
                    retreating_source_refs[company] = []
                retreating_source_refs[company].append(f"R{index}")

        holding_source_refs = {}
        for index, source in enumerate(self.dei.holding_sources, start=1):
            for company in source["companies"]:
                if company not in holding_source_refs:
                    holding_source_refs[company] = []
                holding_source_refs[company].append(f"H{index}")

        # Verify retreating companies
        for company, expected_refs in retreating_source_refs.items():
            self.assertIn(company, self.manager.retreating_companies,
                f"Company {company} from retreating sources not found in processed data")

            # Check that all expected source references are present
            actual_refs = self.manager.retreating_companies[company]
            self.assertTrue(
                set(expected_refs).issubset(set(actual_refs)),
                f"Incorrect source references for {company} in retreating companies. "
                f"Expected subset: {expected_refs}, Actual: {actual_refs}"
            )

        # Verify holding companies
        for company, expected_refs in holding_source_refs.items():
            self.assertIn(company, self.manager.holding_companies,
                f"Company {company} from holding sources not found in processed data")

            # Check that all expected source references are present
            actual_refs = self.manager.holding_companies[company]
            self.assertTrue(
                set(expected_refs).issubset(set(actual_refs)),
                f"Incorrect source references for {company} in holding companies. "
                f"Expected subset: {expected_refs}, Actual: {actual_refs}"
            )

        # Verify companies can appear in both categories
        companies_in_retreating = set(self.manager.retreating_companies.keys())
        companies_in_holding = set(self.manager.holding_companies.keys())

        # Find the newer category for companies in both lists
        overlap = companies_in_retreating.intersection(companies_in_holding)

        # Collect dates for sources mentioning these companies
        newer_in_retreating = []
        newer_in_holding = []
        for company in overlap:
            # Find the most recent date in retreating and holding sources
            retreating_dates = [
                dt.strptime(source['date'], "%Y-%m-%d")
                for source in self.dei.retreating_sources
                if company in source['companies']
            ]
            holding_dates = [
                dt.strptime(source['date'], "%Y-%m-%d")
                for source in self.dei.holding_sources
                if company in source['companies']
            ]

            # Determine which category is newer
            max_retreating_date = max(retreating_dates) if retreating_dates else dt.min
            max_holding_date = max(holding_dates) if holding_dates else dt.min

            if max_retreating_date > max_holding_date:
                newer_in_retreating.append(company)
            elif max_holding_date > max_retreating_date:
                newer_in_holding.append(company)

        print(f"\n{len(overlap)} companies appear in both categories: ")
        print(f"\n{len(newer_in_retreating)} newer in retreating")
        for company in sorted(newer_in_retreating):
            print(f"* {company}")

        print(f"\n{len(newer_in_holding)} newer in holding")
        for company in sorted(newer_in_holding):
            print(f"* {company}")

        # Find new companies in each category
        max_retreating_date = max(
            dt.strptime(source['date'], "%Y-%m-%d")
            for source in self.dei.retreating_sources
        )
        max_holding_date = max(
            dt.strptime(source['date'], "%Y-%m-%d")
            for source in self.dei.holding_sources
        )

        # Get companies in the most recent sources
        latest_retreating_sources = [
            source for source in self.dei.retreating_sources
            if dt.strptime(source['date'], "%Y-%m-%d") == max_retreating_date
        ]
        latest_holding_sources = [
            source for source in self.dei.holding_sources
            if dt.strptime(source['date'], "%Y-%m-%d") == max_holding_date
        ]

        # Collect all companies from previous sources
        previous_retreating_companies = set()
        previous_holding_companies = set()

        for source in self.dei.retreating_sources:
            if dt.strptime(source['date'], "%Y-%m-%d") < max_retreating_date:
                previous_retreating_companies.update(source['companies'])

        for source in self.dei.holding_sources:
            if dt.strptime(source['date'], "%Y-%m-%d") < max_holding_date:
                previous_holding_companies.update(source['companies'])

        # Find new companies on the most recent date
        new_retreating_companies = [
            company for source in latest_retreating_sources
            for company in source['companies']
            if company not in previous_retreating_companies
        ]
        new_holding_companies = [
            company for source in latest_holding_sources
            for company in source['companies']
            if company not in previous_holding_companies
        ]

        print(f"\nNew companies as of the most recent date:")
        print(f"  - Retreating ({max_retreating_date.strftime('%Y-%m-%d')}): {new_retreating_companies}")
        print(f"  - Holding ({max_holding_date.strftime('%Y-%m-%d')}): {new_holding_companies}")

        # Cross-reference new companies
        # Check which new holding companies were in previous retreating sources
        new_h_in_previous_r = [
            company for company in new_holding_companies
            if company in previous_retreating_companies
        ]

        # Check which new retreating companies were in previous holding sources
        new_r_in_previous_h = [
            company for company in new_retreating_companies
            if company in previous_holding_companies
        ]

        if new_h_in_previous_r:
            print("\nNew holding companies previously in retreating:")
            for company in new_h_in_previous_r:
                print(f"* {company}")

        if new_r_in_previous_h:
            print("\nNew retreating companies previously in holding:")
            for company in new_r_in_previous_h:
                print(f"* {company}")

    def test_markdown_consistency(self):
        """
        Verifies that the generated markdown reflects the processed data.
        """
        # Generate markdown
        markdown = self.manager.generate_markdown()

        # Verify both sections exist
        self.assertIn("## Retreating", markdown, "Markdown missing 'Retreating' section")
        self.assertIn("## Holding the line", markdown, "Markdown missing 'Holding the line' section")

        # Extract companies from markdown table
        md_retreating = set()
        md_holding = set()

        table_pattern = r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
        separator_pattern = r"^\s*\|?\s*-{2,}\s*-?\s*\|"

        for match in re.finditer(table_pattern, markdown, re.MULTILINE):
            full_row = match.group(0).strip()

            # Skip separator rows
            if re.match(separator_pattern, full_row):
                continue

            retreating_company = match.group(1).strip()
            holding_company = match.group(3).strip()

            # Ignore table headers
            if retreating_company.lower() == "retreating":
                continue
            if holding_company.lower() == "holding the line":
                continue

            if retreating_company:
                md_retreating.add(retreating_company)
            if holding_company:
                md_holding.add(holding_company)

        # Verify companies in markdown match processed data
        retreating = set(self.manager.retreating_companies.keys())
        holding = set(self.manager.holding_companies.keys())

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

if __name__ == '__main__':
   unittest.main()

