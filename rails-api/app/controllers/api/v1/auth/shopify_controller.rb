module Api
  module V1
    module Auth
      class ShopifyController < ApplicationController
        # GET /api/v1/auth/shopify
        def new
          shop = params[:shop]
          
          unless shop.present?
            return render json: { error: 'Shop parameter required' }, status: :bad_request
          end

          auth_url = ShopifyAPI::Auth::Oauth.begin_auth(
            shop: shop,
            redirect_path: auth_shopify_callback_url,
            is_online: false
          )

          render json: { auth_url: auth_url }
        end

        # GET /api/v1/auth/shopify/callback
        def callback
          begin
            auth_result = ShopifyAPI::Auth::Oauth.validate_auth_callback(
              cookies: cookies.to_hash,
              auth_query: request.query_parameters
            )

            session = auth_result[:session]
            
            store = Store.find_or_initialize_by(shopify_domain: session.shop)
            store.update!(
              access_token: session.access_token,
              scope: session.scope.to_s,
              active: true,
              api_version: ShopifyAPI::Context.api_version
            )

            render json: {
              message: 'Authentication successful',
              store: {
                id: store.id,
                domain: store.shopify_domain
              }
            }
          rescue ShopifyAPI::Errors::InvalidOAuthError => e
            render json: { error: 'Invalid OAuth request' }, status: :unauthorized
          rescue StandardError => e
            Rails.logger.error("Shopify auth error: #{e.message}")
            render json: { error: 'Authentication failed' }, status: :internal_server_error
          end
        end

        # DELETE /api/v1/auth/shopify
        def destroy
          store = Store.find_by(shopify_domain: params[:shop])
          
          if store
            store.update(active: false)
            render json: { message: 'Store disconnected successfully' }
          else
            render json: { error: 'Store not found' }, status: :not_found
          end
        end
      end
    end
  end
end