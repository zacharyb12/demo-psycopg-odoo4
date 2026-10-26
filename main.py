from repository.users_repository import get_all_users,get_user_by_id,create_user,update_user,delete_user
from db.db import get_connection

if __name__ == "__main__":
    continue_app = True
    
    with get_connection() as conn:
        while continue_app:
            print("menu")
            print("1 liste des users")
            print("2 user by id")
            print("3 create user")
            print("4 update user")
            print("5 delete user")
            print("6 Quit")
            choice = input("Entrez votre choix")
            
            match choice:
                case "1":
                    for v in get_all_users(conn):
                        print(v)
                case "2":
                    id = input("Entrez l'id de l'utilisateur")
                    user = get_user_by_id(conn,id)
                    print(user)
                case "3":
                    email = input("Entrez l'email")
                    lastname = input("Entrez le last_name")
                    role = input("Entrez le role")
                    id = create_user(conn,email,lastname,role)
                    print(f"L'utilisateur à bien été crée avec l'id {id}")
                case "4":
                    id = input("Entrez l'id de l'utilisateur")
                    email = input("Entrez l'email")
                    lastname = input("Entrez le last_name")
                    count = update_user(conn,email,lastname,id)
                    print(f"{count} lignes ont été modifié")
                case "5":
                    id = input("Entrez l'id de l'utilisateur à supprimer")
                    count = delete_user(conn,id)
                    print(f"{count} lignes ont été modifié")
                case "6":
                    print("Merci à bientot")
                    continue_app = False
                    