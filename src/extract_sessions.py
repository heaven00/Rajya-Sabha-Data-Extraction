import requests
import re
import logging
import sys
import pandas as pd
import bs4 as bs
from typing import Generator


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_soup(url):
    get_resp = requests.get(url)
    soup = bs.BeautifulSoup(get_resp.text)
    return soup


def extract_aspx_variables_from_soup(soup, var):
    return soup.find('input', {'id':var}).attrs['value']


def get_sessions(url):
    get_resp_soup = get_soup(url)
    session_options = get_resp_soup.find(
        'select',
        {'id': 'ctl00_ContentPlaceHolder1_DropDownList1'}
    ).findAll('option')
    return (opt.text for opt in session_options if 'Select' not in opt.text)


def get_session_id_resp(session_id:int) -> requests.models.Response:
    url = 'http://164.100.47.5/newsite/floor_official_debate/floor_official_debate.aspx'
    get_resp_soup = get_soup(url)
    data = {'ctl00$ContentPlaceHolder1$DropDownList1': session_id,
           '__VIEWSTATE': extract_aspx_variables_from_soup(get_resp_soup, '__VIEWSTATE'),
           '__VIEWSTATEGENERATOR': extract_aspx_variables_from_soup(get_resp_soup, '__VIEWSTATEGENERATOR'),
           '__EVENTVALIDATION': extract_aspx_variables_from_soup(get_resp_soup, '__EVENTVALIDATION'),
           '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$DropDownList1'}
    resp = requests.post(url, data=data)
    return resp


def extract_debate_pdf_links(resp: requests.models.Response) -> Generator[bs.element.Tag, None, None]:
    soup = bs.BeautifulSoup(resp.text)
    pdf_anchor_tags = soup.findAll('a', attrs={'href': re.compile("^http://.*pdf")})
    return ({'url': link.get('href'), 'size': link.text} 
            for link in pdf_anchor_tags 
            if 'Debate' in link.get('href'))


def get_session_date_from_debate_url(url:str) -> str:
    return url.split('/')[-1].strip('.pdf')


def write_session_pdf_link(session_id: str, pdf_links: Generator) -> None:
    with open(f'sessions/session_{session_id}.csv', 'w') as datafile:
        datafile.write('session_id,date,url,size')
        datafile.write('\n')
        for link in pdf_links:
            debate_pdf_url = link['url']
            session_date = get_session_date_from_debate_url(debate_pdf_url)
            size = link['size']
            datafile.write(f'{session_id},{session_date},{debate_pdf_url},{size}')
            datafile.write('\n')
    return None
            

if __name__ == '__main__':
    url = 'http://164.100.47.5/newsite/floor_official_debate/floor_official_debate.aspx'
    sessions = get_sessions(url)
    for session in sessions:
        resp = get_session_id_resp(session)
        pdf_links = extract_debate_pdf_links(resp)
        write_session_pdf_link(session, pdf_links)
        logging.info(f'Completed Writing for Session: {session}')

