Rails.application.routes.draw do
  # Health check
  get '/health', to: 'health#index'

  namespace :api do
    namespace :v1 do
      # Main analytics endpoint
      post '/questions', to: 'questions#create'
      get '/questions/:id', to: 'questions#show'
      get '/questions', to: 'questions#index'

      # Shopify OAuth
      namespace :auth do
        get '/shopify', to: 'shopify#new'
        get '/shopify/callback', to: 'shopify#callback'
        delete '/shopify', to: 'shopify#destroy'
      end

      # Store management
      resources :stores, only: [:index, :show, :update] do
        member do
          get :status
          post :sync
        end
      end

      # Analytics endpoints
      namespace :analytics do
        get '/summary', to: 'summary#index'
        get '/trends', to: 'trends#index'
      end
    end
  end
end