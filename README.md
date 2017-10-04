[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](./LICENSE)


# SciBib

SciBib is an online **Sci**entific **Bib**liography System.  
The aim of SciBib is to provide a system to organizes and distribute publications online.

### Features

- Website to publish publications
- Admin center - Add and edit publication, authors, keywords, categories
- User management
- Filter publications by year, publication type, user
- Publish publications as PDF files
- Export bibtex functionality
- JSON API

## Deployment

SciBib can be deployed by using [Docker](https://www.docker.com/) or via command line on a linux system.  
The recommended way is to use the docker deployment.  
For prerequisites, troubleshooting and remarks the links below should hold all information.  

- [Deploy with Docker](./Documentation/Deployment/docker.md)
- [Deploy without Docker](./Documentation/Deployment/nodocker.md)

## Update

SciBib can be updated by copying the SciBib directory from the repo into the running directory.  
This works for the Docker and the cmd line deployment.

## Built With

* [CakePHP](https://github.com/cakephp/cakephp)
* [Docker](https://www.docker.com/)

## License

This project is licensed under the Apache 2.0 - see the [LICENSE](LICENSE) file for details

Copyright 2017 [University Konstanz - Data Analysis and Visualization Group](https://www.vis.uni-konstanz.de/)
