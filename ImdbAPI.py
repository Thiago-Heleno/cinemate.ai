from bs4 import BeautifulSoup
import requests
import json

# Headers to mimic the curl request
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.imdb.com/",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

class ImdbAPI():
  
  def __init__(self):
        # Initialize your API here
        pass
  
  def search(self, query: str, *args, **kwargs) -> str:
    if args:
      print(f"Additional positional arguments: {args}")
    if kwargs:
      print(f"Additional keyword arguments: {kwargs}")
      
    r = requests.get(f'https://www.imdb.com/search/title/?genres={query}&sort=num_votes,desc', stream=True, headers=headers)

    # Save to .txt file
    # if r.status_code == 200:
    #     # Write the response text to a file with utf-8 encoding
    #     with open("output.txt", "w", encoding="utf-8") as file:
    #         file.write(r.text)
    #     print("Content written to output.txt")
    # else:
    #     print(f"Failed to retrieve the page. Status code: {r.status_code}")


    # Check if the request was successful
    if r.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find the script tag with id __NEXT_DATA__
        next_data_script = soup.find('script', id='__NEXT_DATA__')
        
        if next_data_script:
            # Extract the content of the script tag
            next_data_content = next_data_script.string
            
            response_json = json.loads(next_data_content)
            
            data_str = str(response_json['props']['pageProps']['searchResults']['titleResults']['titleListItems'])
          
            # Convert the string to a list of dictionaries
            data_list = eval(data_str)

            # Remove unnecessary fields
            for item in data_list:
                keys_to_remove = ['canRate', 'titleId', 'titleType', 'primaryImage', 'hasWatchOption', 'ratingSummary', 'topCast', 'creators', 'directors', 'endYear']
                for key in keys_to_remove:
                    item.pop(key, None)

            # Convert the cleaned data back to JSON for better readability
            cleaned_data = json.dumps(data_list, indent=4, ensure_ascii=False)
            return str(cleaned_data)

        else:
            print("No script tag with id '__NEXT_DATA__' found.")
    else:
        print(f"Failed to retrieve the page. Status code: {r.status_code}")