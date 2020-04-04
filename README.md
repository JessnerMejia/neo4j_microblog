# neo4j-flask
Una aplicacion de microblog escrita en python utilizando Flask and Neo4j. Basado en la extension, [Flaskr](http://flask.pocoo.org/docs/0.10/tutorial/). 

Se tomo como base el tutorial [Tutorial] (https://neo4j.com/blog/building-python-web-application-using-flask-neo4j/) Pero tuvieron que hacerse algunos cambios sobre la manera en que opera la libreria py2neo. Espero que te sirva

## Uso

Asegurate primero de que [Neo4j](http://neo4j.com/download/other-releases/) este corriendo sobre tu maquina!

A continuacion los pasos para ponerla a correr en tu maquina:
git clone https://github.com/JessnerMejia/python_projects.git
cd python_projects/bases_datos 
pip install virtualenv
virtualenv tu_nombre
source tu_nombre/bin/activate
pip install -r requirements.txt
python run.py
```
Tu aplicacion estara corriendo en el siguiente link
[http://localhost:5000](http://localhost:5000)
