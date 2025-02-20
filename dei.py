
from datetime import date

retreating_sources = [
    {
        "date": "2025-02-17",
        "title": "Forbes: Banks Including JPMo5rgan Chase and Morgan Stanley Reportedly Cutting Back DEI References",
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

# Extract unique companies and dynamically assign source labels
retreating_companies = {}
holding_companies = {}

# Assign dynamic source labels (R1, R2, ...) based on order in the list
for index, source in enumerate(retreating_sources, start=1):
    source_label = f"R{index}"
    for company in source["companies"]:
        # If the company exists in Holding, remove it first (newest category wins)
        if company in holding_companies:
            del holding_companies[company]

        if company not in retreating_companies:
            retreating_companies[company] = []
        retreating_companies[company].append(source_label)

# Assign dynamic source labels (H1, H2, ...) for holding the line
for index, source in enumerate(holding_sources, start=1):
    source_label = f"H{index}"
    for company in source["companies"]:
        # If the company was already marked as retreating, ignore it (newest source wins)
        if company in retreating_companies:
            continue

        if company not in holding_companies:
            holding_companies[company] = []
        holding_companies[company].append(source_label)

# Sort companies alphabetically
sorted_retreating = sorted(retreating_companies.keys())
sorted_holding = sorted(holding_companies.keys())

# Generate Markdown Table
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

# Generate Markdown for Sources
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

# Generate final Markdown
markdown_output = "# Companies holding on and retreating from DEI"

markdown_output += f'\n*generated {date.today().strftime("%Y-%m-%d")}*\n'


markdown_output += generate_markdown_table() + "\n" + generate_markdown_sources()

# Output Markdown to console
print(markdown_output)
