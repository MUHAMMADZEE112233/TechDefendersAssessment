import scrapy
from scrapy import Request

class CarsSpider(scrapy.Spider):
    name = "cars" # Name of the spider
    allowed_domains = ["cars.com"] # Domains this spider is allowed to scrape
    start_url = ["https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=kia&models%5B%5D=kia-cadenza&maximum_distance=all&zip=60606"] # Starting URL for the spider

    custom_settings = {
        'CONCURRENT_REQUESTS': 8, # Limit the number of concurrent requests
        'DOWNLOAD_DELAY': 2, # Delay between requests to avoid overloading the server
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter' # Filter for duplicate requests

    }

    def start_requests(self):
        # Define headers to mimic a browser request
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Cookie': 'CARS_has_visited=; CARS_logged_in=false; CARS_trip_id=de28577b-8629-4b9b-93ef-fb8d48ab02ce; ...',  # Include your full cookie here
            'Priority': 'u=0, i',
            'Sec-CH-UA': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        # Send a request to the starting URL with the defined headers
        yield scrapy.Request(url=self.start_url[0], headers=headers, callback=self.parse)

    def parse(self, response):
        # Extract the list of car elements from the page
        cars = response.xpath('//div[@class="vehicle-card"]')
        for car in cars:
            # Extract the URL of the individual car's detail page
            car_url = response.urljoin(car.css('a::attr(href)').get())
            # Send a request to the car detail page
            yield Request(url=car_url, callback=self.parse_details, dont_filter=True)

        next_page = response.css('[aria-label="Next page"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)

    def parse_details(self, response):
        # Extract car details from the individual car's detail page
        details = response.css('.listing-title::text').get().split() # Extract title and split into components
        price = response.css('[class="price-section "] span::text').get()
        phone_number = response.css('[class="dealer-phone"]::text').get()
        # Assign year, make, and model from the details
        year = details[0]
        make = details[1]
        model = details[2]
        # Yield the extracted data as a dictionary
        yield {
            "Car's make": make,
            "Model": model,
            "Year": year,
            "Price": price,
            "Seller's Contact": phone_number
        }
