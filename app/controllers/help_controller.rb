class HelpController < ApplicationController
    before_action :ensure_user_logged_in
   
    def show
        @category = params[:category]
        @page = (params[:page] || "index").downcase.gsub(/[^a-z0-9]/, '')
        filename = File.join(Rails.root, 'documentation', @category, @page + '.md')
        begin 
            render :file => filename
        rescue
            raise ActionController::RoutingError.new('Not Found')
        end
    end
end
