import wikipedia
from wikipedia import DisambiguationError, PageError


def get_page(_page_name):

    page_url = ""
    page_summary = ""

    try:
        page = wikipedia.page(page_name)
        page_url = page.title
        page_summary = page.summary
    except DisambiguationError as e:
        print("The page is ambiguous: it may refer to any from the list: ",
              e.options)
    except PageError:
        print("The page couldn't be found")

    return page_url, page_summary


if __name__ == "__main__":

    page_name = input("Enter page title: ")

    url, summary = get_page(page_name)

    if not (url, summary) == ("", ""):
        print("URL: {0}, \nSUMMARY {1}".format(url, summary))
