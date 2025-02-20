# dei-tracker

A tool to help maintain a list of companies retreating and holding the line on DEI, according to cited sources.

## Example

<img width="600" alt="image" src="https://github.com/user-attachments/assets/d8f94aa1-224c-44a5-b1a5-f7cfa885132a" />


## Updating

To update the table and source list, add to the these structures and rerun dei.py.

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
