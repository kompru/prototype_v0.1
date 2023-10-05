from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import tracemalloc
import asyncio

class BearerToken:

# async def scrape_network_requests():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         context = await browser.new_context()
#         page = await context.new_page()

#         await page.route('**', lambda route, request: route.continue_() if not (
#             request.method == 'POST' and request.url == 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-recent-top-searches'
#         ) else (
#             print(request.headers['authorization']),
            
#         ))

#         try:
#             await page.goto('https://www.rappi.com.br/')
#             await page.wait_for_selector('body') 
         
#         except Exception as error:
#             print('An error occurred:', error)
#         finally:
#             await browser.close()
    
    # async def scrape_network_requests():
    #     authorization_header = None  # Initialize the variable to store the header value
    #     async with async_playwright() as p:
    #         browser = await p.chromium.launch()
    #         context = await browser.new_context()
    #         page = await context.new_page()

    #         async def route_handler(route, request):
    #             nonlocal authorization_header  # Use 'nonlocal' to modify the outer variable
    #             if request.method == 'POST' and request.url == 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-recent-top-searches':
    #                 authorization_header = request.headers.get('authorization', None)  # Capture the header value
    #             await route.continue_()
    #             return authorization_header

    #         await page.route('**', route_handler)

    #         try:
    #             await page.goto('https://www.rappi.com.br/')
    #             await page.wait_for_selector('body') 
    #         except Exception as error:
    #             print('An error occurred:', error)
    #         finally:
    #             await browser.close()  
    
    #     return authorization_header  

    # async def main():
    #     authorization_value = await BearerToken.scrape_network_requests()
    #     if authorization_value:
    #         return authorization_value
    #     else:
    #         print('ERROR')
    #         exit()


    
    def scrape_network_requests():
        authorization_header = None 

        with sync_playwright() as p:
            chromium = p.chromium
            browser = chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            def route_handler(route, request):
                nonlocal authorization_header  # Use 'nonlocal' to modify the outer variable
                if request.method == 'POST' and request.url == 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-recent-top-searches':
                    authorization_header = request.headers.get('authorization', None)  
                route.continue_()

            page.route('**', route_handler)
            page.goto('https://www.rappi.com.br/search?query=')
            page.wait_for_selector('body')
            browser.close()

        return authorization_header


# bearer_token = asyncio.run(BearerToken.main())

bearer_token = BearerToken.scrape_network_requests()
if bearer_token:
    print(bearer_token)
else:
    print('ERROR')
    exit()



