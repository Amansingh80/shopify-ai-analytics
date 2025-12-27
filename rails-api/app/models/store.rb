class Store < ApplicationRecord
  has_many :questions, dependent: :destroy

  validates :shopify_domain, presence: true, uniqueness: true
  validates :access_token, presence: true

  encrypts :access_token

  scope :active, -> { where(active: true) }

  def active?
    active && access_token.present?
  end

  def shopify_session
    ShopifyAPI::Auth::Session.new(
      shop: shopify_domain,
      access_token: access_token
    )
  end
end