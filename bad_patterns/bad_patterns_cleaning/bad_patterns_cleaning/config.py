reports_directory = "reports"
articles_directory = "articles"
solutions_directory = "solutions"

# For local
# base_url = "http://localhost:33336"

# For deployed full_parser_api
base_url = 'https://article-extraction.newscatcherapi.xyz'

headers_v3_api = {
    'x-api-token': 'YMqKFMxckBbWoZxb7aAdRPmqjSqpy6Fj'
}

headers_full_parser_api = {
    'x-api-token': 'nSnF5bTbD0QDI1GpM347JfXCCYs6fofkUrbRnkk6kN7xEaMXCl'
}

bad_patterns = {
    # 'copyShortcut': 'https://v3-api.newscatcherapi.com/api/search?q="copyShortcut"&from_=2023/10/26 hours ago&page_size=1000&by_parse_date=true',
    # 'SKIP ADVERTISEMENT': 'https://v3-api.newscatcherapi.com/api/search?q="SKIP ADVERTISEMENT"&from_=2023/10/26 hours ago&page_size=1000&by_parse_date=true',
    #'Terms and Conditions and Privacy Policy': 'https://v3-api.newscatcherapi.com/api/search?q="terms and conditions and privacy policy"&from_=2023/10/31&page_size=1000&by_parse_date=true',
    #'Click here for updates': 'https://v3-api.newscatcherapi.com/api/search?q="Click here for updates"&from_=2023/10/31&page_size=1000&by_parse_date=true',
    # 'Alabama Alaska': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&page=1&from_=2023/10/31&q="Alabama Alaska"&by_parse_date=true',
     'Your cookie preferences': 'https://v3-api.newscatcherapi.com/api/search?from_=2023/10/26 hours ago&page_size=1000&page=1&q="your cookie preferences"&by_parse_date=true'
    # 'youtube.com': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=7 days ago&q="youtube.com"',
    # 'docs.google.com': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=7 days ago&q="docs.google.com"',
    # 'Please enable JS and disable any ad blocker': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=3 days ago&q="Please enable JS and disable any ad blocker"'
    # 'enter your email address': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=7 days ago&q="enter your email address"'
    # 'insertPoint': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=7 days ago&q="insertPoint"'
    #'Please upgrade your browser to view': 'https://v3-api.newscatcherapi.com/api/search?page_size=1000&by_parse_date=true&from_=7 days ago&q="Please upgrade your browser to view"'
}
