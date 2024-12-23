/*
  # Система приоритетов заявок

  1. Новые таблицы
    - `request_priorities`
      - `id` (uuid, primary key)
      - `name` (text, unique)
      - `description` (text)
      - `color` (text)
      - `sla_hours` (integer)
      - `created_at` (timestamptz)

  2. Безопасность
    - Включение RLS
    - Политики для чтения и управления
*/

DO $$ BEGIN
  -- Создание таблицы приоритетов, если она не существует
  CREATE TABLE IF NOT EXISTS request_priorities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL UNIQUE,
    description text,
    color text NOT NULL,
    sla_hours integer NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
  );

  -- Включение RLS
  ALTER TABLE request_priorities ENABLE ROW LEVEL SECURITY;

  -- Безопасное создание политик с проверкой существования
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'request_priorities' 
    AND policyname = 'Все могут просматривать приоритеты'
  ) THEN
    CREATE POLICY "Все могут просматривать приоритеты"
      ON request_priorities
      FOR SELECT
      TO authenticated
      USING (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE tablename = 'request_priorities' 
    AND policyname = 'Только администраторы могут управлять приоритетами'
  ) THEN
    CREATE POLICY "Только администраторы могут управлять приоритетами"
      ON request_priorities
      FOR ALL
      TO authenticated
      USING (auth.jwt() ->> 'role' = 'admin');
  END IF;
END $$;