import json


class BaseTransaction():
    def check_tax(self, tax_calculated, price, tax=0.16):
        """
        :param tax_calculated:
        :param price: The price of the item you want to know the tax
        :param tax: The tax amount you want to calculate
        :return: True or False
        """
        tax = price * tax
        if tax == tax_calculated:
            return True
        else:
            return False


class TransactionJson(BaseTransaction):
    def __init__(self, json_data=[], json_file=""):
        """
        :param json_data: send json
        :param json_file: send file json and load it
        """
        if json_file:
            with open(json_file) as f:
                self.data = json.load(f)
        else:
            self.data = json.load(json_data)

