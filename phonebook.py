import psycopg2
import csv

#connect to database
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="phonebook",
        user="aishassoul",
        password=""
    )
    return conn

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name  VARCHAR(50),
            phone      VARCHAR(20) UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    print("\nAdd new contact:")
    first_name = input("first name: ").strip()
    last_name = input("last name : ").strip()
    phone = input("phone number: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)",
            (first_name, last_name if last_name != "" else None, phone)
        )
        conn.commit()
        print("contact added ")
    except Exception as e:
        print("error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_from_csv():
    print("\nLoad contacts from CSV file")
    path = input("enter file name (f.e phonebook.csv): ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                first_name = row["first_name"].strip()
                last_name = row.get("last_name", "").strip()
                phone = row["phone"].strip()

                try:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)",
                        (first_name, last_name if last_name != "" else None, phone)
                    )
                except:
                    conn.rollback()
                    print("phone already exists, skipping :", phone)

        conn.commit()
        print("CSV loaded.")
    except FileNotFoundError:
        print("file not found:", path)
    except Exception as e:
        print("error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()



def update_contact():
    print("\nUpdate contact:")
    old_phone = input("enter current phone number: ").strip()

    print("what do you want to change?")
    print("1) first name")
    print("2) phone number")
    choice = input("Choose 1 or 2: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_name = input("New first name: ").strip()
            cur.execute("UPDATE phonebook SET first_name=%s WHERE phone=%s",
                        (new_name, old_phone))
        elif choice == "2":
            new_phone = input("New phone number: ").strip()
            cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s",
                        (new_phone, old_phone))
        else:
            print("Wrong option.")
            return

        if cur.rowcount == 0:
            print("contact not found ")
        else:
            conn.commit()
            print("contact updated ")
    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# search contacts
def query_contacts():
    print("\nSearch contacts:")
    print("1) show all contacts")
    print("2) search by first name")
    print("3) search by phone")
    choice = input("choose option: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            cur.execute("SELECT * FROM phonebook ORDER BY id;")
        elif choice == "2":
            name = input("enter part of name ").strip()
            cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s ORDER BY id;",
                        (f"%{name}%",))
        elif choice == "3":
            ph = input("enter part of phone number  ").strip()
            cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY id;",
                        (f"%{ph}%",))
        else:
            print("Wrong option.")
            return

        rows = cur.fetchall()

        if not rows:
            print("No contacts found.")
        else:
            for row in rows:
                print("\nID:", row[0])
                print("First name:", row[1])
                print("Last name:", row[2])
                print("Phone:", row[3])

    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    print("\nDelete contact:")
    print("1) by first name")
    print("2) by phone")
    choice = input("choose: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("enter first name: ").strip()
            cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
        elif choice == "2":
            phone = input("enter phone number: ").strip()
            cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
        else:
            print("wrong option.")
            return

        if cur.rowcount == 0:
            print("nothing deleted")
        else:
            conn.commit()
            print("contact deleted.")

    except Exception as e:
        print("error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def main():
    create_table()

    while True:
        print("\nPhoneBook Menu")
        print("1) add contact")
        print("2) load from CSV")
        print("3) update contact")
        print("4) search contacts")
        print("5) delete contact")
        print("0) exit")

        option = input("choose: ").strip()

        if option == "1":
            insert_from_console()
        elif option == "2":
            insert_from_csv()
        elif option == "3":
            update_contact()
        elif option == "4":
            query_contacts()
        elif option == "5":
            delete_contact()
        elif option == "0":
            print("Bye ")
            break
        else:
            print("wrong menu option")

if __name__ == "__main__":
    main()
