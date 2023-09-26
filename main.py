from api_handler import ApiHandler
from data_handler import NamesDataHandler, ListsDataHandler
from html_maker import HtmlMaker
import colorama
from datetime import datetime, date

# This programme uses the New York Times Books API to obtain data in json format relating to the
# best-selling book charts published by the New York Times. To obtain an API Key:
# 1. Create an account at https://developer.nytimes.com/accounts/create
# 2. Once you have verified your account, sign in and select “Apps” from the drop-down menu.
# 3. Click on "New App"
# 4. Enter a name and description for your app
# 5. Click the “Enable” button corresponding to the Books API, and then click “Save”
# 6. Your API key will now be generated.
API_KEY = "your api key"  # update this value to your API key

# To enable use of the colorama module, the init function must be called
colorama.init()

# prints header
print(colorama.Back.BLUE + colorama.Fore.BLACK + R"""
   _____________________
  |                     |         Generate current and historical New York Times
  |  N o v e l L i s t  |         best-selling book charts by category and date  
  |_____________________|         
 
  Powered by the New York Times Books API
""")

print(colorama.Style.RESET_ALL + "\n NovelList is a program which allows you to generate a list of the New York\n"
                                 " Times top 10 best-selling books for a category and date of your choice. As\n"
                                 " an html file which can be viewed in your web browser.\n")

# array of categories - each tuple contains the category as it is printed in the output, and the encoded category
# which is used in the URL for the API call.
categories = [("Combined Print and E-book Fiction", "combined-print-and-e-book-fiction"),
              ("Hardback Fiction", "hardcover-fiction"),
              ("Paperback Fiction", "trade-fiction-paperback"),
              ("Combined Print and E-book Nonfiction", "combined-print-and-e-book-nonfiction"),
              ("Hardback Nonfiction", "hardcover-nonfiction"),
              ("Paperback Nonfiction", "paperback-nonfiction"),
              ("Children's Picture Books", "picture-books"),
              ("Children's Hardback Fiction", "childrens-middle-grade-hardcover"),
              ("Children's Paperback Fiction", "childrens-middle-grade-paperback"),
              ("Young Adult Hardback Fiction", "young-adult-hardcover"),
              ("Graphic Books and Manga", "graphic-books-and-manga")]

# main loop
program_running = True
while program_running:

    # prints numbered list of categories
    print(colorama.Fore.LIGHTWHITE_EX + colorama.Back.BLACK + "\n Categories")
    print("-----------------------------------------")


    def numbered_category(index: int):
        return f" {index+1}. {categories[index][0]}"


    for i in range(len(categories)):
        if "Children" in categories[i][0]:
            print(colorama.Fore.LIGHTGREEN_EX + numbered_category(i))

        elif "Young Adult" in categories[i][0]:
            print(colorama.Fore.LIGHTBLUE_EX + numbered_category(i))

        elif "Nonfiction" in categories[i][0]:
            print(colorama.Fore.LIGHTYELLOW_EX + numbered_category(i))

        elif "Fiction" in categories[i][0]:
            print(colorama.Fore.LIGHTRED_EX + numbered_category(i))

        else:
            print(colorama.Fore.LIGHTMAGENTA_EX + numbered_category(i))

    # User is prompted to select a category - while loop repeats the prompt until a valid input is received
    print(colorama.Style.RESET_ALL + "")

    chosen_cat_num = 0

    while chosen_cat_num < 1 or chosen_cat_num > len(categories):
        try:
            chosen_cat_num = \
                int(input(f"Please start by choosing a category (enter a number between 1 and {len(categories)}): "))
            if chosen_cat_num < 1 or chosen_cat_num > len(categories):
                print(f"Invalid category number.")
        except ValueError:
            print(f"Invalid input.")
        print("")

    chosen_cat_name = categories[chosen_cat_num - 1][0]
    chosen_cat_encoded = categories[chosen_cat_num - 1][1]

    # instantiate ApiHandler object and make api call to get data relating to list names
    api_handler = ApiHandler(API_KEY)
    names_data = api_handler.list_names_call()

    # instantiate NamesDataHandler object to organise the data returned by the API call
    names_data_handler = NamesDataHandler(names_data)

    frequency = names_data_handler.get_frequency(chosen_cat_encoded)
    start_date = names_data_handler.get_start_date(chosen_cat_encoded)
    end_date = names_data_handler.get_end_date(chosen_cat_encoded)

    # function to change format of date string from YY-MM-DD to DD/MM/YYYY
    def format_date(date: str):
        return f"{date[8:]}/{date[5:7]}/{date[:4]}"


    start_date_formatted = format_date(start_date)
    end_date_formatted = format_date(end_date)

    # print info showing the name of the chosen category and the frequency that it is updated
    print(colorama.Back.BLUE + colorama.Fore.BLACK + f" You chose {chosen_cat_name}.")
    print(f" The New York Times {chosen_cat_name} chart is updated {frequency.lower()}.")

    print(colorama.Style.RESET_ALL + "")

    # function to convert a date string of format DD/MM/YYYY to a date object
    def string_to_date(date: str):
        return datetime.strptime(date, "%d/%m/%Y").date()

    # User is prompted to select a date - while loop repeats the prompt until a valid input is received
    date_valid = False
    chosen_date = ""

    while not date_valid:
        chosen_date = input(f"Please enter a date between {start_date_formatted} and {end_date_formatted} to see "
                            f"the chart \non that date, or press enter to see the current chart (DD/MM/YYYY): ")

        if chosen_date == "":
            date_valid = True

        else:
            try:
                if chosen_date[2] == "/" and chosen_date[5] == "/" and \
                        string_to_date(start_date_formatted) <= string_to_date(chosen_date) <= string_to_date(end_date_formatted):
                    date_valid = True
                elif chosen_date[2] == "/" and chosen_date[5] == "/":
                    print("The date that you have entered is not in the specified range.")
                else:
                    print("You have entered the date in the wrong format.")
            except (IndexError, ValueError):
                print("You have entered the date in the wrong format.")

    # format date for API call URL
    chosen_date_formatted = "current"
    if chosen_date != "":
        chosen_date_formatted = f"{chosen_date[6:]}-{chosen_date[3:5]}-{chosen_date[:2]}"

    print("")

    # make api call to get data relating to chosen book list
    books_data = api_handler.lists_call(chosen_cat_encoded, chosen_date_formatted)

    # file name that results will be written to
    if chosen_date_formatted == "current":
        file_name = f"{chosen_cat_encoded}-{str(date.today())}.html"
    else:
        file_name = f"{chosen_cat_encoded}-{chosen_date_formatted}.html"

    # print books list title to the console and text file
    list_title = f"The New York Times Top 10 Best-Selling {chosen_cat_name} " \
                 f"on {chosen_date if chosen_date!='' else format_date(str(date.today()))}"
    print(colorama.Back.BLUE + colorama.Fore.BLACK + " " + list_title)
    print(f" See {file_name} for more information on each book.\n"
          f" (note: You must exit the program before you are able to view the html file!)")
    print("-" * 77)

    # instantiate ListsDataHandler object
    books_data_handler = ListsDataHandler(books_data)

    # prints books list to the console
    for i in range(10):
        print(" " + books_data_handler.list_entry_string(i))

    # writes books list to html file
    html_maker = HtmlMaker(list_title, books_data)
    html_maker.make_html_file(file_name)

    # User is asked whether they want to generate another book list
    print(colorama.Style.RESET_ALL + "")
    user_continue = "unknown"
    while user_continue == "unknown":
        user_continue = input("Would you like to generate another list? (y/n): ")
        if user_continue.lower() == "n":
            program_running = False
            print(colorama.Fore.BLACK + colorama.Back.BLUE + " I hope you enjoyed using NovelList! Bye!")
        elif user_continue.lower() != "y":
            user_continue = "unknown"
            print("Invalid input.")