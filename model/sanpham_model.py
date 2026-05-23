import pandas as pd
import os

class SanphamModel:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title
        # Tự động tạo file CSV nếu chưa tồn tại
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=self.title)
            df.to_csv(file_path, index=False)

    def danh_sach(self, page, page_size):
        data = pd.read_csv(self.file_path).astype(str)
        if self.title:
            data = data[self.title]
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": [data.iloc[i].to_dict() for i in range(start, min(end, len(data)))]
        }

    def tim_kiem(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path).astype(str)
        if self.title:
            data = data[self.title]
        result = data[data[title_keyword].astype(str).str.contains(keyword)]
        return [result.iloc[i].to_dict() for i in range(len(result))]

    def xoa(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path).astype(str)
        if self.title:
            data = data[self.title]
        result = data[~data[title_keyword].astype(str).str.contains(keyword)]
        result.to_csv(self.file_path, index=False)
        return True

    def cap_nhat(self, title_keyword, keyword, title_edit=[], new_data=[]):
        data = pd.read_csv(self.file_path).astype(str)
        if self.title:
            data = data[self.title]
        for i in title_edit:
            data.loc[data[title_keyword].astype(str).str.contains(keyword), i] = new_data[title_edit.index(i)]
        data.to_csv(self.file_path, index=False)
        return True

    def them(self, new_data):
        data = pd.read_csv(self.file_path).astype(str)
        if self.title:
            data = data[self.title]
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True

    def lay_id_tiep_theo(self):
        data = pd.read_csv(self.file_path).astype(str)
        return len(data) + 1