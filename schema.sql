-- ═══════════════════════════════════════════════════════════════════
-- ScoutPro U9-U10 Database Schema (Username + Password Auth)
-- Run in Supabase SQL Editor
-- ═══════════════════════════════════════════════════════════════════

-- 1. PROFILES
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('coach', 'parent')),
  region TEXT DEFAULT '',
  phone TEXT DEFAULT '',
  email TEXT DEFAULT '',
  organization TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. PLAYERS
CREATE TABLE IF NOT EXISTS players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  birth_date DATE,
  age_group TEXT NOT NULL CHECK (age_group IN ('U9', 'U10')),
  preferred_foot TEXT DEFAULT '右脚' CHECK (preferred_foot IN ('右脚', '左脚', '双脚')),
  position TEXT DEFAULT '多位置轮换',
  created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
  organization TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. EVALUATIONS
CREATE TABLE IF NOT EXISTS evaluations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  evaluator_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  eval_date DATE NOT NULL DEFAULT CURRENT_DATE,
  score_tech NUMERIC(3,2) DEFAULT 0,
  score_tactical NUMERIC(3,2) DEFAULT 0,
  score_physical NUMERIC(3,2) DEFAULT 0,
  score_mental NUMERIC(3,2) DEFAULT 0,
  score_social NUMERIC(3,2) DEFAULT 0,
  score_passion NUMERIC(3,2) DEFAULT 0,
  total_score NUMERIC(3,2) DEFAULT 0,
  item_scores JSONB NOT NULL DEFAULT '{}',
  pos_back TEXT DEFAULT '',
  pos_mid TEXT DEFAULT '',
  pos_front TEXT DEFAULT '',
  strengths TEXT DEFAULT '',
  dev_areas TEXT DEFAULT '',
  action_plan TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. INDEXES
CREATE INDEX IF NOT EXISTS idx_eval_player ON evaluations(player_id);
CREATE INDEX IF NOT EXISTS idx_eval_evaluator ON evaluations(evaluator_id);
CREATE INDEX IF NOT EXISTS idx_eval_date ON evaluations(eval_date DESC);
CREATE INDEX IF NOT EXISTS idx_players_by ON players(created_by);

-- 5. RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "profiles_read" ON profiles FOR SELECT USING (true);
CREATE POLICY "profiles_ins" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_upd" ON profiles FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "players_read" ON players FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "players_ins" ON players FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "players_upd" ON players FOR UPDATE USING (
  created_by = auth.uid() OR EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'coach')
);

CREATE POLICY "eval_read" ON evaluations FOR SELECT USING (
  EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'coach')
  OR EXISTS (SELECT 1 FROM players WHERE players.id = evaluations.player_id AND players.created_by = auth.uid())
  OR evaluator_id = auth.uid()
);
CREATE POLICY "eval_ins" ON evaluations FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "eval_upd" ON evaluations FOR UPDATE USING (evaluator_id = auth.uid());
CREATE POLICY "eval_del" ON evaluations FOR DELETE USING (evaluator_id = auth.uid());

-- 6. TRIGGERS
CREATE OR REPLACE FUNCTION update_updated_at() RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_profiles_upd BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_players_upd BEFORE UPDATE ON players FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- 7. AUTO-CREATE PROFILE ON SIGNUP
CREATE OR REPLACE FUNCTION handle_new_user() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, username, name, role, region, phone, email, organization)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'name', ''),
    COALESCE(NEW.raw_user_meta_data->>'role', 'coach'),
    COALESCE(NEW.raw_user_meta_data->>'region', ''),
    COALESCE(NEW.raw_user_meta_data->>'phone', ''),
    COALESCE(NEW.raw_user_meta_data->>'email', ''),
    COALESCE(NEW.raw_user_meta_data->>'organization', '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
