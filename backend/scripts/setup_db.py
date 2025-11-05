#!/usr/bin/env python3

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_tables():
    """Create the database tables for the investment holdings app."""

    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'thejase'),
        'password': os.getenv('DB_PASSWORD', 'thejas123'),
        'database': os.getenv('DB_NAME', 'investment_holdings')
    }

    # SQL to create tables
    create_tables_sql = """
    -- Create users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create assets table
    CREATE TABLE IF NOT EXISTS assets (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(20) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        asset_type VARCHAR(50) NOT NULL,
        current_price DECIMAL(15, 4) NOT NULL,
        currency VARCHAR(3) DEFAULT 'USD',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create holdings table
    CREATE TABLE IF NOT EXISTS holdings (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        asset_id INTEGER NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
        quantity DECIMAL(15, 8) NOT NULL,
        purchase_price DECIMAL(15, 4) NOT NULL,
        purchase_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, asset_id)
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_holdings_user_id ON holdings(user_id);
    CREATE INDEX IF NOT EXISTS idx_holdings_asset_id ON holdings(asset_id);
    CREATE INDEX IF NOT EXISTS idx_assets_symbol ON assets(symbol);
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        print(f"Connected to database: {db_params['database']}")

        # Execute table creation
        cur.execute(create_tables_sql)
        print("Database tables created successfully!")

        # Insert sample assets
        sample_assets_sql = """
        INSERT INTO assets (symbol, name, asset_type, current_price) VALUES
        ('AAPL', 'Apple Inc.', 'stock', 150.00),
        ('GOOGL', 'Alphabet Inc.', 'stock', 2800.00),
        ('BTC', 'Bitcoin', 'crypto', 35000.00),
        ('VTSAX', 'Vanguard Total Stock Market ETF', 'etf', 110.00)
        ON CONFLICT (symbol) DO NOTHING;
        """

        cur.execute(sample_assets_sql)
        print("Sample assets inserted!")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Failed: Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed: Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Setting up database tables...")
    create_database_tables()
    print("Database setup complete!")