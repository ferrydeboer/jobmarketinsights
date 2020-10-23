import datetime
import re

from bs4 import BeautifulSoup

from jomai.models import Job


class FreelanceNl:
    today_re = re.compile("[0-9]* (uur|minuut|minuten)")

    def parse_file(self, file_name):
        # In case content needs to be read from a file first!
        pass

    def parse_content(self, file_contents):
        # try:
        soup = BeautifulSoup(file_contents, 'html.parser')
        projects_list = soup.find("ul", "listing projects")
        linkid = re.compile("/opdracht/.*")
        projects = projects_list.find_all_next(href=linkid)

        for project in projects:
            job = self.parse_job(project)
            # if vacancy.url in self.vacancies:
            #    org_vacancy = self.vacancies[vacancy.url]
            #    print(f"vacancy {vacancy.title} already exists, updating {org_vacancy.keywords} with {keys}")
            #    org_vacancy.keywords = org_vacancy.keywords + keys
            # else:
            #    self.vacancies[vacancy.url] = vacancy
            yield job

        # except Exception as ex:
        #     TODO: Wrap exception

    def parse_job(self, a_tag):
        url = a_tag['href']
        title_tag = a_tag.find_next("span", {"class": "title"})
        location = title_tag.find_next_sibling("span", {"class": "location"}).text
        applications = title_tag.find_next_sibling("span", {"class": "applications"}).text
        date = self.parse_date(title_tag.find_next_sibling("span", {"class": "date"}).text)
        # can_read = 'pro' not in a_tag.parent.parent['class']

        return Job(
            url=url,
            title=title_tag.text,
            location=location,
            applications=int(applications),
            posted_on=date)

    @staticmethod
    def parse_date(date: str):
        if FreelanceNl.today_re.match(date):
            return datetime.date.today()
        return datetime.datetime.strptime(date, '%d-%m-%Y')
