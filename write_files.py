#%%
import pandas as pd
from dotenv import dotenv_values
import requests
from boxsdk import Client, JWTAuth
from boxsdk.object.collaboration import CollaborationRole
#%%
# LOAD ENVIRONMENT VARIABLES
cfg = dotenv_values(".env") 

def auth_box():
    '''
    Accessing Box API
    '''
    auth = JWTAuth(
        client_id=cfg['clientID'],
        client_secret=cfg['clientSecret'],
        enterprise_id=cfg['enterpriseID'],
        jwt_key_id=cfg['publicKeyID'],
        rsa_private_key_data=cfg['privateKey'],
        rsa_private_key_passphrase=cfg['passphrase']
    )
    access_token = auth.authenticate_instance()
    client = Client(auth)
    print(client.auth)
    return client

def write_box(filepath, data_type, folder_name, client):
    '''
    Writing to Box project folder.
    '''
    if folder_name=='parent':
        folder_id = '194970922440'
    elif folder_name=='CCRB':
        folder_id = '194988612199'
    elif folder_name=='NYPD':
        folder_id = '196912675328'

    # get the subfolder ID
    items = client.folder(folder_id=folder_id).get_items()
    for item in items:
        #print(f'{item.type.capitalize()} {item.id} is named "{item.name}"')
        if item.name == data_type:
            subfolder_id = item.id

    # check if file already exists
    filename = filepath.split('/')[-1]
    filename = filename.split('.')[0]
    filetype = filepath.split('.')[-1]
    exact_filename = f"\"{filename}\""
    check_file = client.search().query(query=exact_filename, 
                                       content_types = ['name'], 
                                       limit=1, 
                                       ancestor_folder_ids=[subfolder_id], 
                                       type='file')    
    file_id = None
    for i in check_file:
        print(f'The item ID is {i.id} and the item name is {i.name}')
        file_id = i.id

    # either update or upload file
    if file_id:
        updated_file = client.file(file_id).update_contents(filepath)
        print('File "{0}" has been updated'.format(updated_file.name))
    else:
        new_file = client.folder(subfolder_id).upload(file_path = filepath, file_name = f"{filename}.{filetype}")
        print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))

def download_report(metric, agency, client):
    '''
    Downloading report URLs.
    '''
    df = pd.read_csv(f"results/{metric}_links.csv")
    for u in range(df.shape[0]):
        print(df.text[u])
        report = requests.get(df.url[u])
        with open(f'tmp/{df.text[u]}.{df.data_type[u]}', 'wb') as outfile:
            outfile.write(report.content)
        write_box(filepath=f'tmp/{df.text[u]}.{df.data_type[u]}', 
                  data_type='Raw',
                  folder_name=agency, 
                  client=client)
# %%

if __name__ == "__main__":
    client = auth_box()
    download_report(metric='vehicle_stops', agency='NYPD', client=client)
    download_report(metric='homicides', agency='NYPD', client=client)
    download_report(metric='sqf', agency='NYPD', client=client)
# %%
