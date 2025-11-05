#!/usr/bin/env python3

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    """Seed the database with sample users and holdings data."""

    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'thejase'),
        'password': os.getenv('DB_PASSWORD', 'thejas123'),
        'database': os.getenv('DB_NAME', 'investment_holdings')
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        print(f"Connected to database: {db_params['database']}")

        # Hash passwords for sample users (keep them short for bcrypt)
        john_password = pwd_context.hash("pass")
        jane_password = pwd_context.hash("theja")

        # Insert sample users
        users_sql = """
        INSERT INTO users (email, password_hash, first_name, last_name) VALUES
        ('thejas@gmail.com', %s, 'Thejas', 'Elandassery'),
        ('jane.smith@example.com', %s, 'Jane', 'Smith')
        ON CONFLICT (email) DO NOTHING;
        """

        cur.execute(users_sql, (john_password, jane_password))
        print("Sample users inserted!")

        # Get user IDs
        cur.execute("SELECT id FROM users WHERE email = 'thejas@gmail.com';")
        john_id = cur.fetchone()[0]

        cur.execute("SELECT id FROM users WHERE email = 'jane.smith@example.com';")
        jane_id = cur.fetchone()[0]

        # Get asset IDs
        cur.execute("SELECT id FROM assets WHERE symbol = 'AAPL';")
        aapl_id = cur.fetchone()[0]

        cur.execute("SELECT id FROM assets WHERE symbol = 'GOOGL';")
        googl_id = cur.fetchone()[0]

        cur.execute("SELECT id FROM assets WHERE symbol = 'BTC';")
        btc_id = cur.fetchone()[0]

        cur.execute("SELECT id FROM assets WHERE symbol = 'VTSAX';")
        vtsax_id = cur.fetchone()[0]

        # Insert sample holdings
        holdings_sql = """
        INSERT INTO holdings (user_id, asset_id, quantity, purchase_price, purchase_date) VALUES
        (%s, %s, 10.0, 140.00, '2023-01-15'),
        (%s, %s, 1.0, 30000.00, '2023-02-20'),
        (%s, %s, 5.0, 2700.00, '2023-01-10'),
        (%s, %s, 50.0, 105.00, '2023-03-05')
        ON CONFLICT (user_id, asset_id) DO NOTHING;
        """

        cur.execute(holdings_sql, (
            john_id, aapl_id,    
            john_id, btc_id,    
            jane_id, googl_id,   
            jane_id, vtsax_id    
        ))
        print("Sample holdings inserted!")

        print("\n📊 Sample Data Summary:")
        print("Users:")
        print("- thejas@gmail.com (password: pass123)")
        print("- jane.smith@example.com (password: pass456)")
        print("\nHoldings:")
        print("- Thejas: 10 AAPL shares, 1 BTC")
        print("- Jane: 5 GOOGL shares, 50 VTSAX shares")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Failed: Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed: Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Seeding database with sample data...")
    seed_database()
    print("Database seeding complete!")