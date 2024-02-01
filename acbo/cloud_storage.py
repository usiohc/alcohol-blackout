from google.cloud import storage
from models import datetime
from json import dumps


storage_client = storage.Client()


def upload_blob_from_memory(bucket_name: str, data: dict, destination_blob_name: str,
                            _storage_client=storage_client):
    # Dict를 JSON 문자열로 변환, loads()로 유니코드 이스케이프 decode
    json_data = dumps(data, ensure_ascii=False).encode('utf-8').decode('utf-8')
    try:
        bucket = _storage_client.bucket(bucket_name)
        bucket_path = f"{datetime.date()}"
        idx = get_blobs_count(bucket_name, bucket_path, _storage_client)

        blob = bucket.blob(bucket_path + "/" + f"{idx}-{destination_blob_name}.json")
        blob.upload_from_string(json_data, content_type="application/json")
        return True
    except Exception as e:
        print(e)
        return False


def get_blobs_count(bucket_name, bucket_path, _storage_client):
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = _storage_client.list_blobs(bucket_name, prefix=bucket_path+"/")

    # Note: The call returns a response only when the iterator is consumed.
    for _ in blobs:
        pass

    # 해당 날짜 폴더가 존재하지 않음 "1-name.json" 이 생성될 때, 해당 blobs.num_results는 0 -> 2가 됨
    length = blobs.num_results
    if length == 0:
        return 1
    else:
        # num_results=2, num_results-1 된 값이 현재 존재하는 json 파일의 counter
        return length
