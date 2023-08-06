from __future__ import print_function
from gdrive_deploy.utilities import *
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():

    argc = len(sys.argv)
    print(str(sys.argv))
    if 4 <= argc <= 5:
        target_file = sys.argv[1]
        target_file_name = sys.argv[2]
        target_file_descr = sys.argv[3]
        credential_file = sys.argv[4] if argc == 5 else 'credentials.json'
        sys.argv = [sys.argv[0]]

        service = get_authenticated(SCOPES, credential_file)
        results = retrieve_all_files(service)

        target_file_id = [file['id'] for file in results if file['name'] == target_file_name]

        if len(target_file_id) == 0:
            print('No file called %s found in root. Create it:' % target_file_name)
            file_uploaded = insert_file(service, target_file_name, target_file_descr, None,
                                        'text/x-script.phyton', target_file)
        else:
            print('File called %s found. Update it:' % target_file_name)
            file_uploaded = update_file(service, target_file_id[0], 'text/x-script.phyton', target_file)

        print(str(file_uploaded))
    else:
        print('Not enough parameters given:\n ' + sys.argv[0] +
              ' file_path file_name file_description [file_credentials]')
        sys.exit(1)


if __name__ == '__main__':
    main()
