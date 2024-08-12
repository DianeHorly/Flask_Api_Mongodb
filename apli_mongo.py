from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
import logging

# Créer une instance de Flask
app = Flask(__name__)

# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG)

# Nom de la base de données
database_name = "APLI"
# URI de connexion à la base de données MongoDB
DB_URI = f"mongodb://localhost:27017/{database_name}"

# Configurer Flask pour utiliser MongoDB
app.config["MONGODB_SETTINGS"] = {
    "db": database_name,
    "host": DB_URI
}

# Initialiser MongoEngine
db = MongoEngine()
db.init_app(app)

# Définir le modèle Book pour MongoDB
class Book(db.Document):
    book_id = db.IntField(required=True, unique=True)
    nom = db.StringField(required=True)
    auteur = db.StringField(required=True)

    def convert_to_json(self):
        return {
            "book_id": self.book_id,
            "nom": self.nom,
            "auteur": self.auteur
        }

# Route pour peupler la base de données avec des livres initiaux
@app.route('/APLI/db_Insertion', methods=['POST'])
def db_Insertion():
    try:
        # Ajouter des livres initiaux
        book1 = Book(book_id=1, nom="A Game of Thrones", auteur="George R. R Martin")
        book2 = Book(book_id=2, nom="Lord of the Rings", auteur="J. R. R. Tolkien")
        book3 = Book(book_id=3, nom="Dead Man", auteur="Jim Jarmush")
        book4 = Book(book_id=4, nom="Melancholia", auteur="Lars von Trier")

        # Sauvegarder les livres dans la base de données
        book1.save()
        logging.info("Book1 saved")
        book2.save()
        logging.info("Book2 saved")
        book3.save()
        logging.info("Book3 saved")
        book4.save()
        logging.info("Book4 saved")

        return make_response(jsonify({"message": "Données inserées dans la base de données avec succès"}), 201)
    except Exception as e:
        logging.error("Erreur d'insertion des données dans la database: %s", str(e))
        return make_response(jsonify({"error": str(e)}), 500)

# Route pour gérer tous les livres
@app.route('/APLI/books', methods=['GET', 'POST'])
def books_app():
    if request.method == 'GET':
        # Récupérer tous les livres de la base de données
        books = Book.objects()
        return make_response(jsonify([book.convert_to_json() for book in books]), 200)
    elif request.method == 'POST':
        # Ajouter un nouveau livre
        content = request.json
        if Book.objects(book_id=content['book_id']).first():
            return make_response(jsonify({"error": "Ce livre existe dejà"}), 400)
        new_book = Book(book_id=content['book_id'], nom=content['nom'], auteur=content['auteur'])
        new_book.save()
        return make_response(jsonify(new_book.convert_to_json()), 201)

# Route pour gérer un livre spécifique par son ID
@app.route('/APLI/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def each_book(book_id):
    book = Book.objects(book_id=book_id).first()
    if request.method == 'GET':
        if book:
            return make_response(jsonify(book.convert_to_json()), 200)
        else:
            return make_response(jsonify({"error": "Livre introuvable"}), 404)
    elif request.method == 'PUT':
        if book:
            content = request.json
            book.update(nom=content['nom'], auteur=content['auteur'])
            updated_book = Book.objects(book_id=book_id).first()
            return make_response(jsonify(updated_book.convert_to_json()), 200)
        else:
            return make_response(jsonify({"error": "Livre introvable"}), 404)
    elif request.method == 'DELETE':
        if book:
            book.delete()
            return make_response(jsonify({"message": "Livre eliminer avec succès"}), 204)
        else:
            return make_response(jsonify({"error": "Livre introuvable"}), 404)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
