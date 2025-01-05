/*
  # Добавление системы категорий заявок

  1. Новые таблицы
    - `request_categories`
      - `id` (uuid, primary key)
      - `name` (text, unique)
      - `description` (text)
      - `is_active` (boolean)
      - `created_at` (timestamp)
  
  2. Безопасность
    - Включение RLS на таблице request_categories
    - Политика для чтения всеми авторизованными пользователями
    - Политика для управления только администраторами
*/

DO $$ BEGIN
  -- Проверяем существование таблицы перед созданием
  IF NOT EXISTS (
    SELECT FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename = 'request_categories'
  ) THEN
    -- Создание таблицы категорий
    CREATE TABLE request_categories (
      id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
      name text NOT NULL UNIQUE,
      description text,
      is_active boolean DEFAULT true,
      created_at timestamptz NOT NULL DEFAULT now()
    );

    -- Включение RLS
    ALTER TABLE request_categories ENABLE ROW LEVEL SECURITY;

    -- Создание политик
    CREATE POLICY "Все могут просматривать категории"
      ON request_categories
      FOR SELECT
      TO authenticated
      USING (true);

    CREATE POLICY "Только администраторы могут управлять категориями"
      ON request_categories
      FOR ALL
      TO authenticated
      USING (auth.jwt() ->> 'role' = 'admin');
  END IF;
END $$;