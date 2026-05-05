import os
import sys
import time
import psycopg2

def wait_for_db():
    host     = os.environ.get("POSTGRES_HOST", "db")
    port     = os.environ.get("POSTGRES_PORT", "5432")
    db_name  = os.environ.get("POSTGRES_DB")
    user     = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")

    print("⏳ Waiting for database...")
    retries = 0

    while True:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=db_name,
                user=user,
                password=password,
            )
            conn.close()
            print(f"✅ Database is ready! (after {retries} retries)")
            break
        except psycopg2.OperationalError as e:
            retries += 1
            print(f"   DB not ready (attempt {retries}) — retrying in 2s... {e}")
            time.sleep(2)

        if retries >= 30:  # 60 seconds max wait
            print("❌ Could not connect to DB after 60 seconds. Exiting.")
            sys.exit(1)

if __name__ == "__main__":
    wait_for_db()