class MatchLogInfosController < ApplicationController
  before_action :ensure_user_logged_in, only: [:show]
  before_filter :require_permission

      def require_permission
        log_info = MatchLogInfo.find(params[:id])
        if current_user != log_info.get_owner then
          redirect_to root_path
        end
      end

      def std_out
        @log_info = MatchLogInfo.find(params[:id])
        send_file @log_info.log_stdout
      end

      def std_err
        @log_info = MatchLogInfo.find(params[:id])
        send_file @log_info.log_stderr
      end
end
