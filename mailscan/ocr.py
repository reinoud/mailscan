import requests
import datetime


def ocr_attachments(conf, attachments) -> list:
    ocr_container = conf['ocr']['containername']
    ocr_container_port = conf['ocr']['containerport']
    default_scanname = conf['ocr']['scanname']
    att_files = []

    for att in attachments:
        filename = att['filename']
        path = att['path']
        if filename.split('.')[-1].upper() == 'PDF':
            url = f'http://{ocr_container}:{ocr_container_port}'
            r = requests.post(url,
                              files={'file': (filename, open(path, 'rb')),
                                     'params': (None, '')},
                              stream=True)
            if r.status_code == 200:
                print('succes')
                # overwrite existing file
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else:
                print(f'error while sending pdf to scanning container: {r.status_code}')
                print(f'request headers: {r.request.headers}')
                print(f'headers: {r.headers}')
        if filename == default_scanname:
            date = datetime.datetime.now()
            filename = f'scan_{date:%Y%m%d}_{date:%H%M%S}.pdf'
        att_files.append({'filename': filename,
                          'path': path})

    return att_files
