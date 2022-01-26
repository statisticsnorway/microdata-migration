import requests

data_store_url = "http://pl-raird-app-qa2.ssb.no:8084/metadata/data-store"

response = requests.get(data_store_url)
print(response)
data_store_dict = response.json()

metadata_all_str = "http://pl-raird-app-qa2.ssb.no:8084/metadata/all?version=<placeholder>"

for dic in data_store_dict["versions"]:
    for key in dic:
        if key == "version":
            metadata_all_url = metadata_all_str.replace("<placeholder>", dic[key])
            print (metadata_all_url)

            # ... to be continued