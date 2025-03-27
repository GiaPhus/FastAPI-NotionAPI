import requests
from fastapi import HTTPException, FastAPI
import os
from dotenv import load_dotenv

app = FastAPI()

class NotionConfig:
    def __init__(self):
        load_dotenv()
        self.NOTION_KEY = os.getenv("NOTION_KEY")
        self.NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
        self.HEADERS = {
            "Authorization": f"Bearer {self.NOTION_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def get_pages(self, num_pages=None):
        url = f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query"
        page_size = 100 if num_pages is None else num_pages
        payload = {"page_size": page_size}

        try:
            response = requests.post(url, json=payload, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from Notion: {str(e)}")

        return data.get("results", [])

    def create_pages(self, data: dict):
        create_url = "https://api.notion.com/v1/pages"
        payload = {"parent": {"database_id": self.NOTION_DATABASE_ID}, "properties": data}

        try:
            res = requests.post(create_url, json=payload, headers=self.HEADERS)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error creating page: {str(e)}")

    def get_product(self):
        url = f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query"
        try:
            response = requests.post(url, headers=self.HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")
        
    def create_properties(data: dict):
        properties = {}

        for key, value in data.items():
            try:
                if key == "Tên sản phẩm":
                    if value:
                        properties[key] = {"title": [{"text": {"content": value}}]}

                elif key in ["Đất", "Ánh sáng", "Phân bón", "Độ ẩm", "Tưới nước", "Nhân giống", "Nhiệt độ"]:
                    if isinstance(value, list) and value:
                        properties[key] = {"multi_select": [{"name": v} for v in value]}

                elif key == "Còn hàng":
                    properties[key] = {"checkbox": bool(value)}

                elif key in ["Tên khoa học", "Đặc điểm", "Lưu ý", "Phong thủy"]:
                    if value:
                        properties[key] = {"rich_text": [{"text": {"content": value}}]}

                elif key == "Báo giá":
                    print(f"⚠️ Bỏ qua cột `{key}` vì đây là công thức.")
                    continue

                elif key == "Giá (VND)":
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"Giá (VND) phải là số, nhưng nhận được {type(value)}")
                    properties[key] = {"number": value}

                elif key == "Nhóm cây":
                    if isinstance(value, str) and value:
                        properties[key] = {"select": {"name": value}}

            except Exception as e:
                print(f"❌ Lỗi ở cột `{key}` với giá trị `{value}`: {e}")

        return properties

    def update_product(self,page_id : str, update_data : dict):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        data = {
            "parent": {"database_id": self.NOTION_DATABASE_ID},
            "properties": NotionConfig.create_properties(update_data)
        }
        try:
            response = requests.patch(url, json=data, headers=self.HEADERS)
            response.raise_for_status()
            return {"message": "Sản phẩm đã được cập nhật!", "data": response.json()}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")
        
    def get_page_id_by_title(self,title):
        url = f"https://api.notion.com/v1/databases/{self.NOTION_DATABASE_ID}/query"
        payload = {
            "filter": {
                "property": "Tên sản phẩm",  # Đổi theo đúng tên column của bạn
                "title": {
                    "equals": title
                }
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.HEADERS)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            if results:
                return results[0]["id"]
            return None
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching page ID: {str(e)}")

    
    def delete_product(self, page_id: str):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        data = {"archived": True}

        try:
            response = requests.patch(url, json=data, headers=self.HEADERS)
            response.raise_for_status()
            return {"message": "Sản phẩm đã bị xóa (archived)!", "data": response.json()}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

    def add_product(self, product: dict):
        url = "https://api.notion.com/v1/pages"
        data = {
            "parent": {"database_id": self.NOTION_DATABASE_ID},
            "properties": NotionConfig.create_properties(product)
        }
        print(data)
        try:
            response = requests.post(url, json=data, headers=self.HEADERS)
            response.raise_for_status()
            return {"message": "Sản phẩm đã được thêm thành công!", "data": response.json()}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error adding product: {str(e)}")

notion = NotionConfig()

@app.post('/product')
def add_product_api(product: dict):
    return notion.add_product(product)

@app.get('/product')
def get_product_api():
    return notion.get_product()

@app.patch('/product/update')
def update_product_api(title: str, updated_product: dict):
    page_id = notion.get_page_id_by_title(title)
    if not page_id:
        raise HTTPException(status_code=404, detail="Page not found")
    
    return notion.update_product(page_id, updated_product)

@app.delete('/product/delete')
def delete_product_api(title: str):
    page_id = notion.get_page_id_by_title(title)
    return notion.delete_product(page_id)