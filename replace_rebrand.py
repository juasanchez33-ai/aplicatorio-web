import os

directory = r"c:\Users\User nuevo\OneDrive\Escritorio\pagina web de finanzas\finance-pro"
extensions = (".html", ".py", ".md", ".json", ".js")
replace_dict = {
    "Aplicativo Web": "Aplicativo Web",
    "Aplicativo_Web": "Aplicativo_Web",
    "finance-pro": "finance-pro" # Not replacing folder reference as discussed
    # Note: 'financepro' is used in db names 'financepro.db', we should probably leave it as is or change to 'aplicativoweb.db', but the user agreed to not touch folder/file names to not break things.
}

for root, dirs, files in os.walk(directory):
    if "venv" in root or ".git" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith(extensions):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for k, v in replace_dict.items():
                new_content = new_content.replace(k, v)
                
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
print("Done replacing.")
