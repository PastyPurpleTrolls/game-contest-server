class HelpController < ApplicationController
    before_action :ensure_user_logged_in

    def index
        @title = "Help"
    end
    #Show documentation markdown files in documentation/(category)/(filename)
    def show
        @category = params[:category]
        #Make sure the user is accessing a "page" and remove all non alphanumeric characters
        #If the user does not provide a page, look for a file with the same name as the category
        @page = (params[:page] || @category).downcase.gsub(/[^a-z0-9]/, '')
        @title = "Help - #{@page.capitalize}"
        filename = File.join(Rails.root, 'documentation', @category, @page + '.md')

        #Catch errors (usually if the file doesn't exist)
        begin 
            render :file => filename
        rescue
            raise ActionController::RoutingError.new('Not Found')
        end
    end
end
