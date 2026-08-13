-- Optional Supabase logging for Trustity LLM preview
-- Apply in a Supabase project when credentials are available.

create table if not exists public.llm_ask_events (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  question text not null,
  mode text,
  source_count int,
  user_agent text,
  ip_hash text
);

alter table public.llm_ask_events enable row level security;

-- service-role inserts only; no public read
create policy "service role full access"
  on public.llm_ask_events
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');
