import requests
import json
import re
from datetime import datetime
import time
from parsehub_config import (
    API_KEY,
    PROJECT_TOKEN,
    RUN_TOKEN,
    NAME,
    DIRECTORY
)


class GenerateReport:
    def __init__(self, file_name, results):
        self.file_name = file_name
        self.result = results
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'data': self.result
        }
        print("Creating report...")
        with open('{}/{}.json'.format(DIRECTORY, self.file_name), 'w') as f:
            json.dump(report, f)
        print("Done")

    def get_now(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            'api_key': self.api_key,
            'format': json
        }
        self.get_data()

    def get_data(self):
        print("Updating the data...")
        requests.post(
            'https://www.parsehub.com/api/v2/projects/{}/run'.format(self.project_token), data=self.params)

        time.sleep(60)

        response = requests.get(
            'https://www.parsehub.com/api/v2/projects/{}/last_ready_run/data'.format(self.project_token), params=self.params)
        self.data = json.loads(response.text)

    def get_total_cases(self):
        data = self.data['total']
        Total_cases = []
        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                Total_cases.append(content)
                return content['value']
        return Total_cases

    def get_total_deaths(self):
        data = self.data['total']
        Total_deaths = []
        for content in data:
            if content['name'] == 'Deaths:':
                Total_deaths.append(content)
                return content['value']
        return Total_deaths

    def get_country_data(self):
        data = self.data['countries']
        countries_data = []
        for content in data:
            if content['name'] and content['total_cases'] and content['active_cases']:
                countries_data.append(content)
        return countries_data

    def run(self):
        print(" Starting looking for data...")
        print("Total cases worldwide...")
        data_total_cases = self.get_total_cases()
        print("Total death cases worldwide...")
        data_total_deaths = self.get_total_deaths()
        print("Data per country...")
        data_countries = self.get_country_data()
        results = {
            'total_cases': data_total_cases,
            'total_deaths': data_total_deaths,
            'data_per_country': data_countries
        }
        return results


if __name__ == "__main__":
    print("Coronavirus cases")
    data = Data(API_KEY, PROJECT_TOKEN)
    results = data.run()
    GenerateReport(NAME, results)
