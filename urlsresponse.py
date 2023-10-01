from seleniumwire import webdriver
from seleniumwire.utils import decode as decodesw
import json

def request_urls(driver, target_url):
    driver.get(target_url)
    urls = []
    for request in driver.requests:
        urls.append({"url": request.url})
    return urls

def response_json(driver, target_url):
    driver.get(target_url)
    responses = []
    for request in driver.requests:
        try:
            data = decodesw(
                request.response.body,
                request.response.header.get("Content-Encoding", "identity")
            )
            response = json.loads(data.decode("utf-8"))
            responses.append(response)
        except Exception as e:
            print(f"Error processing response: {e}")
    return responses

def main():
    #define the keywords that you want to be searching within the response
    keywords = ["api"]
    #make sure you have one of the browsers installed
    driver = webdriver.Firefox(seleniumwire_options={"disable_encoding": True})
    target_url = "https://www.adidas.co.uk/terrex/"
    urls = request_urls(driver, target_url)
    responses = response_json(driver, target_url)

    for url in urls:
        for keyword in keywords:
            if keyword in url["url"]:
                print(url)
    
    with open('data.json', 'w') as f:
        json.dump(responses, f)

    driver.close()


if __name__ == '__main__':
    main()