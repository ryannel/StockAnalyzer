import jsonlines
import pandas


class CompanyStock:
    company_name = None
    industry = None
    sector = None
    exchange = None
    symbol = None
    history = []

    def get_dataframe(self):
        history = pandas.DataFrame(self.history)
        history["CompanyName"] = self.company_name
        history["Industry"] = self.industry
        history["Sector"] = self.sector
        history["Exchange"] = self.exchange
        history["Symbol"] = self.symbol

        history["DateTime"] = pandas.to_datetime(history['DateTime'])
        history = history.set_index('DateTime')
        return history.sort_values("DateTime")


class DataProvider:
    _companies = []

    def __init__(self, data_file_path):
        with jsonlines.open(data_file_path) as reader:
            for company in reader:
                self._companies.append(company)

    def get_company(self, exchange, symbol):
        for company in self._companies:
            for stock in company['Stocks']:
                if stock['Symbol'] == symbol and stock['Exchange'] == exchange:
                    result = CompanyStock()
                    result.company_name = company['CompanyName']
                    result.industry = company['Industry']
                    result.sector = company['Sector']
                    result.exchange = stock['Exchange']
                    result.symbol = stock['Symbol']
                    result.history = stock['History']
                    return result