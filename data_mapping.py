import datetime
import json

SCHEDULE = 'data_templates/schedule.json'
PROFILES = 'data_templates/profiles.json'
NEWS = 'data_templates/news.json'

def ScheduleMapping(group,faculty):
    current_day = datetime.date.today().weekday()
    with open(SCHEDULE, 'r', encoding='utf-8') as file:
        schedule_data = file.read()
        schedule_to_render = json.loads(schedule_data)
    return schedule_to_render[faculty][group][str(current_day)]

def ProfileMapping(name):
    with open(PROFILES, 'r', encoding='utf-8') as file:
        profile_data = file.read()
        profile_to_render = json.loads(profile_data)
    return profile_to_render['students'][name]

def NewsMapping(faculty):
    with open(NEWS, 'r', encoding='utf-8') as file:
        news_data = file.read()
        news_to_render = json.loads(news_data)
    return news_to_render[faculty]
