import subprocess
import pymysql

def export_postgres_schema(user, dbname, output_file):
    command = f"pg_dump -U {user} -d {dbname} --schema-only > {output_file}"
    subprocess.run(command, shell=True, check=True)

def modify_schema_for_mariadb(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Realiza modificaciones necesarias para compatibilidad con MariaDB
            line = line.replace('SERIAL', 'INT AUTO_INCREMENT')
            # Agrega más reemplazos según sea necesario

            outfile.write(line)

def import_schema_to_mariadb(user, password, dbname, input_file):
    connection = pymysql.connect(
        host='localhost',
        user=user,
        password=password,
        db=dbname
    )
    cursor = connection.cursor()
    
    with open(input_file, 'r') as infile:
        schema = infile.read()
    
    commands = schema.split(';')
    for command in commands:
        if command.strip():
            cursor.execute(command)
    
    connection.commit()
    cursor.close()
    connection.close()

def main():
    postgres_user = 'postgres'
    postgres_db = 'violetta'
    mariadb_user = 'root'
    mariadb_password = ''
    mariadb_db = 'violetta'
    postgres_schema_file = 'c:\\Soporte\\esquema_postgres.sql'
    mariadb_schema_file = 'c:\\Soporte\\esquema_mariadb.sql'

    # Exportar esquema de PostgreSQL
    export_postgres_schema(postgres_user, postgres_db, postgres_schema_file)
    print("Esquema exportado desde PostgreSQL.")

    # Modificar esquema para compatibilidad con MariaDB
    modify_schema_for_mariadb(postgres_schema_file, mariadb_schema_file)
    print("Esquema modificado para MariaDB.")

    # Crear base de datos en MariaDB (asumiendo que ya has creado la base de datos manualmente)
    # Importar esquema a MariaDB
    import_schema_to_mariadb(mariadb_user, mariadb_password, mariadb_db, mariadb_schema_file)
    print("Esquema importado en MariaDB.")

if __name__ == '__main__':
    main()