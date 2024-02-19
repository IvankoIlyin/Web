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
    'Skip to content':'http://v3-api.newscatcherapi.com/api/search?q="Skip to content"&from_=30 days ago&page_size=1000&by_parse_date=true'
    # 'BackGround Color':'https://v3-api.newscatcherapi.com/api/search?q="BackGround Color"&from_=120 days ago&page_size=1000&by_parse_date=true',
    # 'console.log':'https://v3-api.newscatcherapi.com/api/search?q="console.log"&from_=120 days ago&page_size=1000&by_parse_date=true',
    # 'background-color':'https://v3-api.newscatcherapi.com/api/search?q="background-color"&from_=120 days ago&page_size=1000&by_parse_date=true',
    # 'Media Only Screen':'https://v3-api.newscatcherapi.com/api/search?q="Media Only Screen"&from_=360 days ago&page_size=1000&by_parse_date=true',
    # 'Console Log':'https://v3-api.newscatcherapi.com/api/search?q="Console Log"&from_=360 days ago&page_size=1000&by_parse_date=true',
    # 'Please Wait':'https://v3-api.newscatcherapi.com/api/search?q="Please Wait"&from_=360 days ago&page_size=1000&by_parse_date=true'
}
