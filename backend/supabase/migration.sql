-- FlashMind AI — Supabase schema
-- Run this in Supabase > SQL Editor once. It is idempotent (safe to re-run).

-- ============ PROFILES ============
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  name text not null default 'Learner',
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ============ DECKS (cards stored as JSONB) ============
create table if not exists public.decks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  title text not null,
  description text not null default '',
  subject text not null default 'General',
  progress int not null default 0,
  color text not null default 'from-indigo-400 to-cyan-400',
  cards jsonb not null default '[]'::jsonb,
  updated text not null default 'Just now',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists decks_user_id_idx on public.decks (user_id);

-- ============ SAVED QUIZ FOLDERS ============
create table if not exists public.saved_quizzes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  title text not null default 'Untitled quiz',
  questions jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists saved_quizzes_user_id_idx on public.saved_quizzes (user_id);

-- ============ STUDY REVIEWS ============
create table if not exists public.study_reviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  deck_id uuid,
  flashcard_id bigint not null,
  rating text not null check (rating in ('again', 'hard', 'good', 'easy')),
  response_time_seconds int,
  reviewed_at timestamptz not null default now(),
  ease_factor float8 not null default 2.5,
  interval int not null default 1,
  repetitions int not null default 0,
  next_review_date text not null default ''
);

create index if not exists study_reviews_user_id_idx on public.study_reviews (user_id);
create index if not exists study_reviews_reviewed_at_idx on public.study_reviews (reviewed_at);

-- ============ ROW LEVEL SECURITY ============
alter table public.profiles enable row level security;
alter table public.decks enable row level security;
alter table public.saved_quizzes enable row level security;
alter table public.study_reviews enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own" on public.profiles for select using (auth.uid() = id);
drop policy if exists "profiles_all_own" on public.profiles;
create policy "profiles_all_own" on public.profiles for all using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "decks_select_own" on public.decks;
create policy "decks_select_own" on public.decks for select using (auth.uid() = user_id);
drop policy if exists "decks_insert_own" on public.decks;
create policy "decks_insert_own" on public.decks for insert with check (auth.uid() = user_id);
drop policy if exists "decks_update_own" on public.decks;
create policy "decks_update_own" on public.decks for update using (auth.uid() = user_id);
drop policy if exists "decks_delete_own" on public.decks;
create policy "decks_delete_own" on public.decks for delete using (auth.uid() = user_id);

drop policy if exists "saved_quizzes_select_own" on public.saved_quizzes;
create policy "saved_quizzes_select_own" on public.saved_quizzes for select using (auth.uid() = user_id);
drop policy if exists "saved_quizzes_insert_own" on public.saved_quizzes;
create policy "saved_quizzes_insert_own" on public.saved_quizzes for insert with check (auth.uid() = user_id);
drop policy if exists "saved_quizzes_update_own" on public.saved_quizzes;
create policy "saved_quizzes_update_own" on public.saved_quizzes for update using (auth.uid() = user_id);
drop policy if exists "saved_quizzes_delete_own" on public.saved_quizzes;
create policy "saved_quizzes_delete_own" on public.saved_quizzes for delete using (auth.uid() = user_id);

drop policy if exists "study_reviews_select_own" on public.study_reviews;
create policy "study_reviews_select_own" on public.study_reviews for select using (auth.uid() = user_id);
drop policy if exists "study_reviews_insert_own" on public.study_reviews;
create policy "study_reviews_insert_own" on public.study_reviews for insert with check (auth.uid() = user_id);
drop policy if exists "study_reviews_delete_own" on public.study_reviews;
create policy "study_reviews_delete_own" on public.study_reviews for delete using (auth.uid() = user_id);