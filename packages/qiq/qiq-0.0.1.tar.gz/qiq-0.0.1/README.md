qiq is the thin layer over pip with some principles.

- requirements.txt becomes qiq.txt
- virtual environment created in project in `venv`
- every package in `qiq.txt` has exact version or links to local directory
- symlinks for local development

No requirements except `Python 3`.

## Usage
 
For example `My-Company-Core` is the Company's core library used almost in all projects. It's development files located relative to current project is `../my_company_core`.
Our `qiq.txt` will be:

    +dev:../my_company_core
    My-Company-Core==1.2.7
    Flask==1.0.2
    flask-cors==3.0.7
    

`+dev` is the flag, which can be given in `qiq` command.
This will symlink `my_company_core` to `../my_company_core`:
    
    qiq +dev
    
And this will install production use code to venv:

    qiq
    
By default used library name is last directory in path. It can be overriden with name and `==`:

    +dev:Company-Core==../my_company_core
    
VCS also supported:
    
    +dev:git+ssh://gitlab.com/myteam/mycompanycore.git@2313ceee
