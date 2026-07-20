import base64
import io
import zipfile


def extract_zip_data(zip_data):
    memory_file = io.BytesIO(zip_data)
    dictionary = dict()

    with zipfile.ZipFile(memory_file, 'r') as zf:
        file_list = zf.namelist()
        for file in file_list:
            with zf.open(file) as file_new:
                content = file_new.read()
                dictionary[file] = content.decode("utf-8")
    return dictionary


def decode_base64_data(base64_data):
    return base64.b64decode(base64_data)


def encode_base64_data(data):
    return base64.b64encode(data)

