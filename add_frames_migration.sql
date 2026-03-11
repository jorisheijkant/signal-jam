-- Migration: Add frames table and link to posts
-- Run this in the Supabase SQL Editor

CREATE TABLE frames (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE posts ADD COLUMN frame_id INTEGER REFERENCES frames(id) ON DELETE SET NULL;

CREATE INDEX idx_posts_frame_id ON posts(frame_id);
