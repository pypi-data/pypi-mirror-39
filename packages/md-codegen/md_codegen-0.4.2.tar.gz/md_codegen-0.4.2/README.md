# Codegen

# Description
**codegen** is tool for generating code for [microservice accelerator](https://github.houston.entsvcs.net/zongying-cao/micro-service-accelerator). The generation engine is based on [Jinja2](https://github.com/pallets/jinja).
It generates code with specified [templates](templates.md).  

# Installation
```
pip install md_codegen
```
**codegen** is developed and tested on python 3.x. Please make sure python 3.x has already installed on your system prior to install it.

# Usage
## Generating with microservice accelerator portal
```
codegen <host_url> --username=<username> --password=<password> --output=<output path> --project=test1 --template-repo=<template_git_repo> --template-tag=<template_git_repo_tag>
```
* `host_url`: the url to download the *microservice definitions*. It would follow the pattern `http://<host>:<port>`.   

## Generating with local data
```
codegen --output=<output path> --template-repo=<template_git_repo> --template-tag=<template_git_repo_tag> --datafile=<datafile>
```

## Developing templates
```
codegen --output=<output path> --template-path=<template-path> --datafile=<datafile>
```

> If you want to update the interface defintion to your code, you should commit the changes in your local and make sure your local git repository is clean or the code generation will abort.
