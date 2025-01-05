/*
  # Создание системы обратной связи
  
  1. Новые таблицы
    - request_feedback (обратная связь по заявкам)
      - id (uuid, первичный ключ)
      - request_id (id заявки)
      - rating (оценка)
      - comment (комментарий)
      - created_by (кто создал)
      - created_at (дата создания)
  
  2. Безопасность
    - Включение RLS
    - Политики доступа для управления отзывами
*/

-- Создание таблицы обратной связи
CREATE TABLE IF NOT EXISTS request_feedback (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id uuid REFERENCES support_requests(id) ON DELETE CASCADE,
  rating integer NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment text,
  created_by uuid REFERENCES employees(id),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Создание индекса
CREATE INDEX IF NOT EXISTS idx_request_feedback_request_id 
ON request_feedback(request_id);

-- Включение RLS
ALTER TABLE request_feedback ENABLE ROW LEVEL SECURITY;

-- Создание политик
CREATE POLICY "Сотрудники могут оставлять отзывы о своих заявках"
  ON request_feedback
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM support_requests
      WHERE id = request_id
      AND employee_id = auth.uid()
    )
  );

CREATE POLICY "Сотрудники могут видеть отзывы о своих заявках"
  ON request_feedback
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM support_requests
      WHERE id = request_feedback.request_id
      AND employee_id = auth.uid()
    )
  );