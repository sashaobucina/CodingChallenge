import argparse
from sys import stdin, stdout


class CustomCSVParser:

    def __init__(self, fd_in, fd_out, multiplier, field, fr_locale=False):
        self.source = fd_in
        self.dest = fd_out
        if field <= 0:
            raise ValueError("A valid field must be greater than 0")
        self.price_index = field-1
        self.rate = multiplier

        self.fr_locale = fr_locale

    def parse_csv(self):
        """
        Parses the input CSV file, converts the price into the proper value and locale format, and writes to the output
        CSV file.
        """
        illegal_chars = {'"', '\''}

        # opening the input and output streams
        if self.source == stdin:
            input_file = stdin
        else:
            input_file = open(self.source, 'r+')

        if self.dest == stdout:
            output_file = stdout
        else:
            output_file = open(self.dest, 'w+')

        # initially write the header
        output_file.write(input_file.readline())

        # convert price to proper locale
        for line in input_file:
            columns = [replace_multiple(column, illegal_chars) for column in line.split(',') if column]
            if not self.fr_locale:
                price = columns.pop(self.price_index) + "," + columns[self.price_index+1]
                converted_price = self.__convert_to_us_locale(price)
            else:
                price = columns[self.price_index]
                converted_price = self.__convert_to_french_locale(price)

            columns[self.price_index] = converted_price
            output_file.write(','.join(columns))

        # close any open file streams
        input_file.close()
        output_file.close()

    """
    """

    def __convert_to_french_locale(self, price):
        """
        Converts the price to french locale format given the conversion rate multiplier.
        
        :param price: The price to convert 
        :return: The converted price in French locale format
        """
        converted_price = "%.2f" % (float(price) * self.rate)
        return "€" + converted_price.replace('.', ',')

    def __convert_to_us_locale(self, price):
        """
        Converts the price to US locale format given the conversion rate multiplier.
        
        :param price: The price to convert
        :return: The converted price in US locale format
        """
        if price[0] == '€':
            converted_price = float(price[1:].replace(',', '.')) * self.rate
        else:
            converted_price = float(price.replace(',', '.')) * self.rate
        return "%.2f" % converted_price


def replace_multiple(string, illegal_chars):
    """
    Replaces all instances of characters in the illegal_chars set in the given string.
    
    :param string: The string to modify
    :param illegal_chars: Set of illegal characters
    :return: The string modified to not include any character from the illegal_chars set
    """
    for elem in illegal_chars:
        string = string.replace(elem, '')
    return string


if __name__ == "__main__":
    # sets the valid positional and optional arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("field", type=int, help="The column number that holds the price")
    parser.add_argument("multiplier", type=float, help="The exchange rate at which to convert the price")
    parser.add_argument("-i", "--input", type=str, help="The CSV file data to read in")
    parser.add_argument("-o", "--output", type=str, help="The CSV file data to write out")
    parser.add_argument("-f", "--french_locale",
                        help="Whether to convert to US locale, converts to French locale if not provided",
                        action="store_false")
    args = parser.parse_args()

    # sets the input and output streams, based on positional argument given
    fd_in = args.input if args.input else stdin
    fd_out = args.output if args.output else stdout

    parser = CustomCSVParser(fd_in, fd_out, args.multiplier, args.field, args.french_locale)
    parser.parse_csv()
