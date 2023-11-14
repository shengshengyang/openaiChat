import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

sharepoint_site_url = os.getenv("SHAREPOINT_BASIC_URL")
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")
relative_url = os.getenv("SHAREPOINT_IT_BOT_URL")



# Authenticate with SharePoint
auth_ctx = AuthenticationContext(sharepoint_site_url)
if auth_ctx.acquire_token_for_user(username, password):
    ctx = ClientContext(sharepoint_site_url, auth_ctx)


    # Ensure the relative URL is correct
    file_url = sharepoint_site_url.rstrip('/') + '/' + relative_url.lstrip('/')
    print(f"Attempting to download file from URL: {file_url}")  # Debug print

    # Download file
    download_path = "./ai_bot_data.xlsx"
    try:
        response = File.open_binary(ctx, file_url)
        if response.status_code == 200:
            with open(download_path, "wb") as local_file:
                local_file.write(response.content)
            print(f"File downloaded to: {download_path}")
        else:
            print(f"Failed to download file. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Authentication failed: ", auth_ctx.get_last_error())