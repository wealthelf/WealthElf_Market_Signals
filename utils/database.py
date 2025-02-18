import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

def get_db_connection():
    """Create a database connection using environment variables."""
    try:
        return psycopg2.connect(
            os.environ['DATABASE_URL'],
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")

def load_market_symbols():
    """Load all market symbols from the database."""
    conn = get_db_connection()
    try:
        query = "SELECT symbol, description FROM market_symbols ORDER BY symbol"
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

def import_market_symbols_from_file(file_path):
    """Import market symbols from a text file into the database."""
    conn = get_db_connection()
    try:
        with open(file_path, 'r') as f:
            cursor = conn.cursor()
            for line in f:
                if line.strip():
                    # Split on tab character and handle potential missing description
                    parts = line.strip().split('\t', 1)
                    symbol = parts[0]
                    description = parts[1] if len(parts) > 1 else ''
                    
                    # Use UPSERT to avoid duplicates
                    cursor.execute("""
                        INSERT INTO market_symbols (symbol, description)
                        VALUES (%s, %s)
                        ON CONFLICT (symbol) DO UPDATE 
                        SET description = EXCLUDED.description,
                            updated_at = CURRENT_TIMESTAMP
                    """, (symbol, description))
            
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error importing market symbols: {str(e)}")
    finally:
        conn.close()
