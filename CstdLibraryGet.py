import requests
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from typing import List,Optional

@dataclass
class CStandardLibraryHeader:
    name: str
    introduced: str
    description: str
    feature_macro: Optional[str] = None
    macro_value: Optional[int] = None

    def __repr__(self):
        return (f"<CStandardLibraryHeader: {self.name}, "
                f"Introduced: {self.introduced}, "
                f"Description: '{self.description[:30]}...', "
                f"Feature Macro: {self.feature_macro or 'N/A'}>")

url = "https://en.cppreference.com/w/c/header"


def extract_introduced_version(text):
    # 使用正则表达式提取版本信息
    match = re.search(r'$([^)]+)$', text)
    if match:
        version = match.group(1)
        if re.match(r'C(\d{2,3}|11|17|23|29)', version):
            return version

    if "C99" in text:
        return "C99"
    if "C11" in text:
        return "C11"
    if "C23" in text:
        return "C23"
    if "C29" in text:
        return "C29"

    return "C89"


def self_or_parent_text(tt):
    pass


def fetch_c_standard_library_headers(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
    try:
        # 获取页面内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找主要区域内容
        content_div = soup.find("div", {'id':"mw-content-text"})
        if not content_div:
            return ValueError("Content div not found")

        # 查找所有头文件定义
        headers = []
        header_tts = content_div.find_all("tt")
        for tt in header_tts:
            a_tag = tt.find("a")
            if a_tag and a_tag.get("href", "").startswith("/w/c/header/"):
                header_name = a_tag.text.strip()
                if any(h.name == header_name for h in headers):
                    continue

                # 查找引入版本
                context = self_or_parent_text(tt)
                introduced = extract_introduced_version(context)

                # 查找描述
                description = ""
                next_sibling = tt.find_next_sibling()
                if next_sibling and next_sibling.name == "dd":
                    description = next_sibling.text.strip()
                    # 清理描述文本
                    if '[edit]' in description:
                        description = description.replace('[edit]','').strip()
                headers.append(CStandardLibraryHeader(name, introduced, description))

        # 提取特性宏和宏值
        feature_table = content_div.find('table', {'class': 'wikitable'})
        if feature_table:
            for row in feature_table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    header_name = cols[1].text.strip().strip('<>')
                    macro = cols[2].text.strip()
                    value = cols[3].text.strip()

                    # 清理宏值
                    if 'L' in value:
                        value = value.replace('L','')

                    # 尝试转换为整数
                    macro_int_value = None
                    if value and value != 'N/A':
                        try:
                            macro_int_value = int(value)
                        except ValueError:
                            if value.startswith('2029'):
                                macro_int_value = 2029
                    # 更新头文件的特性宏和宏值
                    for header in headers:
                        if header.name == header_name:
                            if macro != 'N/A':
                                header.feature_macro = macro
                            header.macro_value = macro_int_value
                            break
        return headers
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# 示例使用
if __name__ == "__main__":
    print("Fetching C standard library headers...")
    c_headers = fetch_c_standard_library_headers(url)

    if not c_headers:
        print("No headers found or an error occurred.")
    else:
        print(f"Found {len(c_headers)} C standard library headers:")

        for i,header in enumerate(c_headers[:5],1):
            print(f"\n{i}. header: {header.name}")
            print(f"   Introduced: {header.introduced}")
            print(f"   Description: {header.description[:50]}...")
            if header.feature_macro:
                print(f"   Feature Macro: {header.feature_macro}")
                if header.macro_value is not None:
                    print(f"   Macro Value: {header.macro_value}")
                else:
                    print("   Macro Value: N/A")
            else:
                print("   Feature Macro: N/A")
            print("-" * 60)
        print("headers list")
        header_names = [header.name for header in c_headers]
        print(",".join(header_names))