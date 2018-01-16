class MatchLogInfosController < ApplicationController
  before_action :ensure_user_logged_in, only: [:show]
  before_action :require_permission

      def require_permission
        log_info = MatchLogInfo.find(params[:id])
        if current_user != log_info.get_owner then
	  #redirect_to "/login", alert: "Log Access, Permission Denied"
	  deny_access
        end
      end

      def std_out
        @log_info = MatchLogInfo.find(params[:id])
        unless File.exist? @log_info.log_stdout
          file_does_not_exist
	end
        send_file @log_info.log_stdout if File.exist? @log_info.log_stdout
      end

      def std_err
        @log_info = MatchLogInfo.find(params[:id])
        unless File.exist? @log_info.log_stderr
          file_does_not_exist
	end
	send_file @log_info.log_stderr if File.exist? @log_info.log_stderr
      end
end
