-- =====================================================================
-- SCHEMA DO BANCO DE DADOS (SUPABASE / POSTGRESQL)
-- Desafio Técnico Mobile - Catálogo & Avaliações
-- =====================================================================

-- 1. Tabela de Usuários (Alunos)
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabela de Obras (Catálogo)
CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  synopsis TEXT NOT NULL,
  category VARCHAR(80) NOT NULL,
  release_year INT NOT NULL,
  poster_url TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabela de Favoritos (Relação N:N)
CREATE TABLE IF NOT EXISTS favorites (
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, item_id)
);

-- 4. Tabela de Avaliações (Reviews)
CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  -- Garante 1 avaliação por aluno em cada obra (para permitir update no reteste)
  UNIQUE (user_id, item_id)
);

-- Índices para busca rápida, filtros e ordenação
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
CREATE INDEX IF NOT EXISTS idx_items_title ON items USING gin (to_tsvector('portuguese', title));
CREATE INDEX IF NOT EXISTS idx_reviews_item_id ON reviews(item_id);
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);

-- Permissões completas para a chave de API (service_role)
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO service_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON ROUTINES TO service_role;
