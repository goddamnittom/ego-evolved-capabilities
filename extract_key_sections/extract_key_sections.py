import pypdf

reader = pypdf.PdfReader("/root/2606.07713.pdf")

def save_pages(start_page, end_page, out_file):
    with open(out_file, "w") as f:
        for p in range(start_page - 1, end_page):
            f.write(f"=== PAGE {p+1} ===\n")
            f.write(reader.pages[p].extract_text())
            f.write("\n\n")

save_pages(14, 21, "/root/section_4_attention_derivation.txt")
save_pages(27, 31, "/root/section_8_mechanization.txt")
print("Key sections extracted successfully.")
