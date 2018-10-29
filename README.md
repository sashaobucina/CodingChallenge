# About
This program converts given CSV files to output prices in the proper country locale.

# Help
Run the command "python3 currency_converter --help" in your terminal to get a description on how to use the program

usage: currency_converter.py [-h] [-i INPUT] [-o OUTPUT] [-f] field multiplier

positional arguments:<br />
  * field                 The column number that holds the price<br />
  * multiplier            The exchange rate at which to convert the price<br />

optional arguments:<br />
  * -h, --help
    * show this help message and exit<br />
  * -i INPUT, --input INPUT<br />
    * The CSV file data to read in
  * -o OUTPUT, --output OUTPUT<br />
    * The CSV file data to write out
  * -f, --french_locale
    * Whether to convert to French locale, converts to US locale if not provided<br />
  

# Example usage
Run "python3 currency_converter.py 2 0.8 < ../datasets/us_format/data.csv > ../datasets/french_format/data-fr.csv" in the custom_parser directory

OR

Run currency_converter.py through an IDE of your choice specifying proper command line arguments

# Requirements
Please run the program using pyhton3.x as to provide ASCII support for the "€" symbol
