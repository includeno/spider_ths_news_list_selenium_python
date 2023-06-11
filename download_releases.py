import os
import requests
import shutil
import zipfile

def download_and_extract(download_url, filename, extract_dir):
    print("download_url", download_url)
    print("filename", filename)
    print("extract_dir", extract_dir)
    # 下载zip文件
    r = requests.get(download_url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    # 解压zip文件
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # 删除zip文件
    os.remove(filename)

def main(username, repo_name, auth_token):
    url = f'https://api.github.com/repos/{username}/{repo_name}/releases'
    headers = {'Authorization': f'token {auth_token}'}
    response = requests.get(url, headers=headers)

    # 解析JSON响应并获取release信息
    releases = []
    if response.ok:
        json_data = response.json()
        for release in json_data:
            release_id = release['id']
            name = release['name']
            tag_name = release['tag_name']

            # 下载并提取zip文件中的数据文件
            for asset in release['assets']:
                if asset['content_type'] == 'application/zip':
                    download_url = asset['browser_download_url']
                    filename = asset['name']
                    extract_dir = f'{repo_name}_extracted_{release_id}'
                    os.makedirs(extract_dir, exist_ok=True)
                    download_and_extract(download_url, filename, extract_dir)
                    data_path = os.path.join(extract_dir, f'app')
                    print("data_path", data_path)
                    if not os.path.exists('out'):
                        os.makedirs('out', exist_ok=True)
                    if os.path.exists(data_path):
                        shutil.copyfile(os.path.join(data_path, 'links.csv'), f'out/{repo_name}_{tag_name}_{release_id}_outputs.csv')
                    # 删除解压后的文件夹
                    shutil.rmtree(extract_dir)

AUTH_TOKEN = open("AUTH_TOKEN", "r").read().strip()

main("includeno", "spider_ths_news_list_selenium_python", AUTH_TOKEN)
