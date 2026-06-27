import os
import re
import asyncio
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen

SUCCESS = 'Success'
ERROR = 'Error'


def make_table(headers, rows):
    widths = [len(header) for header in headers]

    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    border = '+' + '+'.join('-' * (width + 2) for width in widths) + '+'
    header = '|' + '|'.join(
        f' {headers[i].center(widths[i])} '
        for i in range(len(headers))
    ) + '|'

    lines = [border, header, border]

    for row in rows:
        line = '|' + '|'.join(
            f' {str(row[i]).ljust(widths[i])} '
            for i in range(len(row))
        ) + '|'
        lines.append(line)

    lines.append(border)
    return '\n'.join(lines)


def can_write_to_folder(path):
    try:
        os.makedirs(path, exist_ok=True)

        test_file = os.path.join(path, '.write_test')

        with open(test_file, 'w', encoding='utf-8') as file:
            file.write('test')

        os.remove(test_file)
        return True
    except OSError:
        return False


async def async_input(text=''):
    return await asyncio.to_thread(input, text)


async def ask_folder():
    while True:
        folder = (await async_input('save folder: ')).strip()

        if not folder:
            print('folder cannot be empty')
            continue

        if os.path.exists(folder) and not os.path.isdir(folder):
            print('this is not a folder')
            continue

        if not can_write_to_folder(folder):
            print('no access to write here')
            continue

        return folder


def get_filename(url, number):
    name = os.path.basename(urlsplit(url).path)
    name = unquote(name)

    if not name:
        name = 'image.jpg'

    name = re.sub(r'[\\/:*?"<>|]+', '_', name)

    if '.' not in name:
        name += '.jpg'

    return f'{number}_{name}'


def download_sync(url, folder, number):
    try:
        parsed_url = urlsplit(url)

        if parsed_url.scheme not in ('http', 'https') or not parsed_url.netloc:
            return url, ERROR

        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(request, timeout=15) as response:
            content_type = response.headers.get('Content-Type', '')

            if not content_type.startswith('image/'):
                return url, ERROR

            data = response.read()

        path = os.path.join(folder, get_filename(url, number))

        with open(path, 'wb') as file:
            file.write(data)

        return url, SUCCESS

    except Exception:
        return url, ERROR


async def main():
    folder = await ask_folder()
    tasks = []

    print('enter urls (empty to stop):')

    while True:
        url = (await async_input()).strip()

        if not url:
            break

        number = len(tasks) + 1
        task = asyncio.to_thread(download_sync, url, folder, number)
        tasks.append(asyncio.create_task(task))

    if not tasks:
        print('no urls')
        return

    if any(not task.done() for task in tasks):
        print('waiting for downloads...')

    results = await asyncio.gather(*tasks)

    print()
    print(make_table(['Link', 'Status'], results))


if __name__ == '__main__':
    asyncio.run(main())
