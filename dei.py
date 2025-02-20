from datetime import date, datetime

retreating_sources = [
    {
        "date": "2025-02-17",
        "title": "Forbes: Banks Including JPMorgan Chase and Morgan Stanley Reportedly Cutting Back DEI References",
        "url": "https://www.forbes.com/sites/conormurray/2025/02/17/banks-including-jpmorgan-chase-and-morgan-stanley-reportedly-cutting-back-dei-references-here-are-all-the-companies-rolling-back-dei/",
        "companies": [
            "Amtrak", "Bank of America", "Boeing", "Brown-Forman (Jack Daniel's)", "Chipotle",
            "Citigroup", "Coca-Cola", "Comcast", "Deloitte", "Disney", "Ford Motor Co.",
            "General Electric (GE)", "Goldman Sachs", "Google", "Harley-Davidson", "Intel",
            "John Deere", "JPMorgan Chase", "Lowe's", "McDonald's", "Meta (Facebook)",
            "Molson Coors", "Morgan Stanley", "NPR", "PBS", "PayPal", "PepsiCo",
            "Smithsonian Institution", "Target", "The FBI", "Walmart", "Wells Fargo"
        ]
    },
    {
        "date": "2025-02-12",
        "title": "AP: Which US Companies Are Pulling Back on Diversity Initiatives",
        "url": "https://www.ap.org/news-highlights/spotlights/2025/which-us-companies-are-pulling-back-on-diversity-initiatives/",
        "companies": [
            "Amazon", "Brown-Forman (Jack Daniel's)", "Ford Motor Co.", "Goldman Sachs",
            "Google", "Harley-Davidson", "John Deere", "Lowe's", "McDonald's",
            "Meta (Facebook)", "Target", "Tractor Supply", "Walmart"
        ]
    },
    {
        "date": "2025-02-11",
        "title": "TechTarget: What Companies Are Rolling Back DEI Policies",
        "url": "https://www.techtarget.com/whatis/feature/What-companies-are-rolling-back-DEI-policies",
        "companies": ["Apple", "Costco", "Delta Airlines", "Microsoft"]
    }
]

holding_sources = [
    {
        "date": "2025-02-18",
        "title": "Newsweek: DEI Companies Program List Policies Donald Trump",
        "url": "https://www.newsweek.com/dei-companies-program-list-policies-donald-trump-2032960",
        "companies": [
            "Apple", "Costco", "Delta Airlines", "E.L.F. Beauty", "Meijer", "Microsoft",
            "Procter & Gamble", "Sephora"
        ]
    },
    {
        "date": "2025-02-17",
        "title": "Report: 46 Companies Sticking With DEI",
        "url": "https://buildremote.co/companies/keeping-dei/",
        "companies": [
            "Abercrombie and Fitch", "Adobe", "Alliance Health", "Ancestry",
            "Apple", "Ben & Jerry's", "Bering Straits Native Corporation", 
            "Best Buy", "BJ's Wholesale", "Chick-fil-A", "Cigna", "Citigroup",
            "Deutsche Bank", "Dollar Tree", "Gap Inc.", "Goldman Sachs", "GoTo Foods",
            "HLW", "Honda", "Johnson & Johnson", "JPMorgan Chase", "Kroger",
            "Logitech", "Macy's", "Mastercard", "MassMutual", "Match Group",
            "McKinsey & Company", "Meijer", "Microsoft", "Mitre",
            "National Football League", "Nike", "Old Navy", "PepsiCo",
            "Philip Morris International", "Pinterest", "Progressive",
            "Procter & Gamble", "Sephora", "Tiffany & Co", "TJX Companies",
            "Ulta Beauty", "Wilson Sonsini Goodrich & Rosati"
        ]
    },    
    {
        "date": "2025-02-04",
        "title": "The Root: A List of Companies That Continue to Support DEI",
        "url": "https://www.theroot.com/a-list-of-companies-that-continue-to-support-dei-1851755249",
        "companies": [
            "American Airlines", "Apple", "Cisco", "Cleveland Cavaliers", "Costco",
            "Delta Airlines", "E.L.F. Beauty", "Microsoft", "Nasdaq", "Pinterest",
            "Salesforce", "Southwest Airlines", "United Airlines"
        ]
    },
    {
        "date": "2025-01-31",
        "title": "Business Insider: Companies Supporting DEI Efforts - CEO Comments",
        "url": "https://www.businessinsider.com/companies-supporting-dei-efforts-ceo-comments-2025-1",
        "companies": ["Cisco", "Costco", "Deutsche Bank"]
    }
]

def generate_markdown_table():
    table_header = (
        "| Retreating | Sources | Holding the Line | Sources |\n"
        "|------------|---------|------------------|---------|\n"
    )

    max_len = max(len(sorted_retreating), len(sorted_holding))
    table_rows = []
    for i in range(max_len):
        retreating_company = sorted_retreating[i] if i < len(sorted_retreating) else ""
        retreating_sources = ", ".join(sorted(retreating_companies.get(retreating_company, [])))

        holding_company = sorted_holding[i] if i < len(sorted_holding) else ""
        holding_sources = ", ".join(sorted(holding_companies.get(holding_company, [])))

        table_rows.append(f"| {retreating_company} | {retreating_sources} | {holding_company} | {holding_sources} |")

    return table_header + "\n".join(table_rows) + "\n"

def generate_markdown_sources():
    # Holding the Line sources
    source_text = "## Holding the line\n"
    for index, source in enumerate(holding_sources, start=1):
        source_text += f"\n\nH{index}) ({source['date']}) [{source['title']}]({source['url']})"

    # Retreating sources
    source_text += "\n\n## Retreating\n"
    for index, source in enumerate(retreating_sources, start=1):
        source_text += f"\n\nR{index}) ({source['date']}) [{source['title']}]({source['url']})"

    return source_text

class DEISourceManager:
    def __init__(self, retreating_sources=None, holding_sources=None):
        self.retreating_sources = retreating_sources or []
        self.holding_sources = holding_sources or []
        self.retreating_companies = {}
        self.holding_companies = {}
        self.sorted_retreating = []
        self.sorted_holding = []
        
        # Process sources if provided at init
        if retreating_sources or holding_sources:
            self.process_sources()
    
    def process_sources(self):
        """Exactly matches the original source processing logic"""
        self.retreating_companies = {}
        self.holding_companies = {}
        

        # Sort sources by date, newest first
        self.retreating_sources.sort(
            key=lambda s: datetime.strptime(s["date"], "%Y-%m-%d"),
            reverse=True
        )
        self.holding_sources.sort(
            key=lambda s: datetime.strptime(s["date"], "%Y-%m-%d"),
            reverse=True
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
        """Exactly matches the original table generation"""
        table_header = (
            "| Retreating | Sources | Holding the Line | Sources |\n"
            "|------------|---------|------------------|---------|\n"
        )

        max_len = max(len(self.sorted_retreating), len(self.sorted_holding))
        table_rows = []
        for i in range(max_len):
            retreating_company = self.sorted_retreating[i] if i < len(self.sorted_retreating) else ""
            retreating_sources = ", ".join(sorted(self.retreating_companies.get(retreating_company, [])))

            holding_company = self.sorted_holding[i] if i < len(self.sorted_holding) else ""
            holding_sources = ", ".join(sorted(self.holding_companies.get(holding_company, [])))

            table_rows.append(f"| {retreating_company} | {retreating_sources} | {holding_company} | {holding_sources} |")

        return table_header + "\n".join(table_rows) + "\n"

    def generate_markdown_sources(self):
        """Exactly matches the original source list generation"""
        # Holding the Line sources
        source_text = "## Holding the line\n"
        for index, source in enumerate(self.holding_sources, start=1):
            source_text += f"\n\nH{index}) ({source['date']}) [{source['title']}]({source['url']})"

        # Retreating sources
        source_text += "\n\n## Retreating\n"
        for index, source in enumerate(self.retreating_sources, start=1):
            source_text += f"\n\nR{index}) ({source['date']}) [{source['title']}]({source['url']})"

        return source_text

    def generate_markdown(self):
        """Generates the complete markdown output"""
        output = "# Companies holding on and retreating from DEI\n"
        output += f'*generated {date.today().strftime("%Y-%m-%d")}*\n\n'
        output += self.generate_markdown_table() + "\n"
        output += self.generate_markdown_sources()
        return output

if __name__ == "__main__":
    manager = DEISourceManager(retreating_sources, holding_sources)
    print(manager.generate_markdown())