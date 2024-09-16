import asyncio
import requests
import fitz  # import PyMuPDF

async def send_request_process_single(file_index):
    url = "http://eyeh:8088/uploadfile/"
    
    payload = {}
    files=[
      ('file_input',('file',open(f"output/document-{file_index}.pdf",'rb'),'application/octet-stream'))
    ]
    headers = {
      'accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

doc = fitz.open("file-sao-ke.pdf") # open a document

print("doc lens:", len(doc))

async def run_all():
    tasks = []
    for i in range(0, len(doc)):
        tasks.append(send_request_process_single(i))
    results = await asyncio.gather(*tasks)
    return results

# raw_proc_res = await run_all()
loop = asyncio.get_event_loop()
res = loop.run_until_complete(run_all())
loop.close()
print(res)
