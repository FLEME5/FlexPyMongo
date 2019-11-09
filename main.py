from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Portal'
app.config['MONGO_URI'] = 'mongodb+srv://matheuslemes:1ShI5niZ5ZNY6IFE@flexpymongo-jwcen.gcp.mongodb.net/Portal?retryWrites=true&w=majority'

mongo = PyMongo(app)

# ENDPOINT E MÉTODO PARA ADICIONAR NOVAS NOTÍCIAS
@app.route('/noticias/adicionar', methods=['POST'])
def add_noticia():
    noticia = mongo.db.Noticias

    titulo = request.json['titulo']
    texto = request.json['texto']
    autor = request.json['autor']
    idnoticia = request.json['idnoticia']

    noticia_id = noticia.insert({'idnoticia': idnoticia, 'titulo' : titulo, 'texto' : texto, 'autor' : autor})
    new_noticia = noticia.find_one({'_id' : noticia_id})

    output = {'idnoticia': new_noticia['idnoticia'], 'titulo' : new_noticia['titulo'],
    'texto' : new_noticia['texto'], 'autor': new_noticia['autor']}

    return jsonify({'Notícia Inserida': output})


# ENDPOINT E MÉTODO PARA LISTAR TODAS AS NOTÍCIAS
@app.route('/noticias', methods=['GET'])
def get_all_noticias():
    noticias = mongo.db.Noticias

    output = []

    for q in noticias.find():
        output.append({'idnoticia': q['idnoticia'], 'texto' : q['texto'], 'autor' : q['autor'], 'titulo' : q['titulo']})

    return jsonify({'Notícias' : output})

# ENDPOINT E MÉTODO PARA DELETAR UMA NOTÍCIA PASSANDO SEU CAMPO idnoticia
@app.route('/noticias/deletar/<idnoticia>', methods=['DELETE'])
def delete_noticia(idnoticia):
    noticias = mongo.db.Noticias

    q = noticias.find_one({"idnoticia": int(idnoticia)})

    if q:
        output = {'idnoticia': q['idnoticia'], 'texto': q['texto'], 'autor': q['autor'], 'titulo': q['titulo']}
        noticias.delete_one(q)
    else:
        output = 'Não encontrado'

    return jsonify({'Notícia deletada' : output})

# ENDPOINT E MÉTODO PARA EDITAR UMA NOTÍCIA PASSANDO SEU CAMPO idnoticia
@app.route('/noticias/editar/<idnoticia>', methods=['PATCH'])
def update_noticia(idnoticia):
    noticias = mongo.db.Noticias

    q = noticias.find_one({"idnoticia": int(idnoticia)})

    if q:
        output = {'idnoticia': q['idnoticia'], 'texto': q['texto'], 'autor': q['autor'], 'titulo': q['titulo']}
        titulo = request.json['titulo']
        texto = request.json['texto']
        autor = request.json['autor']
        noticias.update_one(q, {"$set": {"titulo": titulo}, "$set": {"texto": texto}, "$set": {"autor": autor}})
    else:
        output = 'Não encontrado'

    return jsonify({'Notícia atualizada' : output})

# ENDPOINT E MÉTODO PARA BUSCAR NOTÍCIAS QUE CONTEM O PARAMETRO PASSADO NO ENDPOINT EM SEU CAMPO titulo
@app.route('/noticias/titulo/<titulo>', methods=['GET'])
def get_noticia_titulo(titulo):
    noticias = mongo.db.Noticias

    output = []

    for q in noticias.find({"titulo": {'$regex': titulo}}):
        output.append({'idnoticia': q['idnoticia'], 'texto': q['texto'], 'autor': q['autor'], 'titulo': q['titulo']})

    if len(output) == 0:
        output = 'Não encontrado'

    return jsonify({'resultado' : output})

# ENDPOINT E MÉTODO PARA BUSCAR NOTÍCIAS QUE CONTEM O PARAMETRO PASSADO NO ENDPOINT EM SEU CAMPO autor
@app.route('/noticias/autor/<autor>', methods=['GET'])
def get_noticia_autor(autor):
    noticias = mongo.db.Noticias

    output = []

    for q in noticias.find({"autor": {'$regex': autor}}):
        output.append({'idnoticia': q['idnoticia'], 'texto': q['texto'], 'autor': q['autor'], 'titulo': q['titulo']})

    if len(output) == 0:
        output = 'Não encontrado'

    return jsonify({'resultado' : output})

# ENDPOINT E MÉTODO PARA BUSCAR NOTÍCIAS QUE CONTEM O PARAMETRO PASSADO NO ENDPOINT EM SEU CAMPO texto
@app.route('/noticias/texto/<texto>', methods=['GET'])
def get_noticia_texto(texto):
    noticias = mongo.db.Noticias

    output = []

    for q in noticias.find({"texto": {'$regex': texto}}):
        output.append({'idnoticia': q['idnoticia'], 'texto': q['texto'], 'autor': q['autor'], 'titulo': q['titulo']})

    if len(output) == 0:
        output = 'Não encontrado'

    return jsonify({'resultado' : output})


if __name__ == '__main__':
    app.run(debug=True)
