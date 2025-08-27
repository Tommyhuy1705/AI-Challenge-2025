import os
from threading import Lock
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth

# class WeaviateConnection:
#     _instance = None
#     _lock = Lock()

#     def __new__(cls):
#         if not cls._instance:
#             with cls._lock:
#                 if not cls._instance:
#                     cls._instance = super().__new__(cls)
#                     cls._instance._initialized = False
#         return cls._instance

#     def __init__(self):
#         if self._initialized:
#             return
#         load_dotenv()
#         self.host = os.getenv("WEAVIATE_URL")
#         self.api_key = os.getenv("WEAVIATE_API_KEY")
#         self.client = None
#         self._connect()
#         self._initialized = True

#     def _connect(self):
#         try:
#             if self.api_key:
#                 self.client = weaviate.connect_to_weaviate_cloud(
#                     cluster_url=self.host,
#                     auth_credentials=Auth.api_key(self.api_key),
#                 )
#             else:
#                 self.client = weaviate.connect_to_local()
#         except Exception as e:
#             raise ConnectionError(f"Failed to connect to Weaviate: {e}")


#     def get_client(self):
#         if not self.client:
#             self._connect()
#         return self.client

def connect_db(cluster_url= None, api_key= None):
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=cluster_url,
        auth_credentials=Auth.api_key(api_key),
        skip_init_checks=True
    )
    return client
