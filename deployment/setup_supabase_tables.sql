-- setup_supabase_tables.sql
-- Run these commands in your Supabase SQL Editor

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    skin_type TEXT,
    concerns TEXT,
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    description TEXT,
    ingredients TEXT,
    purchase_link TEXT,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    skin_type TEXT,
    acne_severity DECIMAL(5,3),
    oiliness_level DECIMAL(5,3),
    skin_tone TEXT,
    image_path TEXT,
    confidence_scores JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_skin_type ON products(skin_type);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_timestamp ON user_progress(timestamp);

-- Enable Row Level Security (RLS)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access to products
CREATE POLICY "Allow public read access to products" ON products
    FOR SELECT USING (true);

-- Create policies for user progress (users can only access their own data)
CREATE POLICY "Users can view own progress" ON user_progress
    FOR SELECT USING (true); -- For demo purposes, allow all reads

CREATE POLICY "Users can insert own progress" ON user_progress
    FOR INSERT WITH CHECK (true); -- For demo purposes, allow all inserts