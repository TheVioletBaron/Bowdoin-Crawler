"""
Casey Edmonds-Estes
Project 2
10/31/18
"""

import sys
from Filters import filter_urls, filter_emails, filter_phones
import requests


class WebPage:
    """
    Seaches a web page for email adresses, phone numbers, and urls
    """
    def __init__(self, url, phone_numbers = [], urls = [], emails = []):
        """
        Initializes a WebPage's state with the url, and populates:
        - the set of urls in the WebPages's source
        - the set of emails in the WebPages's source
        - the set of phone numbers in the WebPages's source
        Args:
            url (str): the url to search
        """        
        self._url = url
        self._phone_numbers = phone_numbers
        self._urls = urls
        self._emails = emails
    

    def __hash__(self):
        """Return the hash of the URL"""
        return hash(self.url())

    def __eq__(self, page):
        """
        return True if and only if the url of this page equals the url
        of page.
        Args:
            page (WebPage): a WebPage object to compare
        """
        if self._url == page._url:
            return True
        else:
            return False

    def populate(self):
        """
        fetch this WebPage object's webpage text and populate its content
        """
        text = requests.get(self._url)
        # can write string method
        if text.status_code == requests.codes.ok:
            self._urls = filter_urls(text.text)
            self._phone_numbers = filter_phones(text.text)
            self._emails = filter_emails(text.text)

    def url(self):
        """return the url asssociated with the WebPage"""
        return self._url

    def phone_numbers(self):
        """return the phone numbers associated with the WebPage"""
        return self._phone_numbers

    def emails(self):
        """return the email addresses associated with the WebPage"""
        return self._emails

    def urls(self):
        """return the URLs associated with the WebPage"""
        return self._urls


class WebCrawler:
    """
    Starting from a base url, seaches through all urls on that page and the pages
    associated with the urls it finds, collecting phone numbers and email adresses
    as it goes
    """
    def __init__(self, base_url, max_links=50, all_phones=[], all_urls=[], all_emails=[]):
        """
        Initialize the data structures required to crawl the web.
        Args:
           base_url (str): the starting point of our crawl
           max_links (int): after traversing this many links, stop the crawl
        """
        self.base_url = base_url
        self.max_links  = max_links
        self.all_phones = all_phones
        self.all_urls = all_urls
        self.all_emails = all_emails

    def crawl(self):
        """
        starting from self._base_url and until stopping conditions are met,
        creates WebPage objects and recursively explores their links.
        """
        data = WebPage(self.base_url)
        data.populate()
        to_visit = data.urls()
        visit_count = 0
        visited_list = []
        while len(to_visit) > visit_count + 1 and visit_count != self.max_links:
            visit_count += 1
            if to_visit[visit_count] not in visited_list:
                current_url = to_visit[visit_count]
                visited_list.append(current_url)
                current_crawl = WebPage(current_url)
                current_crawl.populate()
                to_visit += current_crawl.urls()
                self.all_phones += current_crawl.phone_numbers()
                self.all_emails += current_crawl.emails()
        self.all_urls = set(visited_list)
        self.all_phones = set(self.all_phones)
        self.all_emails = set(self.all_emails)
        
    def all_emails(self):
        """
        returns the set of all email addresses harvested during a
        successful crawl
        """
        return self.to_all_emails

    def all_phones(self):
        """
        returns the set of all phone numbers harvested during a
        successful crawl
        """
        return self.to_all_phones

    def all_urls(self):
        """
        returns the set of all urls traversed during a crawl
        """
        return self.to_all_urls

    def output_results(self, filename):
        """
        In an easy-to-read format, writes the report of a successful crawl
        to the file specified by 'filename'.
        This includes the starting url, the set of urls traversed,
        all emails encountered, and the set of phone numbers (recorded in
        a standardized format of NPA-NXX-XXXX).
        """
        file = open(filename, 'w')
        
        file.write("The url from which this data came is " + self.base_url + "\n")
        file.write("Here are the urls the program found: \n")
        for i in self.all_urls:
            file.write(i + '\n')
        file.write("Here are the phone numbers the program found: \n")
        for i in self.all_phones:
            file.write(i + '\n')
        file.write("Here are all the email addresses the program found: \n")
        for i in self.all_emails:
            file.write(i + '\n')
        file.close()

def usage():
    print("python3 crawl.py <base_url> <report_file>")
    print("\tbase_url: the initial url to crawl")
    print("\treport_file: file where all results are written")

if __name__ == '__main__':

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    base_url = sys.argv[1]
    report_path = sys.argv[2]

    crawl = WebCrawler(base_url, 15) # until you are confident use small max_links
    crawl.crawl()
    crawl.output_results(report_path)
