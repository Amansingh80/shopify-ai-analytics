module Api
  module V1
    class QuestionsController < ApplicationController
      before_action :validate_store, only: [:create]
      before_action :set_question, only: [:show]

      # POST /api/v1/questions
      def create
        question = Question.create!(
          store_id: question_params[:store_id],
          question_text: question_params[:question],
          status: 'processing'
        )

        # Forward to Python AI service
        result = PythonAgentService.new(question).process

        question.update!(
          answer: result[:answer],
          confidence: result[:confidence],
          query_used: result[:query_used],
          data_points: result[:data_points],
          status: 'completed',
          processing_time_ms: result[:processing_time_ms]
        )

        render json: QuestionSerializer.new(question).serializable_hash, status: :created
      rescue StandardError => e
        question&.update(status: 'failed', error_message: e.message)
        render json: { error: e.message }, status: :unprocessable_entity
      end

      # GET /api/v1/questions/:id
      def show
        render json: QuestionSerializer.new(@question).serializable_hash
      end

      # GET /api/v1/questions
      def index
        questions = Question.where(store_id: params[:store_id])
                           .order(created_at: :desc)
                           .page(params[:page])
                           .per(params[:per_page] || 20)

        render json: QuestionSerializer.new(questions).serializable_hash
      end

      private

      def question_params
        params.require(:question).permit(:store_id, :question)
      end

      def validate_store
        store = Store.find_by(shopify_domain: question_params[:store_id])
        
        unless store&.active?
          render json: { error: 'Store not found or inactive' }, status: :not_found
        end
      end

      def set_question
        @question = Question.find(params[:id])
      rescue ActiveRecord::RecordNotFound
        render json: { error: 'Question not found' }, status: :not_found
      end
    end
  end
end