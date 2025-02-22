from datetime import date, datetime

retreating_sources = [
    {
        "date": "2025-02-21",
        "title": "Another DEI rollback as KPMG US ends strategy aimed at underrepresented groups",
        "url": "https://www.businessinsider.com/kpmg-us-rolls-back-dei-strategy-big-four-trump-2025-2",
        "companies": [
            "KPMG US",
        ],
    },
    {
        "date": "2025-02-19",
        "title": "Mark Zuckerberg’s charity guts DEI after assuring staff it would continue",
        "url": "https://www.theguardian.com/technology/2025/feb/19/mark-zuckerberg-chan-dei",
        "companies": [
            "CZI",
        ],
    },
    {
        "date": "2025-02-20",
        "title": "Pepsi Rolling Back Diversity Initiatives",
        "url": "https://www.msn.com/en-us/money/companies/pepsi-rolling-back-diversity-initiatives-here-are-all-the-companies-cutting-dei-programs/ar-AA1x7MGk",
        "companies": [
            "JPMorgan Chase",
            "Morgan Stanley",
            "PepsiCo",
            "Citigroup",
        ],
    },
    {
        "date": "2025-02-17",
        "title": "Forbes: Banks Including JPMorgan Chase and Morgan Stanley Reportedly Cutting Back DEI References",
        "url": "https://www.forbes.com/sites/conormurray/2025/02/17/banks-including-jpmorgan-chase-and-morgan-stanley-reportedly-cutting-back-dei-references-here-are-all-the-companies-rolling-back-dei/",
        "companies": [
            "Amtrak",
            "Bank of America",
            "Boeing",
            "Brown-Forman (Jack Daniel's)",
            "Chipotle",
            "Citigroup",
            "Coca-Cola",
            "Comcast",
            "Deloitte",
            "Disney",
            "Ford Motor Co.",
            "General Electric (GE)",
            "Goldman Sachs",
            "Google",
            "Harley-Davidson",
            "Intel",
            "John Deere",
            "JPMorgan Chase",
            "Lowe's",
            "McDonald's",
            "Meta",
            "Molson Coors",
            "Morgan Stanley",
            "NPR",
            "PBS",
            "PayPal",
            "PepsiCo",
            "Smithsonian Institution",
            "Target",
            "The FBI",
            "Walmart",
            "Wells Fargo",
        ],
    },
    {
        "date": "2025-02-12",
        "title": "AP: Which US Companies Are Pulling Back on Diversity Initiatives",
        "url": "https://www.ap.org/news-highlights/spotlights/2025/which-us-companies-are-pulling-back-on-diversity-initiatives/",
        "companies": [
            "Amazon",
            "Brown-Forman (Jack Daniel's)",
            "Ford Motor Co.",
            "Goldman Sachs",
            "Google",
            "Harley-Davidson",
            "John Deere",
            "Lowe's",
            "McDonald's",
            "Meta",
            "Target",
            "Tractor Supply",
            "Walmart",
        ],
    },
    {
        "date": "2025-02-11",
        "title": "TechTarget: What Companies Are Rolling Back DEI Policies",
        "url": "https://www.techtarget.com/whatis/feature/What-companies-are-rolling-back-DEI-policies",
        "companies": ["Amazon", "Google", "McDonald's", "Meta", "Target", "Walmart"],
    },
]

holding_sources = [
    {
        "date": "2025-02-21",
        "title": "Mastercard diversity page (accessed 2025-02-21",
        "url": "https://www.mastercard.us/en-us/vision/who-we-are/diversity-inclusion.html",
        "companies": [
            "Mastercard",
        ],
    },
    {
        "date": "2025-02-21",
        "title": "Coca-Cola warns of potential negative impact from DEI changes (ed: waffling)",
        "url": "https://fortune.com/2025/02/21/coca-cola-warns-negative-impact-dei-changes/",
        "companies": [
            "Coca-Cola",
        ],
    },
    {
        "date": "2025-02-20",
        "title": "Here are eight major companies that have resisted anti-DEI backlash.",
        "url": "https://www.ebony.com/major-companies-that-are-standing-by-their-dei-programs/",
        "companies": [
            "Apple",
            "Ben & Jerry's",
            "Cisco",
            "Costco",
            "Delta Airlines",
            "Deutsche Bank",
            "e.l.f. Beauty",
            "Goldman Sachs",
            "JP Morgan Chase",
            "Microsoft",
            "Pinterest",
            "REI Co-op",
            "Ulta Beauty",
        ],
    },
    {
        "date": "2025-02-18",
        "title": "Newsweek: DEI Companies Program List Policies Donald Trump",
        "url": "https://www.newsweek.com/dei-companies-program-list-policies-donald-trump-2032960",
        "companies": [
            "Apple",
            "Costco",
            "Delta Airlines",
            "e.l.f. Beauty",
            "Meijer",
            "Microsoft",
            "Procter & Gamble",
            "Sephora",
        ],
    },
    {
        "date": "2025-02-17",
        "title": "Report: 46 Companies Sticking With DEI",
        "url": "https://buildremote.co/companies/keeping-dei/",
        "companies": [
            "Abercrombie and Fitch",
            "Adobe",
            "Alliance Health",
            "Ancestry",
            "Apple",
            "Ben & Jerry's",
            "Bering Straits Native Corporation",
            "Best Buy",
            "BJ's Wholesale",
            "Chick-fil-A",
            "Cigna",
            "Citigroup",
            "Deutsche Bank",
            "Dollar Tree",
            "Gap Inc.",
            "Goldman Sachs",
            "GoTo Foods",
            "HLW",
            "Honda",
            "Johnson & Johnson",
            "JPMorgan Chase",
            "Kroger",
            "Logitech",
            "Macy's",
            "Mastercard",
            "MassMutual",
            "Match Group",
            "McKinsey & Company",
            "Meijer",
            "Microsoft",
            "Mitre",
            "National Football League",
            "Nike",
            "Old Navy",
            "PepsiCo",
            "Philip Morris International",
            "Pinterest",
            "Progressive",
            "Procter & Gamble",
            "Sephora",
            "Tiffany & Co",
            "TJX Companies",
            "Ulta Beauty",
            "Wilson Sonsini Goodrich & Rosati",
        ],
    },
    {
        "date": "2025-02-04",
        "title": "The Root: A List of Companies That Continue to Support DEI",
        "url": "https://www.theroot.com/a-list-of-companies-that-continue-to-support-dei-1851755249",
        "companies": [
            "American Airlines",
            "Apple",
            "Cisco",
            "Cleveland Cavaliers",
            "Costco",
            "Delta Airlines",
            "e.l.f. Beauty",
            "Microsoft",
            "Nasdaq",
            "Pinterest",
            "Salesforce",
            "Southwest Airlines",
            "United Airlines",
        ],
    },
    {
        "date": "2025-01-31",
        "title": "Business Insider: Companies Supporting DEI Efforts - CEO Comments",
        "url": "https://www.businessinsider.com/companies-supporting-dei-efforts-ceo-comments-2025-1",
        "companies": ["Cisco", "Costco", "Deutsche Bank"],
    },
]


class DEISourceManager:
    def __init__(self, retreating_sources=None, holding_sources=None):
        self.retreating_sources = retreating_sources or []
        self.holding_sources = holding_sources or []
        self.retreating_companies = {}
        self.holding_companies = {}
        self.sorted_retreating = []
        self.sorted_holding = []
        self.subtitle = f'This is a point-in-time snapshot, generated on {date.today().strftime("%Y-%m-%d")}, derived from the listed sources. See <a href="https://github.com/judell/dei-tracker">the repo</a> for how to update.\n\n'

        # Process sources if provided at init
        if retreating_sources or holding_sources:
            self.process_sources()

    def process_sources(self):
        self.retreating_companies = {}
        self.holding_companies = {}

        # Sort sources by date, newest first
        self.retreating_sources.sort(
            key=lambda s: datetime.strptime(s["date"], "%Y-%m-%d"), reverse=True
        )
        self.holding_sources.sort(
            key=lambda s: datetime.strptime(s["date"], "%Y-%m-%d"), reverse=True
        )
        # Process retreating sources first
        for index, source in enumerate(self.retreating_sources, start=1):
            source_label = f"R{index}"
            for company in source["companies"]:
                # If the company exists in Holding, remove it first (newest category wins)
                if company in self.holding_companies:
                    del self.holding_companies[company]

                if company not in self.retreating_companies:
                    self.retreating_companies[company] = []
                self.retreating_companies[company].append(source_label)

        # Process holding sources
        for index, source in enumerate(self.holding_sources, start=1):
            source_label = f"H{index}"
            for company in source["companies"]:
                # If the company was already marked as retreating, ignore it (newest source wins)
                if company in self.retreating_companies:
                    continue

                if company not in self.holding_companies:
                    self.holding_companies[company] = []
                self.holding_companies[company].append(source_label)

        # Sort companies
        self.sorted_retreating = sorted(self.retreating_companies.keys())
        self.sorted_holding = sorted(self.holding_companies.keys())

    def generate_markdown_table(self):
        table_header = (
            "| Retreating | Sources | Holding the Line | Sources |\n"
            "|------------|---------|------------------|---------|\n"
        )

        max_len = max(len(self.sorted_retreating), len(self.sorted_holding))
        table_rows = []
        for i in range(max_len):
            retreating_company = (
                self.sorted_retreating[i] if i < len(self.sorted_retreating) else ""
            )
            retreating_sources = ", ".join(
                sorted(self.retreating_companies.get(retreating_company, []))
            )

            holding_company = (
                self.sorted_holding[i] if i < len(self.sorted_holding) else ""
            )
            holding_sources = ", ".join(
                sorted(self.holding_companies.get(holding_company, []))
            )

            table_rows.append(
                f"| {retreating_company} | {retreating_sources} | {holding_company} | {holding_sources} |"
            )

        return table_header + "\n".join(table_rows) + "\n"

    def generate_markdown_sources(self):
        # Retreating sources
        source_text = "\n\n## Retreating\n"
        for index, source in enumerate(self.retreating_sources, start=1):
            source_text += (
                f"\n\nR{index}) ({source['date']}) [{source['title']}]({source['url']})"
            )

        # Holding the Line sources
        source_text += "\n\n## Holding the line\n"
        for index, source in enumerate(self.holding_sources, start=1):
            source_text += (
                f"\n\nH{index}) ({source['date']}) [{source['title']}]({source['url']})"
            )

        return source_text

    def generate_markdown(self):
        """Generates the complete markdown output"""
        output = "# Companies holding on and retreating from DEI\n"
        output += self.subtitle
        output += self.generate_markdown_table() + "\n"
        output += self.generate_markdown_sources()
        return output

    def generate_html(self):
        """Generates the complete HTML output with embedded CSS for styling"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Companies and DEI Initiatives</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            margin-left: .5in;
            margin-right: .5in;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .timestamp {
            color: #666;
            font-style: italic;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            line-height: .5;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .sources {
            margin-top: 40px;
        }
        .sources h2 {
            color: #2c3e50;
            margin-top: 30px;
        }
        .source-item {
            margin: 15px 0;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
"""

        # Add title and timestamp
        html += f"<h1>Companies holding on and retreating from DEI</h1>\n"
        html += self.subtitle

        # Generate table
        html += "<table>\n"
        html += "<tr><th>Retreating</th><th>Sources</th><th>Holding the Line</th><th>Sources</th></tr>\n"

        max_len = max(len(self.sorted_retreating), len(self.sorted_holding))
        for i in range(max_len):
            retreating_company = (
                self.sorted_retreating[i] if i < len(self.sorted_retreating) else ""
            )
            retreating_sources = ", ".join(
                sorted(self.retreating_companies.get(retreating_company, []))
            )

            holding_company = (
                self.sorted_holding[i] if i < len(self.sorted_holding) else ""
            )
            holding_sources = ", ".join(
                sorted(self.holding_companies.get(holding_company, []))
            )

            html += f"<tr><td>{retreating_company}</td><td>{retreating_sources}</td><td>{holding_company}</td><td>{holding_sources}</td></tr>\n"

        html += "</table>\n"

        # Add sources
        html += '<div class="sources">\n'

        # Retreating sources
        html += "<h2>Retreating</h2>\n"
        for index, source in enumerate(self.retreating_sources, start=1):
            html += f'<div class="source-item">\n'
            html += f'R{index}) ({source["date"]}) <a href="{source["url"]}">{source["title"]}</a>\n'
            html += "</div>\n"

        # Holding sources
        html += "<h2>Holding the Line</h2>\n"
        for index, source in enumerate(self.holding_sources, start=1):
            html += f'<div class="source-item">\n'
            html += f'H{index}) ({source["date"]}) <a href="{source["url"]}">{source["title"]}</a>\n'
            html += "</div>\n"

        html += "</div>\n"
        html += "</body>\n</html>"

        return html

    def write_outputs(self, markdown_file="dei.md", html_file="index.html"):
        """Writes both markdown and HTML outputs to files"""
        # Write markdown
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(self.generate_markdown())

        # Write HTML
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(self.generate_html())


if __name__ == "__main__":
    manager = DEISourceManager(retreating_sources, holding_sources)
    manager.write_outputs()
