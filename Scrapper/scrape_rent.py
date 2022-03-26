import requests

from requests_html import HTMLSession

import pandas as pd
import numpy as np
from time import sleep
from bs4 import BeautifulSoup


boros = ['staten-island', 'queens', 'bronx', 'brooklyn', 'manhattan']


def get_manhattan():
    b = boros[4]
    data = pd.DataFrame(columns=['Borough', 'Area', 'Address', 'Num_Beds', 'Num_Baths', 'Sq-Ft', 'Rent'])
    
    slot = 0
    
    page = 1

    url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', 'referer': 'https://streeteasy.com/'}

    res = requests.get(url, headers=head)   
    status = res.status_code

    if status != 200:
        print(res.status_code)
        print(res)
        return data


    html = res.text

    soup = BeautifulSoup(html, 'lxml')
    count = soup.find('h1', {'class': 'srp-result-count'}).text.split(" ")[0]
    if ',' in count:
        count = count.split(',')[0] + count.split(',')[1]

    count = int(count)
    print(count)

    i = 0
    while i < count:
        cards = soup.find_all('div', {'class': 'listingCardBottom listingCardBottom-rental'})
        for flat in cards:
            address = flat.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}).text.split('#')[0]
            address = str(address).strip()
            area = flat.find('p', {'class': 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'}).text.strip()
            if area == 'New Development':
                area = "New_Dev"
            else:
                area = area.split(' in ')
                area=str(area[1]).strip()

            price = flat.find('span', {'class': 'price listingCard-priceMargin'}).text.split('$')[1]
            price = str(price).strip()
            if ',' in price:
                rm_com_pr = price.split(',')
                price = rm_com_pr[0]+rm_com_pr[1:][0]
            price = float(price)
            spatial_info = flat.find_all('span', {'class': 'listingDetailDefinitionsText'})
            spatial_info = [x.text.strip() for x in spatial_info]
            if len(spatial_info) < 3:
                temp = ['0']*(3-len(spatial_info))
                spatial_info+=temp
            spatial_info[2] = spatial_info[2].split('\n')[0] + ' sq-ft'
            if ',' in spatial_info[2]:
                rm_com = spatial_info[2].split(',')
                spatial_info[2] = rm_com[0]+rm_com[1]
            if 'Studio' in spatial_info[0]:
                spatial_info[0] = '0.5 Bed'
            # spatial_info = [float(x.split(" ")[0]) for x in spatial_info]
            spatial_info = [x.split(" ")[0] for x in spatial_info]

            # slot = len(data.index)
            data.loc[slot] = [b, area, address, spatial_info[0], spatial_info[1], spatial_info[2], price]
            # print(data.loc[slot])
            slot+=1
            i+=1

        # if i < count:
        page+=1
        url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
        res = requests.get(url, headers=head) if i < count else res
        status = res.status_code

        if status != 200:
            return data

        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        


    data.to_csv(f'streey_easy_rent_{b}.csv', index=True)


def get_brooklyn():
    b = boros[3]
    data = pd.DataFrame(columns=['Borough', 'Area', 'Address', 'Num_Beds', 'Num_Baths', 'Sq-Ft', 'Rent'])
    
    slot = 0
    
    page = 1

    url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', 
        'referer': 'https://streeteasy.com/'
    }

    res = requests.get(url, headers=head)   
    status = res.status_code

    if status != 200 and len(res.text) == 0:
        print(res.status_code)
        print(res)

        data.to_csv(f'streey_easy_rent_{b}.csv', index=True)
        
        return data


    html = res.text

    soup = BeautifulSoup(html, 'lxml')
    count = soup.find('h1', {'class': 'srp-result-count'}).text.split(" ")[0]
    if ',' in count:
        count = count.split(',')[0] + count.split(',')[1]

    count = int(count)
    print(count)

    i = 0
    while i < count:
        cards = soup.find_all('div', {'class': 'listingCardBottom listingCardBottom-rental'})
        for flat in cards:
            address = flat.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}).text.split('#')[0]
            address = str(address).strip()
            area = flat.find('p', {'class': 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'}).text.strip()
            if area == 'New Development':
                area = "New_Dev"
            else:
                area = area.split(' in ')
                area=str(area[1]).strip()

            price = flat.find('span', {'class': 'price listingCard-priceMargin'}).text.split('$')[1]
            price = str(price).strip()
            if ',' in price:
                rm_com_pr = price.split(',')
                price = rm_com_pr[0]+rm_com_pr[1:][0]
            price = float(price)
            spatial_info = flat.find_all('span', {'class': 'listingDetailDefinitionsText'})
            spatial_info = [x.text.strip() for x in spatial_info]
            if len(spatial_info) < 3:
                temp = ['0']*(3-len(spatial_info))
                spatial_info+=temp
            spatial_info[2] = spatial_info[2].split('\n')[0] + ' sq-ft'
            if ',' in spatial_info[2]:
                rm_com = spatial_info[2].split(',')
                spatial_info[2] = rm_com[0]+rm_com[1]
            if 'Studio' in spatial_info[0]:
                spatial_info[0] = '0.5 Bed'
            # spatial_info = [float(x.split(" ")[0]) for x in spatial_info]
            spatial_info = [x.split(" ")[0] for x in spatial_info]

            # slot = len(data.index)
            data.loc[slot] = [b, area, address, spatial_info[0], spatial_info[1], spatial_info[2], price]
            # print(data.loc[slot])
            slot+=1
            i+=1

        # if i < count:
        page+=1
        url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
        res = requests.get(url, headers=head) if i < count else res
        status = res.status_code

        if status != 200 and len(res.text) == 0:
            print(res)

            data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

            return data

        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        


    data.to_csv(f'streey_easy_rent_{b}.csv', index=True)
    print(data.head())


def get_bronx():
    b = boros[2]
    data = pd.DataFrame(columns=['Borough', 'Area', 'Address', 'Num_Beds', 'Num_Baths', 'Sq-Ft', 'Rent'])
    
    slot = 0
    
    page = 1

    url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', 
        'referer': 'https://streeteasy.com/',
        'origin': 'https://streeteasy.com',
        'Cookie': "__Secure-3PSID=IQht6MfWCb0EMCYH-qKS8vWRuUtKjIge-DhusAL-Ix9Naubd4gbdKQe1bQ5dD3D1yP-N8A.; __Secure-3PAPISID=wZ_9txsKuoRnMf0l/A6RauA94D8k-JVX1C; NID=511=AJAsmWvaddfmYUNMrxXZiUi41L8Xhc0RwlAhdIJGTloHyD_wx8-72m38J9SaR8UPUDKls6MkEQzpLOpswmi7YlobhEKSqGdZ5MuWJ-kDCSeXZp1jTVo2JFz55gMg5HQ36Zep-4u9unvhOXjOsGMHw_Ihhix0daXIt5C4oHITa6RF1kI2pA; __Secure-3PSIDCC=AJi4QfGs_SkbDu70kT2UYlvGTh-G1qzfXbIovbCLPeudQGqNWvGHR54IsiCRBQV4BZxRGnjs5A"
    }

    res = requests.get(url, headers=head)   
    status = res.status_code

    if status != 200:
        print(res.status_code)
        print(res)

        data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

        return data


    html = res.text

    soup = BeautifulSoup(html, 'lxml')
    count = soup.find('h1', {'class': 'srp-result-count'}).text.split(" ")[0]
    if ',' in count:
        count = count.split(',')[0] + count.split(',')[1]

    count = int(count)
    print(count)

    i = 0
    while i < count:
        cards = soup.find_all('div', {'class': 'listingCardBottom listingCardBottom-rental'})
        for flat in cards:
            address = flat.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}).text.split('#')[0]
            address = str(address).strip()
            area = flat.find('p', {'class': 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'}).text.strip()
            if area == 'New Development':
                area = "New_Dev"
            else:
                area = area.split(' in ')
                area=str(area[1]).strip()

            price = flat.find('span', {'class': 'price listingCard-priceMargin'}).text.split('$')[1]
            price = str(price).strip()
            if ',' in price:
                rm_com_pr = price.split(',')
                price = rm_com_pr[0]+rm_com_pr[1:][0]
            price = float(price)
            spatial_info = flat.find_all('span', {'class': 'listingDetailDefinitionsText'})
            spatial_info = [x.text.strip() for x in spatial_info]
            if len(spatial_info) < 3:
                temp = ['0']*(3-len(spatial_info))
                spatial_info+=temp
            spatial_info[2] = spatial_info[2].split('\n')[0] + ' sq-ft'
            if ',' in spatial_info[2]:
                rm_com = spatial_info[2].split(',')
                spatial_info[2] = rm_com[0]+rm_com[1]
            if 'Studio' in spatial_info[0]:
                spatial_info[0] = '0.5 Bed'
            # spatial_info = [float(x.split(" ")[0]) for x in spatial_info]
            spatial_info = [x.split(" ")[0] for x in spatial_info]

            # slot = len(data.index)
            data.loc[slot] = [b, area, address, spatial_info[0], spatial_info[1], spatial_info[2], price]
            # print(data.loc[slot])
            slot+=1
            i+=1

        # if i < count:
        page+=1
        url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
        res = requests.get(url, headers=head) if i < count else res
        status = res.status_code

        if status != 200:
            print(res)

            data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

            return data

        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        


    data.to_csv(f'streey_easy_rent_{b}.csv', index=True)
    print(data.head())


def get_queens():
    b = boros[1]
    data = pd.DataFrame(columns=['Borough', 'Area', 'Address', 'Num_Beds', 'Num_Baths', 'Sq-Ft', 'Rent'])
    
    slot = 0
    
    page = 1

    url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', 
        'referer': 'https://streeteasy.com/'
    }

    res = requests.get(url, headers=head)   
    status = res.status_code

    if status != 200:
        print(res.status_code)
        print(res)

        data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

        return data


    html = res.text

    soup = BeautifulSoup(html, 'lxml')
    count = soup.find('h1', {'class': 'srp-result-count'}).text.split(" ")[0]
    if ',' in count:
        count = count.split(',')[0] + count.split(',')[1]

    count = int(count)
    print(count)

    i = 0
    while i < count:
        cards = soup.find_all('div', {'class': 'listingCardBottom listingCardBottom-rental'})
        for flat in cards:
            address = flat.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}).text.split('#')[0]
            address = str(address).strip()
            area = flat.find('p', {'class': 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'}).text.strip()
            if area == 'New Development':
                area = "New_Dev"
            else:
                area = area.split(' in ')
                area=str(area[1]).strip()

            price = flat.find('span', {'class': 'price listingCard-priceMargin'}).text.split('$')[1]
            price = str(price).strip()
            if ',' in price:
                rm_com_pr = price.split(',')
                price = rm_com_pr[0]+rm_com_pr[1:][0]
            price = float(price)
            spatial_info = flat.find_all('span', {'class': 'listingDetailDefinitionsText'})
            spatial_info = [x.text.strip() for x in spatial_info]
            if len(spatial_info) < 3:
                temp = ['0']*(3-len(spatial_info))
                spatial_info+=temp
            spatial_info[2] = spatial_info[2].split('\n')[0] + ' sq-ft'
            if ',' in spatial_info[2]:
                rm_com = spatial_info[2].split(',')
                spatial_info[2] = rm_com[0]+rm_com[1]
            if 'Studio' in spatial_info[0]:
                spatial_info[0] = '0.5 Bed'
            # spatial_info = [float(x.split(" ")[0]) for x in spatial_info]
            spatial_info = [x.split(" ")[0] for x in spatial_info]

            # slot = len(data.index)
            data.loc[slot] = [b, area, address, spatial_info[0], spatial_info[1], spatial_info[2], price]
            # print(data.loc[slot])
            slot+=1
            i+=1

        # if i < count:
        page+=1
        url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
        res = requests.get(url, headers=head) if i < count else res
        status = res.status_code

        if status != 200:
            print(res)

            data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

            return data

        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        


    data.to_csv(f'streey_easy_rent_{b}.csv', index=True)
    print(data.head())


def get_staten():
    b = boros[0]
    data = pd.DataFrame(columns=['Borough', 'Area', 'Address', 'Num_Beds', 'Num_Baths', 'Sq-Ft', 'Rent'])
    
    slot = 0
    
    page = 1

    url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36', 
        'referer': 'https://streeteasy.com/'
    }

    res = requests.get(url, headers=head)   
    status = res.status_code

    if status != 200:
        print(res.status_code)
        print(res)

        data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

        return data


    html = res.text

    soup = BeautifulSoup(html, 'lxml')
    count = soup.find('h1', {'class': 'srp-result-count'}).text.split(" ")[0]
    if ',' in count:
        count = count.split(',')[0] + count.split(',')[1]

    count = int(count)
    print(count)

    i = 0
    while i < count:
        cards = soup.find_all('div', {'class': 'listingCardBottom listingCardBottom-rental'})
        for flat in cards:
            address = flat.find('address', {'class': 'listingCard-addressLabel listingCard-upperShortLabel'}).text.split('#')[0]
            address = str(address).strip()
            area = flat.find('p', {'class': 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'}).text.strip()
            if area == 'New Development':
                area = "New_Dev"
            else:
                area = area.split(' in ')
                area=str(area[1]).strip()

            price = flat.find('span', {'class': 'price listingCard-priceMargin'}).text.split('$')[1]
            price = str(price).strip()
            if ',' in price:
                rm_com_pr = price.split(',')
                price = rm_com_pr[0]+rm_com_pr[1:][0]
            price = float(price)
            spatial_info = flat.find_all('span', {'class': 'listingDetailDefinitionsText'})
            spatial_info = [x.text.strip() for x in spatial_info]
            if len(spatial_info) < 3:
                temp = ['0']*(3-len(spatial_info))
                spatial_info+=temp
            spatial_info[2] = spatial_info[2].split('\n')[0] + ' sq-ft'
            if ',' in spatial_info[2]:
                rm_com = spatial_info[2].split(',')
                spatial_info[2] = rm_com[0]+rm_com[1]
            if 'Studio' in spatial_info[0]:
                spatial_info[0] = '0.5 Bed'
            # spatial_info = [float(x.split(" ")[0]) for x in spatial_info]
            spatial_info = [x.split(" ")[0] for x in spatial_info]

            # slot = len(data.index)
            data.loc[slot] = [b, area, address, spatial_info[0], spatial_info[1], spatial_info[2], price]
            # print(data.loc[slot])
            slot+=1
            i+=1

        # if i < count:
        page+=1
        url = f'https://streeteasy.com/for-rent/{b}/status:open?page={page}'
        res = requests.get(url, headers=head) if i < count else res
        status = res.status_code

        if status != 200:
            print(res)

            data.to_csv(f'streey_easy_rent_{b}.csv', index=True)

            return data

        html = res.text
        soup = BeautifulSoup(html, 'lxml')
        


    data.to_csv(f'streey_easy_rent_{b}.csv', index=True)
    print(data.head())




def main():
    # get_manhattan()

    # get_brooklyn()

    get_bronx()

    # get_queens()

    # get_staten()
    return



if __name__ == "__main__":
    main()


