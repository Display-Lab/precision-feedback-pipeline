import subprocess

with open('version.txt','r') as version_file:
    current_version = int(version_file.read())

new_version = current_version +1

with open('version.txt','w') as version_file:
    version_file.write(str(new_version))

subprocess.run(['git','add','version.txt'])
subprocess.run(['git','commit','-m',f'Bump version to {new_version}'])
