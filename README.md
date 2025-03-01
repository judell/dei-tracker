# dei-tracker

A tool to help maintain a list of companies retreating and holding the line on DEI, according to cited sources.

## Example

<img width="600" alt="image" src="https://github.com/user-attachments/assets/0c7ebb6c-d0dc-4132-92c8-876fb3c3fc22" />

## Research tips

### Search

Use queries like these:

> companies holding the line on dei after:2025-02-18

> companies retreating from dei after:2025-02-18

### Consolidation

#### How not to use LLMs

Don't expect them to do the research for you, the results will take too much time to check.

#### How to use LLMs

When you find a page like [this](https://time.com/7261857/us-companies-keep-dei-initiatives-list-trump-diversity-order-crackdown/), paste the text into Claude and/or ChatGPT and ask for results like this:

```json
"companies": [
    "Apple",
    "Ben & Jerry's",
    "Costco",
    "Delta Airlines",
    "Francesca's",
    "JPMorgan Chase",
    "Lush",
    "Microsoft",
    "Patagonia",
],
```

This is the kind of gruntwork they can handle, the results are easy to verify, it saves you time and keystrokes.


## Updating

To update the table and source list:

### Add to `retreating_sources` and/or `holding_sources`

```
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
        ...
    }
]
```

```
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
        ...
    }
]
```
### Generate markdown and html

```
python3 dei.py
```

### Test

```
./run-test.sh

Note: 6 companies appear in both categories:
  - Citigroup: Newer in Retreating
  - Coca-Cola: Newer in Holding
  - Goldman Sachs: Newer in Holding
  - JPMorgan Chase: Newer in Holding
  - John Deere: Newer in Holding
  - PepsiCo: Newer in Retreating

New companies as of the most recent date:
  - Retreating (2025-02-21): ['KPMG US']
  - Holding (2025-02-28): ['John Deere', "Francesca's", 'Lush', 'Patagonia']
........
----------------------------------------------------------------------
Ran 8 tests in 0.004s

OK
```
