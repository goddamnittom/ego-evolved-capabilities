import pypdf

reader = pypdf.PdfReader("/root/2606.07713.pdf")
print(f"Total pages: {len(reader.pages)}")

# Let's extract first 2 pages to inspect
for i in range(min(5, len(reader.pages))):
    print(f"--- Page {i+1} ---")
    print(reader.pages[i].extract_text()[:1500])

