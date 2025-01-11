import json
import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "pet_adoption"
}

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Handler for the HTTP server
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/pets"):
            self.handle_get_pets()
        elif self.path.startswith("/adopters"):
            self.handle_get_adopters()
        elif self.path.startswith("/adoptions"):
            self.handle_get_adoptions()
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        if self.path.startswith("/pets"):
            self.handle_create_pet()
        elif self.path.startswith("/adopters"):
            self.handle_create_adopter()
        elif self.path.startswith("/adoptions"):
            self.handle_create_adoption()
        else:
            self.send_error(404, "Endpoint not found")

    def do_PUT(self):
        if self.path.startswith("/adoptions"):
            self.handle_update_adoption()
        else:
            self.send_error(404, "Endpoint not found")

    def do_DELETE(self):
        if self.path.startswith("/pets"):
            self.handle_delete_pet()
        elif self.path.startswith("/adopters"):
            self.handle_delete_adopter()
        elif self.path.startswith("/adoptions"):
            self.handle_delete_adoption()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_get_pets(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pets")
        pets = cursor.fetchall()
        cursor.close()
        connection.close()
        self.send_json_response(200, pets)

    def handle_get_adopters(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Adopters")
        adopters = cursor.fetchall()
        cursor.close()
        connection.close()
        self.send_json_response(200, adopters)

    def handle_get_adoptions(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT A.AdoptionID, P.Name AS PetName, AD.FullName AS AdopterName, A.AdoptionDate, A.Status
            FROM Adoptions A
            JOIN Pets P ON A.PetID = P.PetID
            JOIN Adopters AD ON A.AdopterID = AD.AdopterID
        """)
        adoptions = cursor.fetchall()
        cursor.close()
        connection.close()
        self.send_json_response(200, adoptions)

    def handle_create_pet(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Pets (PetID, Name, Species, Breed, Age, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (post_data["PetID"], post_data["Name"], post_data["Species"], post_data["Breed"], post_data["Age"], post_data["Status"]))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(201, {"message": "Pet created successfully"})

    def handle_create_adopter(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Adopters (AdopterID, FullName, ContactInfo, Address)
            VALUES (%s, %s, %s, %s)
        """, (post_data["AdopterID"], post_data["FullName"], post_data["ContactInfo"], post_data["Address"]))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(201, {"message": "Adopter created successfully"})

    def handle_create_adoption(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Adoptions (AdoptionID, PetID, AdopterID, AdoptionDate, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (post_data["AdoptionID"], post_data["PetID"], post_data["AdopterID"], post_data["AdoptionDate"], post_data["Status"]))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(201, {"message": "Adoption created successfully"})

    def handle_update_adoption(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Adoptions
            SET Status = %s
            WHERE AdoptionID = %s
        """, (post_data["Status"], post_data["AdoptionID"]))
        connection.commit()

        if post_data["Status"] == "Completed":
            cursor.execute("""
                UPDATE Pets
                SET Status = 'Adopted'
                WHERE PetID = (SELECT PetID FROM Adoptions WHERE AdoptionID = %s)
            """, (post_data["AdoptionID"],))
            connection.commit()

        cursor.close()
        connection.close()
        self.send_json_response(200, {"message": "Adoption updated successfully"})

    def handle_delete_pet(self):
        pet_id = self.path.split("/")[-1]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Pets WHERE PetID = %s", (pet_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(200, {"message": "Pet deleted successfully"})

    def handle_delete_adopter(self):
        adopter_id = self.path.split("/")[-1]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Adopters WHERE AdopterID = %s", (adopter_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(200, {"message": "Adopter deleted successfully"})

    def handle_delete_adoption(self):
        adoption_id = self.path.split("/")[-1]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Adoptions WHERE AdoptionID = %s", (adoption_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.send_json_response(200, {"message": "Adoption deleted successfully"})

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

# Start the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()