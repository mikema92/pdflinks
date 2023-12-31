from files import get_filename
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

testdoc = 'testdoc.txt'

mimetype_map = {
    "pdf": ("application/pdf", "application/pdf"),
    "txt": ("application/vnd.google-apps.document", "text/plain"),
    "py": ("application/vnd.google-apps.document", "text/plain")
}

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_CFG = 'service_account.json'
DRIVE_ROOT_FOLDER_ID = '1F9Pk1C8dzZPiZhZkhKoByF1i3i9QyQDQ'

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_CFG, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)
    return service

def create_folder(filename, service):
  """Create a folder and prints the folder ID
  Returns : Folder Id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    file_metadata = {
        "name": filename,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [DRIVE_ROOT_FOLDER_ID]
    }

    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def upload_with_conversion(file, folderid, ext, service):
  """Upload file with conversion
  Returns: ID of the file uploaded

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    file_metadata = {
        'name': get_filename(file, ext),
        'mimeType': mimetype_map[ext][0],
        'parents': [folderid]
    }
    media = MediaFileUpload(file, mimetype=mimetype_map[ext][1], resumable=True)
    # pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File with ID: "{file.get("id")}" has been uploaded.')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")

if __name__ == "__main__":
  service = get_drive_service()
  fid = create_folder("test", service)
  upload_with_conversion(testdoc, fid, "txt", service)
