-- Signal Jam Database Schema

-- Platforms enum
CREATE TYPE platform AS ENUM ('twitter', 'tiktok', 'facebook', 'instagram');

-- Post type: original, reply, retweet/share, quote
CREATE TYPE post_type AS ENUM ('original', 'reply', 'repost', 'quote');

-- Accounts table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    platform platform NOT NULL,
    username VARCHAR(255) NOT NULL,
    account_url TEXT,
    display_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(platform, username)
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    url TEXT,
    platform platform NOT NULL,
    account_id INTEGER NOT NULL REFERENCES accounts(id),

    content TEXT,
    post_type post_type NOT NULL DEFAULT 'original',
    parent_post_id INTEGER REFERENCES posts(id),

    posted_at TIMESTAMPTZ NOT NULL,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),

    likes INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,

    is_checked BOOLEAN DEFAULT FALSE,
    is_relevant BOOLEAN DEFAULT TRUE,
    contains_misinformation BOOLEAN,
    notes TEXT,

    platform_data JSONB,

    UNIQUE(platform, url)
);

-- Frames table (central misinformation themes)
CREATE TABLE frames (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add frame reference to posts
ALTER TABLE posts ADD COLUMN frame_id INTEGER REFERENCES frames(id) ON DELETE SET NULL;

-- Weekly summaries table
CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    week_start DATE NOT NULL UNIQUE,  -- always a Monday
    week_end DATE NOT NULL,           -- always the Sunday of that same week
    content TEXT NOT NULL,
    llm_provider VARCHAR(50),
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_posts_frame_id ON posts(frame_id);
CREATE INDEX idx_posts_posted_at ON posts(posted_at);
CREATE INDEX idx_posts_account_id ON posts(account_id);
CREATE INDEX idx_posts_post_type ON posts(post_type);
CREATE INDEX idx_posts_is_checked ON posts(is_checked);
CREATE INDEX idx_posts_is_relevant ON posts(is_relevant);
CREATE INDEX idx_accounts_platform ON accounts(platform);
