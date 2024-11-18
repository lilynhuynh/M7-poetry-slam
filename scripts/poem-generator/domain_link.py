from bs4 import BeautifulSoup as domain_scraper
import requests

class Domain():
    def __init__(self, query):
        print("Booting up domain finder...")
        url = f"https://www.merriam-webster.com/thesaurus/{query}"
        scraper = self.create_scraper(url)

        sim_span = scraper.find("span", class_="sim-list-scored")
        opp_span = scraper.find("span", class_="opp-list-scored")

        sim_list = sim_span.find("ul")
        opp_list = opp_span.find("ul")

        sim_list_items = sim_list.find_all("span", class_="syl")
        opp_list_items = opp_list.find_all("span", class_="syl")

        synonyms = [span.get_text() for span in sim_list_items]
        antonyms = [span.get_text() for span in opp_list_items]

        print(synonyms)
        print(antonyms)

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
    
def test():
    test = Domain("love")

test()