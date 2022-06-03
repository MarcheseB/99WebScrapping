from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def find_jobs():
    html_text = requests.get('https://www.99freelas.com.br/projects?q=acessor%20de%20investimentos').text
    soup = BeautifulSoup(html_text, 'lxml')
    if soup.find('ul') == None:
        print("Parece que não há ofertas nessa área no momento.")
    else:
        number_item = len(soup.find('div', class_='pagination-component').find_all('span'))
        if (number_item > 3):
            page_number = int(soup.find('div', class_='projects-result-header').find('span', class_='page-item go-to-last-page')['data-page'])
        else: page_number = number_item

        # INITIALIZING VECTORS TO STORE JOBS NAME, SKILLS AND LINK

        names = []
        skills = []
        links = []

        # GETTING THE FIRST JOB, IF THERE'S 'WITH-FLAG' ITEMS
        flag = soup.find('li', class_='with-flag result-item first-with-flag')
        if flag != None:
            first_job = soup.find('li', class_='with-flag result-item first-with-flag')
            first_job_name = first_job.find('h1').text.replace('\n', '')
            first_job_skills = first_job.find('p', class_='item-text habilidades')
            if (first_job_skills != None):
                first_job_skills = first_job_skills.text.strip('\n').replace('\n', ', ')
            else:
                first_job_skills = 'Sem pré-requisitos'
            link = 'https://www.99freelas.com.br/' + first_job.find('h1', class_='title').a['href']
            names.append(first_job_name)
            skills.append(first_job_skills)
            links.append(link)
        else: pass

        # GETTING THE 'WITH-FLAG' JOBS: (wfj)

        with_flag_jobs = soup.find_all('li', class_='with-flag result-item')
        if with_flag_jobs != None:
            for index, wfj in enumerate(with_flag_jobs):
                wfj_name = wfj.find('h1', class_='title').text.replace('\n', '')
                wfj_skills = wfj.find('p', class_="item-text habilidades").text.strip('\n').replace('\n', ', ')
                link = 'https://www.99freelas.com.br/' + wfj.find('h1', class_='title').a['href']
                if wfj_name not in names:
                    names.append(wfj_name)
                    skills.append(wfj_skills)
                    links.append(link)
        else: pass


        # GETTING THE REGULAR JOBS

        for i in range(1,page_number+1):
            print(f'Pagina {i}\n')
            if (i > 1):
                new_url = 'https://www.99freelas.com.br/projects?q=python' + '&page=' + str(i)
                html_text = requests.get(new_url).text
                soup = BeautifulSoup(html_text, 'lxml')
            jobs = soup.find_all('li', class_='result-item')

            # GETTING THE JOBS NAMES AND INFORMATIONS
            if jobs != None:
                for index, job in enumerate(jobs):
                    job_name = job.find('h1', class_='title').text.replace('\n', '')
                    job_skills = job.find('p', class_="item-text habilidades")
                    link = 'https://www.99freelas.com.br/' + job.find('h1', class_='title').a['href']
                    if (job_skills != None):
                        job_skills = job_skills.text.strip('\n').replace('\n', ', ')
                    else: job_skills = 'Sem pré-requisitos'

                    if job_name not in names:
                        names.append(job_name)
                        skills.append(job_skills)
                        links.append(link)
            else:
                pass
        df = pd.DataFrame({'Skills': skills, 'Link': links}, index=names)
        df.to_csv('jobs.csv', header=['Skills', 'Link'])


if __name__ == '__main__':
    while True:
        find_jobs()
        waiting_time = 24*60
        print("Programa executado com sucesso. Próxima execução em 24 horas.")
        time.sleep(60*waiting_time)
