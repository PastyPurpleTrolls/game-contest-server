class HelpController < ApplicationController
    before_action :ensure_user_logged_in
   
    #Show documentation markdown files in documentation/(category)/(filename)
    def show
        @category = params[:category]
        #Make sure the user is accessing a "page" and remove all non alphanumeric characters
        @page = (params[:page] || "index").downcase.gsub(/[^a-z0-9]/, '')
        filename = File.join(Rails.root, 'documentation', @category, @page + '.md')
        #Catch errors (usually if the file doesn't exist)
        begin 
            render :file => filename
        rescue
            raise ActionController::RoutingError.new('Not Found')
        end
    end
end
