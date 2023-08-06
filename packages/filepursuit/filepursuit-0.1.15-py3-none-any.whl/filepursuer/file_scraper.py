import warnings
import requests
from bs4 import BeautifulSoup

cont = 0
next_page = False
headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}

def get_results_list(search_term, row_number, file_type):
    global cont
    global next_page
    global headers
    base_url = "https://filepursuit.com/zearch/{}/filetype/" + file_type + "//startrow/{}"


    page = requests.get(base_url.format(search_term, row_number), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        tbody = soup.select('.table > tbody')[0].descendants
        next_page = has_next_page(base_url.format(search_term, row_number), headers)
    except IndexError:
        print("\nYour search : {}\n- did not match any file. \nSuggestions:\n[*] We highly recommend "
              "you to use English language.\n[*] Make sure that all words are spelled correctly.\n[*] Try different, "
              "fewer or more general keywords.\n[*] Try with valid filetype/extension.\n[*] Type atleast 3 letters.\n"
              .format(search_term)
              )
        return None

    results_list = []
    result = {}
    for i in tbody:
        for item in i:
            try:
                if item != "\n":
                    if "filetype" in item.find('a')['href']:
                        result = {"type": repr(item.find('a')['href'][-3:])}

                    if "/file/" in item.find('a')['href']:
                        result["link"] = repr(item.find('a')['href'])
                        result["name"] = str(item.find('a'))[str(item.find('a')).index('>') + 1:]
                        result["id"] = cont
                        cont += 1
                        results_list.append(result)
            except ValueError:
                result["name"] = str(item.find('a'))
            except:
                continue
    return results_list


def has_next_page(url, headers):  # setNext()
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # CSS Selector of the 'Next' button
    return soup.select('html body div.container div ul.pager li.next.btn-lg a strong') != []


def next():  # getNext()
    return next_page


def get_link(site):
    global headers
    from requests_html import HTMLSession
    session = HTMLSession()

    site = session.get("https://filepursuit.com" + site.replace("'", ""), headers=headers)
    site.html.render()

    # Download link box
    about = site.html.xpath('/html/body/div[2]/div[4]/button')[0]

    return about.attrs.get('data-clipboard-text').replace(" ", "")


def download_file(file_link, file_path, file_name):
    """
    In chunked transfer encoding, the data stream is divided into a series
    of non-overlapping "chunks". The chunks are sent out and received independently
    of one another. No knowledge of the data stream outside the currently-being-processed
    chunk is necessary for both the sender and the receiver at any given time.

    """

    from clint.textui import progress

    try:
        print("\n[INFO] Downloading {} ...".format(file_name))
        file = requests.get(file_link, stream=True, headers={'Connection': 'close'})
        with open("{}{}".format(file_path, file_name), "wb") as output:

            if file.headers.get('content-length') is not None:
                total_length = int(file.headers.get('content-length'))

                for chunk in progress.bar(file.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                    if chunk:
                        output.write(chunk)
                        output.flush()
            else:  # TODO how to show a progress bar without knowing the size of the file?
                output.write(file.content)
            print("[INFO] Download OK")
    except requests.exceptions.ConnectionError as e:
        warnings.warn(e.response)


if __name__ == '__main__':
    pass
