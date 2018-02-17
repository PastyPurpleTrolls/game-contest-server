class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception
  before_action :get_daemon_status

  include SessionsHelper
	include MatchesHelper

  def get_daemon_status
    r, w = IO.pipe

    if OS.mac?
      expr_call = Process.spawn("expr $(gdate +%s) - $(gdate +%s -r #{Rails.root}/tmp/clockworkd.clock.output)", :out=>w)
    else
      expr_call = Process.spawn("expr $(date +%s) - $(date +%s -r #{Rails.root}/tmp/clockworkd.clock.output)", :out=>w)
    end
    Process.wait expr_call

    w.close
    access_time = r.read.to_i
    if access_time > 15
      @daemon_status = false
    else
      @daemon_status = true
    end
  end
end
