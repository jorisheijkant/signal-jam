-- Signal Jam Database Schema

-- Platforms enum
CREATE TYPE platform AS ENUM ('twitter', 'tiktok', 'facebook');

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
    contains_misinformation BOOLEAN,
    notes TEXT,

    platform_data JSONB,

    UNIQUE(platform, url)
);

-- Indexes
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_posts_posted_at ON posts(posted_at);
CREATE INDEX idx_posts_account_id ON posts(account_id);
CREATE INDEX idx_posts_post_type ON posts(post_type);
CREATE INDEX idx_posts_is_checked ON posts(is_checked);
CREATE INDEX idx_accounts_platform ON accounts(platform);
