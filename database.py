# database.py

import mysql.connector

def connect(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

def create_pokemon_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team (
            pokemon_number VARCHAR(10) PRIMARY KEY,
            team_name VARCHAR(50) NOT NULL,
            pokemon_name VARCHAR(50) NOT NULL
        )
    """)
    connection.commit()

def save_pokemon_to_team(connection, team_name, pokemon_data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO team (pokemon_number, team_name, pokemon_name)
        VALUES (%s, %s, %s)
    """, (
        pokemon_data["number"],
        team_name,
        pokemon_data["name"]
    ))
    connection.commit()

def get_team_pokemon(connection, team_name):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT pokemon_number, pokemon_name
        FROM team
        WHERE team_name = %s
    """, (team_name,))
    team_pokemon = cursor.fetchall()
    return team_pokemon

def remove_pokemon_from_team(connection, team_name, pokemon_id):
    cursor = connection.cursor()

    delete_query = "DELETE FROM team WHERE team_name = %s AND (pokemon_number = %s OR pokemon_name = %s)"
    cursor.execute(delete_query, (team_name, pokemon_id, pokemon_id))

    connection.commit()
    cursor.close()
