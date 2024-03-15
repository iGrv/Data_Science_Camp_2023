import sys
import requests


def main():

    # Check the command line arguments
    if len(sys.argv) != 3:
        exit(f'Usage: {sys.argv[0]} title filename.txt')

    # Get the content of a Wikipedia article by a given title
    title = sys.argv[1]
    contents = get_article(title)

    # Save the content to the text file
    filename = sys.argv[2]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(contents)


def get_article(title):
    '''
    Retrieves text content of a Wikipedia article. Uses Wikipedia API
    :param title: title of the article
    :type title: str
    :return: text content of the article
    :rtype: str
    :raises Exception: If API request was not successful
    '''
    # Perform GET request to retrieve the content of Wikipedia article
    params = {
        'action': 'query', 
        'format': 'json',  # Specify JSON format for the response
        'prop': 'extracts',  # Use TextExtracts extension
        'titles': title,
        'explaintext': True
    }
    response = requests.get('https://en.wikipedia.org/w/api.php', params=params)

    # Check if HTTP request was successful
    if response.status_code != 200:
        raise Exception('')

    # Convert the response into JSON
    response = response.json()

    # Return the content of the article page
    page, = response['query']['pages'].values()
    return page['extract']


if __name__ == "__main__":
    main()
