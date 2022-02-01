# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.pi
import json

import requests
from bs4 import BeautifulSoup
import re
import voice_info as vo
import os
import roles

root_path = '/Users/zhangmeng/genshin/语音'
lan_dict = {1: 'zh', 2: 'jp', 3: 'en', 4: 'kr'}


def role_main():
    json_list = []
    for role in roles.roles:
        html_text = download_htmls(role.zh_name)
        voice_json = html_parse(html_text, role.zh_name, role.en_name)
        json_list.append(voice_json)
    with open("/Users/zhangmeng/genshin/voice.json", "w") as fd:
        json.dump(json_list, fd, ensure_ascii=False)
        print("json文件输出完成")


def download_htmls(name):
    url = f"https://wiki.biligame.com/ys/{name}语音"
    print(url)
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception("error")
    return res.text


def html_parse(html, zh_name, en_name):
    voice_json = vo.VoiceInfo()
    voice_json.name = zh_name
    voice_json.en_name = en_name
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all(name='table', attrs='wikitable')
    links = re.findall(r'data-src="(.*?)"', html)
    count = 0
    links_dic = lan_dict.fromkeys(links)
    links = list(links_dic.keys())
    for num in range(2, len(tables)):
        table = tables[num]
        list_str = parse_str(table.text.__str__().replace('\n', 't'))
        title = vo.Title()
        title.text = list_str[0]
        title.content = list_str[5]
        for index in range(1, 5):
            file_name = f'{en_name}_{count}.mp3'
            print(links[count])
            file_path = save_mp3(links[count], file_name, f'{root_path}/{zh_name}/{lan_dict[index]}')
            title.voices.append(file_path)
            count += 1

        voice_json.titles.append(json.dumps(title.to_dic(), ensure_ascii=False))
    return json.dumps(
        voice_json.to_dic(), ensure_ascii=False)


def parse_str(string):
    contents = string.split('tt')
    title = contents[1]
    zh = remove_tag(contents[2])
    jp = remove_tag(contents[3])
    en = remove_tag(contents[4])
    kr = remove_tag(contents[5])
    sub_title = remove_tag(contents[11])
    return [title, zh, jp, en, kr, sub_title]


def remove_tag(origin):
    return str(origin).replace('t', '')


def save_mp3(url, file_name, path):
    url = str(url).replace('&#58;', ':')
    if url == '':
        return ''
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    res = requests.get(url, stream=True)
    file_path = os.path.join(path, file_name)
    print('开始写入文件', file_path)
    with open(file_path, 'wb') as fd:
        for chunk in res.iter_content():
            fd.write(chunk)
    print('下载完成')
    return file_path


if __name__ == '__main__':
    role_main()
