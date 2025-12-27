class Question < ApplicationRecord
  belongs_to :store

  validates :question_text, presence: true
  validates :store_id, presence: true
  validates :status, inclusion: { in: %w[pending processing completed failed] }

  enum status: {
    pending: 'pending',
    processing: 'processing',
    completed: 'completed',
    failed: 'failed'
  }

  scope :recent, -> { order(created_at: :desc) }
  scope :completed, -> { where(status: 'completed') }
  scope :failed, -> { where(status: 'failed') }

  def processing?
    status == 'processing'
  end

  def completed?
    status == 'completed'
  end
end