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
    is_watched BOOLEAN NOT NULL DEFAULT FALSE,   -- on the scrape list, managed from the dashboard (Supabase: see supabase_account_policies.sql)
    is_approved BOOLEAN NOT NULL DEFAULT FALSE,  -- kept in sync by trigger: 3+ posts with contains_misinformation
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(platform, username)
);

-- Term kind: 'search' terms are scraped per platform, 'filter' terms flag posts as relevant for the theme
CREATE TYPE term_kind AS ENUM ('search', 'filter');

-- Search and filter terms per platform, managed from the dashboard (Supabase: see supabase_term_policies.sql)
CREATE TABLE scrape_terms (
    id SERIAL PRIMARY KEY,
    platform platform NOT NULL,
    kind term_kind NOT NULL,
    term TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(platform, kind, term)
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
    relevant_for_signal_jam_theme BOOLEAN NOT NULL DEFAULT FALSE,  -- post matches the theme filter terms
    contains_misinformation BOOLEAN,
    notes TEXT,

    platform_data JSONB,

    UNIQUE(platform, url)
);

-- An account is approved once it has the required number of posts labeled as misinformation
CREATE FUNCTION refresh_account_approval() RETURNS TRIGGER AS $$
BEGIN
    UPDATE accounts
    SET is_approved = (
        SELECT COUNT(*) >= 3 FROM posts
        WHERE account_id = NEW.account_id AND contains_misinformation IS TRUE
    )
    WHERE id = NEW.account_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

CREATE TRIGGER trg_refresh_account_approval
AFTER INSERT OR UPDATE OF contains_misinformation ON posts
FOR EACH ROW EXECUTE FUNCTION refresh_account_approval();

-- Who reposted a post, and when (plain retweets/shares — no own content, so no own label).
-- Quote posts still get their own row in `posts` (post_type = 'quote') since they add commentary.
CREATE TABLE post_reposts (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    reposted_at TIMESTAMPTZ NOT NULL,
    url TEXT,

    UNIQUE(post_id, account_id)
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
    propaganda_channels_content TEXT,  -- summary of Russian propaganda channel coverage, generated from articles
    llm_provider VARCHAR(50),
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Articles table (Russian state media and propaganda sites)
CREATE TABLE articles (
    url          TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    source       TEXT NOT NULL,
    author       TEXT,
    language     VARCHAR(10),
    summary      TEXT,
    content      TEXT,
    published_at TIMESTAMPTZ NOT NULL,
    scraped_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Supabase: enable row level security and let the dashboard read articles with the publishable key.
-- ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Public read access" ON articles FOR SELECT USING (true);

-- Indexes
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_posts_frame_id ON posts(frame_id);
CREATE INDEX idx_posts_posted_at ON posts(posted_at);
CREATE INDEX idx_posts_account_id ON posts(account_id);
CREATE INDEX idx_posts_post_type ON posts(post_type);
CREATE INDEX idx_posts_is_checked ON posts(is_checked);
CREATE INDEX idx_posts_is_relevant ON posts(is_relevant);
CREATE INDEX idx_posts_relevant_for_signal_jam_theme ON posts(relevant_for_signal_jam_theme);
CREATE INDEX idx_accounts_is_approved ON accounts(is_approved);
CREATE INDEX idx_accounts_platform ON accounts(platform);
CREATE INDEX idx_post_reposts_post_id ON post_reposts(post_id);
CREATE INDEX idx_post_reposts_account_id ON post_reposts(account_id);
CREATE INDEX idx_articles_published_at ON articles(published_at);
CREATE INDEX idx_articles_source ON articles(source);

-- Watched accounts that still need labeling: not approved yet, with unreviewed theme posts,
-- and enough own posts (confirmed + unreviewed) to reach the 3 needed for approval.
CREATE VIEW account_review_queue AS
SELECT *
FROM (
    SELECT
        a.id AS account_id,
        a.platform,
        a.username,
        a.account_url,
        a.display_name,
        COUNT(p.id) FILTER (WHERE p.contains_misinformation IS TRUE) AS confirmed_count,
        COUNT(p.id) FILTER (
            WHERE p.is_checked IS FALSE
              AND p.is_relevant
              AND p.relevant_for_signal_jam_theme
              AND p.post_type <> 'repost'
        ) AS unreviewed_count
    FROM accounts a
    JOIN posts p ON p.account_id = a.id
    WHERE a.is_watched AND NOT a.is_approved
    GROUP BY a.id
) counts
WHERE unreviewed_count > 0 AND confirmed_count + unreviewed_count >= 3;
