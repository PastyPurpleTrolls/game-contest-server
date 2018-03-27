class HelpController < ApplicationController
  before_action :ensure_user_logged_in

  def index
  end

  # Show documentation markdown files in documentation/(category)/(filename)
  def show
    @category = params[:category]

    # Make sure the user is accessing a "page" and remove all non alphanumeric characters
    # If the user does not provide a page, look for a file with the same name as the category
    page = (params[:page] || @category).downcase.gsub(/[^a-z0-9]/, '')
    @filename = File.join(Rails.root, 'documentation', @category, page + '.md')

    unless File.exist?(@filename)
      raise ActionController::RoutingError.new('Not Found')
    end
  end
end
