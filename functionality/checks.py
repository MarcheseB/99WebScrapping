
def skills_check(job_skills):
    if (job_skills != None):
        return job_skills.text.strip('\n').replace('\n', ', ')
    else:
        return 'Sem pré-requisitos'

def link_add(job):
    return 'https://www.99freelas.com.br/' + job.find('h1', class_='title').a['href']