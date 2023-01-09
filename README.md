# Logofinder

TLDR: This projects implements webcrawlers that search for companies logos.

## The logic behind code

![](diagram.png)

The system has two main parts: processing and crawling.

The processing is responsible for cleaning up the data, making the crawler search more assertive. That said, the `CompanyDataProcessor` class is the protocol class that represents the processors expected behavior. Each processor should take a `CompanyInfo` list as argument, validates its data and process it.