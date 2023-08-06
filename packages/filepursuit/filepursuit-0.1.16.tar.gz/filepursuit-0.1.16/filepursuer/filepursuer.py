import argparse
# import file_scraper as scraper
from . import file_scraper as scraper


def show_results_page(results):
    for result in results:
        print("[{:0>3s}] {} | {}".format(str(result["id"]), result["type"], result["name"][:-4]))


def show_options(_next):
    if _next:
        _choice = input("\n[1] Next page\n[2] Download \n[*] Exit\n\n[>] Choice?: ")
    else:
        _choice = input("\n[!] There are no more pages left!\n[2] Download \n[*] Exit\n\n[>] Choice?: ")

    return _choice


def show_downloads(results, output):
    lista = list(input("[>] Which ones do you want to download? (space separated values): ").split(" "))
    lista = [int(i) for i in lista]
    if lista != ['']:
        for i in lista:
            try:
                if i <= results[len(results) - 1]["id"]:
                    if results[i]["name"][-1] == '>':  # Some names have a small html tag at the end
                        scraper.download_file(results[i]["link"], output,
                                              results[i]["name"][:-4])
                    else:
                        scraper.download_file(results[i]["link"], output,
                                              results[i]["name"])
                    print(chr(27) + "[2J")  # Clean terminal
                else:
                    print("[INFO] That option is not available, please select another one.")
            except Exception as e:
                print(e)
                continue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="Search terms")
    parser.add_argument("-o", "--output", help="Path of saved files")
    parser.add_argument("-t", "--type", help="Type of searched files (all, video, audio, ebook, archive, mobile)",
                        default="all")
    args = parser.parse_args()

    try:
        total_results = []
        search_term = args.search.replace(" ", "+")
        page_number = 0
        last_page = -1

        print("[INFO] Search results for {}".format(search_term))

        while True:
            if last_page != page_number:
                page_results = scraper.get_results_list(search_term, page_number, args.type)
                total_results.extend(page_results)
                next = scraper.next()

            if page_results is None:
                print("[INFO] Something went wrong getting the page!")
                break

            show_results_page(page_results)
            last_page = page_number
            choice = show_options(next)

            if choice == '1' and next:
                page_number += 49
            elif choice == '2':
                show_downloads(total_results, args.output)
            else:
                break
    except AttributeError:
        parser.print_help()
