import json
import requests
import webbrowser
import base64
import os
import sys
from s3_upload import S3Uploader


def XeroFirstAuth(client_id, client_secret, scope):
    b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')
    redirect_url = 'https://xero.com'

    # 1. Send a user to authorize your app
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)
    
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    #print(auth_code)
    #print('\n')
    
    # 3. Exchange the code
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Authorization': 'Basic ' + b64_id_secret
                            },
                            data = {
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': redirect_url
                            })
    json_response = response.json()
    #print(json_response)
    #print('\n')
    
    # 4. Receive your tokens
    return [json_response['access_token'], json_response['refresh_token']]


# 5. Check the full set of tenants you've been authorized to access
def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
    #print(json_response)
    
    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']


# 6.1 Refreshing access tokens
def XeroRefreshToken(refresh_token):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                            headers = {
                                'Authorization' : 'Basic ' + b64_id_secret,
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type' : 'refresh_token',
                                'refresh_token' : refresh_token
                            })
    json_response = response.json()
    #print(json_response)
    
    new_refresh_token = json_response['refresh_token']
    rt_file = open('C:/folder/refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()
    
    return [json_response['access_token'], json_response['refresh_token']]

def XeroRequests(access_token, tenant_id, source_folder_name):
    
    get_url = 'https://api.xero.com/api.xro/2.0/Invoices'
    response = requests.get(get_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Xero-tenant-id': tenant_id,
                               'Accept': 'application/json'
                           })
    json_response = response.json()
    print(json_response)
    
    xero_output = open( source_folder_name + '/xero_output.json', 'w')
    xero_output.write(response.text)
    xero_output.close()


def main(argv):
    if len (sys.argv) == 6:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
        scope = sys.argv[3]
        ## Specify the source folder where the files are going to be copied 'from'
        source_folder_name = sys.argv[4]
        ## Create a S3 bucket
        bucket_name = sys.argv[5]

        ret_values = XeroFirstAuth(client_id, client_secret, scope)
        tenant_id = XeroTenants(ret_values[0])
        XeroRequests(ret_values[0], tenant_id, source_folder_name)

        s3uploader = S3Uploader()
        print ('creating ............... bucket ...... : ' + bucket_name)
        s3uploader.create_bucket(str(bucket_name))


        ## 3. Initiate file transfer to S3 bucket
        print (s3uploader.upload_files_from_folder_to_s3(source_folder_name, bucket_name))
    else:
        print ('python3 xero.py <xero_client_id> <xero_token> <xero_scope>  <source_folder_name>  <s3_bucket_name>')

if __name__ == "__main__":
   main(sys.argv[1:])