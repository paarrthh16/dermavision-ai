import os
import json
from sqlalchemy import create_engine, text
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env vars
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/skincare.db")


class DatabaseClient:
    def __init__(self):
        self.use_supabase = bool(SUPABASE_URL and SUPABASE_KEY)
        if self.use_supabase:
            print("✅ Using Supabase Database")
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.engine = None
        else:
            print("⚠️ Supabase not configured, using SQLite fallback")
            self.supabase = None
            self.engine = create_engine(DATABASE_URL, echo=False, future=True)
            self._create_sqlite_tables()

    # ----------------- SQLite Fallback Setup -----------------
    def _create_sqlite_tables(self):
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT,
                    category TEXT,
                    skin_type TEXT,
                    concerns TEXT,
                    price REAL,
                    rating REAL,
                    description TEXT,
                    ingredients TEXT,
                    purchase_link TEXT,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    skin_type TEXT,
                    acne_severity REAL,
                    oiliness_level REAL,
                    skin_tone TEXT,
                    image_path TEXT,
                    confidence_scores TEXT, -- stored as JSON string
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))

    # ----------------- Product Methods -----------------
    def insert_product(self, product_data: dict):
        if self.use_supabase:
            return self.supabase.table("products").insert(product_data).execute()
        else:
            with self.engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO products 
                    (name, brand, category, skin_type, concerns, price, rating, description, ingredients, purchase_link, image_url)
                    VALUES (:name, :brand, :category, :skin_type, :concerns, :price, :rating, :description, :ingredients, :purchase_link, :image_url)
                """), product_data)

    def get_products(self, filters: dict = None):
        if self.use_supabase:
            query = self.supabase.table("products").select("*")
            if filters:
                for k, v in filters.items():
                    query = query.eq(k, v)
            return query.execute().data
        else:
            with self.engine.connect() as conn:
                query = "SELECT * FROM products"
                if filters:
                    conditions = " AND ".join([f"{k}='{v}'" for k, v in filters.items()])
                    query += f" WHERE {conditions}"
                result = conn.execute(text(query))
                return [dict(row) for row in result]
            


    def get_products_by_criteria(self, filters: dict):
        """
        Fetches products from the database based on a dictionary of filters.
        This is the more efficient, "production-like" method.
        """
        if self.use_supabase:
            query = self.supabase.table("products").select("*")

            # Apply filters directly to the Supabase query
            if 'max_budget' in filters:
                query = query.lte('price', filters['max_budget'])
            if 'min_rating' in filters:
                query = query.gte('rating', filters['min_rating'])
            if 'skin_type' in filters:
                # ilike is a case-insensitive "LIKE" for partial text matching
                query = query.ilike('skin_type', f"%{filters['skin_type']}%")
            if 'categories' in filters and filters['categories']:
                query = query.in_('category', filters['categories'])

            # For concerns, we need to build a more complex filter
            if 'concerns' in filters and filters['concerns']:
                # Example: "concerns.ilike.%Acne%,concerns.ilike.%Hydration%"
                concern_filters = [f"concerns.ilike.%{c}%" for c in filters['concerns']]
                query = query.or_(",".join(concern_filters))

            return query.execute().data

        else: # SQLite Fallback
            with self.engine.connect() as conn:
                base_query = "SELECT * FROM products"
                where_clauses = []
                params = {}

                if 'max_budget' in filters:
                    where_clauses.append("price <= :max_budget")
                    params['max_budget'] = filters['max_budget']
                if 'min_rating' in filters:
                    where_clauses.append("rating >= :min_rating")
                    params['min_rating'] = filters['min_rating']
                if 'skin_type' in filters:
                    where_clauses.append("skin_type LIKE :skin_type")
                    params['skin_type'] = f"%{filters['skin_type']}%"
                if 'categories' in filters and filters['categories']:
                    # Create placeholders for each category
                    cat_placeholders = ', '.join([f':cat{i}' for i in range(len(filters['categories']))])
                    where_clauses.append(f"category IN ({cat_placeholders})")
                    for i, cat in enumerate(filters['categories']):
                        params[f'cat{i}'] = cat

                if 'concerns' in filters and filters['concerns']:
                    concern_clauses = []
                    for i, concern in enumerate(filters['concerns']):
                        param_name = f'concern{i}'
                        concern_clauses.append(f"concerns LIKE :{param_name}")
                        params[param_name] = f"%{concern}%"
                    where_clauses.append(f"({ ' OR '.join(concern_clauses) })")

                if where_clauses:
                    query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
                else:
                    query = base_query

                result = conn.execute(text(query), params)
                return [dict(row._mapping) for row in result]

    # ----------------- User Progress Methods -----------------
    def insert_progress(self, progress_data: dict):
            if self.use_supabase:
                return self.supabase.table("user_progress").insert(progress_data).execute()
            else:
                # Convert confidence_scores dict to JSON string for SQLite
                if "confidence_scores" in progress_data and isinstance(progress_data["confidence_scores"], dict):
                    progress_data["confidence_scores"] = json.dumps(progress_data["confidence_scores"])

                with self.engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO user_progress 
                        (user_id, skin_type, acne_severity, oiliness_level, skin_tone, image_path, confidence_scores)
                        VALUES (:user_id, :skin_type, :acne_severity, :oiliness_level, :skin_tone, :image_path, :confidence_scores)
                    """), progress_data)

    def get_user_progress(self, user_id: str):
            if self.use_supabase:
                return (
                    self.supabase.table("user_progress")
                    .select("*")
                    .eq("user_id", user_id)
                    .order("timestamp")
                    .execute()
                    .data
                )
            else:
                with self.engine.connect() as conn:
                    result = conn.execute(
                        text("SELECT * FROM user_progress WHERE user_id = :user_id"), 
                        {"user_id": user_id}
                    )
                    
                    rows = []
                    for row in result:
                        row_dict = dict(row)
                        # Convert confidence_scores back to dict if JSON string
                        if row_dict.get("confidence_scores"):
                            try:
                                row_dict["confidence_scores"] = json.loads(row_dict["confidence_scores"])
                            except json.JSONDecodeError:
                                pass
                        rows.append(row_dict)
                    return rows
