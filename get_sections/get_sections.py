import pypdf
import re

reader = pypdf.PdfReader("/root/2606.07713.pdf")
sections = []
for idx, page in enumerate(reader.pages):
    text = page.extract_text()
    for line in text.split('\n'):
        if re.match(r'^[1-9]\d*\.\s+[A-Z]', line) or re.match(r'^[1-9]\d*\.[1-9]\d*\s+[A-Z]', line):
            sections.append((idx+1, line))

for page_num, sec in sections[:40]:
    print(f"Page {page_num}: {sec}")
