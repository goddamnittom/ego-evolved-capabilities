import os
import shutil

staging_dir = "/root/github_staging"
scripts_file = "/root/scripts_to_push.txt"

if not os.path.exists(staging_dir):
    os.makedirs(staging_dir)

with open(scripts_file, 'r') as f:
    scripts = f.readlines()

for script_path in scripts:
    script_path = script_path.strip()
    if not script_path: continue
    
    filename = os.path.basename(script_path)
    name_no_ext = os.path.splitext(filename)[0]
    
    # Create sub-folder
    folder_path = os.path.join(staging_dir, name_no_ext)
    os.makedirs(folder_path, exist_ok=True)
    
    # Copy script
    shutil.copy(script_path, os.path.join(folder_path, filename))
    
    # Generate README
    readme_content = f"# {name_no_ext.replace('_', ' ').title()}\n\nThis script is part of the Ego Evolved Capabilities library.\n\n## Description\nAutonomous capability implemented to enhance AI operational throughput and intelligence.\n\n## Usage\n`python3 {filename}`"
    with open(os.path.join(folder_path, "README.md"), "w") as rf:
        rf.write(readme_content)

print("Staging complete.")
