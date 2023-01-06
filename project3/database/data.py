import re
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
import time


HOST = 'cluster1.leos9pf.mongodb.net'
USER = 'soyheo'
PASSWORD = 'soyheo1234'
DATABASE_NAME = 'Project'
COLLECTION_NAME = 'realtor_api'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"


for page_num in range(501):

    cookies = {
        'visid_incap_2269415': 'iZ2YhhyRS52H8Svt3ySvwp/grmMAAAAAQUIPAAAAAAByhLjWD610OE7KvYiLFwk9',
        'nlbi_2269415': '78EKcH6o5W6tEXLUzBLR3QAAAAC5sMDRLpUP//enIQp1YhEf',
        '_gcl_au': '1.1.1813376162.1672405158',
        '_fbp': 'fb.1.1672405160194.2105768788',
        'gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko': 'gigya-pr_ver4',
        'ASP.NET_SessionId': '55bxbpf3fmsiy2mwlwhnkbjy',
        'visid_incap_2271082': '84Y/WoCfTVi2f1bfR7bYtLDgrmMAAAAAQUIPAAAAAABQt/q3U1fnt9sCuKOrniYI',
        'nlbi_2271082': 'CKoDRbVdmDKNy6k0VPrQ3QAAAADjJ8jno85f+9h4usy2X1UQ',
        'incap_ses_950_2269415': 'B66jE5pQrVCdR5Y/tBQvDTjCr2MAAAAA0ibIVG7/6E7Jkv87b+/L9g==',
        '_gid': 'GA1.2.1433890796.1672493666',
        'incap_ses_950_2271082': 'EvTjObIugRajmFdAtBQvDWM6sGMAAAAAuACZf6ED++cYMBSw0eHljg==',
        '_dc_gtm_UA-12908513-11': '1',
        'reese84': '3:OGkRZnz1vZ47tau/SIcEmA==:Trrh4GPAhYwUqgVDz8VPn+o7bEGoJEWMVjQt9mXQZPLGC9X3dWeGu+p2FNb40R/aEmsv7k+i6OMVr8P6OC3JR7Ol6wTuZI3+cInauaWekQlgSV0/D2ZZeWv9xIRtJnewCSckZFVJwcn+G1zxzcQYPh4s1PkFClL7FOtU8U582AV28kDlrSd0IY6zFSbSsWASh3tcEMeUDU512IeD8PmmOC/21ttwj1/v/JrhFQAfRxmiYtP05yL61P+bi9hrAQgwk2BGdiDCSSxZm2V7jE2K41FWZubnlL7+fejt2Tktbhfez30+U/fUYOWV9mBUbzL8ogkxFPaFxj3xU518LFnG3RDdokoT4txq7quoDxeYqXV4d+l8qUOTDSr2tjwgLTfXG90BFNGcTBNudnN1Oagm9NSTBUwU0yTICZD3csgIj/BZCLX1+pcqANWMgZDjEYrha652LkQQ9F+qDwZAdfn3dIIZuU6ZxQPdRMN+QZA7514=:Gjgi9SRvX5/YEXcjhUNyNAg8+BPEOPYc4R1cFYLdPUI=',
        '_gali': 'homeSearchBtn',
        'nlbi_2269415_2147483392': 'al00WM5CiW1ZdMnUzBLR3QAAAAAqJqmPO0kB5wo5c5Hua3V7',
        '_ga_Y07J3B53QP': 'GS1.1.1672493666.2.1.1672494907.37.0.0',
        '_ga': 'GA1.1.120694163.1672405158',
        '_4c_': '%7B%22_4c_s_%22%3A%22fVTbjtsgEP2ViOeQBYJtyFu1lapVt1LVi%2Fq4IjCO0XqNhUnc7Sr%2F3sF1ku6lzUvgzJmTMxfyRMYGOrLhZSWklpozqcsluYfHgWyeSPQufx3IhnC7ZVCLipamsFQyo6kGVVBea1eXwhpwhizJz6ylGFecF7qoyuOS2H7WeCI2OMhaesXlijNaD5iSfiFUSIbHPga3t%2BkuPfaZN8J2Mbh7DDg4eAt3o3epmQQEu6AN%2BF2TMszUBPcxX%2FA0%2Bs6F8WXajJ7TtNCIbmMYB8iZ100MD7BANYQDNoL8mDKy2Qg1xDjRmpT6YXN1NY7jKoJpU4gra66wnUsy%2BJQLuMAzho29wHSCb02325sdzJZvw24HbnGDQyG1aQdA7HMMB9%2FZTMHbddh3KWadr2GfmsXHgHqIf4HBO%2BiSN22I1%2BHhAaK3pp1%2B7xzJTc7jlHhoA4az6GQZuoz30eH5w7u77zfvsyPBSi15uV5NG8IKXuSm7GP77wbkUsEmH7pLqYh9ix4ri58gNQG3Cu%2FG%2BcyaTLlMdlCbfZvyNc%2FFtmYYvHUw3KfQk%2BO8XZUoFF8zXawFLk9CJ6qULH%2BOf4qblk3%2BzRZKVrx6zZ6l6Wkg0P0nX73OP%2FjT81AVVMJWWyqYqqnkwKjeWkmLstpWTGlb2JKcJfGRIVicLXF1cVSfJKXQxlpd0srUgnIOlmrmSsqEFMbiZBhbkxcuFSveqLI7SV4aPL9TgTYwi3Ok%2BT7NvPnfQKlKr%2FlzbkYy96RoyJvxOJ6l%2FgQ0L8viGXVCjsfjbw%3D%3D%22%7D',
    }

    headers = {
        'authority': 'api2.realtor.ca',
        'accept': '*/*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'visid_incap_2269415=iZ2YhhyRS52H8Svt3ySvwp/grmMAAAAAQUIPAAAAAAByhLjWD610OE7KvYiLFwk9; nlbi_2269415=78EKcH6o5W6tEXLUzBLR3QAAAAC5sMDRLpUP//enIQp1YhEf; _gcl_au=1.1.1813376162.1672405158; _fbp=fb.1.1672405160194.2105768788; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; ASP.NET_SessionId=55bxbpf3fmsiy2mwlwhnkbjy; visid_incap_2271082=84Y/WoCfTVi2f1bfR7bYtLDgrmMAAAAAQUIPAAAAAABQt/q3U1fnt9sCuKOrniYI; nlbi_2271082=CKoDRbVdmDKNy6k0VPrQ3QAAAADjJ8jno85f+9h4usy2X1UQ; incap_ses_950_2269415=B66jE5pQrVCdR5Y/tBQvDTjCr2MAAAAA0ibIVG7/6E7Jkv87b+/L9g==; _gid=GA1.2.1433890796.1672493666; incap_ses_950_2271082=EvTjObIugRajmFdAtBQvDWM6sGMAAAAAuACZf6ED++cYMBSw0eHljg==; _dc_gtm_UA-12908513-11=1; reese84=3:OGkRZnz1vZ47tau/SIcEmA==:Trrh4GPAhYwUqgVDz8VPn+o7bEGoJEWMVjQt9mXQZPLGC9X3dWeGu+p2FNb40R/aEmsv7k+i6OMVr8P6OC3JR7Ol6wTuZI3+cInauaWekQlgSV0/D2ZZeWv9xIRtJnewCSckZFVJwcn+G1zxzcQYPh4s1PkFClL7FOtU8U582AV28kDlrSd0IY6zFSbSsWASh3tcEMeUDU512IeD8PmmOC/21ttwj1/v/JrhFQAfRxmiYtP05yL61P+bi9hrAQgwk2BGdiDCSSxZm2V7jE2K41FWZubnlL7+fejt2Tktbhfez30+U/fUYOWV9mBUbzL8ogkxFPaFxj3xU518LFnG3RDdokoT4txq7quoDxeYqXV4d+l8qUOTDSr2tjwgLTfXG90BFNGcTBNudnN1Oagm9NSTBUwU0yTICZD3csgIj/BZCLX1+pcqANWMgZDjEYrha652LkQQ9F+qDwZAdfn3dIIZuU6ZxQPdRMN+QZA7514=:Gjgi9SRvX5/YEXcjhUNyNAg8+BPEOPYc4R1cFYLdPUI=; _gali=homeSearchBtn; nlbi_2269415_2147483392=al00WM5CiW1ZdMnUzBLR3QAAAAAqJqmPO0kB5wo5c5Hua3V7; _ga_Y07J3B53QP=GS1.1.1672493666.2.1.1672494907.37.0.0; _ga=GA1.1.120694163.1672405158; _4c_=%7B%22_4c_s_%22%3A%22fVTbjtsgEP2ViOeQBYJtyFu1lapVt1LVi%2Fq4IjCO0XqNhUnc7Sr%2F3sF1ku6lzUvgzJmTMxfyRMYGOrLhZSWklpozqcsluYfHgWyeSPQufx3IhnC7ZVCLipamsFQyo6kGVVBea1eXwhpwhizJz6ylGFecF7qoyuOS2H7WeCI2OMhaesXlijNaD5iSfiFUSIbHPga3t%2BkuPfaZN8J2Mbh7DDg4eAt3o3epmQQEu6AN%2BF2TMszUBPcxX%2FA0%2Bs6F8WXajJ7TtNCIbmMYB8iZ100MD7BANYQDNoL8mDKy2Qg1xDjRmpT6YXN1NY7jKoJpU4gra66wnUsy%2BJQLuMAzho29wHSCb02325sdzJZvw24HbnGDQyG1aQdA7HMMB9%2FZTMHbddh3KWadr2GfmsXHgHqIf4HBO%2BiSN22I1%2BHhAaK3pp1%2B7xzJTc7jlHhoA4az6GQZuoz30eH5w7u77zfvsyPBSi15uV5NG8IKXuSm7GP77wbkUsEmH7pLqYh9ix4ri58gNQG3Cu%2FG%2BcyaTLlMdlCbfZvyNc%2FFtmYYvHUw3KfQk%2BO8XZUoFF8zXawFLk9CJ6qULH%2BOf4qblk3%2BzRZKVrx6zZ6l6Wkg0P0nX73OP%2FjT81AVVMJWWyqYqqnkwKjeWkmLstpWTGlb2JKcJfGRIVicLXF1cVSfJKXQxlpd0srUgnIOlmrmSsqEFMbiZBhbkxcuFSveqLI7SV4aPL9TgTYwi3Ok%2BT7NvPnfQKlKr%2FlzbkYy96RoyJvxOJ6l%2FgQ0L8viGXVCjsfjbw%3D%3D%22%7D',
        'origin': 'https://www.realtor.ca',
        'referer': 'https://www.realtor.ca/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }


    data = {
        'ZoomLevel': '11',
        'LatitudeMax': '43.89146',
        'LongitudeMax': '-79.05332',
        'LatitudeMin': '43.52415',
        'LongitudeMin': '-79.69945',
        'Sort': '6-D',
        'PropertyTypeGroupID': '1',
        'PropertySearchTypeId': '0',
        'TransactionTypeId': '2',
        'Currency': 'CAD',
        'RecordsPerPage': '12',
        'ApplicationId': '1',
        'CultureId': '1',
        'Version': '7.0',
        'CurrentPage': str(page_num),
    }


    response = requests.post('https://api2.realtor.ca/Listing.svc/PropertySearch_Post', cookies=cookies, headers=headers, data=data)
    # result_dict = json.loads(response.text)
    # print(result_dict['Results'])

    if response.status_code == 200:
        result = response.json()

    time.sleep(2)

        

        
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    coll = db[COLLECTION_NAME]

    coll.insert_many(result)
    



    