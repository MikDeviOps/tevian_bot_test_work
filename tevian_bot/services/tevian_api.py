import logging
import requests
from requests.auth import HTTPBasicAuth
from config.settings import TEVIAN_BASE_URL, TEVIAN_USERNAME, TEVIAN_PASSWORD, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class TevianAPI:
    def __init__(self):
        self.base_url = TEVIAN_BASE_URL.rstrip('/')
        self.auth = HTTPBasicAuth(TEVIAN_USERNAME, TEVIAN_PASSWORD)
        self.timeout = REQUEST_TIMEOUT
    
    def _handle_response(self, response, operation_name):
        """Универсальная обработка ответов API"""
        if response.status_code == 200:
            logger.info(f"{operation_name}: Success")
            return response
        else:
            logger.error(f"{operation_name}: Error {response.status_code} - {response.text}")
            return response
    
    def create_bucket(self, bucket_name: str):
        endpoint = f"{self.base_url}/api/bucket/{bucket_name}"
        data = {"caption": f"Картотека {bucket_name}"}
        
        response = requests.post(endpoint, auth=self.auth, json=data, timeout=self.timeout)
        return self._handle_response(response, f"Create bucket {bucket_name}")
    
    def get_buckets(self):
        endpoint = f"{self.base_url}/api/v1/buckets"
        params = {'limit': 100, 'with_num_records': True}
        
        response = requests.get(endpoint, auth=self.auth, params=params, timeout=self.timeout)
        return self._handle_response(response, "Get buckets")
    
    def delete_bucket(self, bucket_name: str):
        endpoint = f"{self.base_url}/api/bucket/{bucket_name}"
        
        response = requests.delete(endpoint, auth=self.auth, timeout=self.timeout)
        return self._handle_response(response, f"Delete bucket {bucket_name}")
    
    def add_face_to_bucket(self, bucket_name: str, identity: str, image_bytes: bytes):
        endpoint = f"{self.base_url}/api/bucket_all_faces"
        
        params = {
            'bucket_name': bucket_name,
            'identity': identity
        }
        
        headers = {'Content-Type': 'image/jpeg'}
        
        logger.info(f"Adding face to bucket: {bucket_name}, identity: {identity}")
        
        response = requests.post(
            endpoint, 
            auth=self.auth, 
            params=params, 
            data=image_bytes,
            headers=headers,
            timeout=self.timeout
        )
        
        return self._handle_response(response, f"Add face to {bucket_name}")
    
    def get_all_faces_from_bucket(self, bucket_name: str):
        endpoint = f"{self.base_url}/api/v1/buckets/face/list"
        
        params = {
            'bucket': bucket_name,
            'limit': 100,
            'offset': 0
        }
        
        response = requests.get(endpoint, auth=self.auth, params=params, timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            faces = data.get('data', [])
            logger.info(f"Found {len(faces)} faces in bucket {bucket_name}")
            return faces
        else:
            logger.error(f"Error getting faces from bucket {bucket_name}: {response.status_code}")
            return []

    def delete_face_from_bucket(self, bucket_name: str, face_id: str):
        endpoint = f"{self.base_url}/api/bucket/{bucket_name}/{face_id}"
        
        response = requests.delete(endpoint, auth=self.auth, timeout=self.timeout)
        return self._handle_response(response, f"Delete face {face_id} from {bucket_name}")
    
    def search_by_photo(self, image_bytes: bytes, threshold: float = 0.9, limit: int = 10):
        endpoint = f"{self.base_url}/api/photo/matches"
        
        params = {
            'threshold': threshold,
            'limit': limit,
            'type': 'face'
        }
        
        headers = {'Content-Type': 'image/jpeg'}
        
        logger.info(f"Search by photo: image size {len(image_bytes)} bytes")
        
        response = requests.post(
            endpoint,
            auth=self.auth,
            params=params,
            data=image_bytes,
            headers=headers,
            timeout=self.timeout
        )
        
        return self._handle_response(response, "Search by photo")
    
    def search_similar_faces(self, bucket_name: str, face_id: str, threshold: float = 0.9, limit: int = 10):
        endpoint = f"{self.base_url}/api/bucket/{bucket_name}/{face_id}/matches"
        
        params = {
            'threshold': threshold,
            'limit': limit,
        }
        
        response = requests.get(endpoint, auth=self.auth, params=params, timeout=self.timeout)
        return self._handle_response(response, f"Search similar faces for {face_id}")