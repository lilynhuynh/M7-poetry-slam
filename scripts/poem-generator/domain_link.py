from bs4 import BeautifulSoup as domain_scraper
import requests
import nltk

# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('words')

class Domain():
    def __init__(self, query):
        print("Booting up domain finder...")
        url = f"https://www.merriam-webster.com/thesaurus/{query}"
        scraper = self.create_scraper(url)
        print(url)

        self.synonyms = []
        self.antonyms = []

        sim_span = scraper.find("span", class_="sim-list-scored")
        sim_list = sim_span.find("ul")
        sim_list_items = sim_list.find_all("span", class_="syl")
        self.synonyms = [self.enclosed_case(span.get_text()) for span in sim_list_items]

        opp_span = scraper.find("span", class_="opp-list-scored")
        if opp_span != None:
            opp_list = opp_span.find("ul")
            opp_list_items = opp_list.find_all("span", class_="syl")
            self.antonyms = [self.enclosed_case(span.get_text()) for span in opp_list_items]

        self.domain_words = self.synonyms + self.antonyms

    def create_scraper(self, link):
        """
        Creates a beautiful soup object based on the given page link
        """

        headers = {"User-Agent": "Mozilla/5.0"} # avoids Google blocking
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            return domain_scraper(response.text, "html.parser")
        else:
            print(
                f"Failed to fetch webpage. Status code:{response.status_code}")
            

    def enclosed_case(self, line):
        """
        Handles any enclosed case in the string and returns a string without
        enclosed cases (i.e. parentheses, brackets, curly brackets)
        """

        removed_parentheses = ""
        skip = 0
        for char in line:
            if char == "(" or char == "[" or char == "{":
                skip += 1
            elif char == ")" or char == "]" or char == "}":
                skip -= 1
            elif skip == 0:
                removed_parentheses += char
        return removed_parentheses.strip()
    
# def test():
#     test = Domain("love")
#     print(test.synonyms)
#     print(test.antonyms)

# test()